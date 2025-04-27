import {
  Inject,
  Injectable,
  InternalServerErrorException,
} from '@nestjs/common';
import { nanoid } from 'nanoid';
import { ObjectStorageService } from 'src/object-storage/object-storage.service';
import { UploadDocumentParams } from './types/upload-document-params';
import { NodePgDatabase } from 'drizzle-orm/node-postgres';
import { DATABASE_CONNECTION } from 'src/database/database-connection';
import * as schema from './schema';

@Injectable()
export class DocumentsService {
  constructor(
    private objectStorageService: ObjectStorageService,
    @Inject(DATABASE_CONNECTION)
    private readonly database: NodePgDatabase<typeof schema>,
  ) {}

  async upload(params: UploadDocumentParams) {
    const sanitizedFilename = `${nanoid()}-${params.file.originalname.replaceAll(' ', '_')}`;
    const bucketPath = `${params.user.id}/${sanitizedFilename}`;

    // Upload document
    try {
      await this.objectStorageService.upload({
        bucket: 'documents',
        key: bucketPath,
        buffer: params.file.buffer,
      });
    } catch {
      throw new InternalServerErrorException(
        'An unexpected error occurred when uploading the document',
      );
    }

    // Store document data
    try {
      const document = await this.database.insert(schema.documents).values({
        title: params.title,
        filename: sanitizedFilename,
        userId: params.user.id,
      });

      return document;
    } catch {
      throw new InternalServerErrorException(
        'An error has occured when saving the document record.',
      );
    }
  }
}
