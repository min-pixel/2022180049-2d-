# main_scene.py
from pico2d import *
import time
from gfw import *
from boy import Boy
from timer import Timer
from level_bar import LevelBar
from bullet import Bullet
from enemy import Enemy
from bullet_manager import BulletManager  # BulletManager 임포트
from enemy_spawner import EnemySpawner
from ui_controller import UIController
from skill_tree_ui import SkillTreeUI
import gameover_scene
import gamewin_scene  # Game Win 씬 추가

world = World(['bg', 'player', 'bullet', 'ui'])

canvas_width = 1280
canvas_height = 780
shows_bounding_box = True
shows_object_count = True

# 전역 변수
enemies = []  # 적 리스트

def enter():
    global bg, boy, font, level_bar, enemies, spawner, bullet_manager, exp_item_pool, skill_tree_ui, ui_controller

    # 월드 초기화
    world.clear()
    
    # 배경 추가
    bg = InfiniteScrollBackground('res/InGameBack_1280_960.png', margin=100)
    world.append(bg, world.layer.bg)
    world.bg = bg

    # UIController 생성 및 등록
    ui_controller = UIController()
    world.set_ui_controller(ui_controller)

       # 플레이어 추가
    boy = Boy(world)
    boy.bg = bg
    boy.collision_callback = on_player_collision  # 충돌 콜백 설정
    world.append(boy, world.layer.player)

        # BulletManager 추가
    bullet_manager = BulletManager(boy, world, enemies)
    world.set_bullet_manager(bullet_manager)

    # SkillTreeUI 생성 및 player와 연결
    skill_tree_ui = SkillTreeUI(player=boy,bullet_manager=bullet_manager)  # boy 객체 전달
    boy.skill_tree_ui = skill_tree_ui  # Boy에 스킬 트리 UI 연결
    ui_controller.add_ui_element(skill_tree_ui)
    

   

    # EnemySpawner 초기화 및 등록
    spawner = EnemySpawner(boy, world, bullet_manager)  # BulletManager 전달
    world.set_enemy_spawner(spawner)

    # 폰트 로드
    try:
        font = load_font('res/ENCR10B.TTF', 30)
    except:
        font = None
    if font is None:
        print("Error: Font could not be loaded. Please check the file path.")


    # 타이머 추가 (제한 시간 60초)
    timer = Timer(60, font, on_time_up)
    ui_controller.add_ui_element(timer)


    max_exp = 100
    # 레벨 진행 바 추가
    level_bar = LevelBar('res/progress_bg02.png', 'res/progress_fg02.png', max_exp=max_exp, position=(canvas_width // 2, canvas_height - 50))
    ui_controller.add_ui_element(level_bar)

    boy.level_bar = level_bar  # 레벨 바 연결


def on_player_collision():
    """플레이어가 적과 충돌했을 때 호출"""
    gfw.change(gameover_scene)  # Game Over 씬으로 전환

def on_time_up():
    """제한 시간이 종료되었을 때 호출"""
    
    gfw.change(gamewin_scene)  # Game Win 씬으로 전환


def update():
    world.update()  # world.update()만 호출

def draw():
    clear_canvas()
    world.draw()
    ui_controller.draw()  # UI 요소 그리기
    update_canvas()

def exit():
    global font
    world.clear()
    if font is not None:
        del font

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

def handle_event(e):
    if ui_controller.handle_event(e):  # UIController가 이벤트 처리
        return
    if skill_tree_ui.is_active:  # 스킬 트리 UI 활성화 상태에서는 Boy 이벤트를 처리하지 않음
        return
    boy.handle_event(e)

if __name__ == '__main__':
    gfw.start_main_module()
