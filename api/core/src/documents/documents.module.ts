import { Module } from '@nestjs/common';
import { ObjectStorageModule } from 'src/object-storage/object-storage.module';
import { DocumentsController } from './documents.controller';
import { DocumentsService } from './documents.service';

@Module({
  imports: [ObjectStorageModule],
  controllers: [DocumentsController],
  providers: [DocumentsService],
})
export class DocumentsModule {}
