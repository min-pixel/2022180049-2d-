# bullet.py
import time
from pico2d import *
import gfw

class Bullet(gfw.Sprite):
    def __init__(self, image_path, pos, direction, world, speed=400, lifetime=3.0, effect=None):
        super().__init__(image_path, *pos)
        self.direction = direction
        self.speed = speed
        self.spawn_time = time.time()  # 총알 생성 시간
        self.lifetime = lifetime      # 수명 (초 단위)
        self.world = world
        self.effect = effect  # 추가: 효과 정보 저장

    def apply_effect(self, target):
        if self.effect == "slow":
            target.speed *= 0.5  # 적의 속도를 절반으로 감소
            target.is_slowed = True  # 슬로우 상태를 표시
            target.slow_start_time = time.time()

    
            
    def update(self):
        frame_time = gfw.frame_time
        self.x += self.direction[0] * self.speed * frame_time
        self.y += self.direction[1] * self.speed * frame_time

    def lifetime_expired(self):
        # 총알이 생성된 후 수명이 다했는지 확인
        return (time.time() - self.spawn_time) >= self.lifetime

    def draw(self):
        # 배경을 기준으로 위치 계산
        screen_pos = self.world.bg.to_screen(self.x, self.y) if self.world.bg else (self.x, self.y)
        if hasattr(self, 'image') and self.image:
            self.image.draw(*screen_pos)

            
