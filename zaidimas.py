import pygame
import sys
import glob
from pygame import *
import pickle
from random import randrange

pygame.init()

font = pygame.font.SysFont("calibri", 16)
HEIGHT = 704
WIDTH = 704
cell_size = 32
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
image_path = "img/"
image_format = "*.gif"
right = "right"
left = "left"
up = "up"
down = "down"
up_right = "up_right"
up_left = "up_left"
down_right = "down_right"
down_left = "down_left"
map_size_x = 15
map_size_y = 15
map_image = "img/map/"
map_sprites = []
frame_sprites = []


class Character(pygame.sprite.Sprite):
    def __init__(self, name):
        super(Character, self).__init__()
        self.direction = right
        self.name_string = name
        self.name = font.render(self.name_string, True, (255, 255, 255))
        self.can_go_up = True
        self.can_go_down = True
        self.can_go_left = True
        self.can_go_right = True
        self.can_go_up_right = True
        self.can_go_up_left = True
        self.can_go_down_left = True
        self.can_go_down_right = True
        self.animations = glob.glob(image_path + self.direction + "/"
                                    + image_format)
        self.animations.sort()
        self.stationary = glob.glob(image_path + self.direction +
                                    "/stationary/" + image_format)
        self.index = 0
        self.image = pygame.image.load(self.stationary[0]).convert()
        self.pos_x = 10*cell_size
        self.pos_y = 10*cell_size
        self.count = 0
        self.rect = pygame.Rect(self.pos_x, self.pos_y, 64, 64)
        self.in_action = False
        self.move_cell = 0
        self.radius = 46
        self.name_pos_x = (self.rect.center[0] - font.size(
                           self.name_string)[0] / 2)
        self.name_pos_y = self.pos_y

    def change_direction(self, direction):
        self.direction = direction
        self.animations = glob.glob(image_path + self.direction + "/"
                                    + image_format)
        self.animations.sort()
        self.stationary = glob.glob(image_path + self.direction +
                                    "/stationary/" + image_format)

    def load_surfices(self):
        self.image = pygame.image.load(self.stationary[0]).convert()
        self.rect = pygame.Rect(self.pos_x, self.pos_y, 64, 64)

    def update(self):
        if self.in_action:
            self.move_cell += 1
            self.count += 1
            if self.index == 7 and self.count == 4:
                self.index = 0
                self.count = 0
            if self.count == 4:
                self.index += 1
                self.image = (pygame.image.load(
                              self.animations[self.index]).convert())
                self.count = 0
            if self.move_cell == cell_size:
                self.in_action = False
                self.move_cell = 0
                self.image = pygame.image.load(self.stationary[0]).convert()
        self.rect = pygame.Rect(self.pos_x, self.pos_y, 64, 64)

    def draw_name(self):
        screen.blit(self.name, (self.name_pos_x, self.name_pos_y))


class Map_Ground(pygame.sprite.Sprite):

    def __init__(self, coord_x, coord_y, image):
        super(Map_Ground, self).__init__()
        self.direction = right
        self.delta_x = 0
        self.delta_y = 0
        self.render = False
        self.render_count = 0
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.pos_x = self.coord_x * cell_size
        self.pos_y = self.coord_y * cell_size
        self.image = pygame.image.load(image).convert()
        self.rect = pygame.Rect(self.pos_x, self.pos_y, cell_size, cell_size)
        self.delta_coord()

    def update(self):
        if self.render:
            self.render_count += 1
            self.pos_x += self.delta_x
            self.pos_y += self.delta_y
            if self.render_count == cell_size:
                self.render = False
                self.render_count = 0
            self.rect = pygame.Rect(self.pos_x, self.pos_y, cell_size,
                                    cell_size)

    def change_direction(self, direction):
        self.direction = direction
        self.delta_coord()

    def delta_coord(self):
        if self.direction == right:
            self.delta_x = -1
            self.delta_y = 0
        elif self.direction == left:
            self.delta_x = 1
            self.delta_y = 0
        elif self.direction == up:
            self.delta_x = 0
            self.delta_y = 1
        elif self.direction == down:
            self.delta_x = 0
            self.delta_y = -1
        elif self.direction == up_right:
            self.delta_x = -1
            self.delta_y = 1
        elif self.direction == down_right:
            self.delta_x = -1
            self.delta_y = -1
        elif self.direction == up_left:
            self.delta_x = 1
            self.delta_y = 1
        elif self.direction == down_left:
            self.delta_x = 1
            self.delta_y = -1


