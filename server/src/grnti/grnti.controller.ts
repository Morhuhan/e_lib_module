import { Controller, Get, Header, Query, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { GrntiService } from './grnti.service';
import { SearchGrntiDto } from './search-grnti.dto';

@Controller('grnti')
@UseGuards(AuthGuard('jwt'))
export class GrntiController {
  constructor(private readonly svc: GrntiService) {}

  @Get()
  @Header('Cache-Control', 'no-store')
  async search(@Query() { q }: SearchGrntiDto) {
    return this.svc.search(q);
  }
}