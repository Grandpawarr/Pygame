# TODO: yt video at 1:30:53
import pygame
import random
import os

# Settings Window
FPS = 60
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

# Intial the game and create the windows
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Display the windows title
pygame.display.set_caption("Tony's game")
clock = pygame.time.Clock()

# Load image
background_img = pygame.image.load(os.path.join("Img", "background.png")).convert()
player_img = pygame.image.load(os.path.join("Img", "player.png")).convert()
bullet_img = pygame.image.load(os.path.join("Img", "bullet.png")).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("Img", f"rock{i}.png")).convert())


# Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, (255,0,0), self.rect.center, self.radius)
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speedx = 8
        self.speedy = 4

    def update(self):
        # Player movement
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        elif key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        elif key_pressed[pygame.K_UP]:
            self.rect.y -= self.speedy
        elif key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedy

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


"""
 @brew:
 Create a falling and drifting stone
 that will be reset when it exceeds the bounds of the windows
"""


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey((0, 0, 0))
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 / 2
        # pygame.draw.circle(self.image, (255,0,0), self.rect.center, self.radius)
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 10)
        self.total_degree = 0
        self.rot_degree = random.randrange(-5, 5)

    """ 
     1. Always start from the original image for each update to avoid issues caused
        by multiple updates(as each update and rotation can introduce errors,
        too many updates can lead to image distortion).
        If the rotation angle exceeds 360 degree, take the remainder.
     2. Reposition the center point with ezch image rotation to prevent the frame from distorting 
    """

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (
            self.rect.top > SCREEN_HEIGHT
            or self.rect.left > SCREEN_WIDTH
            or self.rect.right < 0
        ):
            self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 10)


all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

# game loop
is_running = True
while is_running:
    # game can only be executed FPS times in one second
    clock.tick(FPS)
    # Get the input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update game
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        rock = Rock()
        all_sprites.add(rock)
        rocks.add(rock)

    hits = pygame.sprite.spritecollide(player, rocks, False)
    if hits:
        is_running = False

    # Screen display
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()
