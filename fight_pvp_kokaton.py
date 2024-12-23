import pygame as pg
import math
import random  # ランダムモジュールをインポート

class TheWorld:
    """
    時を止めるクラス
    """
    def __init__(self):
        self.time_stop_bird = False   # Bird用の時間停止状態
        self.time_stop_bird2 = False  # Bird_2用の時間停止状態

    def toggle_bird(self):
        """Birdの時間停止を切り替える"""
        self.time_stop_bird = not self.time_stop_bird

    def toggle_bird2(self):
        """Bird_2の時間停止を切り替える"""
        self.time_stop_bird2 = not self.time_stop_bird2

    def is_time_stopped(self, bird_name):
        """指定された鳥が時間停止状態かを返す"""
        if bird_name == "bird":
            return self.time_stop_bird
        elif bird_name == "bird_2":
            return self.time_stop_bird2
        return False

class Bird:
    def __init__(self, x, y, img, speed=5):
        self.x = x
        self.y = y
        self.img = img
        self.speed = speed
        self.dire = (0, 0)  # 初期方向は(0, 0)
        self.rect = self.img.get_rect(topleft=(x, y))  # 位置を設定

    def update(self, keys, time_stopped):
        if time_stopped:
            return 
        # キーに基づいて方向を更新
        self.dire = (0, 0)
        if keys[pg.K_LEFT] and self.x > 400:  # 左半分に制限（x座標が400より小さくならないように）
            self.x -= self.speed
            self.dire = (-1, 0)  # 左
        if keys[pg.K_RIGHT]:
            self.x += self.speed
            self.dire = (1, 0)  # 右
        if keys[pg.K_UP]:
            self.y -= self.speed
            self.dire = (0, -1)  # 上
        if keys[pg.K_DOWN]:
            self.y += self.speed
            self.dire = (0, 1)  # 下
        self.rect.topleft = (self.x, self.y)  # rectの位置を更新

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))


class Bird_2:
    def __init__(self, x, y, img, speed=5):
        self.x = x
        self.y = y
        self.img = img
        self.speed = speed
        self.dire = (0, 0)  # 初期方向は(0, 0)
        self.rect = self.img.get_rect(topleft=(x, y))  # 位置を設定

    def update(self, keys, time_stopped):
        if time_stopped:
            return
        # キーに基づいて方向を更新
        self.dire = (0, 0)
        if keys[pg.K_a] and self.x > 0:  # 左半分に制限（x座標が0より小さくならないように）
            self.x -= self.speed
            self.dire = (-1, 0)  # 左
        if keys[pg.K_d] and self.x < 400:  # 右端に制限（400より右には行かない）
            self.x += self.speed
            self.dire = (1, 0)  # 右
        if keys[pg.K_w]:
            self.y -= self.speed
            self.dire = (0, -1)  # 上
        if keys[pg.K_s]:
            self.y += self.speed
            self.dire = (0, 1)  # 下
        self.rect.topleft = (self.x, self.y)  # rectの位置を更新

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))


class Beam(pg.sprite.Sprite):
    """
    ビームに関するクラス
    """
    def __init__(self, bird, angle=0):
        """
        ビーム画像Surfaceを生成する
        引数 bird：ビームを放つ鳥
        引数 angle: ビームが回転する角度
        """
        super().__init__()
        self.vx, self.vy = bird.dire

        # birdがBirdの場合は左向き、Bird_2の場合は右向きに設定
        if isinstance(bird, Bird):  # Birdから発射されるビームを左向き
            initial_angle = 180  # 180度回転させる
        else:  # Bird_2から発射されるビームを右向き
            initial_angle = 0  # 0度回転させる
        
        self.image = pg.transform.rotozoom(pg.image.load("ex5/fig/beam.png"), initial_angle, 1.0)
        self.vx = math.cos(math.radians(initial_angle))  # x方向の速度
        self.vy = -math.sin(math.radians(initial_angle))  # y方向の速度
        self.rect = self.image.get_rect()
        self.rect.centery = bird.rect.centery + bird.rect.height * self.vy
        self.rect.centerx = bird.rect.centerx + bird.rect.width * self.vx
        self.speed = 10  # ビームの速度

    def update(self, time_stopped):
        """
        ビームを速度ベクトルself.vx, self.vyに基づき移動させる
        また、ビームと鳥が衝突しているか確認する
        """
        if time_stopped:
            return
        self.rect.move_ip(self.speed * self.vx, self.speed * self.vy)

        # birdとbird_2の衝突判定
        if self.rect.colliderect(bird.rect):  # ビームがbirdに当たった場合
            self.kill()  # ビームを削除
        if self.rect.colliderect(bird_2.rect):  # ビームがbird_2に当たった場合
            self.kill()  # ビームを削除

        # ビームが画面外に出たら削除
        if not (0 <= self.rect.left <= 800 and 0 <= self.rect.top <= 600):
            self.kill()  # 画面外に出たビームを削除


