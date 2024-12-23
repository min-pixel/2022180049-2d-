import time
import random  # random 모듈 임포트
from enemy import Enemy, Enemy02, Enemy03, Enemy04  # 모든 필요한 클래스 임포트

class EnemySpawner:
    def __init__(self, player, world, bullet_manager):
        self.player = player
        self.world = world
        
        self.bullet_manager = bullet_manager  # BulletManager 참조
        self.spawn_interval = 1.0  # 적 소환 주기 (1초)
        self.last_spawn_time = time.time()
        self.additional_spawn_interval = 8.0  # 추가 적 수 증가 간격 (5초)
        self.last_additional_spawn_time = time.time()
        self.spawn_count = 1  # 현재 한 번에 소환되는 적 수

        # 가중치 설정
        self.enemy_classes = [Enemy, Enemy02, Enemy03, Enemy04]
        self.enemy_weights = [10, 50, 25, 15]  # Enemy가 가장 자주 등장하고, Enemy04는 드물게 등장

    def update(self):
        current_time = time.time()

        # 1초 간격으로 적 소환
        if current_time - self.last_spawn_time >= self.spawn_interval:
            self.spawn_enemy()
            self.last_spawn_time = current_time

        # 5초 간격으로 한 번에 소환되는 적 수 증가
        if current_time - self.last_additional_spawn_time >= self.additional_spawn_interval:
            self.spawn_count += 1
            self.last_additional_spawn_time = current_time

    def spawn_enemy(self):
        for _ in range(self.spawn_count):
            # 가중치를 고려한 적 타입 선택
            enemy_type = random.choices(self.enemy_classes, weights=self.enemy_weights, k=1)[0]
            enemy = enemy_type(self.player, self.world)
            self.world.append(enemy, self.world.layer.player)

            # BulletManager에 생성된 적 등록
            self.bullet_manager.enemies.append(enemy)
