import time  # 시간 기록을 위해 time 모듈을 임포트
from pico2d import *
import gfw

class Bullet(gfw.Sprite):
    def __init__(self, image_path, pos, direction, world, speed=600, lifetime=1000, layer_index=1):
        super().__init__(image_path, *pos)
        self.direction = direction
        self.speed = speed
        self.spawn_time = time.time()  # 시간을 초로 기록
        self.lifetime = lifetime
        self.world = world  # world 객체를 전달받아 저장
        self.layer_index = layer_index  # 레이어 인덱스 추가

    def update(self):
        # 프레임 시간 계산
        frame_time = gfw.frame_time
        self.x += self.direction[0] * self.speed * frame_time
        self.y += self.direction[1] * self.speed * frame_time

        # 수명이 다 되면 삭제
        if (time.time() - self.spawn_time) * 1000 >= self.lifetime:
            # 객체가 해당 레이어에 있는지 확인 후 삭제
            if self in self.world.objects[self.layer_index]:
                self.world.remove(self, self.layer_index)

    def draw(self):
        if hasattr(self, 'image') and self.image:
            self.image.draw(self.x, self.y)
