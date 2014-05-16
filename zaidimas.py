import pygame
import sys
import os
import glob
import eztext
from pygame import *
import pickle
from random import randrange
from os.path import basename
from datetime import datetime

pygame.init()

font = pygame.font.SysFont("times new roman ", 16)
text_font = pygame.font.SysFont("times new roman ", 24)
console_font = pygame.font.SysFont("times new roman ", 16)
HEIGHT = 672
WIDTH = 864
cell_size = 32
no_1 = pygame.image.load("img/numbers/1.png")
no_2 = pygame.image.load("img/numbers/2.png")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
faction_list = os.listdir("img/chars")
faction_length = len(faction_list)
char_image_path = "img/chars/"
npc_image_path = "img/npc/"
gif_image_format = "*.gif"
png_image_format = "*.png"
right = "right"
left = "left"
up = "up"
down = "down"
up_right = "up_right"
up_left = "up_left"
down_right = "down_right"
down_left = "down_left"
map_image = "img/map/"
in_main_game = True
in_char_create = False
in_mode_selection = False
in_map_selection = False
in_multiplayer = False
in_map_selection = False
in_game = False
multiplayer = False
exp_to_level = {1 : 100, 2: 200, 3: 500, 4: 1000, 5: 5000}
max_level = 5
main_image = pygame.image.load("img/main.png")
int_image = pygame.image.load("img/int.png")
button_path = "img/buttons/normal/"
arrow_left_path = "img/buttons/arrows/left/"
arrow_right_path = "img/buttons/arrows/right/"
text_box = eztext.Input(x = 290, y = 100, maxlength = 16, color = (255, 255, 255), prompt = "Name:" )
characters = []
maps = []
first_player_selected = False
second_player_selected = False
alive_npc_group = pygame.sprite.Group()
main_button_group = pygame.sprite.Group()
char_button_group = pygame.sprite.Group()
map_button_group = pygame.sprite.Group()
mode_button_group = pygame.sprite.Group()
multiplayer_button_group = pygame.sprite.Group()
smplayer_button_group = pygame.sprite.Group()
char_create_button_group = pygame.sprite.Group()


class Character(pygame.sprite.Sprite):
    def __init__(self, name, faction, portrait_path, mini_portrait_path):
        super(Character, self).__init__()
        self.direction = right
        self.health_max = 100
        self.health_remaining = self.health_max
        self.mana_max = 100
        self.mana_remaining = self.mana_max
        self.player_no = 0
        self.exp = 0
        self.level = 1
        self.interface = None
        self.name_string = name
        self.name = font.render(self.name_string, True, (255, 255, 255))
        self.faction = faction
        self.portrait_path = portrait_path
        self.mini_portrait_path = mini_portrait_path
        self.delta_x = 0
        self.delta_y = 0
        self.health_regen = 0
        self.mana_regen = 0
        self.can_go_up = True
        self.can_go_down = True
        self.can_go_left = True
        self.can_go_right = True
        self.can_go_up_right = True
        self.can_go_up_left = True
        self.can_go_down_left = True
        self.can_go_down_right = True
        self.animations = glob.glob(char_image_path + self.faction + "/" + self.direction + "/"
                                    + gif_image_format)
        self.animations.sort()
        self.stationary = glob.glob(char_image_path + self.faction + "/" + self.direction +
                                    "/stationary/" + gif_image_format)
        self.index = 0
        self.image = pygame.image.load(self.stationary[0]).convert()
        self.pos_x = 0
        self.pos_y = 0
        self.count = 0
        self.rect = pygame.Rect(self.pos_x, self.pos_y, 64, 64)
        self.in_action = False
        self.move_cell = 0
        self.radius = 46
        self.name_pos_x = (self.rect.center[0] - font.size(
                           self.name_string)[0] / 2)
        self.name_pos_y = self.pos_y
        self.image_size = self.image.get_size()
        self.delta_coord()
        self.attack_group = pygame.sprite.Group()
        self.attack_delay = False
        self.attack_delay_count = 0

    def reset(self):
        self.direction = right
        self.health_remaining = 100
        self.player_no = 0
        self.interface = None
        self.delta_x = 0
        self.delta_y = 0
        self.can_go_up = True
        self.can_go_down = True
        self.can_go_left = True
        self.can_go_right = True
        self.can_go_up_right = True
        self.can_go_up_left = True
        self.can_go_down_left = True
        self.can_go_down_right = True
        self.in_action = False
        self.move_cell = 0
        self.attack_group.empty()

    def change_direction(self, direction):
        self.direction = direction
        self.animations = glob.glob(char_image_path + self.faction + "/" + self.direction + "/"
                                    + gif_image_format)
        self.animations.sort()
        self.stationary = glob.glob(char_image_path + self.faction + "/" + self.direction +
                                    "/stationary/" + gif_image_format)
        self.delta_coord()

    def create_interface(self, player_no):
        self.player_no = player_no
        self.interface = Player_interface(self.health_max, self.health_remaining, self.exp, exp_to_level[self.level], self.portrait_path, 
                                          self.name_string, self.level, player_no, self.mana_max, self.mana_remaining)

    def delta_coord(self):
        if self.direction == right:
            self.delta_x = 1
            self.delta_y = 0
        elif self.direction == left:
            self.delta_x = -1
            self.delta_y = 0
        elif self.direction == up:
            self.delta_x = 0
            self.delta_y = -1
        elif self.direction == down:
            self.delta_x = 0
            self.delta_y = 1
        elif self.direction == up_right:
            self.delta_x = 1
            self.delta_y = -1
        elif self.direction == down_right:
            self.delta_x = 1
            self.delta_y = 1
        elif self.direction == up_left:
            self.delta_x = -1
            self.delta_y = -1
        elif self.direction == down_left:
            self.delta_x = -1
            self.delta_y = 1

    def set_pos(self,pos):
        self.pos_x = pos[0] * cell_size + 224
        self.pos_y = pos[1] * cell_size
        self.rect.topleft = (self.pos_x, self.pos_y)
        self.name_pos_x = (self.rect.center[0] - font.size(
                           self.name_string)[0] / 2)
        self.name_pos_y = self.pos_y

    def update(self):
        if self.attack_delay:
            if self.attack_delay_count == 40:
                self.attack_delay = False
                self.attack_delay_count = 0
            else:
                self.attack_delay_count += 1
        if self.level < max_level:
            while self.exp >= exp_to_level[self.level] and self.level <= max_level :
                self.exp -= exp_to_level[self.level]
                self.level +=1
                console.print_text("Level: "+str(self.level) + "reached")
        elif self.exp > exp_to_level [self.level]:
            self.exp = exp_to_level[self.level]
        if self.health_remaining < 0:
            self.health_remaining = 0
        if self.health_remaining < self.health_max:
            if self.health_regen == 16:
                self.health_remaining += 1
                self.health_regen = 0
            else:
                self.health_regen +=1
        if self.mana_remaining < self.mana_max:
            if self.mana_regen == 36:
                self.mana_remaining += 1
                self.mana_regen = 0
            else:
                self.mana_regen +=1
        if self.in_action:
            self.pos_x += self.delta_x
            self.pos_y += self.delta_y
            self.name_pos_x += self.delta_x
            self.name_pos_y += self.delta_y
            if self.index == 0 and self.count == 0:
                self.image = (pygame.image.load(
                              self.animations[self.index]).convert())
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
        self.interface.update(self.health_max, self.health_remaining, self.exp, exp_to_level[self.level], self.level, self.mana_remaining)
        self.attack_group.update()
        attack_collisions(self.attack_group, self.player_no)

    def attack(self):
        if not self.attack_delay and self.mana_remaining >=10:
            self.attack_delay = True
            self.mana_remaining -= 10
            self.attack_group.add(Attack(self.rect.center, self.delta_x, self.delta_y, char_image_path + "/" + self.faction + "/attack/" + self.direction + ".png", randrange(5,20), self))

    def draw_name(self):
        screen.blit(self.name, (self.name_pos_x, self.name_pos_y))
        self.attack_group.draw(screen)

    def to_string(self):
        self.image = pygame.image.tostring(self.image, "RGBA")
        self.name = None

    def from_string(self):
        self.image = pygame.image.fromstring(self.image, self.image_size, "RGBA")
        self.name = font.render(self.name_string, True, (255, 255, 255))


