import random  # random 모듈을 import하여 문제 해결
import math
from pico2d import *
import gfw
from behavior_tree import BehaviorTree, Selector, LeafNode


class Enemy(gfw.Sprite):
    def __init__(self, player):
        image_path = r"C:\Users\msi\Desktop\PokemonSub\res\Enemy.png"
        x, y = random.randint(0, get_canvas_width()), random.randint(0, get_canvas_height())
        super().__init__(image_path, x, y)
        self.speed = 80  # 이동 속도
        self.player = player  # 추적할 플레이어 객체
        self.build_behavior_tree()

    def build_behavior_tree(self):
        # 간단한 추적 행동을 정의
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
            return BT_FAIL  # 거리가 0일 때 실패 반환

        # 플레이어 방향으로 이동
        self.x += (dx / distance) * self.speed * gfw.frame_time
        self.y += (dy / distance) * self.speed * gfw.frame_time
        return BT_SUCCESS

    def update(self):
        # 행동 트리를 실행하여 추적 동작 수행
        self.bt.run()

    def draw(self):
        # 적의 현재 위치를 화면에 그리기
        self.image.draw(self.x, self.y)

    def get_bb(self):
        # 충돌 체크를 위한 바운딩 박스
        hw, hh = self.image.w // 2, self.image.h // 2
        return self.x - hw, self.y - hh, self.x + hw, self.y + hh
