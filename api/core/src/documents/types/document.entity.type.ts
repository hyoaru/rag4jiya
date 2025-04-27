export type Document = {
  id: string;
  title: string;
  filename: string;
  createdAt: string;
  updatedAt: string;
  userId: string | null;
  documentTypeId: string | null;
};
