import os
import sys
import random
import pygame
from pygame import display
from pygame import mixer
from pygame import Rect
from pygame import Surface
from pygame import time
from pygame import transform
from pygame.locals import RESIZABLE, RLEACCEL

mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
display.set_caption("RunningPVP-T-rex by_Let`sGitIt")
gamer_name = ''
scr_size = (width, height) = (800, 400)
# 최소 화면 설정
pvp_scr_size = (pvp_width, pvp_height) = (1200, 400)
FPS = 60
gravity = 0.65

background_col = (235, 235, 235)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 200, 0)
orange = (255, 127, 0)
blue = (0, 0, 225)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
bright_orange = (255, 215, 0)
red = (255, 18, 18)
dark_red = (237, 0, 0)
deep_red = (201, 0, 0)
dark_blue = (10, 112, 138)
dark_pink = (147, 0, 0)


large_font = pygame.font.Font('DungGeunMo.ttf', 75)
font = pygame.font.Font('DungGeunMo.ttf', 32)
small_font = pygame.font.Font('DungGeunMo.ttf', 25)
xsmall_font = pygame.font.Font('DungGeunMo.ttf', 15)
full_screen = False
monitor_size = (monitor_width, monitor_height) = (display.Info().current_w,
                                                  display.Info().current_h)
high_score = 0
hard_high_score = 0
easy_high_score = 0


# scr_size_pvp = (width, height) = (1200, 400)
# resized_screen_pvp = display.set_mode((scr_size_pvp), RESIZABLE)
# screen_pvp = resized_screen.copy()
# resized_screen_pvp_center = (0, 0)

resized_screen = display.set_mode((scr_size), RESIZABLE)
screen = resized_screen.copy()

resized_screen_center = (0, 0)
r_width = resized_screen.get_width()
r_height = resized_screen.get_height()
button_offset = 0.2
select_offset = 0.15
width_offset = 0.3
clock = time.Clock()
on_pushtime = 0
off_pushtime = 0

dino_size = [44, 47]
object_size = [40, 40]
ptera_size = [46, 40]

pvp_dino_size = [35,47]
pvp_object_size = [30,40]
pvp_ptera_size = [40, 40]

collision_immune_time = 500
shield_time = 2000
speed_up_limit = 700
global bgm_on
bgm_on = True
jump_sound = mixer.Sound('sprites/jump.wav')
die_sound = mixer.Sound('sprites/die.wav')
# check_point_sound = mixer.Sound('sprites/checkPoint.wav')
sound_vol = 0.3
# HERE: REMOVE SOUND!!
pygame.mixer.music.load('sprites/t-rex_bgm1.mp3')
pygame.mixer.music.set_volume(sound_vol)


# 게임 내에 text를 넣을때 쓰는 함수
def draw_text(text, font, surface, x, y, main_color):
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)


def text_objects(text, font):
    text_surface = font.render(text, True, (black))
    return text_surface, text_surface.get_rect()


# 투명한 이미지 불러오기
def alpha_image(name, sizex=-1, sizey=-1,color_key=None):
    full_name = os.path.join('sprites', name)
    img = pygame.image.load(full_name)
    if color_key is not None:
        if color_key == -1:
            color_key = img.get_at((0, 0))
        img.set_colorkey(color_key, RLEACCEL)
    if sizex != -1 or sizey != -1:
        img = transform.scale(img, (sizex, sizey))
    img.convert_alpha()
    return (img, img.get_rect())

# 게임 내 image를 넣을 때 쓰는 함수
def load_image(name, sizex=-1, sizey=-1, color_key=None):
    full_name = os.path.join('sprites', name)
    img = pygame.image.load(full_name)
    img = img.convert()
    if color_key is not None:
        if color_key == -1:
            color_key = img.get_at((0, 0))
        img.set_colorkey(color_key, RLEACCEL)
    if sizex != -1 or sizey != -1:
        img = transform.scale(img, (sizex, sizey))
    return (img, img.get_rect())


