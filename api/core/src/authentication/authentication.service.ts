import { ForbiddenException, Injectable } from '@nestjs/common';
import { UsersService } from 'src/users/users.service';
import * as argon from 'argon2';
import { SignUpParams } from './types/sign-up-params';
import { SignInParams } from './types/sign-in-params';
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class AuthenticationService {
  constructor(
    private usersService: UsersService,
    private jwtService: JwtService,
  ) {}

  async signUp(params: SignUpParams) {
    const hashedPassword = await argon.hash(params.password);

    return await this.usersService.create({
      firstName: params.firstName,
      lastName: params.lastName,
      email: params.email,
      password: hashedPassword,
    });
  }

  async signIn(params: SignInParams) {
    const user = await this.usersService.findOneByEmail(params.email);

    const isValid = await argon.verify(user.password, params.password);
    if (!isValid) throw new ForbiddenException('Invalid credentials');

    const accessToken = await this.jwtService.signAsync({
      sub: user.id,
      username: user.email,
    });

    return {
      email: user.email,
      token: accessToken,
    };
  }
}
