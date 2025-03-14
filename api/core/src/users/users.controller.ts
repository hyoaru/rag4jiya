import { Controller, Get, Param } from '@nestjs/common';
import { UsersService } from './users.service';
import { ApiResponse } from '@nestjs/swagger';
import { UserDto } from './dto/user.dto';
import { plainToInstance } from 'class-transformer';

@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get()
  @ApiResponse({ status: 200, type: UserDto, isArray: true })
  async findAll(): Promise<UserDto[]> {
    const records = await this.usersService.findAll();
    return plainToInstance(UserDto, records, {
      excludeExtraneousValues: true,
    });
  }

  @Get(':id')
  @ApiResponse({ status: 200, type: UserDto })
  async findOne(@Param('id') id: string): Promise<UserDto> {
    const record = await this.usersService.findOne(id);
    return plainToInstance(UserDto, record, {
      excludeExtraneousValues: true,
    });
  }
}
