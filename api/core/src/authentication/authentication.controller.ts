import { Body, Controller, Post, Res, UseGuards } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { ApiBody, ApiResponse } from '@nestjs/swagger';
import { plainToInstance } from 'class-transformer';
import { Response } from 'express';
import { User } from 'src/users/types/user.entity.type';
import { AuthenticationService } from './authentication.service';
import { AuthenticatedUser } from './decorators/authenticated-user.decorator';
import { LocalAuthRequest } from './dto/local-auth.request.dto';
import { SignUpRequestDto } from './dto/sign-up.request.dto';
import { SignUpResponseDto } from './dto/sign-up.response.dto';
import { LocalAuthGuard } from './guards/local-auth.guard';
import { JwtPayload } from './types/jwt-payload';
import { ConfigService } from '@nestjs/config';
import { JwtRefreshAuthGuard } from './guards/jwt-refresh.guard';

@Controller('authentication')
export class AuthenticationController {
  constructor(
    private authenticationService: AuthenticationService,
    private jwtService: JwtService,
    private configService: ConfigService,
  ) {}

  @Post('sign-up')
  @ApiResponse({ status: 200, type: SignUpResponseDto })
  async signUp(@Body() dto: SignUpRequestDto): Promise<SignUpResponseDto> {
    const record = await this.authenticationService.signUp({
      firstName: dto.first_name,
      lastName: dto.last_name,
      email: dto.email,
      password: dto.password,
    });

    return plainToInstance(SignUpResponseDto, record, {
      excludeExtraneousValues: true,
    });
  }

  @Post('sign-in')
  @UseGuards(LocalAuthGuard)
  @ApiBody({ type: LocalAuthRequest })
  @ApiResponse({ status: 204 })
  async signIn(@Res() res: Response, @AuthenticatedUser() user: User) {
    const jwtTokens = await this.authenticationService.signIn({ user });

    const decodedAccessToken: JwtPayload = this.jwtService.verify(
      jwtTokens.accessToken,
      {
        secret: this.configService.getOrThrow('JWT_ACCESS_TOKEN_SECRET'),
      },
    );

    const decodedRefreshToken: JwtPayload = this.jwtService.verify(
      jwtTokens.refreshToken,
      {
        secret: this.configService.getOrThrow(
          'JWT_REFRESH_ACCESS_TOKEN_SECRET',
        ),
      },
    );

    const accessTokenExpiresAt = new Date(decodedAccessToken.exp * 1000);
    const refreshTokenExpiresAt = new Date(decodedRefreshToken.exp * 1000);

    res.cookie('Authentication', jwtTokens.accessToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      expires: accessTokenExpiresAt,
    });

    res.cookie('Refresh', jwtTokens.refreshToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      expires: refreshTokenExpiresAt,
    });

    return res.status(204).send();
  }

  @Post('refresh')
  @UseGuards(JwtRefreshAuthGuard)
  @ApiResponse({ status: 200 })
  async refresh(@Res() res: Response, @AuthenticatedUser() user: User) {
    const jwtTokens = await this.authenticationService.signIn({ user });

    const decodedAccessToken: JwtPayload = this.jwtService.verify(
      jwtTokens.accessToken,
      {
        secret: this.configService.getOrThrow('JWT_ACCESS_TOKEN_SECRET'),
      },
    );

    const decodedRefreshToken: JwtPayload = this.jwtService.verify(
      jwtTokens.refreshToken,
      {
        secret: this.configService.getOrThrow(
          'JWT_REFRESH_ACCESS_TOKEN_SECRET',
        ),
      },
    );

    const accessTokenExpiresAt = new Date(decodedAccessToken.exp * 1000);
    const refreshTokenExpiresAt = new Date(decodedRefreshToken.exp * 1000);

    res.cookie('Authentication', jwtTokens.accessToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      expires: accessTokenExpiresAt,
    });

    res.cookie('Refresh', jwtTokens.refreshToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      expires: refreshTokenExpiresAt,
    });

    return res.status(204).send();
  }
}
