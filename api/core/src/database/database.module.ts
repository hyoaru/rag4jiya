import { Module } from '@nestjs/common';
import { drizzle } from 'drizzle-orm/node-postgres';
import { ConfigService } from '@nestjs/config';
import { Pool } from 'pg';
import * as schemaUsers from 'src/users/schema';
import * as schemaDocuments from 'src/documents/schema';
import * as schemaDocumentTypes from 'src/document-type/schema';
import { DATABASE_CONNECTION } from './database-connection';

@Module({
  providers: [
    {
      provide: DATABASE_CONNECTION,
      useFactory: (configService: ConfigService) => {
        const pool = new Pool({
          connectionString: configService.get('DATABASE_URL'),
        });

        return drizzle(pool, {
          schema: {
            ...schemaUsers,
            ...schemaDocuments,
            ...schemaDocumentTypes,
          },
        });
      },
      inject: [ConfigService],
    },
  ],
  exports: [DATABASE_CONNECTION],
})
export class DatabaseModule {}
