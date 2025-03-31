import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { PassportStrategy } from '@nestjs/passport';
import { plainToInstance } from 'class-transformer';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { UsersService } from 'src/users/users.service';
import { LocalAuthResponseDto } from '../dto/local-auth.response.dto';
import { JwtPayload } from '../types/jwt-payload';
import { Request } from 'express';
import { AuthenticationService } from '../authentication.service';

@Injectable()
export class JwtRefreshStrategy extends PassportStrategy(
  Strategy,
  'jwt-refresh',
) {
  constructor(
    private userService: UsersService,
    private authenticationService: AuthenticationService,
    configService: ConfigService,
  ) {
    super({
      jwtFromRequest: ExtractJwt.fromExtractors([
        (request: Request & { cookies?: { Refresh?: string } }) =>
          request.cookies?.Refresh || null,
      ]),
      secretOrKey: configService.getOrThrow('JWT_REFRESH_ACCESS_TOKEN_SECRET'),
      passReqToCallback: true,
    });
  }

  async validate(
    request: Request & { cookies?: { Refresh: string } },
    payload: JwtPayload,
  ) {
    const user = await this.userService.findByEmail(payload.email);
    await this.authenticationService.validateUserRefreshToken({
      refreshToken: request.cookies?.Refresh,
      user: user,
    });

    return plainToInstance(LocalAuthResponseDto, user, {
      excludeExtraneousValues: true,
    });
  }
}
