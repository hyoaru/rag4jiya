import {
  Body,
  Controller,
  Post,
  UploadedFile,
  UseGuards,
  UseInterceptors,
} from '@nestjs/common';
import { DocumentsService } from './documents.service';
import { ApiConsumes, ApiCookieAuth, ApiResponse } from '@nestjs/swagger';
import { JwtAuthGuard } from 'src/authentication/guards/jwt.guard';
import { FileInterceptor } from '@nestjs/platform-express';
import { UploadDocumentRequestDto } from './dto/upload-document.request.dto';

@Controller('documents')
export class DocumentsController {
  constructor(private documentsService: DocumentsService) {}

  @Post('upload')
  @UseGuards(JwtAuthGuard)
  @ApiCookieAuth('Authentication')
  @UseInterceptors(
    FileInterceptor('file', {
      fileFilter: (_, file, callback) => {
        const allowedMimetypes = ['application/pdf'];

        if (!allowedMimetypes.includes(file.mimetype)) {
          return callback(new Error('Only PDF files are allowed!'), false);
        }

        callback(null, true);
      },
    }),
  )
  @ApiResponse({ status: 200, type: String })
  @ApiConsumes('multipart/form-data')
  async upload(
    @UploadedFile() file: Express.Multer.File,
    @Body() dto: UploadDocumentRequestDto,
  ) {
    await this.documentsService.upload({
      file: file,
      title: dto.title,
    });
  }
}
