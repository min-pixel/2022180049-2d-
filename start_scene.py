import gfw
from pico2d import *
import loading_scene

import sys
self = sys.modules[__name__]

canvas_width = loading_scene.canvas_width  # 타이틀 씬의 기본 캔버스 크기 설정
canvas_height = loading_scene.canvas_height

center_x = canvas_width // 2
center_y = canvas_height // 2

world = gfw.World(2)  # 두 개의 레이어 사용: 0 - 타이틀 이미지, 1 - 버튼 텍스트 이미지

def enter():
    # 타이틀 이미지 로드 및 월드에 추가
    self.title_image = gfw.Sprite('res/title.png', center_x, center_y)
    world.append(self.title_image, 0)  # 첫 번째 레이어에 이미지 추가

    # "Press the Button" 이미지 로드 및 월드에 추가
    self.start_button_image = gfw.Sprite('res/startButtontxt.png', center_x, center_y - 100)
    world.append(self.start_button_image, 1)  # 두 번째 레이어에 버튼 텍스트 이미지 추가

def update():
    # 업데이트 로직이 필요 없으므로 비워둡니다.
    pass

def draw():
    # 월드에 있는 타이틀 이미지와 버튼 텍스트 이미지를 그립니다.
    world.draw()

def handle_event(e):
    # 키 이벤트를 처리하여 로딩 씬으로 전환합니다.
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        # 아무 키나 누르면 로딩 씬으로 전환
        gfw.change(loading_scene)

def exit():
    # 타이틀 이미지와 버튼 텍스트 이미지 언로드 및 리소스 정리
    gfw.image.unload('res/title.png')
    gfw.image.unload('res/startButtontxt.png')
    world.clear()

if __name__ == '__main__':
    gfw.start_main_module()
