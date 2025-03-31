import { User } from 'src/users/types/user.entity.type';

export type ValidateUserRefreshTokenParams = {
  user: User;
  refreshToken: string;
};
