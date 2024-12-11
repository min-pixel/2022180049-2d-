import random
import math
import time
from pico2d import *
import gfw
from behavior_tree import BehaviorTree, Selector, LeafNode, BT_SUCCESS, BT_FAIL
from exp_item import ExpItem

class Enemy(gfw.Sprite):
    def __init__(self, player, world, image_path="res/Enemy.png", speed=230, health=1):
        super().__init__(image_path, random.randint(0, get_canvas_width()), random.randint(0, get_canvas_height()))
        self.speed = speed  # 이동 속도
        self.original_speed = speed  # 원래 속도 저장
        self.health = health  # 체력
        self.player = player  # 추적할 플레이어 객체
        self.world = world  # World 객체 참조 저장
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
        self.is_slowed = False  # 슬로우 상태 여부
        self.slow_start_time = None  # 슬로우 시작 시간
        self.slow_duration = 3.0  # 슬로우 효과 지속 시간
        self.build_behavior_tree()
        self.is_paused = False  # 정지 상태
        self.pause_end_time = 0  # 정지 종료 시간

    def build_behavior_tree(self):
        self.bt = BehaviorTree(
            Selector('FollowPlayer', [
                LeafNode('Chase', self.chase_player)
            ])
        )

    def pause(self, duration):
        """적을 일정 시간 동안 정지 상태로 만듭니다."""
        self.is_paused = True
        self.pause_end_time = time.time() + duration

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

        # 정지 상태라면 정지 시간이 끝날 때까지 업데이트 중단
        if self.is_paused:
            if time.time() >= self.pause_end_time:
                self.is_paused = False  # 정지 해제
            else:
                return

                # 슬로우 상태 업데이트
        if self.is_slowed:
            if time.time() - self.slow_start_time >= self.slow_duration:
                self.speed = self.original_speed  # 속도 복구
                self.is_slowed = False
        
        
        if self.is_hit:
            if time.time() - self.hit_start_time >= self.flash_duration:
                if self.health <= 0:
                    self.remove()
                else:
                    self.is_hit = False
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

        # 배경 좌표를 기준으로 화면 좌표 계산
        if self.world and self.world.bg:
            screen_x, screen_y = self.world.bg.to_screen(self.x, self.y)
        else:
            screen_x, screen_y = self.x, self.y

        if self.is_hit:
            if int((time.time() - self.hit_start_time) * 10) % 2 == 0:
                self.image.clip_draw(x, y, self.frame_width, self.frame_height, screen_x, screen_y, self.frame_width * self.scale, self.frame_height * self.scale)
        else:
            self.image.clip_draw(x, y, self.frame_width, self.frame_height, screen_x, screen_y, self.frame_width * self.scale, self.frame_height * self.scale)
        
    def get_bb(self):
        hw, hh = (self.frame_width // 2) * self.scale, (self.frame_height // 2) * self.scale
        return self.x - hw, self.y - hh, self.x + hw, self.y + hh

    def hit_by_bullet(self, effect=None):
        self.is_hit = True
        self.health -= 1  # 체력 감소
        self.hit_start_time = time.time()

                # 슬로우 효과 적용
        if effect == "slow" and not self.is_slowed:
            self.is_slowed = True
            self.speed *= 0  # 속도를 절반으로 감소
            self.slow_start_time = time.time()
            

        if self.health <= 0:
            exp_item = ExpItem((self.x, self.y), amount=10)
            exp_item.set_world(self.world)  # World 객체 설정
            self.world.append(exp_item, self.world.layer.bullet)

    def remove(self):
        self.world.remove(self, self.world.layer.player)


class Enemy02(Enemy):
    def __init__(self, player, world):
        super().__init__(player, world, "res/Enemy02.png", speed=100, health=2)


class Enemy03(Enemy):
    def __init__(self, player, world):
        super().__init__(player, world, "res/Enemy03.png", speed=90, health=3)


class Enemy04(Enemy):
    def __init__(self, player, world):
        super().__init__(player, world, "res/Enemy04.png", speed=80, health=4)
