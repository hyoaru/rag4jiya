import { ApiProperty } from '@nestjs/swagger';
import { IsString, MaxLength } from 'class-validator';

export class UploadDocumentRequestDto {
  @ApiProperty({ type: 'string', format: 'binary' })
  file: Express.Multer.File;

  @ApiProperty({ example: '2025 Transes', maxLength: 255 })
  @IsString()
  @MaxLength(255)
  title: string;
}
