import { ApiProperty } from '@nestjs/swagger';
import { IsString, IsNotEmpty, MaxLength, IsEmail } from 'class-validator';

export class LocalAuthRequest {
  @ApiProperty({ example: 'john.doe@example.com', maxLength: 255 })
  @IsEmail()
  @IsNotEmpty()
  @MaxLength(255)
  email: string;

  @ApiProperty({
    example: 'Str0ng@Passw0rd',
    minLength: 8,
    maxLength: 255,
    description:
      'Must contain at least one uppercase letter, one number, and one special character.',
  })
  @IsString()
  @IsNotEmpty()
  password: string;
}
