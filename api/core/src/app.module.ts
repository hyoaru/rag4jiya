import { Module } from '@nestjs/common';
import { DatabaseModule } from './database/database.module';
import { ConfigModule } from '@nestjs/config';
import { UsersModule } from './users/users.module';
import { AuthenticationModule } from './authentication/authentication.module';
import { DocumentsModule } from './documents/documents.module';
import { DocumentTypeModule } from './document-type/document-type.module';
import { ObjectStorageModule } from './object-storage/object-storage.module';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    DatabaseModule,
    UsersModule,
    AuthenticationModule,
    DocumentsModule,
    DocumentTypeModule,
    ObjectStorageModule,
  ],
  controllers: [],
  providers: [],
})
export class AppModule {}
