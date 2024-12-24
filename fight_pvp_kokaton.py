import pygame as pg
import math
import random  # ランダムモジュールをインポート
pg.mixer.init()
move_sound = pg.mixer.Sound("ex5/fig/ワープ.mp3")
boot_sound = pg.mixer.Sound("ex5/fig/起動.mp3")
import time

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

class Status:
    """
    HP（ヒットポイント）とMP（魔法ポイント）を管理するクラス。
    HPやMPの増減、画面上への表示を行う。
    """

    def __init__(self, mp=100, hp=100):
        """
        MPとHPを初期化。デフォルト値はどちらも100。
        """
        self.mp = mp  # 魔法ポイント（MP）
        self.hp = hp  # ヒットポイント（HP）

    def decrease_mp(self,amount = 1 ):
        """
        MPを1減少（MPが0より大きい場合のみ）
        """
        if self.mp > 0:
            self.mp -= 1
            if keys[pg.K_0]:
                self.mp -=50


    def decrease_hp(self, amount=2,):
        """
        HPを指定量減少（HPが0より大きい場合のみ）
        """



        if self.hp > 0:
            self.hp -= amount

    # def increace_hp(self, amount=2, ):
    #     """
    #     HPを指定量減少（HPが0より大きい場合のみ）
    #     """



    #     if self.hp > 0:
    #         if shields == True:
    #             self.hp += 1

    def draw(self, screen, x_offset, y_offset):
        """
        MPとHPの値を画面に描画
        """
        font = pg.font.Font(None, 36)
        mp_text = font.render(f'MP: {self.mp}', True, (0, 0, 0))
        hp_text = font.render(f'HP: {self.hp}', True, (0, 0, 0))
        screen.blit(mp_text, (x_offset, y_offset))
        screen.blit(hp_text, (x_offset, y_offset - 30))

class Finish:
    """
    ゲームの終了時に勝者を表示するクラス
    """
    def __init__(self, winner_name, winner_img):
        """
        初期化メソッド。勝者の名前と画像を設定
        """
        self.winner_name = winner_name
        self.winner_img = winner_img

    def draw(self, screen):
        """
        勝者の名前と画像を画面に描画
        """
        font = pg.font.Font(None, 80)
        message = font.render(f"{self.winner_name} WINN!!", True, (255, 0, 0))
        message_rect = message.get_rect(center=(400, 300))
        screen.blit(message, message_rect)

        winner_left_rect = self.winner_img.get_rect(center=(200, 300))
        winner_right_rect = self.winner_img.get_rect(center=(600, 300))
        screen.blit(self.winner_img, winner_left_rect)
        screen.blit(self.winner_img, winner_right_rect)

