import { Injectable } from '@nestjs/common';
import { ObjectStorageService } from 'src/object-storage/object-storage.service';
import { UploadDocumentParams } from './types/upload-document-params';

@Injectable()
export class DocumentsService {
  constructor(private objectStorageService: ObjectStorageService) {}

  async upload(params: UploadDocumentParams) {
    await this.objectStorageService.upload({
      bucket: 'documents',
      key: params.file.originalname,
      buffer: params.file.buffer,
    });
  }
}
