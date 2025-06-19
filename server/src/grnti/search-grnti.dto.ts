import { IsOptional, IsString } from 'class-validator';

export class SearchGrntiDto {
  @IsOptional()
  @IsString()
  q?: string;
}