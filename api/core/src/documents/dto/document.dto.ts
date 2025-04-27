import { ApiProperty } from '@nestjs/swagger';
import { Expose } from 'class-transformer';

export class DocumentDto {
  constructor(partial: Partial<DocumentDto>) {
    Object.assign(this, partial);
  }

  @ApiProperty({
    example: '4c808ef1-9bb4-489c-ab32-417facdb03f8',
    description: "Document's Id",
  })
  @Expose()
  readonly id: string;

  @ApiProperty({
    example: '2025 Transes',
    description: "Document's title",
  })
  @Expose()
  title: string;

  @ApiProperty({
    example: '2025-Transes.pdf',
    description: "Document's filename",
  })
  @Expose()
  filename: string;

  @ApiProperty({
    example: '4c808ef1-9bb4-489c-ab32-417facdb03f8',
    description: "Document's user id",
    name: 'user_id',
  })
  @Expose({ name: 'userId' })
  readonly user_id: string;

  @ApiProperty({
    example: '4c808ef1-9bb4-489c-ab32-417facdb03f8',
    description: 'Document type id',
    name: 'document_type_id',
  })
  @Expose({ name: 'documentTypeId' })
  readonly document_type_id: string;

  @ApiProperty({
    example: '2023-01-01T00:00:00.000Z',
    description: "Document's creation date",
    name: 'created_at',
  })
  @Expose({ name: 'createdAt' })
  readonly created_at: string;

  @ApiProperty({
    example: '2023-01-01T00:00:00.000Z',
    description: "Document's last update date",
    name: 'updated_at',
  })
  @Expose({ name: 'updatedAt' })
  readonly updated_at: string;
}
