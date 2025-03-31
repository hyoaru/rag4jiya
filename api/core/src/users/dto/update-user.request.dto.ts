import { ApiProperty } from '@nestjs/swagger';
import {
  IsString,
  MaxLength,
  IsEmail,
  MinLength,
  IsStrongPassword,
  IsOptional,
} from 'class-validator';

export class UpdateUserRequestDto {
  @ApiProperty({ example: 'John', maxLength: 100 })
  @IsString()
  @IsOptional()
  @MaxLength(100)
  first_name: string;

  @ApiProperty({ example: 'Doe', maxLength: 100 })
  @IsString()
  @IsOptional()
  @MaxLength(100)
  last_name: string;

  @ApiProperty({ example: 'john.doe@example.com', maxLength: 255 })
  @IsEmail()
  @IsOptional()
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
  @IsOptional()
  @MinLength(8)
  @MaxLength(255)
  @IsStrongPassword(
    {
      minLength: 8,
      minLowercase: 1,
      minUppercase: 1,
      minNumbers: 1,
      minSymbols: 1,
    },
    {
      message:
        'Password must be at least 8 characters and include an uppercase letter, a number, and a special character.',
    },
  )
  password: string;

  @ApiProperty({
    example: null,
    description: "User's refresh token",
    required: false,
    nullable: true,
  })
  @IsString()
  @IsOptional()
  refresh_token: string | null;
}
