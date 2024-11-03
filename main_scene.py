from pico2d import * 
from gfw import *
from boy import Boy
from timer import Timer
from level_bar import LevelBar  # LevelBar 클래스 임포트
from bullet import Bullet  # bullet.py에서 Bullet 클래스를 임포트
import time

world = World(['bg', 'player', 'ui'])

canvas_width = 1280
canvas_height = 780
shows_bounding_box = True
shows_object_count = True

def enter():
    global bg, boy, font, level_bar

    bg = InfiniteScrollBackground('res/InGameBack_1280_960.png', margin=100)
    world.append(bg, world.layer.bg)
    world.bg = bg

    boy = Boy()
    boy.bg = bg
    world.append(boy, world.layer.player)

    # 폰트 로드
    try:
        font = load_font('res/ENCR10B.TTF', 30)
    except:
        font = None
    if font is None:
        print("Error: Font could not be loaded. Please check the file path.")

    # 타이머 객체 생성 및 월드에 추가
    start_time = time.time()  # 타이머 시작 시간 설정
    timer = Timer(start_time, font)
    world.append(timer, world.layer.ui)  # 타이머는 UI 레이어에 추가

    # 레벨 바 객체 생성 및 월드에 추가
    level_bar = LevelBar('res/progress_bg02.png', 'res/progress_fg02.png', max_time=60, position=(canvas_width // 2, canvas_height - 50))
    world.append(level_bar, world.layer.ui)  # 레벨 바는 UI 레이어에 추가

def update():
    world.update()

def draw():
    clear_canvas()  # 캔버스를 지웁니다.
    world.draw()    # 월드 내의 모든 객체를 그립니다.
    update_canvas()  # 캔버스를 업데이트합니다.

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
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)
        return

    if e.key == SDLK_SPACE:  # 스페이스 키로 총을 발사
        gun_shoot()  # 총알 발사 함수 호출
        return    

    boy.handle_event(e)

# 총을 쏘는 함수 예시
def gun_shoot():
    directions = [
        (1, 0), (1, 1), (0, 1), (-1, 1),
        (-1, 0), (-1, -1), (0, -1), (1, -1)
    ]
    for dx, dy in directions:
        direction = (dx, dy)
        bullet = Bullet('res/bullet.png', (boy.x, boy.y), direction, world)  # 여기서 'world' 인자를 추가하여 전달
        world.append(bullet, world.layer.player)  # 명시적으로 player 레이어에 추가

if __name__ == '__main__':
    gfw.start_main_module()
