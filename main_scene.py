# main_scene.py
from pico2d import *
import time
from gfw import *
from boy import Boy
from timer import Timer
from level_bar import LevelBar
from bullet import Bullet
from enemy import Enemy
from bullet_manager import BulletManager  # BulletManager 임포트

world = World(['bg', 'player', 'bullet', 'ui'])

canvas_width = 1280
canvas_height = 780
shows_bounding_box = True
shows_object_count = True

# 전역 변수
enemies = []  # 적 리스트

def enter():
    global bg, boy, font, level_bar, enemies

    # 배경 추가
    bg = InfiniteScrollBackground('res/InGameBack_1280_960.png', margin=100)
    world.append(bg, world.layer.bg)
    world.bg = bg

    # 플레이어 추가
    boy = Boy()
    boy.bg = bg
    world.append(boy, world.layer.player)

    # 적 추가 (예: 5명의 적)
    enemies.extend(Enemy(boy) for _ in range(5))
    for enemy in enemies:
        world.append(enemy, world.layer.player)

    # BulletManager 추가 및 World에 등록
    bullet_manager = BulletManager(boy, world, enemies)
    world.set_bullet_manager(bullet_manager)  # BulletManager 등록

    # 폰트 로드
    try:
        font = load_font('res/ENCR10B.TTF', 30)
    except:
        font = None
    if font is None:
        print("Error: Font could not be loaded. Please check the file path.")

    # 타이머 및 레벨 바 추가
    start_time = time.time()
    timer = Timer(start_time, font)
    world.append(timer, world.layer.ui)

    level_bar = LevelBar('res/progress_bg02.png', 'res/progress_fg02.png', max_time=60, position=(canvas_width // 2, canvas_height - 50))
    world.append(level_bar, world.layer.ui)

def update():
    world.update()  # world.update()만 호출

def draw():
    clear_canvas()
    world.draw()
    update_canvas()

def exit():
    global font
    world.clear()
    if font is not None:
        del font

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

def handle_event(e):
    boy.handle_event(e)

if __name__ == '__main__':
    gfw.start_main_module()
