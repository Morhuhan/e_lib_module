import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Grnti } from './grnti.entity';

@Injectable()
export class GrntiService {
  constructor(
    @InjectRepository(Grnti)
    private readonly repo: Repository<Grnti>,
  ) {}

  /** Поиск ГРНТИ по коду или описанию */
  async search(q?: string): Promise<{ id: number; code: string; description: string | null }[]> {
    const term = (q ?? '').trim().toLowerCase();
    if (!term) return [];

    const like = `%${term}%`;
    const list = await this.repo
      .createQueryBuilder('g')
      .where('LOWER(g.code) LIKE :like', { like })
      .orWhere('LOWER(COALESCE(g.description, \'\')) LIKE :like', { like })
      .orderBy('g.code', 'ASC')
      .limit(25)
      .getMany();

    return list.map((g) => ({
      id: g.id,
      code: g.code,
      description: g.description,
    }));
  }
}