import pygame
from support import import_sprite


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, speed=3, patrol_range=100):
        super().__init__()
        self._import_enemy_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations["idle"][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        # enemy movement
        self.direction = pygame.math.Vector2(1, 0)  # Start moving right
        self.speed = speed
        self.patrol_range = patrol_range
        self.start_pos = pygame.math.Vector2(pos)
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def _import_enemy_assets(self):
        character_path = "assets/enemy/"
        self.animations = {
            "idle": [],
            "walk": [],
            "attack": [],
            "die": []
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_sprite(full_path)

    def _animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        image = pygame.transform.scale(image, (35, 50))
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def _patrol(self):
        if abs(self.rect.x - self.start_pos.x) >= self.patrol_range:
            self.direction.x *= -1
            self.facing_right = not self.facing_right

    def _get_status(self):
        if self.direction.x != 0:
            self.status = "walk"
        else:
            self.status = "idle"

    def update(self):
        self._get_status()
        self._patrol()
        self.rect.x += self.direction.x * self.speed
        self._animate()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