def load_sprite_sheet(sheet_name, nx, ny,
                      scalex=-1, scaley=-1, color_key=None):
    full_name = os.path.join('sprites', sheet_name)
    sheet = pygame.image.load(full_name)
    sheet = sheet.convert()
    sheet_rect = sheet.get_rect()
    sprites = []
    sizex = sheet_rect.width / nx
    sizey = sheet_rect.height / ny
    for i in range(0, ny):
        for j in range(0, nx):
            rect = Rect((j * sizex, i * sizey, sizex, sizey))
            # Rect((left, top), (width, height)) -> Rect
            img = Surface(rect.size)
            img = img.convert()
            img.blit(sheet, (0, 0), rect)
            if color_key is not None:
                if color_key == -1:
                    color_key = img.get_at((0, 0))
                img.set_colorkey(color_key, RLEACCEL)
            if scalex != -1 or scaley != -1:
                img = transform.scale(img, (scalex, scaley))
            sprites.append(img)
    sprite_rect = sprites[0].get_rect()
    return sprites, sprite_rect


def disp_gameover_msg(gameover_img):
    gameover_rect = gameover_img.get_rect()
    gameover_rect.centerx = width / 2
    gameover_rect.centery = height * 0.35
    screen.blit(gameover_img, gameover_rect)


def disp_store_buttons(btn_exit, btn_back):
    btn_exit_rect = btn_exit.get_rect()
    btn_back_rect = btn_back.get_rect()
    btn_exit_rect.centerx = width * (0.5)
    btn_back_rect =  (width * 0.025, height * 0.025)
    btn_exit_rect.centery = height * 0.5
    screen.blit(btn_exit, btn_exit_rect)
    screen.blit(btn_back, btn_back_rect)


def disp_gameover_buttons(btn_restart, btn_save, btn_exit):
    btn_restart_rect = btn_restart.get_rect()
    btn_save_rect = btn_save.get_rect()
    btn_exit_rect = btn_exit.get_rect()
    btn_restart_rect.centerx = width * 0.25
    btn_save_rect.centerx = width * 0.5
    btn_exit_rect.centerx = width * 0.75
    btn_restart_rect.centery = height * 0.6
    btn_save_rect.centery = height * 0.6
    btn_exit_rect.centery = height * 0.6
    screen.blit(btn_restart, btn_restart_rect)
    screen.blit(btn_save, btn_save_rect)
    screen.blit(btn_exit, btn_exit_rect)


def disp_pvp_gameover_buttons(btn_restart, btn_exit):
    btn_restart_rect = btn_restart.get_rect()
    btn_exit_rect = btn_exit.get_rect()
    btn_restart_rect.centerx = width * 0.35
    btn_exit_rect.centerx = width * 0.65
    btn_restart_rect.centery = height * 0.5
    btn_exit_rect.centery = height * 0.5
    screen.blit(btn_restart, btn_restart_rect)
    screen.blit(btn_exit, btn_exit_rect)


def disp_pvp_winner_loser(player1):
    win = large_font.render("WIN", True, black)
    lose = large_font.render("LOSE", True, black)
    if not player1.is_dead:
        win_width = width * 0.17
        lose_width = width * 0.70
    else:
        win_width = width * 0.70
        lose_width = width * 0.17

    screen.blit(win, (win_width, height * 0.15))
    screen.blit(lose, (lose_width, height * 0.15))

def disp_pvp_r_winner_loser(player1):
    win = large_font.render("WIN", True, black)
    lose = large_font.render("LOSE", True, black)
    if not player1.is_dead:
        win_height = height * 0.6
        lose_height = height * 0.1
    else:
        win_height = height * 0.1
        lose_height = height * 0.6

    screen.blit( win, ((width * 0.43) , win_height ))
    screen.blit( lose, ((width * 0.415) , lose_height ))


