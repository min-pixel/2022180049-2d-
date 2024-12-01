from pico2d import *
import gfw


class SkillTreeUI:
    def __init__(self, player, bullet_manager):
        self.is_active = False
        self.player = player  # 플레이어 참조 저장
        self.bullet_manager = bullet_manager  # BulletManager 참조
        self.options = [
            "res/slow.png",
            "res/pierce.png",
            "res/shield.png"
        ]
        icon_spacing = 100  # 아이콘 간 간격
        icon_start_y = get_canvas_height() // 2 + (len(self.options) - 1) * icon_spacing // 2

        self.sprites = [gfw.Sprite(option, get_canvas_width() // 2, icon_start_y - (i * icon_spacing)) 
                        for i, option in enumerate(self.options)]
        self.background_image = gfw.Sprite("res/skillback.png", get_canvas_width() // 2, get_canvas_height() // 2)

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def update(self):
        if not self.is_active:
            return

    def draw(self):
        if not self.is_active:
            return

        # 배경 이미지 그리기
        self.background_image.draw()

        # 옵션 이미지 그리기
        for sprite in self.sprites:
            sprite.draw()

    def handle_event(self, e):
        if not self.is_active:
            return False

        if e.type == SDL_MOUSEBUTTONDOWN:
            x, y = e.x, get_canvas_height() - e.y
            for i, sprite in enumerate(self.sprites):
                button_x, button_y = sprite.x - sprite.width // 2, sprite.y - sprite.height // 2
                button_width, button_height = sprite.width, sprite.height
                if (button_x <= x <= button_x + button_width and
                        button_y <= y <= button_y + button_height):
                    print(f"Selected: Option {i+1}")
                    if i == 0:  # slow 선택 시
                        self.bullet_manager.set_bullet_image("res/bullet02.png")  # BulletManager 호출
                        self.player.bullet_effect = "slow"
                    elif i == 1:  # pierce 선택
                        self.bullet_manager.set_bullet_image("res/bullet03.png")  # BulletManager 호출
                        self.player.bullet_effect = "pierce"
                    elif i == 2:  # shield 선택
                        self.player.shield_enabled = True
                        self.player.activate_shield()  # 쉴드 활성화
                        
                        
                        
                    self.deactivate()
                    gfw.resume()  # 일시정지 해제
                    self.player.reset_state()  # 플레이어 상태 초기화
                    return True
        return False
