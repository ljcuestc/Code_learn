import sys
import random
import pygame

# Game settings
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 700
FPS = 60


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # draw a simple triangular plane shape
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.polygon(
            self.image,
            (0, 255, 0),
            [(30, 0), (0, 60), (60, 60)],
        )
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5
        self.bullets = pygame.sprite.Group()
        self.kill_count = 0

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def shoot(self):
        damage = 2 if self.kill_count >= 5 else 1
        bullet = Bullet(self.rect.centerx, self.rect.top, damage)
        self.bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40), pygame.SRCALPHA)
        # simple enemy shape
        pygame.draw.polygon(
            self.image,
            (255, 0, 0),
            [(0, 0), (50, 20), (0, 40)]
        )
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(1, 3)
        self.health = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, damage):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -7
        self.damage = damage

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Plane Battle")
    clock = pygame.time.Clock()

    player = Player()
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)

    enemy_spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy_spawn_event, 1000)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.shoot()
            elif event.type == enemy_spawn_event:
                enemy = Enemy()
                enemies.add(enemy)
                all_sprites.add(enemy)

        keys = pygame.key.get_pressed()
        player.update(keys)
        player.bullets.update()
        enemies.update()

        # collision detection
        hits = pygame.sprite.groupcollide(enemies, player.bullets, False, True)
        for enemy, bullets in hits.items():
            for bullet in bullets:
                enemy.health -= bullet.damage
            if enemy.health <= 0:
                enemy.kill()
                player.kill_count += 1

        if pygame.sprite.spritecollideany(player, enemies):
            running = False

        # drawing
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        player.bullets.draw(screen)

        # draw enemy health bars
        for enemy in enemies:
            bar_width = enemy.rect.width
            bar_height = 5
            fill_width = int(bar_width * (enemy.health / 2))
            bar_x = enemy.rect.x
            bar_y = enemy.rect.y - bar_height - 2
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
