import gfw
from pico2d import *
import time

class ExpItem(gfw.Sprite):
    def __init__(self, pos, amount=10):
        super().__init__('res/exp_item.png', *pos)
        self.amount = amount
        self.world = None

    def set_world(self, world):
        self.world = world

    def update(self):
        # 충돌 감지 로직
        if self.world:
            player = self.world.get_player()  # World에서 플레이어 가져오기
            if player and gfw.world.collides_box(player, self):
                self.handle_collision(player)

    def handle_collision(self, player):
        # 경험치 추가 및 제거 처리
        if hasattr(player, 'level_bar'):
            leveled_up = player.level_bar.add_exp(self.amount)
            if leveled_up:
                player.level_up()

        # 월드에서 아이템 제거
        if self.world:
            self.world.remove(self, self.world.layer.bullet)
