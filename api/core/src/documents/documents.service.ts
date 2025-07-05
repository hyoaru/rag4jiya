import {
  Inject,
  Injectable,
  InternalServerErrorException,
  NotFoundException,
} from '@nestjs/common';
import { NodePgDatabase } from 'drizzle-orm/node-postgres';
import { customAlphabet } from 'nanoid';
import { DATABASE_CONNECTION } from 'src/database/database-connection';
import { ObjectStorageService } from 'src/object-storage/object-storage.service';
import * as schema from './schema';
import { Document } from './types/document.entity.type';
import { FindAllDocumentParams } from './types/find-all-document-params';
import { UploadDocumentParams } from './types/upload-document-params';
import { FindOneDocumentParams } from './types/find-one-document-params';

@Injectable()
export class DocumentsService {
  constructor(
    private objectStorageService: ObjectStorageService,
    @Inject(DATABASE_CONNECTION)
    private readonly database: NodePgDatabase<typeof schema>,
  ) {}

  async create(params: UploadDocumentParams): Promise<Document> {
    const nanoid = customAlphabet('123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', 10);
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
      const [record] = await this.database
        .insert(schema.documents)
        .values({
          title: params.title,
          filename: sanitizedFilename,
          userId: params.user.id,
        })
        .returning();

      return record;
    } catch {
      throw new InternalServerErrorException(
        'An error has occured when saving the document record.',
      );
    }
  }

  async findAll(params: FindAllDocumentParams): Promise<Document[]> {
    const records = await this.database.query.documents.findMany({
      where: (document, { eq }) => eq(document.userId, params.user.id),
    });

    return records;
  }

  async findOne(params: FindOneDocumentParams): Promise<Document> {
    const record = await this.database.query.documents.findFirst({
      where: (document, { eq }) => eq(document.id, params.id),
    });

    if (!record) {
      throw new NotFoundException('Document not found');
    }

    return record;
  }
}
