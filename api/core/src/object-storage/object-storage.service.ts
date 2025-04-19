import { PutObjectCommand, S3Client } from '@aws-sdk/client-s3';
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { UploadFileParams } from './types/upload-file-paramts';

@Injectable()
export class ObjectStorageService {
  private readonly objectStorageClient: S3Client;

  constructor(configService: ConfigService) {
    this.objectStorageClient = new S3Client({
      region: configService.getOrThrow('S3_REGION'),
      endpoint: configService.getOrThrow('S3_ENDPOINT'),
      forcePathStyle: true,
      credentials: {
        accessKeyId: configService.getOrThrow('S3_ACCESS_KEY_ID'),
        secretAccessKey: configService.getOrThrow('S3_SECRET_ACCESS_KEY'),
      },
    });
  }

  async upload(params: UploadFileParams) {
    const command = new PutObjectCommand({
      Bucket: params.bucket,
      Key: params.key,
      Body: params.buffer,
    });

    return await this.objectStorageClient.send(command);
  }
}