def check_bound(rect):
    left, top, right, bottom = rect.left, rect.top, rect.right, rect.bottom
    return 0 <= left <= 800 and 0 <= top <= 600


# ゲーム初期化
pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()

# 背景と鳥の画像を読み込む
background = pg.image.load("ex5/fig/pg_bg.jpg")
bird_img = pg.image.load("ex5/fig/0.png")
bird_2_img = pg.image.load("ex5/fig/1.png")

# Birdインスタンスを作成（fig/0は右半分のランダムな位置に設定）
bird = Bird(random.randint(400, 800), random.randint(100, 500), bird_img)  # x:400〜800の範囲、y:100〜500
bird_2 = Bird_2(300, 100, bird_2_img)

# ビーム用のスプライトグループを作成
beams = pg.sprite.Group()

the_world = TheWorld()

pause_overlay = pg.Surface((800, 600), pg.SRCALPHA)
pause_overlay.fill((0, 0, 0, 153))  # 透明度60%の黒背景

# ゲームループ
running = True
while running:
    screen.fill((255, 255, 255))  # 画面を白で塗りつぶす
    
    # 背景を描画
    screen.blit(background, (0, 0))

    # 中央に赤い線を描画
    pg.draw.line(screen, (255, 0, 0), (400, 0), (400, 600), 3)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_TAB:  # Birdの時停止切り替え
                the_world.toggle_bird()
            if event.key == pg.K_p:  # Bird_2の時停止切り替え
                the_world.toggle_bird2()

    keys = pg.key.get_pressed()

    # 鳥の更新
    bird.update(keys, the_world.is_time_stopped("bird"))
    bird_2.update(keys, the_world.is_time_stopped("bird_2"))


    # 鳥を描画  
    bird.draw(screen)
    bird_2.draw(screen)

    # ビーム発射（右シフトはbird、左シフトはbird_2）
    if keys[pg.K_RSHIFT]:  # birdのビーム（右シフト）
        beam = Beam(bird)
        beams.add(beam)

    if keys[pg.K_LSHIFT]:  # bird_2のビーム（左シフト）
        beam = Beam(bird_2)
        beams.add(beam)

    # ビームを更新して描画
    if the_world.is_time_stopped("bird"):
        beam = Beam(bird, "bird")
        beams.add(beam)
        beam.update(the_world.is_time_stopped("bird"))
    elif the_world.is_time_stopped("bird_2"):
        beam_2 = Beam(bird_2, "bird_2")
        beams.add(beam_2)
        beam_2.update(the_world.is_time_stopped("bird_2"))
    else:
        beams.update(None)
    beams.draw(screen)

    if the_world.is_time_stopped("bird") or the_world.is_time_stopped("bird_2"):
        screen.blit(pause_overlay, (0, 0))
        font = pg.font.Font(None, 74)
        if the_world.is_time_stopped("bird"):
            text = font.render("BIRD TIME STOPPED", True, (255, 0, 0))
            screen.blit(text, (200, 250))
        if the_world.is_time_stopped("bird_2"):
            text = font.render("BIRD_2 TIME STOPPED", True, (0, 0, 255))
            screen.blit(text, (200, 350))

    pg.display.flip()
    clock.tick(60)

pg.quit()