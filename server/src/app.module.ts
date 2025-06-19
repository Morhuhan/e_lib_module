import { Module } from '@nestjs/common';
import { ServeStaticModule } from '@nestjs/serve-static';
<<<<<<< HEAD
import { ConfigModule } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { join } from 'path';
=======
import { join } from 'path';

import { ConfigModule } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
>>>>>>> 17a3b8170ab6bda512c448c38bb77960536aa94a
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { UsersModule } from './users/users.module';
import { AuthModule } from './_auth/auth.module';
import { BooksModule } from './books/book.module';
import { BorrowRecordsModule } from './borrow-records/borrow-records.module';
import { BookCopiesModule } from './book-copies/book-copies.module';
import { PersonsModule } from './persons/persons.module';
import { ReportsModule } from './_reports/reports.module';
import { AdminSeeder } from './_seeders/admin.seeder';
<<<<<<< HEAD
import { AuthorsModule } from './authors/authors.module';
=======
import { Author } from './authors/author.entity';
import { AuthorsModule } from './authors/authors.module';
import { Bbk } from './bbk/bbk.entity';
>>>>>>> 17a3b8170ab6bda512c448c38bb77960536aa94a
import { BbkModule } from './bbk/bbk.module';
import { UdcModule } from './udc/udc.module';
import { PublishersModule } from './publisher/publishers.module';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
    }),
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: 'localhost',
      port: 5432,
      username: 'postgres',
      password: '2121212q',
      database: 'Library',
      entities: [__dirname + '/**/*.entity{.ts,.js}'],
      synchronize: false,
    }),

    // ВАЖНО: ServeStaticModule раздаёт React-сборку
    // exclude: ['/api*'] — чтобы не перехватывать запросы, идущие на /api
    ServeStaticModule.forRoot({
      rootPath: join(__dirname, '..', '..', 'client', 'build'),
      exclude: ['/api*'],
    }),

    UsersModule,
    AuthModule,
    BooksModule,
    BorrowRecordsModule,
    BookCopiesModule,
    PersonsModule,
    ReportsModule,
    AuthorsModule, 
    BbkModule,
    UdcModule,
    PublishersModule,
  ],
  controllers: [AppController],
  providers: [AppService, AdminSeeder],
})
export class AppModule {}