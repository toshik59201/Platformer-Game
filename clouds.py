import pygame
import random
from settings import WIDTH, HEIGHT


class Cloud:
    def __init__(self, image, x, y, speed):
        self.original_image = image
        self.image = image.copy()
        self.x = x
        self.y = y
        self.speed = speed
        self.alpha = 0
        self.image.set_alpha(self.alpha)

    def move(self):
        self.x += self.speed
        if self.x > WIDTH:
            return True
        return False

    def draw(self, screen):
        if self.alpha < 255:
            self.alpha += 1  # Increase transparency gradually
            self.image.set_alpha(self.alpha)
        screen.blit(self.image, (self.x, self.y))

class CloudManager:
    def __init__(self, screen, cloud_images, min_clouds=5, max_clouds=10):
        self.screen = screen
        self.cloud_images = cloud_images
        self.min_clouds = min_clouds
        self.max_clouds = max_clouds
        self.clouds = []
        self.cloud_timer = 0

        for _ in range(self.min_clouds):
            self.add_cloud()

    def add_cloud(self):
        cloud_image = random.choice(self.cloud_images)
        x = random.randint(-cloud_image.get_width(), WIDTH)
        y = random.randint(0, HEIGHT // 2)
        speed = random.uniform(0.5, 2)
        self.clouds.append(Cloud(cloud_image, x, y, speed))

    def update(self):
        self.cloud_timer += 1
        if self.cloud_timer > 60:  # Adjust cloud generation frequency
            if len(self.clouds) < self.max_clouds:
                self.add_cloud()
            self.cloud_timer = 0

        for cloud in self.clouds[:]:
            if cloud.move():
                self.clouds.remove(cloud)
            cloud.draw(self.screen)
