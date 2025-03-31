export type UpdateUserParams = {
  id: string;
  data: {
    firstName?: string;
    lastName?: string;
    email?: string;
    password?: string;
    refreshToken?: string | null;
  };
};
