from pico2d import *
import gfw
from functools import reduce
import pickle
import os

class World:
    def __init__(self, layer_count=1):
        if isinstance(layer_count, list):
            layer_names = layer_count
            layer_count = len(layer_count)
            index = 0
            self.layer = lambda: None # 임의의 객체를 생성할 때 python 에서 즐겨 사용하는 방식
            for name in layer_names:
                self.layer.__dict__[name] = index
                index += 1
            

        self.objects = [[] for i in range(layer_count)]
        self.bullet_manager = None  # BulletManager를 위한 변수
        self.enemy_spawner = None  # EnemySpawner를 위한 변수
        self.ui_controller = None  # UIController 변수 추가
    def append(self, go, layer_index=None):
        if layer_index is None:
            layer_index = go.layer_index
        self.objects[layer_index].append(go)
    def remove(self, go, layer_index=None):
        if layer_index is None:
            layer_index = go.layer_index
        self.objects[layer_index].remove(go)
    def clear(self):
        layer_count = len(self.objects)
        self.objects = [[] for i in range(layer_count)]
    def update(self):
        for go in self.all_objects():
            go.update()
        if self.ui_controller:
            self.ui_controller.update()  # UIController 업데이트
        if self.enemy_spawner:
            self.enemy_spawner.update()  # EnemySpawner 업데이트
        # BulletManager 업데이트
        if self.bullet_manager:
            self.bullet_manager.update()
    def draw(self):
        for go in self.all_objects():
            go.draw()
        if self.ui_controller:
            self.ui_controller.draw()  # UIController 렌더링
        if gfw.shows_bounding_box:
            for go in self.all_objects():
                if not hasattr(go, 'get_bb'): continue
                l,b,r,t = go.get_bb()
                if hasattr(self, 'bg'):
                  l,b = self.bg.to_screen(l,b)
                  r,t = self.bg.to_screen(r,t)
                draw_rectangle(l,b,r,t)
        if gfw.shows_object_count and gfw._system_font is not None:
            gfw._system_font.draw(10, 20, str(list(map(len, self.objects))) + ' ' + str(self.count()))
        
    def set_bullet_manager(self, bullet_manager):
        self.bullet_manager = bullet_manager  # BulletManager 등록

    def all_objects(self):
        for objs in self.objects:
            for i in range(len(objs) - 1, -1, -1):
                yield objs[i]

    def objects_at(self, layer_index):
        objs = self.objects[layer_index]
        for i in range(len(objs) - 1, -1, -1):
            yield objs[i]

    def count_at(self, layer_index):
        return len(self.objects[layer_index])

    def count(self):
        return reduce(lambda sum, a: sum + len(a), self.objects, 0)

    def save(self, fn='world.pickle'):
        with open(fn, 'wb') as f:
            pickle.dump(self.objects, f)

    def load(self, fn='world.pickle'):
        if not os.path.exists(fn):
            return False
        with open(fn, 'rb') as f:
            self.objects = pickle.load(f)
        return True
    
    def set_enemy_spawner(self, spawner):
        self.enemy_spawner = spawner

    def set_ui_controller(self, ui_controller):
        self.ui_controller = ui_controller

def collides_box(a, b): # a or b is a Sprite
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ba > tb: return False
    if ta < bb: return False

    return True
