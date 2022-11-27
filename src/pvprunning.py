from pygame.image import load
from src.dino import *
from src.obstacle import *
from src.item import *
from src.interface import *
from db.db_interface import InterfDB
import src.setting as setting
import src.game
from src.game_value import *
from time import sleep
import threading
import time

db = InterfDB("db/data.db")

def pvprunning():
    global game_over
    global paused
    global resized_screen
    global cacti
    global fire_cacti
    global pteras
    global stones
    global last_obstacle

    global cacti2
    global fire_cacti2
    global pteras2
    global stones2
    global last_obstacle2
    global dust_item
    global is_dust_time
    global is_dust_time_2p
    global is_water_time
    global is_water_time_2p

    cacti = pygame.sprite.Group()
    fire_cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    stones = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()
    # 아이템 추가 11/08
    mask_items = pygame.sprite.Group()
    dust_items = pygame.sprite.Group()

    cacti2 = pygame.sprite.Group()
    fire_cacti2 = pygame.sprite.Group()
    pteras2 = pygame.sprite.Group()
    stones2 = pygame.sprite.Group()
    last_obstacle2 = pygame.sprite.Group()
    # 아이템 추가 11/08
    Cactus.containers = cacti
    fire_Cactus.containers = fire_cacti
    Ptera.containers = pteras
    Stone.containers = stones # add stone containers
    Mask_item.containers = mask_items
    Dust_item.containers = dust_items

    Cactus_pvp_running.containers = cacti2
    fire_Cactus_pvp_running.containers = fire_cacti2
    Ptera_pvp_running.containers = pteras2
    Stone_pvp_running.containers = stones2 # add stone containers

    start_menu = False
    game_over = False
    game_quit = False
    # HERE: REMOVE SOUND!!
    if setting.bgm_on:
        pygame.mixer.music.play(-1)  # 배경음악 실행

    #

    player1_dino = Dino(dino_size[0], dino_size[1], type='original' )
    player2_dino = Dino(dino_size[0], dino_size[1], type='PURPLE', loc=-2)

    # 플레이어1과 플레이어 2의 목숨 수
    heart_1p = HeartIndicator(player1_dino, loc=1)
    heart_2p = HeartIndicator(player2_dino)
    background = ImgBack(RUN_GAME_SPEED, "spring", type=1)
    background_2p = ImgBack(RUN_GAME_SPEED, "spring",type=2)
    new_ground = Ground(-1 * RUN_GAME_SPEED)
    new_ground_2p = Ground(-1 * RUN_GAME_SPEED, DEFAULT_HEIGHT_2P)
    # alpha_back, alpha_back_rect = alpha_image('alpha_back2.png', width + 20, height)
    # alpha_back_rect.left = -20    
    speed_indicator = Scoreboard(width * 0.12, height * 0.15)
    counter = 0
    
    # 게임 중  pause 상태
    paused = False
    
    # 게임 종료 후 노출 문구
    game_over_image, game_over_rect = load_image('game_over.png', 380, 100, -1)
    
    # 게임 후 버튼
    r_btn_restart, r_btn_restart_rect = load_image(*resize('btn_restart.png', 150, 80, -1))
    btn_restart, btn_restart_rect = load_image('btn_restart.png', 150, 80, -1)
    r_btn_exit, r_btn_exit_rect = load_image(*resize('btn_exit.png', 150, 80, -1))
    btn_exit, btn_exit_rect = load_image('btn_exit.png', 150, 80, -1)

    # 방향키 구현
    go_left_1p = False
    go_right_1p = False
    go_left_2p = False
    go_right_2p = False

    # 이단 점프
    jumpingx2_1p = False
    jumpingx2_2p = False

    # 미사일 발사.
    space_go_1p = False
    m_list_1p = []
    bk_1p = 0

    # 익룡이 격추되었을때
    isDown1=False
    boomCount=0
    isDown2=False
    boomCount=0

    # 황사 변수설정
    is_dust_time= False
    is_dust_time_2p = False
    dust=DustImg()
    dust_2p = DustImg_2p()
    global dust_rest_time
    global dust_rest_time_2p
    dust_rest_time = 0
    dust_rest_time_2p = 0
    dust_appear()
    dust_appear_2p()

    # 산성비 변수설정
    is_water_time = False
    is_water_time_2p = False
    pm_list = []
    pm_list_2p = []
    # water = DustImg()
    # water_2p = DustImg_2p()
    global water_rest_time
    global water_rest_time_2p
    water_rest_time = 0
    water_rest_time_2p = 0
    water_appear()
    water_appear_2p()


    space_go_2p = False
    m_list_2p = []
    bk_2p = 0

    global mask_rest_time
    mask_rest_time = ITEM_TIME

    while not game_quit:
        while start_menu:
            pass
        while not game_over:
            if pygame.display.get_surface() is None:
                print("Couldn't load display surface")
                game_quit = True
                game_over = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_quit = True
                        game_over = True

                    if event.type == pygame.KEYDOWN:
                        # 1p dino
                        if event.key == pygame.K_w:
                            # 스페이스 누르는 시점에 공룡이 땅에 닿아있으면 점프한다.
                            if player1_dino.rect.bottom == int(DEFAULT_HEIGHT * height):
                                player1_dino.is_jumping = True
                                if pygame.mixer.get_init() is not None:
                                    jump_sound.play()
                                player1_dino.movement[1] = -1 * player1_dino.jump_speed_running

                        if event.key == pygame.K_s:
                            # 아래방향키를 누르는 시점에 공룡이 점프중이지 않으면 숙인다.
                            if not (player1_dino.is_jumping and player1_dino.is_dead):
                                player1_dino.is_ducking = True
                        if event.key == pygame.K_a:
                            go_left_1p = True
                        if event.key == pygame.K_d:
                            go_right_1p = True
                        if event.key == pygame.K_LCTRL:
                            space_go_1p = True
                            bk_1p = 0
                        if event.key == pygame.K_TAB:
                            jumpingx2_1p = True

                        # 2p dino        
                        if event.key == pygame.K_UP:
                            # 스페이스 누르는 시점에 공룡이 땅에 닿아있으면 점프한다.
                            if player2_dino.rect.bottom == int(DEFAULT_HEIGHT_2P * height):
                                player2_dino.is_jumping = True
                                if pygame.mixer.get_init() is not None:
                                    jump_sound.play()
                                player2_dino.movement[1] = -1 * player2_dino.jump_speed_running
                        if event.key == pygame.K_DOWN:
                            # 아래방향키를 누르는 시점에 공룡이 점프중이지 않으면 숙인다.
                            if not (player2_dino.is_jumping and player2_dino.is_dead):
                                player2_dino.is_ducking = True
                        if event.key == pygame.K_LEFT:
                            # print("left")
                            go_left_2p = True
                        if event.key == pygame.K_RIGHT:
                            # print("right")
                            go_right_2p = True
                        if event.key == pygame.K_p:
                            space_go_2p = True
                            bk_2p = 0
                        if event.key == pygame.K_o:
                            jumpingx2_2p = True
                        if event.key == pygame.K_ESCAPE:
                            paused = not paused
                            paused = src.game.pausing()

                    if event.type == pygame.KEYUP:
                        # 1p dino
                        if event.key == pygame.K_s:
                            player1_dino.is_ducking = False
                        if event.key == pygame.K_a:
                            go_left_1p = False
                        if event.key == pygame.K_d:
                            go_right_1p = False
                        if event.key == pygame.K_LCTRL:
                            space_go_1p = False
                        if event.key == pygame.K_TAB:
                            jumpingx2_1p = False
                        # 2p dino
                        if event.key == pygame.K_DOWN:
                            player2_dino.is_ducking = False
                        if event.key == pygame.K_LEFT:
                            go_left_2p = False
                        if event.key == pygame.K_RIGHT:
                            go_right_2p = False
                        if event.key == pygame.K_p:
                            space_go_2p = False
                        if event.key == pygame.K_o:
                            jumpingx2_2p = False
                    if event.type == pygame.VIDEORESIZE:
                        check_scr_size(event.w, event.h)

            if not paused:
                if go_left_1p:
                    if player1_dino.rect.left < 0:
                        player1_dino.rect.left = 0
                    else:
                        player1_dino.rect.left = player1_dino.rect.left - RUN_GAME_SPEED
                if go_right_1p:
                    if player1_dino.rect.right > width :
                        player1_dino.rect.right = width 
                    else:
                        player1_dino.rect.left = player1_dino.rect.left + RUN_GAME_SPEED
                if space_go_1p and (int(bk_1p % MISSILE) == 0):
                    # print(bk)
                    missile_1p = Obj()

                    # 디노의 종류에 따라 다른 총알이 나가도록 합니다.
                    if player1_dino.type == 'RED':
                        missile_1p.put_img("./sprites/black_bullet.png")
                        missile_1p.change_size(10, 10)
                    elif player1_dino.type == 'YELLOW':
                        missile_1p.put_img("./sprites/blue_bullet.png")
                        missile_1p.change_size(10, 10)
                    elif player1_dino.type == 'PURPLE':
                        missile_1p.put_img("./sprites/pink_bullet.png")
                        missile_1p.change_size(15, 5)
                    else:
                        missile_1p.put_img("./sprites/red_bullet.png")
                        missile_1p.change_size(10, 10)
                    if not player1_dino.is_ducking:
                        missile_1p.x = round(player1_dino.rect.centerx)
                        missile_1p.y = round(player1_dino.rect.top * 1.035)
                    if player1_dino.is_ducking:
                        missile_1p.x = round(player1_dino.rect.centerx)
                        missile_1p.y = round(player1_dino.rect.centery * 1.01)
                    missile_1p.move = MISSILE_SPEED
                    m_list_1p.append(missile_1p)
                    
                bk_1p = bk_1p + 1
                d_list_1p = []
                for i in range(len(m_list_1p)):
                    m = m_list_1p[i]
                    m.x += m.move
                    if m.x > width:
                        d_list_1p.append(i)

                # 1p의 미사일이 2p를 맞추었을 때
                if len(m_list_1p) == 0:
                    pass
                else:
                    for m_1p in m_list_1p:
                        if (m_1p.x >= player2_dino.rect.left) and (m_1p.x <= player2_dino.rect.right) and (
                                m_1p.y > player2_dino.rect.top) and (m_1p.y < player2_dino.rect.bottom):
                            player2_dino.decrease_life()
                            if player2_dino.is_life_zero():
                                player2_dino.is_dead = True
                            m_list_1p.remove(m_1p)
                d_list_1p.reverse()
                for d in d_list_1p:
                    del m_list_1p[d]
                if jumpingx2_1p:
                    if player1_dino.rect.bottom == int(height * DEFAULT_HEIGHT):
                        player1_dino.is_jumping = True
                        player1_dino.movement[1] = -1 * player1_dino.super_jump_speed_running
                if go_left_2p:
                    if player2_dino.rect.left <= 0:
                        player2_dino.rect.left = 0.5
                    else:
                        player2_dino.rect.left = player2_dino.rect.left - RUN_GAME_SPEED
                if go_right_2p:
                    if player2_dino.rect.right > width:
                        player2_dino.rect.right = width
                    else:
                        player2_dino.rect.left = player2_dino.rect.left + RUN_GAME_SPEED
                if space_go_2p and (int(bk_2p % MISSILE) == 0):
                    # print(bk)
                    missile_2p = Obj()
                    # 디노의 종류에 따라 다른 총알이 나가도록 합니다.
                    if player2_dino.type == 'RED':
                        missile_2p.put_img("./sprites/black_bullet.png")
                        missile_2p.change_size(10, 10)
                    elif player2_dino.type == 'YELLOW':
                        missile_2p.put_img("./sprites/blue_bullet.png")
                        missile_2p.change_size(10, 10)
                    elif player2_dino.type == 'PURPLE':
                        missile_2p.put_img("./sprites/pink_bullet.png")
                        missile_2p.change_size(15, 5)
                    else:
                        missile_2p.put_img("./sprites/orange_bullet.png")
                        missile_2p.change_size(10, 10)

                    if not player2_dino.is_ducking:
                        missile_2p.x = round(player2_dino.rect.centerx)
                        missile_2p.y = round(player2_dino.rect.top * 1.035)
                    if player2_dino.is_ducking:
                        missile_2p.x = round(player2_dino.rect.centerx)
                        missile_2p.y = round(player2_dino.rect.centery * 1.01)
                    missile_2p.move = MISSILE_SPEED
                    m_list_2p.append(missile_2p)
                bk_2p = bk_2p + 1
                d_list_2p = []
                for i in range(len(m_list_2p)):
                    m = m_list_2p[i]
                    m.x += m.move
                    if m.x > width:
                        d_list_2p.append(i)
                

                # 2p의 미사일이 1p를 맞추었을 때
                if len(m_list_2p) == 0:
                    pass
                else:
                    for m_2p in m_list_2p:
                        if (m_2p.x >= player1_dino.rect.left) and (m_2p.x <= player1_dino.rect.right) and (
                                m_2p.y > player1_dino.rect.top) and (m_2p.y < player1_dino.rect.bottom):
                            player1_dino.decrease_life()
                            if player1_dino.is_life_zero():
                                player1_dino.is_dead = True
                            m_list_2p.remove(m_2p)
                        if m.x < 0:
                            m_list_2p.remove(m_2p)

                for c in cacti:
                    c.movement[0] = -1 * RUN_GAME_SPEED
                    if not player1_dino.collision_immune:
                        if pygame.sprite.collide_mask(player1_dino, c):
                            player1_dino.collision_immune = True
                            player1_dino.life -= 1
                            collision_time = pygame.time.get_ticks()
                            if player1_dino.life == 0:
                                player1_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not player1_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player1_dino.collision_immune = False

                for f in fire_cacti:
                    f.movement[0] = -1 * RUN_GAME_SPEED
                    if not player1_dino.collision_immune:
                        if pygame.sprite.collide_mask(player1_dino, f):
                            player1_dino.collision_immune = True
                            player1_dino.life -= 1
                            collision_time = pygame.time.get_ticks()
                            if player1_dino.life == 0:
                                player1_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not player1_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player1_dino.collision_immune = False

                for p in pteras:
                    p.movement[0] = -1 * RUN_GAME_SPEED

                    # 7. 익룡이 미사일에 맞으면 익룡과 미사일 모두 사라집니다.

                    if (len(m_list_1p)==0):
                        pass
                    else:
                        if (m_1p.x>=p.rect.left)and(m_1p.x<=p.rect.right)and(m_1p.y>p.rect.top)and(m_1p.y<p.rect.bottom):
                            print("격추 성공")
                            isDown1=True
                            boom=Obj()
                            boom.put_img("./sprites/boom.png")
                            boom.change_size(200,100)
                            boom.x=p.rect.centerx-round(p.rect.width)*2.5
                            boom.y=p.rect.centery-round(p.rect.height)*1.5
                            p.kill()
                            # 여기만 바꿈
                            m_list_1p.remove(m_1p)
                            #
                    #

                    if not player1_dino.collision_immune:
                        if pygame.sprite.collide_mask(player1_dino, p):
                            player1_dino.collision_immune = True
                            player1_dino.life -= 1
                            collision_time = pygame.time.get_ticks()
                            if player1_dino.life == 0:
                                player1_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not player1_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player1_dino.collision_immune = False

                for s in stones:
                    s.movement[0] = -1 * RUN_GAME_SPEED
                    if not player1_dino.collision_immune:
                        if pygame.sprite.collide_mask(player1_dino, s):
                            player1_dino.collision_immune = True
                            player1_dino.life -= 1
                            collision_time = pygame.time.get_ticks()
                            if player1_dino.life == 0:
                                player1_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                # 2p 장애물
                for c in cacti2:
                    c.movement[0] = -1 * RUN_GAME_SPEED
                    if not player2_dino.collision_immune:
                        if pygame.sprite.collide_mask(player2_dino, c):
                            player2_dino.collision_immune = True
                            player2_dino.life -= 1
                            collision_time = pygame.time.get_ticks()
                            if player2_dino.life == 0:
                                player2_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not player2_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player2_dino.collision_immune = False

                for f in fire_cacti2:
                    f.movement[0] = -1 * RUN_GAME_SPEED
                    if not player2_dino.collision_immune:
                        if pygame.sprite.collide_mask(player2_dino, f):
                            player2_dino.collision_immune = True
                            player2_dino.life -= 1
                            collision_time = pygame.time.get_ticks()
                            if player2_dino.life == 0:
                                player2_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not player2_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player2_dino.collision_immune = False

                for p in pteras2:
                    p.movement[0] = -1 * RUN_GAME_SPEED

                    # 7. 익룡이 미사일에 맞으면 익룡과 미사일 모두 사라집니다.

                    if (len(m_list_2p)==0):
                        pass
                    else:
                        if (m_2p.x>=p.rect.left)and(m_2p.x<=p.rect.right)and(m_2p.y>p.rect.top)and(m_2p.y<p.rect.bottom):
                            print("격추 성공")
                            isDown2=True
                            boom = Obj()
                            boom.put_img("./sprites/boom.png")
                            boom.change_size(200,100)
                            boom.x=p.rect.centerx-round(p.rect.width)*2.5
                            boom.y=p.rect.centery-round(p.rect.height)*1.5
                            p.kill()
                            # 여기만 바꿈
                            m_list_2p.remove(m_2p)

                    if not player2_dino.collision_immune:
                        if pygame.sprite.collide_mask(player2_dino, p):
                            player2_dino.collision_immune = True
                            player2_dino.life -= 1
                            collision_time = pygame.time.get_ticks()
                            if player2_dino.life == 0:
                                player2_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not player2_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player2_dino.collision_immune = False

                for s in stones2:
                    s.movement[0] = -1 * RUN_GAME_SPEED
                    if not player2_dino.collision_immune:
                        if pygame.sprite.collide_mask(player2_dino, s):
                            player2_dino.collision_immune = True
                            player2_dino.life -= 1
                            collision_time = pygame.time.get_ticks()
                            if player2_dino.life == 0:
                                player2_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                for m in mask_items:
                    m.movement[0] = -1 * RUN_GAME_SPEED
                    if not player2_dino.collision_immune:
                        if pygame.sprite.collide_mask(player2_dino, m):
                            player2_dino.collision_immune = True
                            background.update(background.name,1)
                            background_2p.update('winter',2)
                            collision_time = pygame.time.get_ticks()
                            player2_dino.score2 = 0
                            m.image.set_alpha(0)
                            is_water_time = True
                            water_rest_time = ITEM_TIME
                            water_appear()
                            

                    if not player1_dino.collision_immune:
                        if pygame.sprite.collide_mask(player1_dino, m):
                            player1_dino.collision_immune = True
                            background.update('winter',1)
                            background_2p.update(background_2p.name,2)                         
                            collision_time = pygame.time.get_ticks()
                            player2_dino.score2 = 0
                            m.image.set_alpha(0)
                            is_water_time_2p = True
                            water_rest_time_2p = ITEM_TIME
                            water_appear_2p()

                    
                for d in dust_items:
                    d.movement[0] = -1 * RUN_GAME_SPEED
                    if not player2_dino.collision_immune:
                        if pygame.sprite.collide_mask(player2_dino, d):
                            player2_dino.collision_immune = True
                            collision_time = pygame.time.get_ticks()
                            player2_dino.score2 = 0
                            d.image.set_alpha(0)
                            #황사
                            is_dust_time_2p = True
                            dust_rest_time_2p = ITEM_TIME
                            dust_appear_2p()
                            
                    if not player1_dino.collision_immune:
                        if pygame.sprite.collide_mask(player1_dino, d):
                            player1_dino.collision_immune = True                      
                            collision_time = pygame.time.get_ticks()
                            player2_dino.score2 = 0
                            d.image.set_alpha(0)
                            #황사
                            is_dust_time = True
                            dust_rest_time = ITEM_TIME
                            dust_appear()
                            
                d_list_2p.reverse()
                for d in d_list_2p:
                    del m_list_2p[d]
                if jumpingx2_2p:
                    if player2_dino.rect.bottom == int(height * DEFAULT_HEIGHT_2P):
                        player2_dino.is_jumping = True
                        player2_dino.movement[1] = -1 * player2_dino.super_jump_speed_running

                player1_dino.update('pvp')
                player2_dino.update('pvp')
                cacti.update()
                fire_cacti.update()
                pteras.update()
                stones.update()

                cacti2.update()
                fire_cacti2.update()
                pteras2.update()
                stones2.update()                
                new_ground.update()
                new_ground_2p.update()
                speed_indicator.update(RUN_GAME_SPEED)
                heart_1p.update(player1_dino.life)
                heart_2p.update(player2_dino.life)
                mask_items.update()
                dust_items.update()

                if pygame.display.get_surface() is not None:
                    screen.fill(background_col)
                    background.draw()
                    background_2p.draw()
                    new_ground.draw()
                    new_ground_2p.draw()
                    # screen.blit(alpha_back, alpha_back_rect)
                    # pygame.draw.line(screen, black, [width/2,0],[width/2,height],3)
                    heart_1p.draw()
                    heart_2p.draw()

                    for m in m_list_1p:
                        m.show()

                    for m in m_list_2p:
                        m.show()
                cacti.draw(screen)
                pteras.draw(screen)
                stones.draw(screen)
                fire_cacti.draw(screen)
                
                cacti2.draw(screen)
                pteras2.draw(screen)
                stones2.draw(screen)
                fire_cacti2.draw(screen)

                if is_dust_time:
                    dust.draw()

                if dust_rest_time == 0 :
                    is_dust_time = False
                    dust.kill()
                    dust_rest_time = ITEM_TIME

                if is_dust_time_2p:
                    dust_2p.draw()

                if dust_rest_time_2p == 0 :
                    is_dust_time_2p = False
                    dust_2p.kill()
                    dust_rest_time_2p = ITEM_TIME

                for pm in pm_list:
                    pm.show()
                
                if is_water_time:
                    pm = Obj()
                    pm.put_img("./sprites/water_drop.png")
                    pm.change_size(40,40)
                    pm.x = random.randrange(40, 800-40)
                    pm.y = 210
                    pm.move = 3
                    if len(pm_list) <= 5:
                        pm_list.append(pm) 
                    pd_list = []
                    for i in range(len(pm_list)):
                        pm = pm_list[i]
                        pm.y += pm.move
                        if pm.y > height or pm.x < 0:
                            pd_list.append(i)
                    pd_list.reverse()
                    for d in pd_list:
                        del pm_list[d]

                if is_water_time_2p:
                    pm_2p = Obj()
                    pm_2p.put_img("./sprites/water_drop.png")
                    pm_2p.change_size(40,40)
                    pm_2p.x = random.randrange(40, 800-40)
                    pm_2p.y = 10
                    pm_2p.move = 3
                    if len(pm_list_2p) <= 5:
                        pm_list_2p.append(pm_2p)
                    pd_list_2p = []

                    for i in range(len(pm_list_2p)):
                        pm_2p = pm_list_2p[i]
                        pm_2p.y += pm_2p.move
                        if pm_2p.y > (height * DEFAULT_HEIGHT_2P) or pm_2p.x < 0:
                            pd_list_2p.append(i)

                    pd_list_2p.reverse()
                    for d in pd_list_2p:
                        del pm_list_2p[d]
                    

                if water_rest_time == 0 :
                    is_water_time = False
                    pm_list = []
                    water_rest_time = ITEM_TIME

                for pm_2p in pm_list_2p:
                    pm_2p.show()

                if water_rest_time_2p == 0 :
                    is_water_time_2p = False
                    pm_list_2p = []
                    water_rest_time_2p = ITEM_TIME


                player1_dino.draw()
                player2_dino.draw()

                mask_items.draw(screen)
                dust_items.draw(screen)

                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                    resized_screen_center)
                pygame.display.update()
                clock.tick(FPS)

                if len(cacti) < 2:
                    if len(cacti) == 0:
                        last_obstacle.empty()
                        last_obstacle.add(Cactus(RUN_GAME_SPEED, object_size[0], object_size[1]))
                    else:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(Cactus(RUN_GAME_SPEED, object_size[0], object_size[1]))

                if len(fire_cacti) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL * 5) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(fire_Cactus(RUN_GAME_SPEED, object_size[0], object_size[1]))

                if len(stones) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(STONE_INTERVAL * 3) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(Stone(RUN_GAME_SPEED, object_size[0], object_size[1]))

                if len(pteras) == 0 and random.randrange(PTERA_INTERVAL) == MAGIC_NUM and counter > PTERA_INTERVAL:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE:
                            last_obstacle.empty()
                            last_obstacle.add(Ptera(RUN_GAME_SPEED, ptera_size[0], ptera_size[1]))

                if len(cacti2) < 2:
                    if len(cacti2) == 0:
                        last_obstacle.empty()
                        last_obstacle.add(Cactus_pvp_running(RUN_GAME_SPEED, object_size[0], object_size[1]))
                    else:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(Cactus_pvp_running(RUN_GAME_SPEED, object_size[0], object_size[1]))

                if len(fire_cacti2) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL * 5) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(fire_Cactus_pvp_running(RUN_GAME_SPEED, object_size[0], object_size[1]))

                if len(stones2) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(STONE_INTERVAL * 3) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(Stone_pvp_running(RUN_GAME_SPEED, object_size[0], object_size[1]))

                if len(pteras2) == 0 and random.randrange(PTERA_INTERVAL) == MAGIC_NUM and counter > PTERA_INTERVAL:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE:
                            last_obstacle.empty()
                            last_obstacle.add(Ptera_pvp_running(RUN_GAME_SPEED, ptera_size[0], ptera_size[1]))

                    resized_screen.blit(
                        pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                        resized_screen_center)
                    pygame.display.update()
                if len(mask_items) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(MASK_INTERVAL) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(Mask_item(RUN_GAME_SPEED, object_size[0], object_size[1],type=1))
                            last_obstacle.add(Mask_item(RUN_GAME_SPEED, object_size[0], object_size[1],type=2))


                if len(dust_items) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(DUST_INTERVAL) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(Dust_item(RUN_GAME_SPEED, object_size[0], object_size[1],type=1))
                            last_obstacle.add(Dust_item(RUN_GAME_SPEED, object_size[0], object_size[1],type=2))
                
                if (len(pm_list)== 0):
                    pass
                else:
                    for pm in pm_list:
                        if (pm.x >= player1_dino.rect.left) and (pm.x <= player1_dino.rect.right) and (pm.y > player1_dino.rect.top) and (pm.y < player1_dino.rect.bottom):
                            print("1p가 공격에 맞음.")
                            # if pygame.sprite.collide_mask(player_dino, pm):
                            player1_dino.collision_immune = True
                            player1_dino.life -= 1
                            collision_time = pygame.time.get_ticks()
                            if player1_dino.life == 0:
                                player1_dino.is_dead = True
                            pm_list.remove(pm)

                if (len(pm_list_2p)== 0):
                    pass
                else:
                    for pm_2p in pm_list_2p:
                        if (pm_2p.x >= player2_dino.rect.left) and (pm_2p.x <= player2_dino.rect.right) and (pm_2p.y > player2_dino.rect.top) and (pm_2p.y < player2_dino.rect.bottom):
                            print("2p가 공격에 맞음.")
                            # if pygame.sprite.collide_mask(player_dino, pm):
                            player2_dino.collision_immune = True
                            player2_dino.life -= 1
                            collision_time = pygame.time.get_ticks()
                            if player2_dino.life == 0:
                                player1_dino.is_dead = True
                            pm_list_2p.remove(pm_2p)

                if player1_dino.is_dead:
                    game_over = True
                    pygame.mixer.music.stop()
                if player2_dino.is_dead:
                    game_over = True
                    pygame.mixer.music.stop()
                heart_1p.update(player1_dino.life)
                heart_2p.update(player2_dino.life)
                
            counter += 1

        if game_quit:
            break

        while game_over:
            if pygame.display.get_surface() is None:
                print("Couldn't load display surface")
                game_quit = True
                game_over = False
                dust_rest_time = 10
                dust_rest_time_2p = 10
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_quit = True
                        game_over = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game_quit = True
                            game_over = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            game_over = False
                            game_quit = True

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # game_over = False
                        # game_quit = True
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            x, y = event.pos
                            if r_btn_restart_rect.collidepoint(x, y):
                                pvprunning()

                            if r_btn_exit_rect.collidepoint(x, y):
                                src.game.intro_screen()

                    if event.type == pygame.VIDEORESIZE:
                        check_scr_size(event.w, event.h)
                r_btn_restart_rect.centerx, r_btn_restart_rect.centery = resized_screen.get_width() * 0.35, resized_screen.get_height() * 0.55
                r_btn_exit_rect.centerx, r_btn_exit_rect.centery = resized_screen.get_width() * 0.65, resized_screen.get_height() * 0.55
                disp_pvp_gameover_buttons(btn_restart, btn_exit)
                disp_pvp_winner_loser(player1_dino)

                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                    resized_screen_center)
                pygame.display.update()
            if pygame.display.get_surface() is not None:
                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                    resized_screen_center)
                pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()

