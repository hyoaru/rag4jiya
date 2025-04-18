import { relations, sql } from 'drizzle-orm';
import { pgTable, timestamp, uuid, varchar } from 'drizzle-orm/pg-core';
import { documentType } from 'src/document-type/schema';
import { users } from 'src/users/schema';

export const documents = pgTable('documents', {
  id: uuid('id').primaryKey().defaultRandom(),
  title: varchar('title', { length: 255 }).notNull(),
  url: varchar('url', { length: 255 }),
  userId: uuid('user_id').references(() => users.id),
  documentTypeId: uuid('documentTypeId').references(() => documentType.id),
  createdAt: timestamp('created_at', { withTimezone: true, mode: 'string' })
    .defaultNow()
    .notNull(),
  updatedAt: timestamp('updated_at', { withTimezone: true, mode: 'string' })
    .defaultNow()
    .notNull()
    .$onUpdate(() => sql`NOW()`),
});

export const documentsRelations = relations(documents, ({ one }) => ({
  user: one(users, {
    fields: [documents.userId],
    references: [users.id],
  }),
  documentType: one(documentType, {
    fields: [documents.documentTypeId],
    references: [documentType.id],
  }),
}));
