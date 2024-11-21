import sys
import os
import math
import random

# gobj.py 파일이 있는 디렉토리를 sys.path에 추가합니다.
gobj_dir = r"C:\Users\msi\Desktop\PokemonSub\gfw"
sys.path.append(gobj_dir)

from pico2d import *
import gfw

class Boy(gfw.Sprite):
    def __init__(self):
        super().__init__('res/PokemonPlayer.png', get_canvas_width() // 2, get_canvas_height() // 2)
        self.time = 0  # 총 지나간 시간
        self.frame = 0
        self.dx, self.dy = 0, 0
        self.speed = 200
        self.action = 1  # 1=오른쪽으로 이동, 0=왼쪽으로 이동
        self.mag = 1
        self.target = None
        self.level_bar = None  # LevelBar 객체 참조
        self.frame_count = 8  # 각 방향마다 8개의 프레임
        self.frame_width = self.image.w // self.frame_count
        self.frame_height = self.image.h // 2  # 이미지가 2개의 행으로 구성됨

    def draw(self):
        # 현재 프레임과 액션에 따른 이미지 좌표 계산
        x = self.frame * self.frame_width
        y = self.action * self.frame_height
        screen_pos = self.bg.to_screen(self.x, self.y) if self.bg else (self.x, self.y)
        # 클립 드로우를 사용해 이미지에서 특정 부분만 그립니다.
        self.image.clip_draw(x, y, self.frame_width, self.frame_height, *screen_pos)

    def update(self):
        # 프레임 업데이트 로직
        self.time += gfw.frame_time
        fps = 10  # 초당 10 프레임
        self.frame = round(self.time * fps) % self.frame_count  # 프레임을 설정

        # 위치 업데이트
        self.x += self.dx * self.speed * self.mag * gfw.frame_time
        self.y += self.dy * self.speed * self.mag * gfw.frame_time

        # 타겟이 있는 경우 타겟까지 이동
        if self.target is not None:
            tx, ty = self.target
            if (self.dx > 0 and self.x >= tx) or (self.dx < 0 and self.x <= tx):
                self.x, self.dx = tx, 0
            if (self.dy > 0 and self.y >= ty) or (self.dy < 0 and self.y <= ty):
                self.y, self.dy = ty, 0
            if self.dx == 0 and self.dy == 0:
                self.target = None
                self.adjust_action()

        if self.bg:
            self.bg.show(self.x, self.y)

    def adjust_delta(self, x, y):
        if self.target is not None:
            self.dx, self.dy = 0, 0
            self.target = None
        self.dx += x
        self.dy += y

    def set_target(self, mx, my):
        tx, ty = self.bg.from_screen(mx, my) if self.bg else (mx, my)
        if self.x == tx and self.y == ty:
            self.target = None
            self.dx, self.dy = 0, 0
            return
        self.target = tx, ty
        rad = math.atan2(ty - self.y, tx - self.x)
        self.dx, self.dy = math.cos(rad), math.sin(rad)

    def handle_event(self, e):
        dx, dy = self.dx, self.dy
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_LEFT:
                self.adjust_delta(-1, 0)
                self.action = 0  # 왼쪽으로 이동
            elif e.key == SDLK_RIGHT:
                self.adjust_delta(1, 0)
                self.action = 1  # 오른쪽으로 이동
            elif e.key == SDLK_DOWN:
                self.adjust_delta(0, -1)
            elif e.key == SDLK_UP:
                self.adjust_delta(0, 1)
            elif e.key == SDLK_LSHIFT:
                self.mag *= 2

        elif e.type == SDL_KEYUP:
            if e.key == SDLK_LEFT:
                self.adjust_delta(1, 0)
            elif e.key == SDLK_RIGHT:
                self.adjust_delta(-1, 0)
            elif e.key == SDLK_DOWN:
                self.adjust_delta(0, 1)
            elif e.key == SDLK_UP:
                self.adjust_delta(0, -1)
            elif e.key == SDLK_LSHIFT:
                self.mag //= 2

        elif e.type == SDL_MOUSEBUTTONDOWN:
            self.set_target(e.x, get_canvas_height() - e.y - 1)
        elif e.type == SDL_MOUSEMOTION:
            if self.target is not None:
                self.set_target(e.x, get_canvas_height() - e.y - 1)

    def get_bb(self):
        hw, hh = 20, 34
        return self.x - hw, self.y - hh, self.x + hw, self.y + hh

    def check_collision_with_exp(self, exp_items, level_bar):
        for item in exp_items[:]:
            if gfw.world.collides_box(self, item):
                     # 경험치 추가
                leveled_up = level_bar.add_exp(item.amount)
                
                # 경험치 아이템 제거
                exp_items.remove(item)
                self.world.remove(item, self.world.layer.bullet)

                if leveled_up:
                    self.level_up()

    def level_up(self):
        print("Level Up!")
        gfw.pause()  # 일시 정지 처리

    def get_bb(self):
        hw, hh = 20, 34  # 경계 박스 크기 조정 필요
        return self.x - hw, self.y - hh, self.x + hw, self.y + hh
        
    def __repr__(self):
        return 'Boy'
