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
        self.min_shoot_distance = 0.1  # 최소 거리 조건 (픽셀 단위)
        self.current_bullet_image = 'res/bullet.png'  # 기본 총알 이미지

    def set_bullet_image(self, new_image):
        """총알 이미지를 변경하는 메서드"""
        self.current_bullet_image = new_image
        
        

    def update(self):
        # 1초 간격으로 총알 발사
        if time.time() - self.last_shot_time >= self.shot_interval:
            self.shoot_bullet()
            self.last_shot_time = time.time()

        # 모든 총알 업데이트 및 수명 만료된 총알 제거
        for bullet in self.bullets[:]:
            bullet.update()

            

            # 충돌 감지
            for enemy in self.enemies:
                if self.check_collision(bullet, enemy):
                    enemy.hit_by_bullet(effect=bullet.effect)  # 적이 맞았을 때 효과 추가
                    if bullet.effect != "pierce":  # 관통 효과가 아니면 총알 제거
                        self.bullets.remove(bullet)
                        self.world.remove(bullet, self.world.layer.bullet)
                    break  # 이미 충돌했으므로 다른 적과 충돌 확인 생략

    def check_collision(self, bullet, enemy):
        # 정확한 바운드 박스를 가져옵니다.
        bullet_bb = bullet.get_bb()
        enemy_bb = enemy.get_bb()

        # 충돌 판정 로직 (Bounding Box 방식)
        return not (
            bullet_bb[2] < enemy_bb[0] or  # 총알 오른쪽이 적의 왼쪽보다 왼쪽에 있음
            bullet_bb[0] > enemy_bb[2] or  # 총알 왼쪽이 적의 오른쪽보다 오른쪽에 있음
            bullet_bb[3] < enemy_bb[1] or  # 총알 위쪽이 적의 아래쪽보다 아래에 있음
            bullet_bb[1] > enemy_bb[3]     # 총알 아래쪽이 적의 위쪽보다 위에 있음
        )

    def shoot_bullet(self):
        # 가장 가까운 적을 찾기
        nearest_enemy = self.get_nearest_enemy()
        if nearest_enemy is None:
            return  # 적이 없으면 발사하지 않음

        # 플레이어와 적 사이 거리 계산
        dx, dy = nearest_enemy.x - self.player.x, nearest_enemy.y - self.player.y
        distance = math.sqrt(dx**2 + dy**2)

        # 너무 가까운 적은 무시
        if distance < self.min_shoot_distance:
            return

        # 방향 계산
        direction = (dx / distance, dy / distance) if distance != 0 else (1, 0)

        # 총알 생성 및 월드에 추가
        bullet = Bullet(self.current_bullet_image, (self.player.x, self.player.y), direction, self.world, effect=self.player.bullet_effect)
        self.bullets.append(bullet)
        self.world.append(bullet, self.world.layer.bullet)

        
    def get_nearest_enemy(self):
        min_distance = float('inf')
        nearest_enemy = None
        for enemy in self.enemies:
            # 적이 삭제된 상태가 아니어야만 거리 계산
            if enemy.is_hit:
                continue

            dx, dy = enemy.x - self.player.x, enemy.y - self.player.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance < min_distance:
                min_distance = distance
                nearest_enemy = enemy
        return nearest_enemy
