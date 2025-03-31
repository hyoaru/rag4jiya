import { createParamDecorator, ExecutionContext } from '@nestjs/common';
import { User } from 'src/users/types/user.entity.type';

export const AuthenticatedUser = createParamDecorator(
  (_data: unknown, context: ExecutionContext) =>
    context.switchToHttp().getRequest<{ user: User }>().user,
);