class Obsticles(pygame.sprite.Sprite):

    def __init__(self, coord_x, coord_y, image):
        super(Obsticles, self).__init__()
        self.direction = right
        self.delta_x = 0
        self.delta_y = 0
        self.render = False
        self.render_count = 0
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.pos_x = self.coord_x * cell_size
        self.pos_y = self.coord_y * cell_size
        self.image = pygame.image.load(image).convert()
        self.rect = pygame.Rect(self.pos_x, self.pos_y, 64, 32)

    def update(self):
        if self.render:
            self.render_count += 1
            self.pos_x += self.delta_x
            self.pos_y += self.delta_y
            if self.render_count == cell_size:
                self.render = False
                self.render_count = 0
            self.rect = pygame.Rect(self.pos_x, self.pos_y, cell_size * 2,
                                    cell_size)

    def change_direction(self, direction):
        self.direction = direction
        self.delta_coord()

    def delta_coord(self):
        if self.direction == right:
            self.delta_x = -1
            self.delta_y = 0
        elif self.direction == left:
            self.delta_x = 1
            self.delta_y = 0
        elif self.direction == up:
            self.delta_x = 0
            self.delta_y = 1
        elif self.direction == down:
            self.delta_x = 0
            self.delta_y = -1
        elif self.direction == up_right:
            self.delta_x = -1
            self.delta_y = 1
        elif self.direction == down_right:
            self.delta_x = -1
            self.delta_y = -1
        elif self.direction == up_left:
            self.delta_x = 1
            self.delta_y = 1
        elif self.direction == down_left:
            self.delta_x = 1
            self.delta_y = -1


class Map_Frame(pygame.sprite.Sprite):

    def __init__(self, coord_x, coord_y, image):
        super(Map_Frame, self).__init__()
        self.direction = right
        self.delta_x = 0
        self.delta_y = 0
        self.render = False
        self.render_count = 0
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.pos_x = self.coord_x * cell_size
        self.pos_y = self.coord_y * cell_size
        self.image = pygame.image.load(image).convert()
        self.rect = pygame.Rect(self.pos_x, self.pos_y, cell_size, cell_size)
        self.delta_coord()

    def update(self):
        if self.render:
            self.render_count += 1
            self.pos_x += self.delta_x
            self.pos_y += self.delta_y
            if self.render_count == cell_size:
                self.render = False
                self.render_count = 0
            self.rect = pygame.Rect(self.pos_x, self.pos_y, cell_size,
                                    cell_size)

    def change_direction(self, direction):
        self.direction = direction
        self.delta_coord()

    def delta_coord(self):
        if self.direction == right:
            self.delta_x = -1
            self.delta_y = 0
        elif self.direction == left:
            self.delta_x = 1
            self.delta_y = 0
        elif self.direction == up:
            self.delta_x = 0
            self.delta_y = 1
        elif self.direction == down:
            self.delta_x = 0
            self.delta_y = -1
        elif self.direction == up_right:
            self.delta_x = -1
            self.delta_y = 1
        elif self.direction == down_right:
            self.delta_x = -1
            self.delta_y = -1
        elif self.direction == up_left:
            self.delta_x = 1
            self.delta_y = 1
        elif self.direction == down_left:
            self.delta_x = 1
            self.delta_y = -1


def collision_movement(sprite, group):
    for i in pygame.sprite.spritecollide(sprite, group, False,
                                         pygame.sprite.collide_circle):
        if (i.rect.left == sprite.rect.right and
            i.rect.top != sprite.rect.bottom and
            i.rect.bottom != sprite.rect.top):
            sprite.can_go_right = False
        if (i.rect.right == sprite.rect.left and i.rect.top !=
            sprite.rect.bottom and i.rect.bottom != sprite.rect.top):
            sprite.can_go_left = False
        if (i.rect.top == sprite.rect.bottom and i.rect.right !=
            sprite.rect.left and i.rect.left != sprite.rect.right):
            sprite.can_go_down = False
        if (i.rect.bottom == sprite.rect.top and i.rect.right !=
            sprite.rect.left and i.rect.left != sprite.rect.right):
            sprite.can_go_up = False
        if ((i.rect.bottom == sprite.rect.top and i.rect.right ==
             sprite.rect.left) or
            (i.rect.bottom == sprite.rect.top and i.rect.left <
             sprite.rect.right - cell_size) or
            (i.rect.right == sprite.rect.left and i.rect.top <
             sprite.rect.bottom - cell_size)):
            sprite.can_go_up_left = False
        if ((i.rect.bottom == sprite.rect.top and i.rect.left ==
             sprite.rect.right) or
            (i.rect.bottom == sprite.rect.top and i.rect.right >
             sprite.rect.left + cell_size) or
            (i.rect.left == sprite.rect.right and i.rect.top <
             sprite.rect.bottom - cell_size)):
            sprite.can_go_up_right = False
        if ((i.rect.top == sprite.rect.bottom and i.rect.left ==
             sprite.rect.right) or
            (i.rect.top == sprite.rect.bottom and i.rect.right >
             sprite.rect.left + cell_size) or
            (i.rect.left == sprite.rect.right and i.rect.bottom >
             sprite.rect.top + cell_size)):
            sprite.can_go_down_right = False
        if ((i.rect.top == sprite.rect.bottom and i.rect.right ==
             sprite.rect.left) or
            (i.rect.top == sprite.rect.bottom and i.rect.left <
             sprite.rect.right - cell_size) or
            (i.rect.right == sprite.rect.left and i.rect.bottom >
             sprite.rect.top + cell_size)):
            sprite.can_go_down_left = False


