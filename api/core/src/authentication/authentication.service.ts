import { Injectable, UnauthorizedException } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { JwtService } from '@nestjs/jwt';
import * as argon from 'argon2';
import { User } from 'src/users/types/user.entity.type';
import { UsersService } from 'src/users/users.service';
import { SignInParams } from './types/sign-in-params';
import { SignUpParams } from './types/sign-up-params';
import { VerifyUserParams } from './types/verify-user-params';
import { SignInResponse } from './types/sign-in-response';
import { ValidateUserRefreshTokenParams } from './types/validate-user-refresh-token-params';

@Injectable()
export class AuthenticationService {
  constructor(
    private usersService: UsersService,
    private jwtService: JwtService,
    private configService: ConfigService,
  ) {}

  async verifyUser(params: VerifyUserParams): Promise<User> {
    const user = await this.usersService.findByEmail(params.email);

    const isValid = await argon.verify(user.password, params.password);
    if (!isValid) throw new UnauthorizedException('Invalid credentials');
    return user;
  }

  async signUp(params: SignUpParams): Promise<User> {
    const hashedPassword = await argon.hash(params.password);

    return await this.usersService.create({
      firstName: params.firstName,
      lastName: params.lastName,
      email: params.email,
      password: hashedPassword,
    });
  }

  async signIn(params: SignInParams): Promise<SignInResponse> {
    const tokenPayload = { email: params.user.email };

    const accessToken = await this.jwtService.signAsync(tokenPayload, {
      secret: this.configService.getOrThrow('JWT_ACCESS_TOKEN_SECRET'),
      expiresIn: this.configService.getOrThrow('JWT_ACCESS_TOKEN_EXPIRATION'),
    });

    const refreshToken = await this.jwtService.signAsync(tokenPayload, {
      secret: this.configService.getOrThrow('JWT_REFRESH_ACCESS_TOKEN_SECRET'),
      expiresIn: this.configService.getOrThrow(
        'JWT_REFRESH_ACCESS_TOKEN_EXPIRATION',
      ),
    });

    const hashedRefreshToken = await argon.hash(refreshToken);
    await this.usersService.update({
      id: params.user.id,
      data: { refreshToken: hashedRefreshToken },
    });

    return { accessToken, refreshToken };
  }

  async validateUserRefreshToken(params: ValidateUserRefreshTokenParams) {
    const isValid = await argon.verify(
      params.user.refreshToken!,
      params.refreshToken,
    );

    if (!isValid) throw new UnauthorizedException('Invalid credentials');
    return params.user;
  }
}
