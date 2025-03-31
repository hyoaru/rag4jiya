import { Expose } from 'class-transformer';
import { User } from 'src/users/types/user.entity.type';

export class LocalAuthResponseDto {
  constructor(partial: Partial<Omit<User, 'password'>>) {
    Object.assign(this, partial);
  }

  @Expose()
  readonly id: string;

  @Expose({ name: 'firstName' })
  first_name: string;

  @Expose({ name: 'lastName' })
  last_name: string;

  @Expose()
  email: string;

  @Expose({ name: 'createdAt' })
  readonly created_at: string;

  @Expose({ name: 'updatedAt' })
  readonly updated_at: string;
}