def movement_handler(direction):
    character_sprite.change_direction(direction)
    character_sprite.in_action = True
    for i in map_group:
        i.change_direction(direction)
        i.render = True
    for i in frame_group:
        i.change_direction(direction)
        i.render = True
    for i in obsticle_group:
        i.change_direction(direction)
        i.render = True


def char_can_go():
    character_sprite.can_go_up = True
    character_sprite.can_go_down = True
    character_sprite.can_go_left = True
    character_sprite.can_go_right = True
    character_sprite.can_go_up_right = True
    character_sprite.can_go_up_left = True
    character_sprite.can_go_down_left = True
    character_sprite.can_go_down_right = True

character_sprite = Character("Gintautas")
for i in range(1, map_size_x + 1):
    for j in range(1, map_size_y + 1):
        map_sprites.append(Map_Ground(i, j, map_image +
                           str(randrange(1, 21)) + ".GIF"))
obsticle_sprite = Obsticles(4, 4, "img/obsticles/2.gif")

frame_sprites.append(Map_Frame(0, 0, "img/frames/top_left.gif"))
frame_sprites.append(Map_Frame(0, map_size_y + 1,
                               "img/frames/bottom_left.gif"))
frame_sprites.append(Map_Frame(map_size_x + 1, 0, "img/frames/top_right.gif"))
frame_sprites.append(Map_Frame(map_size_x + 1, map_size_y + 1,
                               "img/frames/bottom_right.gif"))

for i in range(1, map_size_x + 1):
    frame_sprites.append(Map_Frame(0, i, "img/frames/left.gif"))
    frame_sprites.append(Map_Frame(i, 0, "img/frames/top.gif"))
    frame_sprites.append(Map_Frame(map_size_x + 1, i, "img/frames/right.gif"))
    frame_sprites.append(Map_Frame(i, map_size_x + 1, "img/frames/bottom.gif"))

characters_group = pygame.sprite.Group(character_sprite)
map_group = pygame.sprite.Group(map_sprites)
frame_group = pygame.sprite.Group(frame_sprites)
obsticle_group = pygame.sprite.Group(obsticle_sprite)
pygame.key.set_repeat(1, 1)
while True:

    char_can_go()
    collision_movement(character_sprite, frame_group)
    collision_movement(character_sprite, obsticle_group)

    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[K_q]:
            sys.exit(0)
        elif keys[K_s] and keys[K_d] and character_sprite.can_go_down_right:
            if not character_sprite.in_action:
                movement_handler(down_right)
        elif keys[K_s] and keys[K_a] and character_sprite.can_go_down_left:
            if not character_sprite.in_action:
                movement_handler(down_left)
        elif keys[K_w] and keys[K_d] and character_sprite.can_go_up_right:
            if not character_sprite.in_action:
                movement_handler(up_right)
        elif keys[K_w] and keys[K_a] and character_sprite.can_go_up_left:
            if not character_sprite.in_action:
                movement_handler(up_left)
        elif keys[K_d] and character_sprite.can_go_right:
            if not character_sprite.in_action:
                movement_handler(right)
        elif keys[K_a] and character_sprite.can_go_left:
            if not character_sprite.in_action:
                movement_handler(left)
        elif keys[K_w] and character_sprite.can_go_up:
            if not character_sprite.in_action:
                movement_handler(up)
        elif keys[K_s] and character_sprite.can_go_down:
            if not character_sprite.in_action:
                movement_handler(down)

    characters_group.update()
    map_group.update()
    frame_group.update()
    obsticle_group.update()
    map_group.draw(screen)
    obsticle_group.draw(screen)
    characters_group.draw(screen)
    frame_group.draw(screen)
    character_sprite.draw_name()
    pygame.display.flip()
    clock.tick(64)