class Player_interface():
    def __init__(self, health_total, health_remaining, exp, exp_to_next, portrait_path, name, level, player_no, mana_total, mana_remaining):
        self.player_no = player_no
        self.health_total = health_total
        self.health_remaining = health_remaining
        self.mana_total = mana_total
        self.mana_remaining = mana_remaining
        self.exp = exp
        self.name = name
        self.level = level
        self.heading = font.render(self.name + "     Level: " + str(self.level), True, (255, 255, 255))
        self.portrait_path = portrait_path
        self.exp_to_next = exp_to_next
        self.health_color = (255, 0, 0)
        self.exp_color = (143, 135, 135)
        self.mana_color = (0, 0, 255)
        if self.portrait_path != "":
            self.portrait = pygame.image.load(self.portrait_path)
            self.portrait_size = self.portrait.get_size()
        self.bar = pygame.image.load("img/interface/bar.png")
        self.bar_size = self.bar.get_size()
        self.portrait_frame = pygame.image.load("img/interface/frame.png")
        self.frame_size = self.portrait_frame.get_size()
        self.bar_size_x = 18
        self.health_bar_size_y = (174 * self.health_remaining)/self.health_total
        self.exp_bar_size_y = (174 * self.exp)/ self.exp_to_next
        self.mana_bar_size_y = (174 * self.mana_remaining)/ self.mana_total
        
    def update(self, health_total, health_remaining, exp, exp_to_next, level, mana_remaining):
        self.health_total = health_total
        self.health_remaining = health_remaining
        self.mana_remaining = mana_remaining
        self.level = level
        self.exp = exp
        self.exp_to_next = exp_to_next
        self.heading = font.render(self.name + "     Level: " + str(self.level), True, (255, 255, 255))
        self.health_bar_size_y = (174 * self.health_remaining)/self.health_total
        self.exp_bar_size_y = (174 * self.exp)/ self.exp_to_next
        self.mana_bar_size_y = (174 * self.mana_remaining)/ self.mana_total

    def draw(self, screen):
        if self.player_no ==1:
            screen.blit(self.heading,(10, 10))
            screen.blit(self.portrait, (16, 35))
            screen.blit(self.portrait_frame, (10, 30))
            pygame.draw.rect(screen, self.health_color,((93, 43),(self.bar_size_x, self.health_bar_size_y)))
            screen.blit(self.bar, (88, 30))
            pygame.draw.rect(screen, self.mana_color,((131, 43),(self.bar_size_x, self.mana_bar_size_y)))
            screen.blit(self.bar, (126, 30))
            pygame.draw.rect(screen, self.exp_color,((169, 43),(self.bar_size_x, self.exp_bar_size_y)))
            screen.blit(self.bar, (164, 30))
        elif self.player_no == 2:
            screen.blit(self.heading,(10, 330))
            screen.blit(self.portrait, (16, 355))
            screen.blit(self.portrait_frame, (10, 350))
            pygame.draw.rect(screen, self.health_color,((93, 363),(self.bar_size_x, self.health_bar_size_y)))
            screen.blit(self.bar, (88, 350))
            pygame.draw.rect(screen, self.mana_color,((131, 363),(self.bar_size_x, self.mana_bar_size_y)))
            screen.blit(self.bar, (126, 350))
            pygame.draw.rect(screen, self.exp_color,((169, 363),(self.bar_size_x, self.exp_bar_size_y)))
            screen.blit(self.bar, (164, 350))

