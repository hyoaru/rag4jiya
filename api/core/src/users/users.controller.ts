import { Body, Controller, Get, Param, Patch, UseGuards } from '@nestjs/common';
import { UsersService } from './users.service';
import { ApiCookieAuth, ApiResponse } from '@nestjs/swagger';
import { UserDto } from './dto/user.dto';
import { plainToInstance } from 'class-transformer';
import { JwtAuthGuard } from 'src/authentication/guards/jwt.guard';
import { UpdateUserRequestDto } from './dto/update-user.request.dto';

@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get()
  @UseGuards(JwtAuthGuard)
  @ApiCookieAuth('Authentication')
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

  @Patch(':id')
  @ApiResponse({ status: 200, type: UserDto })
  async update(@Param('id') id: string, @Body() dto: UpdateUserRequestDto) {
    const record = await this.usersService.update({
      id: id,
      data: {
        firstName: dto.first_name,
        lastName: dto.last_name,
        email: dto.email,
        password: dto.password,
        refreshToken: dto.refresh_token,
      },
    });

    return plainToInstance(UserDto, record, {
      excludeExtraneousValues: true,
    });
  }
}
