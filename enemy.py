import random
import math
from pico2d import *
import gfw
from behavior_tree import BehaviorTree, Selector, LeafNode, BT_SUCCESS, BT_FAIL





class Enemy(gfw.Sprite):
    def __init__(self, player):
        image_path = r"C:\Users\msi\Desktop\PokemonSub\res\Enemy.png"
        super().__init__(image_path, random.randint(0, get_canvas_width()), random.randint(0, get_canvas_height()))
        self.speed = 80  # 이동 속도
        self.player = player  # 추적할 플레이어 객체
        self.frame = 0
        self.action = 0  # 0은 왼쪽 이동, 1은 오른쪽 이동
        self.frame_count = 8  # 각 행에 포함된 프레임 수
        self.frame_width = self.image.w // self.frame_count
        self.frame_height = self.image.h // 2  # 이미지가 두 줄로 구성됨
        self.animation_speed = 0.2  # 애니메이션 속도 조절 (값이 작을수록 빨라짐)
        self.time_accumulator = 0  # 시간 누적 변수
        self.scale = 2.0  # 적 크기 확대 비율
        self.build_behavior_tree()

    def build_behavior_tree(self):
        self.bt = BehaviorTree(
            Selector('FollowPlayer', [
                LeafNode('Chase', self.chase_player)
            ])
        )

    def chase_player(self):
        # 플레이어와의 거리 계산
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0:
            return BT_FAIL

        # 플레이어 방향으로 이동
        self.x += (dx / distance) * self.speed * gfw.frame_time
        self.y += (dy / distance) * self.speed * gfw.frame_time

        # 이동 방향에 따른 액션 설정
        self.action = 1 if dx > 0 else 0  # 오른쪽 이동은 1, 왼쪽 이동은 0
        return BT_SUCCESS

    def update(self):
        self.bt.run()
        # 애니메이션 속도 조절
        self.time_accumulator += gfw.frame_time
        if self.time_accumulator >= self.animation_speed:
            self.frame = (self.frame + 1) % self.frame_count  # 프레임 업데이트
            self.time_accumulator = 0  # 누적 시간 초기화

    def draw(self):
        # 현재 프레임과 액션에 따른 이미지 좌표 계산
        x = self.frame * self.frame_width
        y = self.action * self.frame_height
        # 적을 크게 그리기 위해 scale을 적용하여 clip_draw 사용
        self.image.clip_draw(x, y, self.frame_width, self.frame_height, self.x, self.y, self.frame_width * self.scale, self.frame_height * self.scale)

    def get_bb(self):
        hw, hh = (self.frame_width // 2) * self.scale, (self.frame_height // 2) * self.scale
        return self.x - hw, self.y - hh, self.x + hw, self.y + hh
