// src/utils/interfaces.tsx
import { z } from 'zod';
import { ReactNode } from 'react';

/* ---------- базовые ---------- */
export interface User {
  id: number;
  username: string;
  pass?: string;
}

export interface Person {
  id: number;
  firstName: string;
  lastName: string;
  patronymic: string;
  sex: string;
  birthDate: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
}

export interface PaginationProps {
  page: number;
  totalPages: number;
  limit: number;
  onPageChange: (newPage: number) => void;
  onLimitChange: (newLimit: number) => void;
}

export interface ErrorResponse {
  message?: string;
  error?: string;
}

/* ---------- доменные ---------- */
export interface Author {
  id: number;
  firstName: string;
  patronymic: string | null;
  lastName: string;
  birthYear: number | null;
}

export interface Bbk {
  id: number;
  bbkAbb: string;
  description: string | null;
}

export interface Udc {
  id: number;
  udcAbb: string;
  description: string | null;
}

export interface BookBbkRaw {
  bookId: number;
  bbkCode: string;
}

export interface BookUdcRaw {
  bookId: number;
  udcCode: string;
}

export interface Publisher {
  id: number;
  name: string;
}

export interface BookPubPlace {
  id: number;
  bookId: number;
  publisher: Publisher | null;
  city: string | null;
  pubYear: number | null;
}

export interface BookCopy {
  id: number;
  inventoryNo: string;
  receiptDate: string | null;
  storagePlace: string | null;
  price: number | null;
  book: Book;
  borrowRecords?: BorrowRecord[];
}

export interface BorrowRecord {
  id: number;
  borrowDate: string;
  expectedReturnDate: string | null;
  dueDate: string | null;
  returnDate: string | null;
  person?: Person | null;
  issuedByUser?: User;
  acceptedByUser?: User | null;
  bookCopy: BookCopy;
}

export interface Grnti {
  id: number;
  code: string;
  description: string | null;
}

export interface BookGrntiRaw {
  bookId: number;
  grntiCode: string;
}

export interface Book {
  id: number;
  title: string | null;
  description: string;
  bookType: string | null;
  edit: string | null;
  editionStatement: string | null;
  physDesc: string | null;
  series: string | null;
  authors: Author[] | null;
  bbks: Bbk[] | null;
  udcs: Udc[] | null;
  bbkRaws: BookBbkRaw[] | null;
  udcRaws: BookUdcRaw[] | null;
  bookCopies: BookCopy[] | null;
  publicationPlaces: BookPubPlace[] | null;
  grntiAbbs?: string;
  grntiRaw?:  string;
  grntis?: { id: number; code: string }[];
  grntiRaws?: { grntiCode: string }[];
}

export const bookSchema = z.object({
  title: z.string().optional(),
  bookType: z.string().optional(),
  edit: z.string().optional(),
  editionStatement: z.string().optional(),
  series: z.string().optional(),
  physDesc: z.string().optional(),
  description: z.string().optional(),
  authors: z.string().optional(),
  bbkAbbs: z.string().optional(),
  udcAbbs: z.string().optional(),
  bbkRaw: z.string().optional(),
  udcRaw: z.string().optional(),
  grntiAbbs: z.string().optional(),
  grntiRaw: z.string().optional(),
  pubCity: z.string().optional(),
  pubName: z.string().optional(),
  pubYear: z.number().optional(),
});
export type FormValues = z.infer<typeof bookSchema>;