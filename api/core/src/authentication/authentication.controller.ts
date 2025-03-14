import { Body, Controller, Post } from '@nestjs/common';
import { AuthenticationService } from './authentication.service';
import { ApiResponse } from '@nestjs/swagger';
import { SignUpRequestDto } from './dto/sign-up.request.dto';
import { SignUpResponseDto } from './dto/sign-up.response.dto';
import { plainToInstance } from 'class-transformer';
import { SignInResponseDto } from './dto/sign-in.response.dto';
import { SignInRequestDto } from './dto/sign-in.request.dto';

@Controller('authentication')
export class AuthenticationController {
  constructor(private readonly authenticationService: AuthenticationService) {}

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
  @ApiResponse({ status: 200, type: SignInResponseDto })
  async signIn(@Body() dto: SignInRequestDto): Promise<SignInResponseDto> {
    const record = await this.authenticationService.signIn({
      email: dto.email,
      password: dto.password,
    });

    return plainToInstance(SignInResponseDto, record, {
      excludeExtraneousValues: true,
    });
  }
}
