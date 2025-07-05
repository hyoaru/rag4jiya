import { User } from 'src/users/types/user.entity.type';

export type UploadDocumentParams = {
  file: Express.Multer.File;
  title: string;
  user: User;
};
