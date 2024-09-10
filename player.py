import pygame
from support import import_sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self._import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations["idle"][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.gravity = 0.8
        self.jump_move = -16
        # player status
        self.life = 5
        self.game_over = False
        self.win = False
        self.status = "idle"
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def _import_character_assets(self):
        character_path = "assets/player/"
        self.animations = {"idle": [], "walk": [], "jump": [], "fall": [], "lose": [], "win": [], "attack": []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_sprite(full_path)

    def _animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0 if self.status != "attack" else len(animation) - 1
        image = animation[int(self.frame_index)]
        image = pygame.transform.scale(image, (35, 50))
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def _get_input(self, player_event):
        if player_event != False:
            if player_event == "right":
                self.direction.x = 1
                self.facing_right = True
            elif player_event == "left":
                self.direction.x = -1
                self.facing_right = False
            elif player_event == "left_mouse":
                self.status = "attack"
        else:
            self.direction.x = 0

    def _jump(self):
        self.direction.y = self.jump_move

    def _get_status(self):
        if self.status == "attack" and self.frame_index < len(self.animations["attack"]) - 1:
            return
        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > 1:
            self.status = "fall"
        elif self.direction.x != 0:
            self.status = "walk"
        else:
            self.status = "idle"

    def update(self, player_event):
        self._get_status()
        if self.life > 0 and not self.game_over:
            if player_event == "space" and self.on_ground:
                self._jump()
            else:
                self._get_input(player_event)
        elif self.game_over and self.win:
            self.direction.x = 0
            self.status = "win"
        else:
            self.direction.x = 0
            self.status = "lose"
        self._animate()

    def draw(self, surface, offset):
        """Draw player on screen with camera offset."""
        surface.blit(self.image, (self.rect.x - offset.x, self.rect.y - offset.y))
