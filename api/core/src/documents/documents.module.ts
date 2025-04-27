import { Module } from '@nestjs/common';
import { ObjectStorageModule } from 'src/object-storage/object-storage.module';
import { DocumentsController } from './documents.controller';
import { DocumentsService } from './documents.service';
import { DatabaseModule } from 'src/database/database.module';

@Module({
  imports: [ObjectStorageModule, DatabaseModule],
  controllers: [DocumentsController],
  providers: [DocumentsService],
})
export class DocumentsModule {}
