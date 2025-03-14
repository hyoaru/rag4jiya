import {
  ConflictException,
  Inject,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { NodePgDatabase } from 'drizzle-orm/node-postgres';
import { DATABASE_CONNECTION } from 'src/database/database-connection';
import * as schema from './schema';
import { InferInsertModel, InferSelectModel } from 'drizzle-orm';

@Injectable()
export class UsersService {
  constructor(
    @Inject(DATABASE_CONNECTION)
    private readonly database: NodePgDatabase<typeof schema>,
  ) {}

  async create(
    params: InferInsertModel<typeof schema.users>,
  ): Promise<InferSelectModel<typeof schema.users>> {
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

  async findAll(): Promise<InferSelectModel<typeof schema.users>[]> {
    return await this.database.query.users.findMany();
  }

  async findOne(id: string): Promise<InferSelectModel<typeof schema.users>> {
    const record = await this.database.query.users.findFirst({
      where: (users, { eq }) => eq(users.id, id),
    });

    if (!record) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }

    return record;
  }

  async findOneByEmail(
    email: string,
  ): Promise<InferSelectModel<typeof schema.users>> {
    const record = await this.database.query.users.findFirst({
      where: (users, { eq }) => eq(users.email, email),
    });

    if (!record) {
      throw new NotFoundException(`User with email ${email} not found`);
    }

    return record;
  }
}
