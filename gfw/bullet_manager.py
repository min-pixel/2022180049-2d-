# bullet_manager.py
import time
import math
from bullet import Bullet

class BulletManager:
    def __init__(self, player, world, enemies):
        self.player = player  # 플레이어 객체
        self.world = world    # 월드 객체
        self.enemies = enemies  # 적 객체 리스트
        self.bullets = []       # 발사된 총알 리스트
        self.last_shot_time = 0  # 마지막 발사 시간 초기화
        self.shot_interval = 1.0  # 1초 간격으로 발사

    def update(self):
        # 1초 간격으로 총알 발사
        if time.time() - self.last_shot_time >= self.shot_interval:
            self.shoot_bullet()
            self.last_shot_time = time.time()

        # 모든 총알 업데이트 및 수명 만료된 총알 제거
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.lifetime_expired():
                self.bullets.remove(bullet)
                self.world.remove(bullet, self.world.layer.bullet)

    def shoot_bullet(self):
        # 가장 가까운 적을 찾기
        nearest_enemy = self.get_nearest_enemy()
        if nearest_enemy is None:
            return  # 적이 없으면 발사하지 않음

        # 플레이어 위치와 가장 가까운 적 위치를 기반으로 방향 계산
        dx, dy = nearest_enemy.x - self.player.x, nearest_enemy.y - self.player.y
        distance = math.sqrt(dx**2 + dy**2)
        direction = (dx / distance, dy / distance) if distance != 0 else (1, 0)

        # 총알 생성 및 월드에 추가
        bullet = Bullet('res/bullet.png', (self.player.x, self.player.y), direction, self.world)
        self.bullets.append(bullet)
        self.world.append(bullet, self.world.layer.bullet)

    def get_nearest_enemy(self):
        min_distance = float('inf')
        nearest_enemy = None
        for enemy in self.enemies:
            dx, dy = enemy.x - self.player.x, enemy.y - self.player.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance < min_distance:
                min_distance = distance
                nearest_enemy = enemy
        return nearest_enemy