class Attack(pygame.sprite.Sprite):
    def __init__(self,position, delta_x, delta_y, sprite_path, damage, obj = None):
        super(Attack, self).__init__()
        self.position = position
        self.pos_x = position[0]
        self.pos_y = position[1]
        self.delta_x = delta_x * 3
        self.delta_y = delta_y * 3
        self.image = pygame.image.load(sprite_path)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.obj = obj
        self.damage = damage

    def update(self):
        self.pos_x += self.delta_x
        self.pos_y += self.delta_y
        self.position = (self.pos_x, self.pos_y)
        self.rect.center = self.position

class Map():
    def __init__(self, map_size_x, map_size_y, name, spawn_points ):
        self.map_size_x = map_size_x
        self.map_size_y = map_size_y
        self.map_group = pygame.sprite.Group()
        self.frame_group = pygame.sprite.Group()
        self.obsticle_group = pygame.sprite.Group()
        self.npc_group = pygame.sprite.Group()
        self.map_list = []
        self.frame_list = []
        self.obsticle_list = []
        self.npc_list = []
        self.spawn_points = spawn_points
        self.name = name
        self.map_positions = {}

    def draw(self):
        self.map_group.draw(screen)
        self.obsticle_group.draw(screen)
        self.frame_group.draw(screen)
        self.npc_group.draw(screen)
        for i in self.npc_group:
            i.draw_rest(screen)

    def update(self):
        self.npc_group.update()

    def to_string(self):
        for i in self.map_group:
            i.to_string()
            self.map_list.append(i)
        for i in self.frame_group:
            i.to_string()
            self.frame_list.append(i)
        for i in self.obsticle_group:
            i.to_string()
            self.obsticle_list.append(i)
        for i in self.npc_group:
            i.to_string()
            self.npc_list.append(i)

    def from_string(self):
        self.map_group = pygame.sprite.Group(self.map_list)
        self.frame_group = pygame.sprite.Group(self.frame_list)
        self.obsticle_group = pygame.sprite.Group(self.obsticle_list)
        self.npc_group = pygame.sprite.Group(self.npc_list)
        for i in self.map_group:
            i.from_string()
        for i in self.frame_group:
            i.from_string()
        for i in self.obsticle_group:
            i.from_string()
        for i in self.npc_group:
            i.from_string()

class Map_Object(pygame.sprite.Sprite):

    def __init__(self, coord_x, coord_y, image, rect_size_x, rect_size_y):
        super(Map_Object, self).__init__()
        self.rect_size_x = rect_size_x
        self.rect_size_y = rect_size_y -32
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.image_path = image
        self.pos_x = self.coord_x * cell_size +224
        self.pos_y = self.coord_y * cell_size
        self.image = pygame.image.load(self.image_path)
        self.image.convert_alpha()
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.rect_size_x, self.rect_size_y)
        self.image_size = self.image.get_rect().size

    def to_string(self):
        self.image = None

    def from_string(self):
        self.image = pygame.image.load(self.image_path)
        self.image.convert_alpha()
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.rect_size_x, self.rect_size_y)

    def get_pos(self):
        return (self.pos_x, self.pos_y)


class NPC(pygame.sprite.Sprite):

    def __init__(self, coord_x, coord_y, name, health):
        super(NPC, self).__init__()
        self.hit_by = {}
        self.health_color = (255,0,0)
        self.name_string = name
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.pos_x = self.coord_x * cell_size +224
        self.pos_y = self.coord_y * cell_size
        self.max_health = health
        self.current_health = health
        self.stationary_path = npc_image_path + self.name_string + "/stationary.png"
        self.hit_path = glob.glob(npc_image_path + self.name_string + "/hit/" + png_image_format)
        self.hit_path.sort()
        self.animation_path = glob.glob(npc_image_path + self.name_string + "/animation/" + png_image_format)
        self.animation_path.sort()
        self.dead_path = glob.glob(npc_image_path + self.name_string + "/dead/" + png_image_format)
        self.dead_path.sort()
        self.dead = False
        self.animate = False
        self.hit = False
        self.image = pygame.image.load(self.stationary_path)
        self.image.convert_alpha()
        self.image_size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos_x, self.pos_y)
        self.name = font.render(self.name_string, True, (255, 255, 255))
        self.name_pos_y = self.rect.top -20
        self.name_pos_x = (self.rect.center[0] - font.size(
                           self.name_string)[0] / 2)
        self.animation_iterator = 0

    def update(self):
        if self.current_health <= 0 and not self.dead:
            self.dead = True
            self.hit = False
            for i in self.hit_by:
                i.exp += self.hit_by[i]
            self.current_health = 0

        if not self.dead and not self.hit and not self.animate and randrange(0, 200) == 1:
            self.animate = True

        if self.dead and self.animation_iterator < 64:
            self.image = pygame.image.load(self.dead_path[(self.animation_iterator/8)])
            self.image.convert_alpha()
            self.animation_iterator +=1

        if self.hit:
            self.image = pygame.image.load(self.hit_path[(self.animation_iterator/8)])
            self.image.convert_alpha()
            self.animation_iterator +=1
            if self.animation_iterator == 64:
                self.animation_iterator = 0
                self.hit = False

        if self.animate:
            self.image = pygame.image.load(self.animation_path[(self.animation_iterator/8)])
            self.image.convert_alpha()
            self.animation_iterator +=1
            if self.animation_iterator == 64:
                self.animation_iterator = 0
                self.animate = False

    def hit_npc(self, damage, hit_by_char):
        if hit_by_char in self.hit_by.keys():
            self.hit_by[hit_by_char] += damage
        else:
            self.hit_by[hit_by_char] = damage
        self.current_health -= damage
        self.hit = True
        self.animate = False
        self.animation_iterator = 0

    def draw_rest(self, screen):
        pygame.draw.rect(screen, self.health_color,(self.rect.topleft,(self.current_health * self.image_size[0]/self.max_health, 4)))
        screen.blit(self.name, (self.name_pos_x, self.name_pos_y))

    def to_string(self):
        self.image = None
        self.name = None

    def from_string(self):
        self.image = pygame.image.load(self.stationary_path)
        self.name = font.render(self.name_string, True, (255, 255, 255))


