import random
import math
import time
from pico2d import *
import gfw
from behavior_tree import BehaviorTree, Selector, LeafNode, BT_SUCCESS, BT_FAIL

class Enemy(gfw.Sprite):
    def __init__(self, player, world):
        image_path = r"C:\Users\msi\Desktop\PokemonSub\res\Enemy.png"
        super().__init__(image_path, random.randint(0, get_canvas_width()), random.randint(0, get_canvas_height()))
        self.speed = 80  # 이동 속도
        self.player = player  # 추적할 플레이어 객체
        self.world = world    # World 객체 참조 저장
        self.frame = 0
        self.action = 0  # 0은 왼쪽 이동, 1은 오른쪽 이동
        self.frame_count = 8  # 각 행에 포함된 프레임 수
        self.frame_width = self.image.w // self.frame_count
        self.frame_height = self.image.h // 2  # 이미지가 두 줄로 구성됨
        self.animation_speed = 0.2  # 애니메이션 속도 조절 (값이 작을수록 빨라짐)
        self.time_accumulator = 0  # 시간 누적 변수
        self.scale = 2.0  # 적 크기 확대 비율
        self.is_hit = False  # 맞았는지 여부
        self.hit_start_time = None  # 맞은 시간 기록
        self.flash_duration = 0.5  # 깜빡임 지속 시간
        self.build_behavior_tree()

    def build_behavior_tree(self):
        self.bt = BehaviorTree(
            Selector('FollowPlayer', [
                LeafNode('Chase', self.chase_player)
            ])
        )

    def chase_player(self):
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0:
            return BT_FAIL

        self.x += (dx / distance) * self.speed * gfw.frame_time
        self.y += (dy / distance) * self.speed * gfw.frame_time

        self.action = 1 if dx > 0 else 0
        return BT_SUCCESS

    def update(self):
        if self.is_hit:
            if time.time() - self.hit_start_time >= self.flash_duration:
                self.remove()
                return
        else:
            self.bt.run()

        self.time_accumulator += gfw.frame_time
        if self.time_accumulator >= self.animation_speed:
            self.frame = (self.frame + 1) % self.frame_count
            self.time_accumulator = 0

    def draw(self):
        x = self.frame * self.frame_width
        y = self.action * self.frame_height
        if self.is_hit:
            if int((time.time() - self.hit_start_time) * 10) % 2 == 0:
                self.image.clip_draw(x, y, self.frame_width, self.frame_height, self.x, self.y, self.frame_width * self.scale, self.frame_height * self.scale)
        else:
            self.image.clip_draw(x, y, self.frame_width, self.frame_height, self.x, self.y, self.frame_width * self.scale, self.frame_height * self.scale)

    def get_bb(self):
        hw, hh = (self.frame_width // 2) * self.scale, (self.frame_height // 2) * self.scale
        return self.x - hw, self.y - hh, self.x + hw, self.y + hh

    def hit_by_bullet(self):
        self.is_hit = True
        self.hit_start_time = time.time()

    def remove(self):
        self.world.remove(self, self.world.layer.player)