def dust_appear():
    global game_over
    global paused
    global is_dust_time
    if game_over:
        return
    if paused:
        return
    if is_dust_time == False:
        return
    threading.Timer(ONE_SECOND,dust_appear).start()
    global dust_rest_time
    
    dust_rest_time -= 1
    if dust_rest_time <= 0:
        dust_rest_time = 0

def dust_appear_2p():
    global game_over
    global paused
    global is_dust_time_2p
    if game_over:
        return
    if paused:
        return
    if is_dust_time_2p == False:
        return
    threading.Timer(ONE_SECOND,dust_appear_2p).start()
    global dust_rest_time_2p
    dust_rest_time_2p -= 1
    if dust_rest_time_2p <= 0:
        dust_rest_time_2p = 0

def water_appear():
        global game_over
        global paused
        global is_dust_time
        if game_over:
            return
        if paused:
            return
        if is_water_time == False:
            return

        threading.Timer(ONE_SECOND,water_appear).start()
        global water_rest_time
        water_rest_time -= 1
        if water_rest_time <= 0:
            water_rest_time = 0

def water_appear_2p():
        global game_over
        global paused
        global is_water_time_2p
        if game_over:
            return
        if paused:
            return
        if is_water_time_2p == False:
            return
        
        threading.Timer(ONE_SECOND,water_appear_2p).start()
        global water_rest_time_2p
        water_rest_time_2p -= 1
        if water_rest_time_2p <= 0:
            water_rest_time_2p = 0