class Bird:
    """
    鳥_1キャラクターを表すクラスで、1P用の操作を実装
    """
    def __init__(self, x, y, img, status, speed=5):
        """
        初期化メソッド。位置、画像、ステータス、速度を設定
        """
        self.x = x
        self.y = y
        self.img = img
        self.speed = speed
        self.dire = (0, 0)  # 初期方向は(0, 0)
        self.rect = self.img.get_rect(topleft=(x, y))  # 位置を設定
        self.status = status
        self.base_speed = speed  # デフォルトの速度
        self.dire = (0, 0)  # 初期方向
        self.rect = self.img.get_rect(topleft=(x, y))
        self.trail = []  # 残像の位置リスト
        self.boost_timer = 0  # 加速タイマー (10秒 = 600フレーム @ 60FPS)
       


    def update(self, keys, time_stopped):
        if time_stopped:
            return 
        if keys[pg.K_0] and self.boost_timer == 0:
            self.boost_timer = 600  # 10秒ブースト
            #bird.status.decrease_mp(50)  # MPを50消費
            boot_sound.play()


        # ブースト中の処理
        if self.boost_timer > 0:
            self.speed = self.base_speed * 7 #4倍速
            self.boost_timer -= 1
        else:
            self.speed = self.base_speed
            self.trail.clear()  # 残像をクリアする
        # キーに基づいて方向を更新
        self.dire = (0, 0)
        if keys[pg.K_LEFT] and self.x > 400:
            self.x -= self.speed
            self.dire = (-1, 0)  # 左
            if self.boost_timer > 0:
                move_sound.play()
        if keys[pg.K_RIGHT]:
            self.x += self.speed
            self.dire = (1, 0)  # 右
            if self.boost_timer > 0:
                move_sound.play()
        if keys[pg.K_UP]:
            self.y -= self.speed
            self.dire = (0, -1)  # 上
            if self.boost_timer > 0:
                move_sound.play()
        if keys[pg.K_DOWN]:
            self.y += self.speed
            self.dire = (0, 1)  # 下
            if self.boost_timer > 0:
                move_sound.play()
        self.rect.topleft = (self.x, self.y)  # rectの位置を更新
        if self.boost_timer > 0:
            self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)

        if keys[pg.K_LEFT] and self.x > 400:  # 左半分に制限（x座標が400より小さくならないように）
            self.x -= self.speed
    def draw(self, screen):
        for i, (tx, ty) in enumerate(self.trail):
            trail_img = self.img.copy()
            # 残像の色を薄い赤に変更
            red_surface = pg.Surface(self.img.get_size(), flags=pg.SRCALPHA)
            red_surface.fill((255, 100, 100, 150))  # 薄い赤色（透明度150）
            trail_img.blit(red_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
            alpha = max(0, 255 - (i * 25))  # 古い残像ほど透明にする
            trail_img.set_alpha(alpha)
            screen.blit(trail_img, (tx, ty))

        # ブースト中は色を変更
        if self.boost_timer > 0:
            self.acceleration_effect(screen)
        else:
            screen.blit(self.img, (self.x, self.y))
    

    # 音声ファイルの読み込み



    def acceleration_effect(self, screen):
        """加速中は画像を薄い赤色に変更"""
        tinted_img = self.img.copy()
        red_surface = pg.Surface(self.img.get_size(), flags=pg.SRCALPHA)
        red_surface.fill((255, 100, 100, 180))  # 薄い赤
        tinted_img.blit(red_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        screen.blit(tinted_img, (self.x, self.y))
        



class Bird_2:
    """
    鳥_2キャラクターを表すクラスで、2P用の操作を実装
    """
    def __init__(self, x, y, img, status, speed=5):
        """
        初期化メソッド。位置、画像、ステータス、速度を設定
        """
        self.x = x
        self.y = y
        self.img = img
        self.speed = speed
        self.dire = (0, 0)  # 初期方向は(0, 0)
        self.rect = self.img.get_rect(topleft=(x, y))  # 位置を設定
        self.status = status
        self.base_speed = speed  # デフォルトの速度
        self.dire = (0, 0)  # 初期方向
        self.rect = self.img.get_rect(topleft=(x, y))
        self.trail = []  # 残像の位置リスト
        self.boost_timer = 0  # 加速タイマー (10秒 = 600フレーム @ 60FPS)


    def update(self, keys, time_stopped):
        if time_stopped:
            return
        if keys[pg.K_1] and self.boost_timer == 0:
            self.boost_timer = 600  # 10秒ブースト
            bird_2.status.decrease_mp(50)  # MPを50消費
            boot_sound.play()

        # ブースト中の処理
        if self.boost_timer > 0:
            self.speed = self.base_speed * 4 #4倍速
            self.boost_timer -= 1
        else:
            self.speed = self.base_speed
            self.trail.clear()  # 残像をクリアする
        # キーに基づいて方向を更新
        self.dire = (0, 0)
        if keys[pg.K_a] and self.x > 0:  # 左半分に制限（x座標が0より小さくならないように）
            self.x -= self.speed
        # キーに基づいて方向を更新
        self.dire = (0, 0)
        if keys[pg.K_a] and self.x > 0:
            self.x -= self.speed
            self.dire = (-1, 0)  # 左
            if self.boost_timer > 0:
                move_sound.play()
        if keys[pg.K_d] and self.x < 400:  # 右端に制限（400より右には行かない）
            self.x += self.speed
            self.dire = (1, 0)  # 右
            if self.boost_timer > 0:
                move_sound.play()
        if keys[pg.K_w]:
            self.y -= self.speed
            self.dire = (0, -1)  # 上
            if self.boost_timer > 0:
                move_sound.play()
        if keys[pg.K_s]:
            self.y += self.speed
            self.dire = (0, 1)  # 下
            if self.boost_timer > 0:
                move_sound.play()
        self.rect.topleft = (self.x, self.y)  # rectの位置を更新
        # 残像の位置を記録 (ブースト中のみ)
        if self.boost_timer > 0:
            self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)

    def draw(self, screen):
        for i, (tx, ty) in enumerate(self.trail):
            trail_img = self.img.copy()
            # 残像の色を薄い水色に変更
            blue_surface = pg.Surface(self.img.get_size(), flags=pg.SRCALPHA)
            blue_surface.fill((100, 100, 255, 150))  # 薄い水色（透明度150）
            trail_img.blit(blue_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
            alpha = max(0, 255 - (i * 25))  # 古い残像ほど透明にする
            trail_img.set_alpha(alpha)
            screen.blit(trail_img, (tx, ty))

        # ブースト中は色を変更
        if self.boost_timer > 0:
            self.acceleration_effect(screen)
        else:
            screen.blit(self.img, (self.x, self.y))
    
      
    def acceleration_effect(self, screen):
        """加速中は画像を薄い水色に変更"""
        tinted_img = self.img.copy()
        blue_surface = pg.Surface(self.img.get_size(), flags=pg.SRCALPHA)
        blue_surface.fill((100, 100, 255, 180))  # 薄い水色
        tinted_img.blit(blue_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        screen.blit(tinted_img, (self.x, self.y))


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

    def update(self):
        """
        ビームを速度ベクトルself.vx, self.vyに基づき移動させる
        また、ビームと鳥が衝突しているか確認する
        """
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

    def update(self):
        """
        ビームを速度ベクトルself.vx, self.vyに基づき移動させる
        また、ビームと鳥が衝突しているか確認する
        """
        self.rect.move_ip(self.speed * self.vx, self.speed * self.vy)

        # birdとbird_2の衝突判定
        if self.rect.colliderect(bird.rect):  # ビームがbirdに当たった場合
            self.kill()  # ビームを削除
        if self.rect.colliderect(bird_2.rect):  # ビームがbird_2に当たった場合
            self.kill()  # ビームを削除

        # ビームが画面外に出たら削除
        if not (0 <= self.rect.left <= 800 and 0 <= self.rect.top <= 600):
            self.kill()  # 画面外に出たビームを削除

class Shield(pg.sprite.Sprite):
    """
    防御壁に関するクラス
    """
    def __init__(self, bird, life=300, width_factor=0.1, height_factor=0.1):
        """
        防御壁を生成する
        引数 bird：防御壁を設置するこうかとん
        引数 life：防御壁の寿命（フレーム数）
        """
        super().__init__()
        self.life = life

        # シールドを画像に変更
        original_image = pg.image.load("ex5/fig/at.png").convert_alpha()  # 4.pngを読み込む
        
        # リサイズ（width_factorとheight_factorで指定された倍率でリサイズ）
        new_width = int(original_image.get_width() * width_factor)
        new_height = int(original_image.get_height() * height_factor)
        self.image = pg.transform.scale(original_image, (new_width, new_height))
        self.rect = self.image.get_rect(center=bird.rect.center)
        self.initial_position = self.rect.center  # 発動時に位置を固定
        

    def update(self, bird):
        self.life -= 1  # 寿命を減らす
        if self.life <= 0:
            self.kill()  # 寿命が尽きたら削除
        
        # # 位置を固定して動かさない
        # self.rect.center = self.initial_position  # 固定された位置に維持
        self.rect.center = bird.rect.center

class Shield2(pg.sprite.Sprite):
    """
    防御壁に関するクラス
    """
    def __init__(self, bird, life=300, width_factor=0.1, height_factor=0.1):
        """
        防御壁を生成する
        引数 bird：防御壁を設置するこうかとん
        引数 life：防御壁の寿命（フレーム数）
        """
        super().__init__()
        self.life = life

        # シールドの画像を4.pngに変更
        original_image = pg.image.load("ex5/fig/at.png").convert_alpha() 
        # リサイズ（width_factorとheight_factorで指定された倍率でリサイズ）
        new_width = int(original_image.get_width() * width_factor)
        new_height = int(original_image.get_height() * height_factor)
        self.image = pg.transform.scale(original_image, (new_width, new_height))  # リサイズされた画像  # 4.pngを読み込む
        self.rect = self.image.get_rect(center=bird.rect.center)
        self.initial_position = self.rect.center  # 発動時に位置を固定
        

    def update(self, bird):
        self.life -= 1  # 寿命を減らす
        if self.life <= 0:
            self.kill()  # 寿命が尽きたら削除
        # # 位置を固定して動かさない
        # self.rect.center = self.initial_position  # 固定された位置に維持
        
        self.rect.center = bird_2.rect.center



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

    def update(self, bird, bird_2, time_stopped):
        """
        ビームの位置を更新し、他の鳥と衝突した場合にHPを減少。
        また、画面外に出たビームを削除
        """
        if time_stopped:
            return 
        self.rect.move_ip(self.speed * self.vx, self.speed * self.vy)
        if self.rect.colliderect(bird.rect):
            bird.status.decrease_hp() 
            self.kill()
        if self.rect.colliderect(bird_2.rect):
            bird_2.status.decrease_hp()
            self.kill()

        if not (0 <= self.rect.left <= 800 and 0 <= self.rect.top <= 600):
            self.kill()

###################
class HomingBeam(pg.sprite.Sprite):
    """
    追尾弾（ホーミングビーム）に関するクラス
    """
    def __init__(self, bird, target):
        """
        追尾弾の初期化
        引数 bird: 発射する鳥
        引数 target: 追尾するターゲット（敵の鳥）
        """
        super().__init__()
        self.image = pg.image.load("ex5/fig/beam.png")
        self.image = pg.transform.scale(self.image, (15, 15))  # 追尾弾のサイズを小さくする
        self.rect = self.image.get_rect(center=bird.rect.center)

        self.speed = 5  # 追尾弾の速度
        self.target = target  # 追尾対象
        self.spawn_time = time.time()  # 発射時の時間を記録


        # 初期速度ベクトルを設定
        self.vx, self.vy = 0, 0

    def calculate_velocity(self):
        """
        ターゲットの位置に向かって速度ベクトルを計算する
        """
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery

        # ベクトルを正規化して速度に乗じる
        length = math.hypot(dx, dy)
        if length != 0:
            self.vx = self.speed * (dx / length)
            self.vy = self.speed * (dy / length)

    def update(self,*args):
        """
        毎フレームごとにターゲットの位置を追尾し、移動する
        """
        self.calculate_velocity()
        self.rect.move_ip(self.vx, self.vy)

        # ターゲットに当たったら弾を消す
        if self.rect.colliderect(self.target.rect):
            self.target.status.decrease_hp(amount=1)  # HPを減らす処理を追加（必要に応じて）
            self.kill()

        if time.time() - self.spawn_time > 3:
            self.kill()
        # 画面外に出たら削除
        if not check_bound(self.rect):
            self.kill()
##################








def check_bound(rect):
    left, top, right, bottom = rect.left, rect.top, rect.right, rect.bottom
    return 0 <= left <= 800 and 0 <= top <= 600





# ゲーム初期化
pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()
pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()

# 背景と鳥の画像を読み込む
background = pg.image.load("ex5/fig/pg_bg.jpg")
bird_img = pg.image.load("ex5/fig/0.png")
bird_2_img = pg.image.load("ex5/fig/1.png")
# 背景と鳥の画像を読み込む
background = pg.image.load("ex5/fig/pg_bg.jpg")
bird_img = pg.image.load("ex5/fig/0.png")
bird_2_img = pg.image.load("ex5/fig/1.png")



# ビーム用のスプライトグループを作成
beams = pg.sprite.Group()

# シールド用のスプライトグループを作成
shields = pg.sprite.Group()
shields2 = pg.sprite.Group()

# シールドの発動フラグを追加
shield_active_bird = False
shield_active_bird_2 = False


if shield_active_bird == True:
    Status.bird.decrease_hp(-50)  # hpを30消費
    


    #.status.decrease_hp(0)  # hpを30消費

if shield_active_bird_2 == True:
    Status.bird.decrease_hp(-50)  # hpを30消費
    
# Birdインスタンスを作成（fig/0は右半分のランダムな位置に設定）
bird_status = Status()
bird_2_status = Status()
bird = Bird(random.randint(400, 800), random.randint(100, 500), bird_img, bird_status)
bird_2 = Bird_2(300, 100, bird_2_img, bird_2_status)

# ビーム用のスプライトグループを作成
beams = pg.sprite.Group()

the_world = TheWorld()

pause_overlay = pg.Surface((800, 600), pg.SRCALPHA)
pause_overlay.fill((0, 0, 0, 153))  # 透明度60%の黒背景
background = pg.image.load("ex5/fig/pg_bg.jpg")
bird_img = pg.image.load("ex5/fig/0.png")
bird_2_img = pg.image.load("ex5/fig/1.png")

running = True
finish = None
while running:
    screen.fill((255, 255, 255))  # 画面を白で塗りつぶす
    
    # 背景を描画
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    pg.draw.line(screen, (255, 0, 0), (400, 0), (400, 600), 5)

    # 中央に赤い線を描画
    pg.draw.line(screen, (255, 0, 0), (400, 0), (400, 600), 3)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_TAB:  # Birdの時停止切り替え
                the_world.toggle_bird()
                bird.status.decrease_mp(100)  # MPを50消費
            if event.key == pg.K_p:  # Bird_2の時停止切り替え
                the_world.toggle_bird2()
                bird_2.status.decrease_mp(100)  # MPを50消費

    keys = pg.key.get_pressed()


    if finish is None:
        bird.update(keys, the_world.is_time_stopped("bird"))
        bird_2.update(keys, the_world.is_time_stopped("bird_2"))
        print(f"MP: Bird = {bird.status.mp}, Bird_2 = {bird_2.status.mp}")  # デバッグ用
        # ビーム発射（右シフトはbird、左シフトはbird_2）
        if keys[pg.K_RSHIFT] and bird.status.mp > 0:
            beam = Beam(bird)
            beams.add(beam)
            bird.status.decrease_mp()

        if keys[pg.K_LSHIFT] and bird_2.status.mp > 0:
            beam_2 = Beam(bird_2)
            beams.add(beam_2)
            bird_2.status.decrease_mp()

        if not keys[pg.K_RSHIFT] and bird.status.mp < 100:
            bird.status.mp += 0.2

        if not keys[pg.K_LSHIFT] and bird_2.status.mp < 100:
            bird_2.status.mp += 0.2

    # ビームを更新して描画
        if the_world.is_time_stopped("bird"):
            beam = Beam(bird, "bird")
            beams.add(beam)
            beam.update(bird, bird_2, the_world.is_time_stopped("bird"))
        elif the_world.is_time_stopped("bird_2"):
            beam_2 = Beam(bird_2, "bird_2")
            beams.add(beam_2)
            beam_2.update(bird, bird_2, the_world.is_time_stopped("bird_2"))
        else:
            beams.update(bird, bird_2, None)
            beams.draw(screen)
        #################
        # 追尾弾発射（新しいキー設定）
        if keys[pg.K_o]:  # Bird（右側の鳥）から追尾弾を発射（Eキー）
            homing_beam = HomingBeam(bird, bird_2)  # Bird_2をターゲットにする
            beams.add(homing_beam)
            bird.status.decrease_mp(5)  # MPを5消費

        if keys[pg.K_q]:  # Bird_2（左側の鳥）から追尾弾を発射（Qキー）
            homing_beam_2 = HomingBeam(bird_2, bird)  # Birdをターゲットにする
            beams.add(homing_beam_2)
            bird_2.status.decrease_mp(5)
            #################

        if bird.status.hp <= 0:
            finish = Finish("Bird_2", bird_2_img)
        elif bird_2.status.hp <= 0:
            finish = Finish("Bird", bird_img)
        
        pg.mixer.init()

    # シールド展開時の音を読み込む
    shield_sound = pg.mixer.Sound("ex5/fig/at.wav")  # 音声ファイルのパスを指定

    # シールド発生（右Ctrlはbird、左Ctrlはbird_2）
    if keys[pg.K_RCTRL] and not shield_active_bird:  # bird用シールド
        shield = Shield(bird)
        shields.add(shield)
        bird.status.decrease_mp(30)  # MPを30消費
        shield_sound.play()
        shield_active_bird = True  # birdのシールドは1回だけ発動

    if keys[pg.K_LCTRL] and not shield_active_bird_2:  # bird_2用シールド
        shield_2 = Shield2(bird_2)
        shields2.add(shield_2)
        bird_2.status.decrease_mp(30)  # MPを30消費
        shield_sound.play()
        shield_active_bird_2 = True  # bird_2のシールドは1回だけ発動
    
    # シールドが消えたら再発動できるようにする
    if not shields:  # birdのシールドが無くなった場合
        shield_active_bird = False

    if not shields2:  # bird_2のシールドが無くなった場合
        shield_active_bird_2 = False

    # シールドの更新
    shields.update(bird)
    shields.draw(screen)
    shields2.update(bird_2)
    shields2.draw(screen)

    if finish is None:
        bird.draw(screen)
        bird_2.draw(screen)
        beams.draw(screen)
        bird.status.draw(screen, 650, 570)
        bird_2.status.draw(screen, 50, 570)
    else:
        finish.draw(screen)


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

