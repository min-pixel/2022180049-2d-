import sys
import os
import math
import random
import time  # time 모듈 임포트
from enemy import Enemy  # Enemy 클래스 임포트
import gfw



# gobj.py 파일이 있는 디렉토리를 sys.path에 추가합니다.
gobj_dir = r"C:\Users\msi\Desktop\PokemonSub\gfw"
sys.path.append(gobj_dir)

from pico2d import *
import gfw

class Boy(gfw.Sprite):
    def __init__(self, world, skill_tree_ui=None):
        super().__init__('res/PokemonPlayer.png', get_canvas_width() // 2, get_canvas_height() // 2)
        self.skill_tree_ui = skill_tree_ui  # SkillTreeUI 참조 저장
        self.world = world  # World 객체 참조
        self.bullet_effect = None  # 기본 효과 없음
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

        # 쉴드 관련 속성
        self.shield_enabled = False  # 스킬 트리에서 쉴드 활성화 여부
        self.is_shielded = False  # 무적 상태 여부
        self.shield_duration = 4.0  # 쉴드 지속 시간 (초)
        self.shield_start_time = 0  # 쉴드 시작 시간
        self.shield_cooldown = 5.0  # 쉴드 재사용 대기시간 (초)
        self.last_shield_time = 0  # 마지막 쉴드 활성화 시간

    def activate_shield(self):

        if not self.shield_enabled:
            return


        
        current_time = time.time()
        if current_time - self.last_shield_time < self.shield_cooldown:
            remaining_time = self.shield_cooldown - (current_time - self.last_shield_time)
        
            return
        
        
        self.is_shielded = True
        self.shield_start_time = current_time
        
        
        # 쉴드 이미지로 변경
        self.image = gfw.image.load('res/PokemonPlayershieldmod.png')  # 쉴드 활성화 이미지
        

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

        # 배경 위치와 동기화
        if self.bg:
            self.bg.show(self.x, self.y)

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

        
            # 쉴드 활성화 상태일 때 적과 충돌 무시
        if self.is_shielded:
            elapsed_time = time.time() - self.shield_start_time
    
            if elapsed_time >= self.shield_duration:
                self.is_shielded = False
                self.last_shield_time = time.time()
                self.image = gfw.image.load('res/PokemonPlayer.png')  # 원래 이미지로 복구
                

        # 쿨타임 확인 후 쉴드 재활성화 (스킬 트리에서 선택된 경우만)
        if self.shield_enabled and not self.is_shielded:
            current_time = time.time()
            cooldown_elapsed = current_time - self.last_shield_time
            if cooldown_elapsed >= self.shield_cooldown:
                self.activate_shield()
              
        # 적과의 충돌 확인
        if self.world and not self.is_shielded:
            for enemy in self.world.objects_at(self.world.layer.player):
                if isinstance(enemy, Enemy) and self.check_collision(enemy):
                    if self.collision_callback:  # 충돌 콜백이 정의되어 있으면 호출
                        self.collision_callback()
                    return

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


    def check_collision(self, enemy):
        """적과의 충돌을 확인"""
        player_bb = self.get_bb()
        enemy_bb = enemy.get_bb()
        return not (
            player_bb[2] < enemy_bb[0] or
            player_bb[0] > enemy_bb[2] or
            player_bb[3] < enemy_bb[1] or
            player_bb[1] > enemy_bb[3]
        )

    def level_up(self):
        print("Level Up!")
        if self.level_bar:
            self.level_bar.reset_for_level_up()  # 레벨 바 초기화 및 최대량 증가
        gfw.pause()  # 일시 정지 처리
        if self.skill_tree_ui:
            self.skill_tree_ui.activate()  # 스킬 트리 UI 활성화

    def reset_state(self):
        self.dx = 0
        self.dy = 0
        self.target = None
            
    def __repr__(self):
        return 'Boy'
