import { PassportStrategy } from '@nestjs/passport';
import { Strategy } from 'passport-local';
import { AuthenticationService } from '../authentication.service';
import { Injectable } from '@nestjs/common';
import { LocalAuthResponseDto } from '../dto/local-auth.response.dto';
import { plainToInstance } from 'class-transformer';

@Injectable()
export class LocalStrategy extends PassportStrategy(Strategy, 'local') {
  constructor(private authService: AuthenticationService) {
    super({ usernameField: 'email' });
  }

  async validate(email: string, password: string) {
    const user = await this.authService.verifyUser({ email, password });

    return plainToInstance(LocalAuthResponseDto, user, {
      excludeExtraneousValues: true,
    });
  }
}