class Button(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, image_path, text = "", obj = None, portrait_path = None):
        super(Button, self).__init__()
        self.pressed = False
        self.portrait_path = portrait_path
        if self.portrait_path != None:
            self.portrait = pygame.image.load(portrait_path)
        self.obj = obj
        self.str_text = text
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.button_pressed = image_path + "pressed.png"
        self.button_normal = image_path + "normal.png"
        self.image = pygame.image.load(self.button_normal)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos_x, self.pos_y)
        self.p_no = 0
        if self.str_text != "":
            self.text = text_font.render(self.str_text, True, (255, 255, 255))
            self.text_pos_x = (self.rect.center[0] - text_font.size(
                               self.str_text)[0] / 2)
            if self.portrait_path != None:
                self.text_pos_x += 35
            self.text_pos_y = self.rect.center[1]-14
    
    def update(self):
        if self.pressed:
            self.image = pygame.image.load(self.button_pressed)
        else:
            self.image = pygame.image.load(self.button_normal)

    def set_player_no(self, p_no):
        self.p_no = p_no

    def draw_text(self):
        if self.str_text !="":
            screen.blit(self.text, (self.text_pos_x, self.text_pos_y))

    def draw_image(self):
        screen.blit(self.portrait, (self.rect.topleft[0] + 35, self.rect.topleft[1] + 16))
        if self.p_no == 1:
            screen.blit(no_1, (self.rect.topleft[0] + 10, self.rect.topleft[1] + 8))
        elif self.p_no == 2:
            screen.blit(no_2, (self.rect.topleft[0] + 10, self.rect.topleft[1] + 8))

    def set_text(self, text):
        self.str_text = text
        self.text = text_font.render(self.str_text, True, (255, 255, 255))
        self.text_pos_x = (self.rect.center[0] - text_font.size(
                           self.str_text)[0] / 2)
        if self.portrait_path != None:
            self.text_pos_x += 35
        self.text_pos_y = self.rect.center[1]-14


class Console():

    def __init__(self):
        self.background_color = (32, 25, 14)
        self.font_color = (255, 255, 255)
        self.pos_x = 0
        self.pos_y = HEIGHT - 32
        self.size_x = WIDTH
        self.size_y = 32
        self.text_pos_x = 10
        self.text_pos_y = self.pos_y + 10
        self.str_text = str(datetime.now()) + ": Game Started"
        self.text = console_font.render(self.str_text, True, self.font_color)

    def print_text(self, text):
        self.str_text = str(datetime.now()) + ": " + text
        self.text = console_font.render(self.str_text, True, self.font_color)

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, ((self.pos_x, self.pos_y), (self.size_x, self.size_y)))
        screen.blit(self.text, (self.text_pos_x, self.text_pos_y))


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

def attack_collisions(attack_group, player_no):
    global multiplayer
    global first_player_sprite
    global second_player_sprite
    pygame.sprite.groupcollide(game_map.frame_group, attack_group, False, True)
    pygame.sprite.groupcollide(game_map.obsticle_group, attack_group, False, True)
    col_dict = pygame.sprite.groupcollide(game_map.npc_group, attack_group, False, False)
    for i in col_dict:
        if not i.dead:
            for j in col_dict[i]:
                i.hit_npc(j.damage, j.obj)
                console.print_text(j.obj.name_string + " hit for " + str(j.damage) + " damage")
                j.kill()
    if multiplayer:
        if player_no == 1:
            for i in pygame.sprite.spritecollide(second_player_sprite, attack_group, False):
                second_player_sprite.health_remaining -= i.damage
                console.print_text(first_player_sprite.name_string + " hit for " + str(i.damage) + " damage")
                i.kill()
        elif player_no ==2:
            for i in pygame.sprite.spritecollide(first_player_sprite, attack_group, False):
                first_player_sprite.health_remaining -= i.damage
                console.print_text(second_player_sprite.name_string + " hit for " + str(i.damage) + " damage")
                i.kill()

def movement_handler(direction, character_sprite):
    character_sprite.change_direction(direction)
    character_sprite.in_action = True

def char_can_go(character_sprite):
    character_sprite.can_go_up = True
    character_sprite.can_go_down = True
    character_sprite.can_go_left = True
    character_sprite.can_go_right = True
    character_sprite.can_go_up_right = True
    character_sprite.can_go_up_left = True
    character_sprite.can_go_down_left = True
    character_sprite.can_go_down_right = True

