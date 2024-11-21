import gfw
from pico2d import *
import main_scene

import sys
self = sys.modules[__name__]

canvas_width = main_scene.canvas_width
canvas_height = main_scene.canvas_height

center_x = canvas_width // 2
center_y = canvas_height // 2

world = gfw.World(2)

def enter():
    self.gauge = gfw.Gauge('res/progress_bg.png', 'res/progress_fg.png')
    self.font = load_font('res/ENCR10B.TTF', 30)

    world.append(gfw.Sprite('res/title.png', center_x, center_y), 0)
    world.append(self, 1)

    self.image_index = 0
    self.image_count = len(IMAGE_FILES)
    self.images = iter(IMAGE_FILES)
    self.file = ''
    self.progress_y = canvas_height // 3
    self.progress_w = canvas_width * 2 // 3
    self.other_x = center_x - self.progress_w // 2
    self.color = (87, 41, 138) #57298a
    # print(len(list(images)))

def update():
    self.file = next(images, None)
    if file is None:
        gfw.change(main_scene)
        return
    print(f'Loading {file=}')
    gfw.image.load(file)
    self.image_index += 1

def draw():
    progress = image_index / image_count
    gauge.draw(center_x, progress_y, progress_w, progress)
    font.draw(other_x, progress_y - 50, self.file, self.color)
    font.draw(other_x, progress_y + 50, '%.1f%%' % (progress * 100), self.color)

def exit():
    gfw.image.unload('res/title.png')
    gfw.image.unload('res/progress_bg.png')
    gfw.image.unload('res/progress_fg.png')
    world.clear()
    del self.font

def handle_event(e):
    pass

IMAGE_FILES = [
    "res/InGameBack_1280_960.png",
    "res/PokemonPlayer.png",
    "res/bullet.png",
    "res/Progress_bg02.png",
    "res/Progress_fg02.png",
    "res/enemy.png",
    "res/exp_item.png"
]

if __name__ == '__main__':
    gfw.start_main_module()
