import pygame
from settings import tile_size, WIDTH
from tile import Tile
from dirt import Dirt
from trap import Trap
from goal import Goal
from player import Player
from enemy import Enemy
from game import Game


class World:
    def __init__(self, world_data, screen):
        self.screen = screen
        self.world_data = world_data
        self._setup_world(world_data)
        self.world_shift = 0
        self.current_x = 0
        self.gravity = 0.8
        self.game = Game(self.screen)
        self.sprites = pygame.sprite.Group()  # Группа для всех спрайтов

    def add(self, sprite):
        """Добавление спрайта в группу спрайтов."""
        self.sprites.add(sprite)

    def draw(self, screen):
        """Отрисовка всех спрайтов в мире."""
        self.sprites.draw(screen)

    # Генерация частей мира (игрок, препятствия, цель, клетка)
    def _setup_world(self, layout):
        self.tiles = pygame.sprite.Group()
        self.dirt = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()  # Группа для врагов

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x, y = col_index * tile_size, row_index * tile_size
                if cell == "X":
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == "D":
                    tile = Dirt((x, y), tile_size)
                    self.dirt.add(tile)
                elif cell == "t":
                    tile = Trap((x + (tile_size // 4), y + (tile_size // 4)), tile_size // 2)
                    self.traps.add(tile)
                elif cell == "P":
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                elif cell == "G":
                    goal_sprite = Goal((x, y), tile_size)
                    self.goal.add(goal_sprite)
                elif cell == "E":  # Добавляем врагов
                    enemy_sprite = Enemy((x, y))
                    self.enemies.add(enemy_sprite)
                    self.add(enemy_sprite)  # Добавляем врага в общий список спрайтов

    def _scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < WIDTH // 3 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > WIDTH - (WIDTH // 3) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 3

    def _apply_gravity(self, player):
        player.direction.y += self.gravity
        player.rect.y += player.direction.y

    def _horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def _vertical_movement_collision(self):
        player = self.player.sprite
        self._apply_gravity(player)
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        for sprite in self.dirt.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def _handle_traps(self):
        player = self.player.sprite
        for sprite in self.traps.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0 or player.direction.y > 0:
                    player.rect.x += tile_size
                elif player.direction.x > 0 or player.direction.y > 0:
                    player.rect.x -= tile_size
                player.life -= 1

    def update(self, player_event):
        # Обновляем все группы спрайтов
        self.tiles.update(self.world_shift)
        self.dirt.update(self.world_shift)
        self.traps.update(self.world_shift)
        self.goal.update(self.world_shift)
        self.enemies.update()  # Обновляем врагов

        # Обновляем игрока
        self.player.update(player_event)
        
        # Обработка всех столкновений и гравитации
        self._scroll_x()
        self._horizontal_movement_collision()
        self._vertical_movement_collision()
        self._handle_traps()
        
        # Отображение состояния игры
        self.game.show_life(self.player.sprite)
        self.game.game_state(self.player.sprite, self.goal.sprite)
        
        # Отрисовка всех групп спрайтов
        self.tiles.draw(self.screen)
        self.dirt.draw(self.screen)
        self.traps.draw(self.screen)
        self.goal.draw(self.screen)
        
        # Отрисовка игрока
        self.player.draw(self.screen)

        # Отрисовка врагов
        self.enemies.draw(self.screen)
