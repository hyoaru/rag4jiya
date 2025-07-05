import {
  BadRequestException,
  ConflictException,
  Inject,
  Injectable,
  InternalServerErrorException,
  NotFoundException,
} from '@nestjs/common';
import { eq } from 'drizzle-orm';
import { NodePgDatabase } from 'drizzle-orm/node-postgres';
import { DATABASE_CONNECTION } from 'src/database/database-connection';
import * as schema from './schema';
import { CreateUserParams } from './types/create-user-params';
import { UpdateUserParams } from './types/update-user-params';
import { User } from './types/user.entity.type';

@Injectable()
export class UsersService {
  constructor(
    @Inject(DATABASE_CONNECTION)
    private readonly database: NodePgDatabase<typeof schema>,
  ) {}

  async create(params: CreateUserParams): Promise<User> {
    try {
      const [record] = await this.database
        .insert(schema.users)
        .values(params)
        .returning();

      return record;
    } catch (error: unknown) {
      if ((error as { code?: string })?.code === '23505') {
        throw new ConflictException('Email is already in use');
      }

      throw error;
    }
  }

  async findAll(): Promise<User[]> {
    return await this.database.query.users.findMany();
  }

  async findOne(id: string): Promise<User> {
    const record = await this.database.query.users.findFirst({
      where: (users, { eq }) => eq(users.id, id),
    });

    if (!record) {
      throw new NotFoundException('User not found');
    }

    return record;
  }

  async findByEmail(email: string): Promise<User> {
    const record = await this.database.query.users.findFirst({
      where: (users, { eq }) => eq(users.email, email),
    });

    if (!record) {
      throw new NotFoundException('User not found');
    }

    return record;
  }

  async update(params: UpdateUserParams): Promise<User> {
    if (!params.data || Object.keys(params.data).length === 0) {
      throw new BadRequestException('No fields provided to update');
    }

    try {
      const [record] = await this.database
        .update(schema.users)
        .set(params.data)
        .where(eq(schema.users.id, params.id))
        .returning();

      return record;
    } catch {
      throw new InternalServerErrorException(
        'An unexpected error occurred while updating the user',
      );
    }
  }
}
