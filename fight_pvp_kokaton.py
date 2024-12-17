import pygame

class Bird:
    def __init__(self, x, y, img, speed=5):
        self.x = x
        self.y = y
        self.img = img
        self.speed = speed
    
    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
    
    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

class Bird_2:
    def __init__(self, x, y, img, speed=5):
        self.x = x
        self.y = y
        self.img = img
        self.speed = speed
    
    def update(self, keys):
        if keys[pygame.K_a]:  # 左
            self.x -= self.speed
        if keys[pygame.K_d]:  # 右
            self.x += self.speed
        if keys[pygame.K_w]:  # 上
            self.y -= self.speed
        if keys[pygame.K_s]:  # 下
            self.y += self.speed
    
    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

# ゲーム初期化
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# 背景画像の読み込み
background = pygame.image.load("ex5/fig/pg_bg.jpg")

# 画像の設定 (動く□)
bird_img = pygame.image.load("ex5/fig/0.png")  # 赤い□の画像
bird_2_img = pygame.image.load("ex5/fig/1.png")  # 緑色の□の画像

# こうかとんと二体目のインスタンス生成
bird = Bird(100, 100, bird_img)
bird_2 = Bird_2(300, 100, bird_2_img)

# ゲームループ
running = True
while running:
    screen.fill((255, 255, 255))  # 背景を白に
    
    # 背景画像を描画
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # こうかとんの更新と描画
    bird.update(keys)
    bird.draw(screen)

    # 二体目のこうかとんの更新と描画
    bird_2.update(keys)
    bird_2.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
