import { ApiProperty } from '@nestjs/swagger';
import { Expose } from 'class-transformer';

export class SignInResponseDto {
  @ApiProperty({ example: 'john.doe@example.com' })
  @Expose()
  email: string;

  @ApiProperty({
    example:
      'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2M2I2YjE0OC1lYzUwLTRiMjAtYWFhYS1kZTc5Nzk4NzgwNjkiLCJ1c2VybmFtZSI6ImpvaG4uZG9lQGV4YW1wbGUuY29tIiwiaWF0IjoxNzQxOTQzMTE3LCJleHAiOjE3NDE5NDQwMTd9.ARojfTpzPlZJw3PUcTVcV-c5jeerBKd4XPbXWYKKyJY',
  })
  @Expose()
  token: string;
}
