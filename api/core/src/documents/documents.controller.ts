import {
  Body,
  Controller,
  Get,
  Param,
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
import { AuthenticatedUser } from 'src/authentication/decorators/authenticated-user.decorator';
import { User } from 'src/users/types/user.entity.type';
import { DocumentDto } from './dto/document.dto';

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
  @ApiResponse({ status: 200, type: DocumentDto })
  @ApiConsumes('multipart/form-data')
  async upload(
    @UploadedFile() file: Express.Multer.File,
    @Body() dto: UploadDocumentRequestDto,
    @AuthenticatedUser() user: User,
  ) {
    return await this.documentsService.create({
      file: file,
      title: dto.title,
      user: user,
    });
  }

  @Get()
  @UseGuards(JwtAuthGuard)
  @ApiCookieAuth('Authentication')
  @ApiResponse({ status: 200, type: DocumentDto, isArray: true })
  async findAll(@AuthenticatedUser() user: User) {
    return await this.documentsService.findAll({
      user: user,
    });
  }

  @Get(':id')
  @UseGuards(JwtAuthGuard)
  @ApiCookieAuth('Authentication')
  @ApiResponse({ status: 200, type: DocumentDto })
  async findOne(@Param('id') id: string) {
    return await this.documentsService.findOne({
      id: id,
    });
  }
}