def disp_intro_buttons(btn_gamestart, btn_board, btn_store, btn_option):
    # btn_1p_rect = btn_1p.get_rect()
    btn_gamestart_rect = btn_gamestart.get_rect()
    btn_board_rect = btn_board.get_rect()
    btn_store_rect = btn_store.get_rect()
    btn_option_rect = btn_option.get_rect()
    # btn_1p_rect.centerx = width * 0.8
    btn_gamestart_rect.centerx = width * 0.8
    btn_board_rect.centerx = width * 0.8
    btn_store_rect.centerx = width * 0.8
    btn_option_rect.centerx = width * 0.8
    # btn_1p_rect.centery = height * 0.25
    btn_gamestart_rect.centery = height * 0.35
    btn_board_rect.centery = height * (0.35 + 0.75 * button_offset)
    btn_store_rect.centery = height * (0.35 + 1.5 * button_offset)
    btn_option_rect.centery = height * (0.35 + 2.25 * button_offset)
    # screen.blit(btn_1p, btn_1p_rect)
    screen.blit(btn_gamestart, btn_gamestart_rect)
    screen.blit(btn_board, btn_board_rect)
    screen.blit(btn_store, btn_store_rect)
    screen.blit(btn_option, btn_option_rect)


def disp_select_buttons(btn_easy, btn_hard, btn_store, btn_set, btn_back):
    btn_easy_rect = btn_easy.get_rect()
    btn_hard_rect = btn_hard.get_rect()
    btn_store_rect = btn_store.get_rect()
    btn_set_rect = btn_set.get_rect()
    btn_back_rect = btn_back.get_rect()

    btn_easy_rect.centerx = width * 0.5
    btn_hard_rect.centerx = width * 0.5
    btn_store_rect.centerx = width * 0.5
    btn_set_rect.centerx = width * 0.5
    btn_back_rect.centerx = width * 0.1

    btn_easy_rect.centery = height * 0.26
    btn_hard_rect.centery = height * (0.26 + select_offset)
    btn_store_rect.centery = height * (0.26 + 2 * select_offset)
    btn_set_rect.centery = height * (0.26 + 3 * select_offset)
    btn_back_rect.centery = height * 0.1
    screen.blit(btn_easy, btn_easy_rect)
    screen.blit(btn_hard, btn_hard_rect)
    screen.blit(btn_store, btn_store_rect)
    screen.blit(btn_set, btn_set_rect)
    screen.blit(btn_back, btn_back_rect)


def check_scr_size(eventw, eventh):
    if (eventw < width and eventh < height) or (eventw < width) or (eventh < height):
        # 최소해상도
        resized_screen = display.set_mode((scr_size), RESIZABLE)
    else:
        if (eventw / eventh) != (width / height):
            # 고정화면비
            adjusted_height = int(eventw / (width / height))
            resized_screen = display.set_mode((eventw, adjusted_height), RESIZABLE)

def pvp_check_scr_size(eventw, eventh):
    if (eventw < pvp_width and eventh < pvp_height) or (eventw < pvp_width) or (eventh < pvp_height):
        # 최소해상도
        resized_screen = display.set_mode((pvp_scr_size), RESIZABLE)
    else:
        if (eventw / eventh) != (width / height):
            adjusted_height = int(eventw / (pvp_width/pvp_height))
            resized_screen = display.set_mode((eventw, adjusted_height), RESIZABLE)

def full_screen_issue():
    global scr_size
    resized_screen = display.set_mode((scr_size), RESIZABLE)
    resized_screen = display.set_mode((scr_size), RESIZABLE)


def extract_digits(number):
    if number > -1:
        digits = []
        i = 0
        while ((number / 10) != 0):
            digits.append(number % 10)
            number = int(number / 10)
        digits.append(number % 10)
        for i in range(len(digits), 5):
            digits.append(0)
        digits.reverse()
        return digits


def resize(name, w, h, color):
    global width, height, resized_screen
    print("resized_screen: (", resized_screen.get_width(),
          ",", resized_screen.get_height(), ")")
    return (name, w * resized_screen.get_width() // width,
            h * resized_screen.get_height() // height, color)


def text_size(size):
    font = pygame.font.Font('DungGeunMo.ttf', size)
    return font


def score_board(btn_back):
    btn_back_rect = btn_back.get_rect()
    btn_back_rect.centerx = width * 0.1
    btn_back_rect.centery = height * 0.1
    screen.blit(btn_back, btn_back_rect)