def game():
    global in_game
    global game_map
    global multiplayer
    first_player_sprite.set_pos(game_map.spawn_points[0])
    first_player_sprite.create_interface(1)
    if multiplayer:
        second_player_sprite.set_pos(game_map.spawn_points[1])
        second_player_sprite.create_interface(2)
    while in_game:

        screen.fill((0, 0, 0))
        alive_npc_group.empty()
        for i in game_map.npc_group:
            if not i.dead:
                alive_npc_group.add(i)
        keys = pygame.key.get_pressed()
        events = pygame.event.get()

        char_can_go(first_player_sprite)
        collision_movement(first_player_sprite, game_map.frame_group)
        collision_movement(first_player_sprite, game_map.obsticle_group)
        collision_movement(first_player_sprite, alive_npc_group)

        for event in events:
            if event.type == pygame.QUIT or keys[K_q]:
                exit()
            elif keys[K_s] and keys[K_d] and first_player_sprite.can_go_down_right:
                if not first_player_sprite.in_action:
                   movement_handler(down_right, first_player_sprite)
            elif keys[K_s] and keys[K_a] and first_player_sprite.can_go_down_left:
                if not first_player_sprite.in_action:
                    movement_handler(down_left, first_player_sprite)
            elif keys[K_w] and keys[K_d] and first_player_sprite.can_go_up_right:
                if not first_player_sprite.in_action:
                    movement_handler(up_right, first_player_sprite)
            elif keys[K_w] and keys[K_a] and first_player_sprite.can_go_up_left:
                if not first_player_sprite.in_action:
                    movement_handler(up_left, first_player_sprite)
            elif keys[K_d] and first_player_sprite.can_go_right:
                if not first_player_sprite.in_action:
                    movement_handler(right, first_player_sprite)
            elif keys[K_a] and first_player_sprite.can_go_left:
                if not first_player_sprite.in_action:
                    movement_handler(left, first_player_sprite)
            elif keys[K_w] and first_player_sprite.can_go_up:
                if not first_player_sprite.in_action:
                    movement_handler(up, first_player_sprite)
            elif keys[K_s] and first_player_sprite.can_go_down:
                if not first_player_sprite.in_action:
                    movement_handler(down, first_player_sprite)
            elif keys[K_h]:
                first_player_sprite.health_remaining -= 10
            elif keys[K_x]:
                first_player_sprite.exp += 1
            elif keys[K_c]:
                first_player_sprite.exp += 500
            if keys[K_SPACE]:
                first_player_sprite.attack()

        if multiplayer:
            char_can_go(second_player_sprite)
            collision_movement(second_player_sprite, game_map.frame_group)
            collision_movement(second_player_sprite, game_map.obsticle_group)
            collision_movement(second_player_sprite, alive_npc_group)

            keys = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.QUIT or keys[K_q]:
                    exit()
                elif keys[K_DOWN] and keys[K_RIGHT] and second_player_sprite.can_go_down_right:
                    if not second_player_sprite.in_action:
                       movement_handler(down_right, second_player_sprite)
                elif keys[K_DOWN] and keys[K_LEFT] and second_player_sprite.can_go_down_left:
                    if not second_player_sprite.in_action:
                        movement_handler(down_left, second_player_sprite)
                elif keys[K_UP] and keys[K_RIGHT] and second_player_sprite.can_go_up_right:
                    if not second_player_sprite.in_action:
                        movement_handler(up_right, second_player_sprite)
                elif keys[K_UP] and keys[K_LEFT] and second_player_sprite.can_go_up_left:
                    if not second_player_sprite.in_action:
                        movement_handler(up_left, second_player_sprite)
                elif keys[K_RIGHT] and second_player_sprite.can_go_right:
                    if not second_player_sprite.in_action:
                        movement_handler(right, second_player_sprite)
                elif keys[K_LEFT] and second_player_sprite.can_go_left:
                    if not second_player_sprite.in_action:
                        movement_handler(left, second_player_sprite)
                elif keys[K_UP] and second_player_sprite.can_go_up:
                    if not second_player_sprite.in_action:
                        movement_handler(up, second_player_sprite)
                elif keys[K_DOWN] and second_player_sprite.can_go_down:
                    if not second_player_sprite.in_action:
                        movement_handler(down, second_player_sprite)
                elif keys[K_h]:
                    first_player_sprite.health_remaining -= 10
                elif keys[K_x]:
                    first_player_sprite.exp += 1
                elif keys[K_c]:
                    first_player_sprite.exp += 500
                if keys[K_RSHIFT]:
                    second_player_sprite.attack()

        characters_group.update()
        game_map.update()
        game_map.draw()
        characters_group.draw(screen)
        screen.blit(int_image, (0, 0))
        console.draw(screen)
        for i in characters_group:
            i.draw_name()
            i.interface.draw(screen)
        pygame.display.flip()
        clock.tick(64)

