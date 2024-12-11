from pico2d import *
import gfw
import main_scene

import sys
self = sys.modules[__name__]

canvas_width = 1280
canvas_height = 780

center_x = canvas_width // 2
center_y = canvas_height // 2

world = gfw.World(1)  # 한 개의 레이어 사용

def enter():
    # "Game Over" 이미지 로드 및 월드에 추가
    self.gameover_image = gfw.Sprite('res/gameover.png', center_x, center_y)
    world.append(self.gameover_image, 0)  # 첫 번째 레이어에 이미지 추가

def update():
    pass  # 별도의 업데이트 로직 없음

def draw():
    # 월드에 있는 "Game Over" 이미지를 그리기
    world.draw()

def handle_event(e):
    # 키 이벤트를 처리하여 게임을 재시작하거나 종료
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_RETURN:  # 엔터 키로 메인 씬 재시작
            
            gfw.change(main_scene)
        elif e.key == SDLK_q:
            gfw.quit()
        else:  # 다른 키 입력 시 게임 종료
            pass

def exit():
    # "Game Over" 이미지 언로드 및 리소스 정리
    gfw.image.unload('res/gameover.png')
    world.clear()

if __name__ == '__main__':
    gfw.start_main_module()
