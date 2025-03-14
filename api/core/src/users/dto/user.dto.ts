import { ApiProperty } from '@nestjs/swagger';
import { Expose } from 'class-transformer';

export class UserDto {
  constructor(partial: Partial<UserDto>) {
    Object.assign(this, partial);
  }

  @ApiProperty({
    example: '4c808ef1-9bb4-489c-ab32-417facdb03f8',
    description: "User's Id",
  })
  @Expose()
  readonly id: string;

  @ApiProperty({
    example: 'John',
    description: "User's first name",
    name: 'first_name',
  })
  @Expose({ name: 'firstName' })
  first_name: string;

  @ApiProperty({
    example: 'Doe',
    description: "User's last name",
    name: 'last_name',
  })
  @Expose({ name: 'lastName' })
  last_name: string;

  @ApiProperty({
    example: 'john.doe@example.com',
    description: "User's email",
  })
  @Expose()
  email: string;

  @ApiProperty({
    example: '2023-01-01T00:00:00.000Z',
    description: "User's creation date",
    name: 'created_at',
  })
  @Expose({ name: 'createdAt' })
  readonly created_at: string;

  @ApiProperty({
    example: '2023-01-01T00:00:00.000Z',
    description: "User's last update date",
    name: 'updated_at',
  })
  @Expose({ name: 'updatedAt' })
  readonly updated_at: string;
}