def mode_screen():
    global in_mode_selection
    global in_map_selection
    global in_multiplayer
    global multiplayer
    while in_mode_selection:
        screen.blit(main_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and button_singleplayer.rect.collidepoint(pygame.mouse.get_pos()):
                console.print_text("Choosing map")
                in_map_selection = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and button_multiplayer.rect.collidepoint(pygame.mouse.get_pos()):
                in_multiplayer = True
                multiplayer = True
                console.print_text("Choosing multiplayer mode")
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and button_back.rect.collidepoint(pygame.mouse.get_pos()):
                console.print_text("Back")
                in_mode_selection = False

            if pygame.mouse.get_pressed()[0] and button_singleplayer.rect.collidepoint(pygame.mouse.get_pos()):
                button_singleplayer.pressed = True
            else:
                button_singleplayer.pressed = False
            if pygame.mouse.get_pressed()[0] and button_multiplayer.rect.collidepoint(pygame.mouse.get_pos()):
                button_multiplayer.pressed = True
            else:
                button_multiplayer.pressed = False
            if pygame.mouse.get_pressed()[0] and button_back.rect.collidepoint(pygame.mouse.get_pos()):
                button_back.pressed = True
            else:
                button_back.pressed = False
       
        mode_button_group.update()
        mode_button_group.draw(screen)
        for i in mode_button_group:
            i.draw_text()
        console.draw(screen)

        pygame.display.flip()
        clock.tick(64)
        if in_map_selection:
            map_selection()
        if in_multiplayer:
            multiplayer_selection()

def exit():
    console.print_text("Exiting game")
    for i in characters:
        i.reset()
        i.to_string()
    save(characters, "chars/chars")
    sys.exit(0)

def multiplayer_selection():
    global in_multiplayer
    global in_map_selection
    global multiplayer
    global second_player_selected
    while in_multiplayer:
        screen.blit(main_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and hot_seat_button.rect.collidepoint(pygame.mouse.get_pos()):
                if second_player_selected:
                    in_map_selection = True
                    characters_group.add(second_player_sprite)
                else:
                    console.print_text("Second character not selected")
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and lan_button.rect.collidepoint(pygame.mouse.get_pos()):
                console.print_text("Not ready yet!")
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and online_button.rect.collidepoint(pygame.mouse.get_pos()):
                console.print_text("Not ready yet!")
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and multiplayer_back_button.rect.collidepoint(pygame.mouse.get_pos()):
                in_multiplayer = False
                multiplayer = False

            if pygame.mouse.get_pressed()[0] and hot_seat_button.rect.collidepoint(pygame.mouse.get_pos()):
                hot_seat_button.pressed = True
            else:
                hot_seat_button.pressed = False
            if pygame.mouse.get_pressed()[0] and lan_button.rect.collidepoint(pygame.mouse.get_pos()):
                lan_button.pressed = True
            else:
                lan_button.pressed = False
            if pygame.mouse.get_pressed()[0] and online_button.rect.collidepoint(pygame.mouse.get_pos()):
                online_button.pressed = True
            else:
                online_button.pressed = False
            if pygame.mouse.get_pressed()[0] and multiplayer_back_button.rect.collidepoint(pygame.mouse.get_pos()):
                multiplayer_back_button.pressed = True
            else:
                multiplayer_back_button.pressed = False

        multiplayer_button_group.update()
        multiplayer_button_group.draw(screen)
        for i in multiplayer_button_group:
            i.draw_text()
        console.draw(screen)

        pygame.display.flip()
        clock.tick(64)
        if in_map_selection:
            map_selection()

def map_selection():
    global in_map_selection
    global in_game
    global game_map
    while in_map_selection:
        screen.blit(main_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and smstart_button.rect.collidepoint(pygame.mouse.get_pos()):
                for i in map_button_group:
                    if i.pressed:
                        game_map = i.obj
                if game_map.map_size_x != 0:
                    in_game = True
                    console.print_text("Entering game in single player mode")
                else:
                    console.print_text("Map not selected")
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and smback_button.rect.collidepoint(pygame.mouse.get_pos()):
                for i in map_button_group:
                    i.pressed = False
                console.print_text("Back")
                in_map_selection = False
            for i in map_button_group:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and i.rect.collidepoint(pygame.mouse.get_pos()):
                    temp = i.pressed
                    for l in map_button_group:
                        l.pressed = False
                    i.pressed = not temp
                    console.print_text("Map selected: " + i.str_text)



            if pygame.mouse.get_pressed()[0] and smstart_button.rect.collidepoint(pygame.mouse.get_pos()):
                smstart_button.pressed = True
            else:
                smstart_button.pressed = False
            if pygame.mouse.get_pressed()[0] and smback_button.rect.collidepoint(pygame.mouse.get_pos()):
                smback_button.pressed = True
            else:
                smback_button.pressed = False

        smplayer_button_group.update()
        map_button_group.update()
        smplayer_button_group.draw(screen)
        map_button_group.draw(screen)
        for i in smplayer_button_group:
            i.draw_text()
        for i in map_button_group:
            i.draw_text()
        console.draw(screen)

        pygame.display.flip()
        clock.tick(64)
        if in_game:
            game()

def create_char():
    global in_char_create
    global character_list_length
    pygame.key.set_repeat(1000, 100)
    faction_index = 0
    faction_button.set_text(faction_list[faction_index])
    current_faction = faction_button.str_text
    portrait_index = 0
    portrait_list = glob.glob(char_image_path + current_faction + "/portraits/" + png_image_format)
    portrait_list.sort()
    portrait_list_length = len(portrait_list)
    current_portrait_path = portrait_list[portrait_index]
    portrait_image = pygame.image.load(current_portrait_path)

    while in_char_create:
        name_invalid = False
        screen.blit(main_image, (0, 0))
        events = pygame.event.get()
        for event in events:

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and create_back_button.rect.collidepoint(pygame.mouse.get_pos()):
                text_box.value = ""
                console.print_text("Back")
                pygame.key.set_repeat(10, 10)
                in_char_create = False
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and create_button.rect.collidepoint(pygame.mouse.get_pos()):
                if text_box.value != "":
                    for i in characters:
                        if text_box.value == i.name_string:
                            name_invalid = True
                    if not name_invalid:
                        characters.append(Character(text_box.value, current_faction, current_portrait_path,
                                          char_image_path + current_faction + "/mini_portraits/" +
                                          basename(current_portrait_path)))
                        char_button_group.empty()
                        char_buttons(characters)
                        character_list_length = len(characters)
                        console.print_text("character created: " + text_box.value)
                        text_box.value = ""
                        pygame.key.set_repeat(10, 10)
                        in_char_create = False
                    else:
                        console.print_text("Name already in use")
                else:
                    console.print_text("Name not entered")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and faction_right_button.rect.collidepoint(pygame.mouse.get_pos()):
                if faction_index +1 == faction_length:
                    faction_index = 0
                else:
                    faction_index += 1
                faction_button.set_text(faction_list[faction_index])
                current_faction = faction_list[faction_index]
                portrait_index = 0
                portrait_list = glob.glob(char_image_path + current_faction + "/portraits/" + png_image_format)
                portrait_list.sort()
                portrait_list_length = len(portrait_list)
                current_portrait_path = portrait_list[portrait_index]
                portrait_image = pygame.image.load(current_portrait_path)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and faction_left_button.rect.collidepoint(pygame.mouse.get_pos()):
                if faction_index == 0:
                    faction_index = faction_length - 1
                else:
                    faction_index -= 1
                faction_button.set_text(faction_list[faction_index])
                current_faction = faction_list[faction_index]
                portrait_index = 0
                portrait_list = glob.glob(char_image_path + current_faction + "/portraits/" + png_image_format)
                portrait_list.sort()
                portrait_list_length = len(portrait_list)
                current_portrait_path = portrait_list[portrait_index]
                portrait_image = pygame.image.load(current_portrait_path)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and portrait_right_button.rect.collidepoint(pygame.mouse.get_pos()):
                if portrait_index +1 == portrait_list_length:
                    portrait_index = 0
                else:
                    portrait_index += 1
                current_portrait_path = portrait_list[portrait_index]
                portrait_image = pygame.image.load(current_portrait_path)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and portrait_left_button.rect.collidepoint(pygame.mouse.get_pos()):
                if portrait_index == 0:
                    portrait_index = portrait_list_length -1
                else:
                    portrait_index -= 1
                current_portrait_path = portrait_list[portrait_index]
                portrait_image = pygame.image.load(current_portrait_path)


            if event.type == pygame.QUIT:
                exit()
            if pygame.mouse.get_pressed()[0] and create_back_button.rect.collidepoint(pygame.mouse.get_pos()):
                create_back_button.pressed = True
            else:
                create_back_button.pressed = False
            if pygame.mouse.get_pressed()[0] and create_button.rect.collidepoint(pygame.mouse.get_pos()):
                create_button.pressed = True
            else:
                create_button.pressed = False

        char_create_button_group.update()
        char_create_button_group.draw(screen)
        for i in char_create_button_group:
            i.draw_text()
        text_box.update(events)
        text_box.draw(screen)
        console.draw(screen)
        screen.blit(portrait_image, (405, 338))
        pygame.display.flip()
        clock.tick(64)

def load(load_from):
    with open(load_from, "rb") as save:
        load_to = pickle.load(save)
        return load_to
    save.close()

def save(save_from, save_to):
    with open(save_to, "wb") as save:
        pickle.dump(save_from, save, pickle.HIGHEST_PROTOCOL)
    save.close()

def char_buttons(characters):
    global first_player_selected
    global second_player_selected
    first_player_selected = False
    second_player_selected = False
    m = 0
    for i in characters:
        char_button_group.add(Button(500,(m * 175 + 115), button_path, i.name_string, i, i.mini_portrait_path ))
        m += 1

def main_game_buttons():
    global button_start
    global button_delete_char
    global button_create_char
    global button_quit
    global button_options
    global button_load

    button_start = Button(100, 36, button_path, "Start")
    button_create_char = Button(100, 136, button_path, "Create character")
    button_delete_char = Button(100, 236, button_path, "Delete character")
    button_options = Button(100, 336, button_path, "Options" )
    button_load = Button(100, 436, button_path, "Load")
    button_quit = Button(100, 536, button_path, "Quit")

    main_button_group.add(button_start)
    main_button_group.add(button_delete_char)
    main_button_group.add(button_create_char)
    main_button_group.add(button_quit)
    main_button_group.add(button_options)
    main_button_group.add(button_load)

def multiplayer_mode_buttons():
    global hot_seat_button
    global lan_button
    global online_button
    global multiplayer_back_button

    hot_seat_button = Button(307, 100, button_path, "Hot seat")
    lan_button = Button(307, 200, button_path, "LAN")
    online_button = Button(307, 300, button_path, "Online")
    multiplayer_back_button = Button(307, 400, button_path, "Back")

    multiplayer_button_group.add(hot_seat_button)
    multiplayer_button_group.add(lan_button)
    multiplayer_button_group.add(online_button)
    multiplayer_button_group.add(multiplayer_back_button)

def map_buttons():
    m = 0
    for i in maps:
        map_button_group.add(Button(307,(100 + 100*m), button_path, i.name, i ))
        m+=1

def mode_buttons():
    global button_singleplayer
    global button_multiplayer
    global button_back

    button_singleplayer = Button(307, 100, button_path, "Single Player")
    button_multiplayer = Button(307, 220, button_path, "Multiplayer")
    button_back = Button(307, 360, button_path, "Back")

    mode_button_group.add(button_singleplayer)
    mode_button_group.add(button_multiplayer)
    mode_button_group.add(button_back)

def smplayer_buttons():
    global smstart_button
    global smback_button

    smstart_button = Button(100, 560, button_path, "Start Game")
    smback_button = Button(514, 560, button_path, "Back")

    smplayer_button_group.add(smstart_button)
    smplayer_button_group.add(smback_button)

def char_creation_buttons():
    global faction_button
    global faction_left_button
    global faction_right_button
    global portrait_left_button
    global portrait_right_button
    global create_button
    global create_back_button

    faction_button = Button(307, 200, button_path)
    faction_left_button = Button(217, 212, arrow_left_path)
    faction_right_button = Button(607, 212, arrow_right_path)
    portrait_left_button = Button(217, 350, arrow_left_path)
    portrait_right_button = Button(607, 350, arrow_right_path)
    create_button = Button(100, 560, button_path, "Create")
    create_back_button = Button(514, 560, button_path, "Back")

    char_create_button_group.add(faction_button)
    char_create_button_group.add(faction_left_button)
    char_create_button_group.add(faction_right_button)
    char_create_button_group.add(portrait_left_button)
    char_create_button_group.add(portrait_right_button)
    char_create_button_group.add(create_button)
    char_create_button_group.add(create_back_button)

console = Console()

characters = load("chars/chars")
for i in characters:
    i.from_string()
character_list_length = len(characters)
maps = load("maps/maps")
for i in maps:
    i.from_string()

game_map = Map(18,18,"", ((0,0),(0,0)))
first_player_sprite = Character("","Inferno","", "")
second_player_sprite = Character("","Inferno","", "")

char_buttons(characters)
main_game_buttons()
char_creation_buttons()
mode_buttons()
map_buttons()
smplayer_buttons()
multiplayer_mode_buttons()

pygame.key.set_repeat(10, 10)
while in_main_game:
    screen.blit(main_image, (0, 0))
    deleted_chars = 0
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and button_start.rect.collidepoint(pygame.mouse.get_pos()):
            for i in char_button_group:
                if i.p_no == 1:
                   first_player_sprite = i.obj
                elif i.p_no == 2:
                   second_player_sprite = i.obj
            if first_player_selected:
                in_mode_selection = True
                characters_group = pygame.sprite.Group(first_player_sprite)
                console.print_text("Choosing game mode")
            else:
                console.print_text("Character not selected")

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and button_delete_char.rect.collidepoint(pygame.mouse.get_pos()):
            for i in char_button_group:
                if i.pressed:
                    if i.obj in characters:
                        characters.remove(i.obj)
                        console.print_text("Character deleted: " + i.obj.name_string)
                        character_list_length = len(characters)
                        deleted_chars += 1
            if deleted_chars == 0:
                console.print_text("Can't delete character: character not selected")
            char_button_group.empty()
            char_buttons(characters)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and button_create_char.rect.collidepoint(pygame.mouse.get_pos()):
            if character_list_length >= 3:
                console.print_text("Maximum characters allowed: 3")
            else:
                in_char_create = True
                console.print_text("Creating Character")

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and button_options.rect.collidepoint(pygame.mouse.get_pos()):
            console.print_text("Options: not ready yet")

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and button_load.rect.collidepoint(pygame.mouse.get_pos()):
            console.print_text("Load: not ready yet")

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and button_quit.rect.collidepoint(pygame.mouse.get_pos()):
            exit()

        for i in char_button_group:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and i.rect.collidepoint(pygame.mouse.get_pos()):
                if i.pressed:
                    i.pressed = False
                    if i.p_no == 1:
                        i.set_player_no(0)
                        first_player_selected = False
                    elif i.p_no == 2:
                        i.set_player_no(0)
                        second_player_selected = False
                else:
                    if not first_player_selected: 
                        i.pressed = True
                        first_player_selected = True
                        i.set_player_no(1)
                    elif not second_player_selected:
                        i.pressed = True
                        second_player_selected = True
                        i.set_player_no(2)



        if event.type == pygame.QUIT or keys[K_q]:
            exit()
        if pygame.mouse.get_pressed()[0] and button_start.rect.collidepoint(pygame.mouse.get_pos()):
            button_start.pressed = True
        else:
            button_start.pressed = False
        if pygame.mouse.get_pressed()[0] and button_delete_char.rect.collidepoint(pygame.mouse.get_pos()):
            button_delete_char.pressed = True
        else:
            button_delete_char.pressed = False
        if pygame.mouse.get_pressed()[0] and button_create_char.rect.collidepoint(pygame.mouse.get_pos()):
            button_create_char.pressed = True
        else:
            button_create_char.pressed = False
        if pygame.mouse.get_pressed()[0] and button_options.rect.collidepoint(pygame.mouse.get_pos()):
            button_options.pressed = True
        else:
            button_options.pressed = False
        if pygame.mouse.get_pressed()[0] and button_load.rect.collidepoint(pygame.mouse.get_pos()):
            button_load.pressed = True
        else:
            button_load.pressed = False
        if pygame.mouse.get_pressed()[0] and button_quit.rect.collidepoint(pygame.mouse.get_pos()):
            button_quit.pressed = True
        else:
            button_quit.pressed = False

    main_button_group.update()
    char_button_group.update()
    main_button_group.draw(screen)
    char_button_group.draw(screen)
    for i in main_button_group:
        i.draw_text()
    for i in char_button_group:
        i.draw_text()
        i.draw_image()
    console.draw(screen)
    pygame.display.flip()
    clock.tick(64)
    if in_mode_selection:
        mode_screen()
    elif in_char_create:
        create_char()
