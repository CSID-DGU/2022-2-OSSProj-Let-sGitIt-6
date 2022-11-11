from pygame.image import load
from src.dino import *
from src.obstacle import *
from src.item import *
from src.interface import *
# from src.option import *
import src.setting as setting
from src.game_value import *
from db.db_interface import InterfDB
# from src.store import store
from src.pvp import *
from src.pvprunning import *
from src.story import *
from time import sleep
import threading
import time
db = InterfDB("db/data.db")

## 시작 화면 ##
def intro_screen():
    global resized_screen
    global temp_dino
    # global type_idx
    global dino_type
    dino_type = ['ORIGINAL','RED','ORANGE','YELLOW','GREEN','PURPLE','BLACK','PINK']
    global skin_type
    # global type_idx2
    click_count = 0
    #
    temp_dino = Dino(dino_size[0], dino_size[1])
    temp_dino.is_blinking = True
    game_start = False
    background, background_rect  = load_image('intro_background.png', width, height)
    # 버튼 이미지 (pvp모드에 대한 p 주석)
    # r_r_btn_gamestart,_gamestart_oad_image(*resize('r_btn_gamestart.0, 60, -1))
    # r_btn_gamestart,amestart_oad_image('r_btn_gamestart.0, 60, -1)
    # r_btn_2p, r_btn_2p_rect = load_image(*resize('btn_2p.png', 150, 60, -1))
    # btn_2p, btn_2p_rect = load_image('btn_2p.png', 150, 60, -1)
    r_btn_gamestart, r_btn_gamestart_rect = load_image(*resize('game_start.png', 150, 50, -1))
    btn_gamestart, btn_gamestart_rect = load_image('game_start.png', 150, 50, -1)
    r_btn_board, r_btn_board_rect = load_image(*resize('score_board.png', 150, 50, -1))
    btn_board, btn_board_rect = load_image('score_board.png', 150, 50, -1)
    r_btn_option, r_btn_option_rect = load_image(*resize('option.png', 150, 50, -1))
    btn_option, btn_option_rect = load_image('option.png', 150, 50, -1)
    # DINO IMAGE
    while not game_start:
        if pygame.display.get_surface() == None:
            print("Couldn't load display surface")
            return True
        else:
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE and not full_screen:
                    background_rect.bottomleft = (width * 0, height)
                if event.type == pygame.QUIT:
                    game_start = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                # 버튼 클릭했을 때 event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        x, y = event.pos
                        # 1player game button
                        # if r_btn_gamestart.colidepoint(x, y):
                        #     # temp_dino.is_jumping = True
                        #     # temp_dino.is_blinking = False
                        #     temp_dino.movement[1] = -1 * temp_dino.jump_speed
                        #     game_start = True
                        # # # 2player game button
                        # # if r_btn_2p_rect.collidepoint(x, y):
                        # #     pvp()

                        #game button
                        if r_btn_gamestart_rect.collidepoint(x, y):
                            temp_dino.movement[1] = -1 * temp_dino.jump_speed
                            game_start = True
                            select_mode()
                        #board button
                        if r_btn_board_rect.collidepoint(x, y):
                            board()
                        # option button
                        if r_btn_option_rect.collidepoint(x, y):
                            option()

        # interface draw
        if pygame.display.get_surface() is not None:
            r_btn_gamestart_rect.centerx = resized_screen.get_width() * 0.8
            r_btn_board_rect.centerx = resized_screen.get_width() * 0.8
            r_btn_option_rect.centerx = resized_screen.get_width() * 0.8

            r_btn_gamestart_rect.centery = resized_screen.get_height() * (0.25 + 0.75 * button_offset)
            r_btn_board_rect.centery = resized_screen.get_height() * (0.25 + 1.5 * button_offset)
            r_btn_option_rect.centery = resized_screen.get_height() * (0.25 + 2.25 * button_offset)
            screen.blit(background, background_rect)
            disp_intro_buttons(btn_gamestart, btn_board, btn_option)


            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())), resized_screen_center)
            pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()



def option():
    global on_pushtime
    global off_pushtime
    # global bgm_on
    global high_score
    global resized_screen
    btnpush_interval = 500  # ms
    pygame.mixer.music.stop()
    done = False
    db_init = False
    large_text = pygame.font.Font('freesansbold.ttf', 60)
    text_surf, text_rect = load_image("Big_Option.png", 300, 50, -1)
    btn_bgm_on, btn_bgm_on_rect = load_image('btn_bgm_on.png', 80, 80, -1)
    btn_bgm_off, btn_bgm_off_rect = load_image('btn_bgm_off.png', 80, 80, -1)
    r_btn_bgm_on, r_btn_bgm_on_rect = load_image(*resize('btn_bgm_on.png', 80, 80, -1))
    init_btn_image, init_btn_rect = load_image('scorereset.png', 80, 80, -1)
    r_init_btn_image, r_init_btn_rect = load_image(*resize('scorereset.png', 80, 80, -1))
    btn_gamerule, btn_gamerule_rect = load_image('btn_gamerule.png', 80, 80, -1)
    r_btn_gamerule, r_btn_gamerule_rect = load_image(*resize('btn_gamerule.png', 80, 80, -1))
    btn_home, btn_home_rect = load_image('main_button.png', 70, 62, -1)
    r_btn_home, r_btn_home_rect = load_image(*resize('main_button.png', 70, 62, -1))
    btn_credit, btn_credit_rect = load_image('btn_credit.png', 150, 50, -1)
    r_btn_credit, r_btn_credit_rect = load_image(*resize('btn_credit.png', 180, 80, -1))

    text_rect.center = (width * 0.5, height * 0.15)
    btn_bgm_on_rect.center = (width * 0.25, height * 0.5)
    init_btn_rect.center = (width * 0.5, height * 0.5)
    btn_gamerule_rect.center = (width * 0.75, height * 0.5)
    btn_home_rect.center = (width * 0.9, height * 0.15)
    btn_credit_rect.center = (width * 0.9, height * 0.85)

    while not done:
        for event in pygame.event.get():

            # CHANGE SIZE START
            if event.type == pygame.VIDEORESIZE and not full_screen:
                pass
            # CHANGE SIZE END
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    x, y = event.pos
                    if r_btn_home_rect.collidepoint(x, y):
                        intro_screen()

                    if r_btn_bgm_on_rect.collidepoint(x, y) and setting.bgm_on:
                        off_pushtime = pygame.time.get_ticks()
                        if off_pushtime - on_pushtime > btnpush_interval:
                            setting.bgm_on = False

                    if r_btn_bgm_on_rect.collidepoint(x, y) and not setting.bgm_on:
                        on_pushtime = pygame.time.get_ticks()
                        if on_pushtime - off_pushtime > btnpush_interval:
                            setting.bgm_on = True

                    if r_init_btn_rect.collidepoint(x, y):
                        db.query_db("delete from hard_mode;")
                        db.query_db("delete from easy_mode")
                        db.commit()
                        high_score = 0
                        db_init = True

                    if r_btn_gamerule_rect.collidepoint(x, y):
                        gamerule()

                    if r_btn_credit_rect.collidepoint(x, y):
                        credit()

            # if event.type == pygame.VIDEORESIZE:
            #     check_scr_size(event.w, event.h)

        r_init_btn_rect.centerx = resized_screen.get_width() * 0.5
        r_init_btn_rect.centery = resized_screen.get_height() * 0.5
        r_btn_gamerule_rect.centerx = resized_screen.get_width() * 0.75
        r_btn_gamerule_rect.centery = resized_screen.get_height() * 0.5
        r_btn_home_rect.centerx = resized_screen.get_width() * 0.9
        r_btn_home_rect.centery = resized_screen.get_height() * 0.15
        r_btn_credit_rect.centerx = resized_screen.get_width() * 0.9
        r_btn_credit_rect.centery = resized_screen.get_height() * 0.85

        screen.fill(background_col)
        screen.blit(text_surf, text_rect)
        screen.blit(init_btn_image, init_btn_rect)
        screen.blit(btn_gamerule, btn_gamerule_rect)
        screen.blit(btn_home, btn_home_rect)
        screen.blit(btn_credit, btn_credit_rect)

        if setting.bgm_on:
            screen.blit(btn_bgm_on, btn_bgm_on_rect)
            r_btn_bgm_on_rect.centerx = resized_screen.get_width() * 0.25
            r_btn_bgm_on_rect.centery = resized_screen.get_height() * 0.5
        if not setting.bgm_on:
            screen.blit(btn_bgm_off, btn_bgm_on_rect)
            r_btn_bgm_on_rect.centerx = resized_screen.get_width() * 0.25
            r_btn_bgm_on_rect.centery = resized_screen.get_height() * 0.5
        if db_init:
            draw_text("Scoreboard cleared", font, screen, 400, 300, black)

        resized_screen.blit(
            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
            resized_screen_center)
        pygame.display.update()

        clock.tick(FPS)
    pygame.quit()
    quit()

def select_mode():
    global resized_screen
    game_start = False
    btnpush_interval = 500

    # 버튼 이미지
    back_btn_image, back_btn_rect = load_image('back.png', 75, 30, -1)
    r_back_btn_image, r_back_btn_rect = load_image(*resize('back.png', 75, 30, -1))
    ##easy mode button
    easymode_btn_image, easymode_btn_rect = load_image('Easy-Mode.png', 150, 50, -1)
    r_easymode_btn_image, r_easy_btn_rect = load_image(*resize('Easy-Mode.png', 150, 50, -1))
    # hardmode button
    btn_hardmode, btn_hardmode_rect = load_image('Hard-Mode.png', 150, 50, -1)
    r_btn_hardmode, r_btn_hardmode_rect = load_image(*resize('Hard-Mode.png', 150, 50, -1))
    # runningmode button, 임시로 hardmode 이미지로 진행
    btn_runningmode, btn_runningmode_rect = load_image('PvP-Running.png', 150, 50, -1)
    r_btn_runningmode, r_btn_runningmode_rect = load_image(*resize('PvP-Running.png', 150, 50, -1))
    # battlemode button, 임시로 hardmode 이미지로 진행
    btn_battlemode, btn_battlemode_rect = load_image('PvP-Battle.png', 150, 50, -1)
    r_btn_battlemode, r_btn_battlemode_rect = load_image(*resize('PvP-Battle.png', 150, 50, -1))
    
    
    # 배경 이미지
    Background, Background_rect = load_image('mode_background.png', width, height)

    # 뒤로가기 버튼
    back_btn_rect =  (width * 0.05, height * 0.1)
    # 이지, 하드모드 버튼
    easymode_btn_rect.center = (width * 0.66, height * 0.5)
    btn_hardmode_rect.center = (width * 0.66, height * 0.75)
    # 러닝, 배틀모드 버튼
    btn_runningmode_rect.center = (width * 0.33, height * 0.5)
    btn_battlemode_rect.center = (width * 0.33, height * 0.75)


    while not game_start:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                game_start = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    x, y = event.pos
                    if r_back_btn_rect.collidepoint(x, y):
                        intro_screen()

                    if r_easy_btn_rect.collidepoint(x, y):
                        gameplay_story1()
                    if r_btn_hardmode_rect.collidepoint(x, y):
                        gameplay_hard()

                    if r_btn_runningmode_rect.collidepoint(x, y):
                        pvprunning()
                    
                    if r_btn_battlemode_rect.collidepoint(x, y):
                        pvp()

            if event.type == pygame.VIDEORESIZE:
                check_scr_size(event.w, event.h)
        r_back_btn_rect.centerx, r_back_btn_rect.centery = resized_screen.get_width() * 0.075, resized_screen.get_height() * 0.1
        r_easy_btn_rect.centerx, r_easy_btn_rect.centery = resized_screen.get_width() * 0.66, resized_screen.get_height() * 0.5
        r_btn_hardmode_rect.centerx, r_btn_hardmode_rect.centery = resized_screen.get_width() * 0.66, resized_screen.get_height() * (
                0.75)
        r_btn_runningmode_rect.centerx, r_btn_runningmode_rect.centery = resized_screen.get_width() * 0.33, resized_screen.get_height() * (
                0.5)
        r_btn_battlemode_rect.centerx, r_btn_battlemode_rect.centery = resized_screen.get_width() * 0.33, resized_screen.get_height() * (
                0.75)

        
        screen.blit(Background, Background_rect)
        screen.blit(back_btn_image, back_btn_rect)
        screen.blit(easymode_btn_image, easymode_btn_rect)
        screen.blit(btn_hardmode, btn_hardmode_rect)
        screen.blit(btn_runningmode, btn_runningmode_rect)
        screen.blit(btn_battlemode, btn_battlemode_rect)


        resized_screen.blit(
            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
            resized_screen_center)
        pygame.display.update()

        clock.tick(FPS)
    pygame.quit()
    quit()





## 게임 작동 ##
def gameplay_easy():
    global resized_screen
    global high_score
    spring_image, spring_rect = load_image('ex_spring.png', 230, 210, -1)
    r_spring_image, r_spring_rect = load_image(*resize('ex_spring.png', 230, 210, -1))
    un_spring_image, un_spring_rect = load_image('unselect_spring.png', 230, 210, -1)
    r_un_spring_image, r_un_spring_rect = load_image(*resize('unselect_spring.png', 230, 210, -1))
    screen.blit(spring_image, spring_rect)
    result = db.query_db("select score from user order by score desc;", one=True)
    if result is not None:
        high_score = result['score']
    #    if bgm_on:
    #       pygame.mixer.music.play(-1) # 배경음악 실행
    game_speed = 4
    startMenu = False
    game_over = False
    game_quit = False
    paused = False
    life = 5
    # # 캐릭터 생성
    player_dino = Dino(dino_size[0], dino_size[1])

    new_ground = Ground(-1 * game_speed)
    scb = Scoreboard( y = height * SCB_HEIGHT)
    highsc = Scoreboard(width * SCB_WIDTH, height * SCB_HEIGHT)
    heart = HeartIndicator(life)
    speed_indicator = Scoreboard(width * INDICATOR_X, height * INDICATOR_Y)
    counter = 0
    speed_text = font.render("SPEED", True, black)

    cacti = pygame.sprite.Group()
    fire_cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    stones = pygame.sprite.Group()

    last_obstacle = pygame.sprite.Group()
    shield_items = pygame.sprite.Group()
    life_items = pygame.sprite.Group()
    slow_items = pygame.sprite.Group()
    # highjump_items = pygame.sprite.Group()

    Stone.containers = stones
    Cactus.containers = cacti
    fire_Cactus.containers = fire_cacti
    Ptera.containers = pteras
    Cloud.containers = clouds
    ShieldItem.containers = shield_items
    LifeItem.containers = life_items
    SlowItem.containers = slow_items
    # HighJumpItem.containers = highjump_items
    # BUTTON IMG LOAD
    # retbutton_image, retbutton_rect = load_image('replay_button.png', 70, 62, -1)
    game_over_image, game_over_rect = load_image('game_over.png', OVER_X, OVER_Y, -1)
    my_font = pygame.font.Font('DungGeunMo.ttf', 30)
    high_image = my_font.render('HI', True, black)
    high_rect = high_image.get_rect()
    high_rect.top = height * HI_HEIGHT
    high_rect.left = width * HI_WIDTH

    while not game_quit:
        while startMenu:
            pass
        while not game_over:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                game_quit = True
                game_over = True


            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # 종료
                        game_quit = True
                        game_over = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:  # 스페이스 누르는 시점에 공룡이 땅에 닿아있으면 점프한다.
                            if player_dino.rect.bottom == int(0.98 * height):
                                player_dino.is_jumping = True
                                if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                                player_dino.movement[1] = -1 * player_dino.jump_speed

                        if event.key == pygame.K_DOWN:  # 아래방향키를 누르는 시점에 공룡이 점프중이지 않으면 숙인다.
                            if not (player_dino.is_jumping and player_dino.is_dead):
                                player_dino.is_ducking = True

                        if event.key == pygame.K_ESCAPE:
                            paused = not paused
                            paused = pausing()

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            player_dino.is_ducking = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed() == (1, 0, 0) and player_dino.rect.bottom == int(0.98 * height):
                            # (mouse left button, wheel button, mouse right button)
                            player_dino.is_jumping = True
                            if pygame.mixer.get_init() != None:
                                jump_sound.play()
                            player_dino.movement[1] = -1 * player_dino.jump_speed

                        if pygame.mouse.get_pressed() == (0, 0, 1):
                            # (mouse left button, wheel button, mouse right button)
                            if not (player_dino.is_jumping and player_dino.is_dead):
                                player_dino.is_ducking = True

                    if event.type == pygame.MOUSEBUTTONUP:
                        player_dino.is_ducking = False

                    if event.type == pygame.VIDEORESIZE:
                        check_scr_size(event.w, event.h)

            if not paused:

                for s in stones:
                    s.movement[0] = -1 * game_speed
                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, s):
                            player_dino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                player_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                for c in cacti:
                    c.movement[0] = -1 * game_speed
                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, c):
                            player_dino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                player_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not player_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player_dino.collision_immune = False

                for f in fire_cacti:
                    f.movement[0] = -1 * game_speed
                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, f):
                            player_dino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                player_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not player_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player_dino.collision_immune = False

                for p in pteras:
                    p.movement[0] = -1 * game_speed
                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, p):
                            player_dino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                player_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not player_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player_dino.collision_immune = False


                    elif not player_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player_dino.collision_immune = False

                if not player_dino.is_super:
                    for s in shield_items:
                        s.movement[0] = -1 * game_speed
                        if pygame.sprite.collide_mask(player_dino, s):
                            # if pygame.mixer.get_init() is not None:
                            #     check_point_sound.play()
                            # player_dino.collision_immune = True
                            # player_dino.is_super = True
                            s.kill()
                            item_time = pygame.time.get_ticks()
                        elif s.rect.right < 0:
                            s.kill()

                STONE_INTERVAL = 50
                CACTUS_INTERVAL = 50
                PTERA_INTERVAL = 300
                CLOUD_INTERVAL = 300
                SHIELD_INTERVAL = 500
                LIFE_INTERVAL = 1000
                SLOW_INTERVAL = 1000
                HIGHJUMP_INTERVAL = 300
                OBJECT_REFRESH_LINE = width * 0.8
                MAGIC_NUM = 10

                if len(cacti) < 2:
                    if len(cacti) == 0:
                        last_obstacle.empty()
                        last_obstacle.add(Cactus(game_speed, object_size[0], object_size[1]))
                    else:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(Cactus(game_speed, object_size[0], object_size[1]))

                if len(fire_cacti) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL * 5) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(fire_Cactus(game_speed, object_size[0], object_size[1]))

                if len(stones) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(STONE_INTERVAL * 3) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(Stone(game_speed, object_size[0], object_size[1]))

                if len(pteras) == 0 and random.randrange(PTERA_INTERVAL) == MAGIC_NUM and counter > PTERA_INTERVAL:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE:
                            last_obstacle.empty()
                            last_obstacle.add(Ptera(game_speed, ptera_size[0], ptera_size[1]))

                if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                    Cloud(width, random.randrange(height / 5, height / 2))

                player_dino.update()
                cacti.update()
                fire_cacti.update()
                pteras.update()
                clouds.update()
                shield_items.update()
                life_items.update()
                # highjump_items.update()
                new_ground.update()
                scb.update(player_dino.score)
                highsc.update(high_score)
                speed_indicator.update(game_speed - 3)
                heart.update(life)
                slow_items.update()

                stones.update()

                if pygame.display.get_surface() != None:
                    screen.fill(background_col)
                    new_ground.draw()
                    clouds.draw(screen)
                    scb.draw()
                    speed_indicator.draw()
                    screen.blit(speed_text, (width * 0.01, height * 0.13))
                    heart.draw()
                    if high_score != 0:
                        highsc.draw()
                        screen.blit(HI_image, HI_rect)
                    cacti.draw(screen)
                    stones.draw(screen)
                    fire_cacti.draw(screen)
                    pteras.draw(screen)
                    shield_items.draw(screen)
                    life_items.draw(screen)
                    slow_items.draw(screen)
                    # highjump_items.draw(screen)
                    player_dino.draw()
                    resized_screen.blit(
                        pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                        resized_screen_center)
                    pygame.display.update()
                clock.tick(FPS)

                if player_dino.is_dead:
                    game_over = True
                    pygame.mixer.music.stop()  # 죽으면 배경음악 멈춤
                    if player_dino.score > high_score:
                        high_score = player_dino.score

                if counter % speed_up_limit == speed_up_limit - 1:
                    new_ground.speed -= 1
                    game_speed += 1

                counter = (counter + 1)
                
        if game_quit:
            break

        while game_over:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                game_quit = True
                game_over = False
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
                            type_score(player_dino.score)
                            if not db.is_limit_data(player_dino.score, mode="easy"):
                                db.query_db(
                                    f"insert into easy_mode (username, score) values ('{gamer_name}', '{player_dino.score}');")
                                db.commit()
                                board("easy")
                            else:
                                board("easy")

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        game_over = False
                        game_quit = True
                        type_score(player_dino.score)
                        if not db.is_limit_data(player_dino.score):
                            db.query_db(
                                f"insert into easy_mode (username, score) values ('{gamer_name}', '{player_dino.score}');")
                            db.commit()
                            board("easy")
                        else:
                            board("easy")

                    if event.type == pygame.VIDEORESIZE:
                        check_scr_size(event.w, event.h)

            highsc.update(high_score)
            if pygame.display.get_surface() != None:
                disp_gameover_msg(game_over_image)
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image, HI_rect)
                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                    resized_screen_center)
                pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()

def gameplay_hard():
    global resized_screen
    global high_score
    result = db.query_db("select score from user order by score desc;", one=True)
    if result is not None:
        high_score = result['score']

    # HERE: REMOVE SOUND!!    
    # if bgm_on:
    #     pygame.mixer.music.play(-1)  # 배경음악 실행
    
    game_speed = 4
    startMenu = False
    game_over = False
    game_quit = False
    ###
    life = 5
    ###
    paused = False
    
    # # 디노 타입 때문에 변경된 부분
    player_dino = Dino(dino_size[0], dino_size[1])
    # 

    new_ground = Ground(-1 * game_speed)
    #배경 변경하는 코드
    new_ground = ImgBack(-1 * game_speed, "spring")
    scb = Scoreboard()
    highsc = Scoreboard(width * 0.78)
    heart = HeartIndicator(life)
    speed_indicator = Scoreboard(width * 0.12, height * 0.15)
    counter = 0

    speed_text = font.render("SPEED", True, black)

    cacti = pygame.sprite.Group()
    fire_cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    stones = pygame.sprite.Group() #add stones
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()
    shield_items = pygame.sprite.Group()
    life_items = pygame.sprite.Group()
    slow_items = pygame.sprite.Group()


    Cactus.containers = cacti
    fire_Cactus.containers = fire_cacti
    Ptera.containers = pteras
    Cloud.containers = clouds
    ShieldItem.containers = shield_items
    LifeItem.containers = life_items
    SlowItem.containers = slow_items
    Stone.containers = stones # add stone containers

    # BUTTON IMG LOAD
    # retbutton_image, retbutton_rect = load_image('replay_button.png', 70, 62, -1)
    game_over_image, game_over_rect = load_image('game_over.png', 380, 22, -1)

    temp_images, temp_rect = load_sprite_sheet('numbers.png', 12, 1, 11, int(15 * 6 / 5), -1)
    HI_image = pygame.Surface((30, int(15 * 6 / 5)))
    HI_rect = HI_image.get_rect()
    HI_image.fill(background_col)
    HI_image.blit(temp_images[10], temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11], temp_rect)
    HI_rect.top = height * 0.05
    HI_rect.left = width * 0.73

    # 1. 미사일 발사.
    space_go=False
    m_list=[]
    bk=0
    # 익룡이 격추되었을때
    isDown=False
    boomCount=0
    #

    # 방향키 구현
    go_left=False
    go_right=False
    #

    # 보스몬스터 변수설정
    isPkingTime=False
    isPkingAlive=True
    pking=PteraKing()
    pm_list = []
    pm_vector = []
    pm_pattern0_count = 0
    pm_pattern1_count = 0
    pking_appearance_score = 100
    #

    #
    jumpingx2 = False

    while not game_quit:
        while startMenu:
            pass
        while not game_over:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                game_quit = True
                game_over = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_quit = True
                        game_over = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:  # 스페이스 누르는 시점에 공룡이 땅에 닿아있으면 점프한다.
                            if player_dino.rect.bottom == int(0.98 * height):
                                player_dino.is_jumping = True
                                if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                                player_dino.movement[1] = -1 * player_dino.jump_speed

                        if event.key == pygame.K_DOWN:  # 아래방향키를 누르는 시점에 공룡이 점프중이지 않으면 숙인다.
                            if not (player_dino.is_jumping and player_dino.is_dead):
                                player_dino.is_ducking = True

                        if event.key == pygame.K_LEFT:
                            # print("left")
                            go_left=True

                        if event.key == pygame.K_RIGHT:
                            # print("right")
                            go_right=True

                        if event.key == pygame.K_ESCAPE:
                            paused = not paused
                            paused = pausing()

                        # jumping x2 ( press key s)
                        if event.key == pygame.K_s:
                            jumpingx2=True

                        # 2. a키를 누르면, 미사일이 나갑니다.
                        if event.key == pygame.K_a:
                            space_go=True
                            bk=0
                        #

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            player_dino.is_ducking = False

                        # 3.a키에서 손을 떼면, 미사일이 발사 되지 않습니다.
                        if event.key == pygame.K_a:
                            space_go = False
                        #

                        # 방향키 추가
                        if event.key == pygame.K_LEFT:
                            go_left=False

                        if event.key == pygame.K_RIGHT:
                            go_right=False
                        #

                        ## jumgpingx2
                        if event.key == pygame.K_s:
                            jumpingx2 = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed() == (1, 0, 0) and player_dino.rect.bottom == int(0.98 * height):
                            # (mouse left button, wheel button, mouse right button)
                            player_dino.is_jumping = True
                            if pygame.mixer.get_init() != None:
                                jump_sound.play()
                            player_dino.movement[1] = -1 * player_dino.jump_speed

                        if pygame.mouse.get_pressed() == (0, 0, 1):
                            # (mouse left button, wheel button, mouse right button)
                            if not (player_dino.is_jumping and player_dino.is_dead):
                                player_dino.is_ducking = True

                    if event.type == pygame.MOUSEBUTTONUP:
                        player_dino.is_ducking = False

                    if event.type == pygame.VIDEORESIZE:
                        check_scr_size(event.w, event.h)

            if not paused:
                if go_left:
                    if player_dino.rect.left < 0:
                        player_dino.rect.left = 0
                    else:
                        player_dino.rect.left = player_dino.rect.left - game_speed
                if go_right:
                    if player_dino.rect.right > width:
                        player_dino.rect.right = width
                    else:
                        player_dino.rect.left = player_dino.rect.left + game_speed

                # 4. space_go가 True이고, 일정 시간이 지나면, 미사일을 만들고, 이를 미사일 배열에 넣습니다.
                if (space_go==True) and (int(bk%15)==0):
                    # print(bk)
                    mm=Obj()

                    # # 디노의 종류에 따라 다른 총알이 나가도록 합니다.
                    # if player_dino.type == 'RED':
                    #     mm.put_img("./sprites/black_bullet.png")
                    #     mm.change_size(10,10)
                    # elif player_dino.type == 'YELLOW':
                    #     mm.put_img("./sprites/blue_bullet.png")
                    #     mm.change_size(10,10)
                    # elif player_dino.type == 'ORANGE':
                    #     mm.put_img("./sprites/blue_bullet.png")
                    #     mm.change_size(10,10)
                    # elif player_dino.type == 'PURPLE':
                    #     mm.put_img("./sprites/pink_bullet.png")
                    #     mm.change_size(15,5)
                    # elif player_dino.type == 'PINK':
                    #     mm.put_img("./sprites/heart_bullet.png")
                    #     mm.change_size(10,10)
                    # else:                    
                    mm.put_img("./sprites/red_bullet.png")
                    mm.change_size(10,10)
                    # 
                    
                    if player_dino.is_ducking ==False:
                        mm.x = round(player_dino.rect.centerx)
                        mm.y = round(player_dino.rect.top*1.035)
                    if player_dino.is_ducking ==True:
                        mm.x = round(player_dino.rect.centerx)
                        mm.y = round(player_dino.rect.centery*1.01)
                    mm.move = 15
                    m_list.append(mm)
                bk=bk+1
                d_list=[]

                for i in range(len(m_list)):
                    m=m_list[i]
                    m.x +=m.move
                    if m.x>width:
                        d_list.append(i)

                d_list.reverse()
                for d in d_list:
                    del m_list[d]
                #

                if jumpingx2 :
                    if  player_dino.rect.bottom == int(height * 0.98):
                        player_dino.is_jumping = True
                        player_dino.movement[1] = -1 * player_dino.super_jump_speed

                # 보스 몬스터 패턴0(위에서 가만히 있는 패턴): 보스 익룡이 쏘는 미사일.
                if (isPkingTime) and (pking.pattern_idx == 0) and (int(pm_pattern0_count % 20) == 0):
                    pm=Obj()
                    pm.put_img("./sprites/pking bullet.png")
                    pm.change_size(15,15)
                    pm.x = round(pking.rect.centerx)
                    pm.y = round(pking.rect.centery)
                    pm.x_move = random.randint(0,15)
                    pm.y_move = random.randint(1,3)

                    pm_list.append(pm)
                pm_pattern0_count += 1
                pd_list = []

                for i in range(len(pm_list)):
                    pm = pm_list[i]
                    pm.x -= pm.x_move
                    pm.y += pm.y_move
                    if pm.y > height or pm.x < 0:
                        pd_list.append(i)
                pd_list.reverse()
                for d in pd_list:
                    del pm_list[d]


                #

                # 보스 몬스터 패턴1(좌우로 왔다갔다 하는 패턴): 보스 익룡이 쏘는 미사일.
                if (isPkingTime) and (pking.pattern_idx == 1) and (int(pm_pattern1_count % 20) == 0):
                    # print(pm_list)
                    pm=Obj()
                    pm.put_img("./sprites/pking bullet.png")
                    pm.change_size(15,15)
                    pm.x = round(pking.rect.centerx)
                    pm.y = round(pking.rect.centery)
                    pm.move = 3
                    pm_list.append(pm)
                pm_pattern1_count += 1
                pd_list = []

                for i in range(len(pm_list)):
                    pm=pm_list[i]
                    pm.y +=pm.move
                    if pm.y>height or pm.x < 0:
                        pd_list.append(i)

                pd_list.reverse()
                for d in pd_list:
                    del pm_list[d]
                #


                for c in cacti:
                    c.movement[0] = -1 * game_speed
                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, c):
                            player_dino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                player_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not player_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player_dino.collision_immune = False

                for f in fire_cacti:
                    f.movement[0] = -1 * game_speed
                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, f):
                            player_dino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                player_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not player_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player_dino.collision_immune = False

                for p in pteras:
                    p.movement[0] = -1 * game_speed

                    # 7. 익룡이 미사일에 맞으면 익룡과 미사일 모두 사라집니다.

                    if (len(m_list)==0):
                        pass
                    else:
                        if (m.x>=p.rect.left)and(m.x<=p.rect.right)and(m.y>p.rect.top)and(m.y<p.rect.bottom):
                            print("격추 성공")
                            isDown=True
                            boom=Obj()
                            boom.put_img("./sprites/boom.png")
                            boom.change_size(200,100)
                            boom.x=p.rect.centerx-round(p.rect.width)*2.5
                            boom.y=p.rect.centery-round(p.rect.height)*1.5
                            player_dino.score+=30
                            p.kill()
                            # 여기만 바꿈
                            m_list.remove(m)
                            #
                    #

                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, p):
                            player_dino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                player_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not player_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player_dino.collision_immune = False

                for s in stones:
                    s.movement[0] = -1 * game_speed
                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, s):
                            player_dino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                player_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                if not player_dino.is_super:
                    for s in shield_items:
                        s.movement[0] = -1 * game_speed
                        if pygame.sprite.collide_mask(player_dino, s):
                            # if pygame.mixer.get_init() is not None:
                            #     check_point_sound.play()
                            player_dino.collision_immune = True
                            player_dino.is_super = True
                            s.kill()
                            item_time = pygame.time.get_ticks()
                        elif s.rect.right < 0:
                            s.kill()
                else:
                    for s in shield_items:
                        s.movement[0] = -1 * game_speed
                        if pygame.sprite.collide_mask(player_dino, s):
                            # if pygame.mixer.get_init() is not None:
                            #     check_point_sound.play()
                            player_dino.collision_immune = True
                            player_dino.is_super = True
                            s.kill()
                            item_time = pygame.time.get_ticks()
                        elif s.rect.right < 0:
                            s.kill()

                    if pygame.time.get_ticks() - item_time > shield_time:
                        player_dino.collision_immune = False
                        player_dino.is_super = False

                for l in life_items:
                    l.movement[0] = -1 * game_speed
                    if pygame.sprite.collide_mask(player_dino, l):
                        # if pygame.mixer.get_init() is not None:
                        #     check_point_sound.play()
                        life += 1
                        l.kill()
                    elif l.rect.right < 0:
                        l.kill()

                for k in slow_items:
                    k.movement[0] = -1 * game_speed
                    if pygame.sprite.collide_mask(player_dino, k):
                        # if pygame.mixer.get_init() is not None:
                        #     check_point_sound.play()
                        game_speed -= 1
                        new_ground.speed += 1
                        k.kill()
                    elif k.rect.right < 0:
                        k.kill()


                STONE_INTERVAL = 100
                CACTUS_INTERVAL = 50
                # 익룡을 더 자주 등장시키기 위해 12로 수정했습니다. (원래값은 300)
                PTERA_INTERVAL = 12
                #
                CLOUD_INTERVAL = 300
                SHIELD_INTERVAL = 100
                LIFE_INTERVAL = 1000
                SLOW_INTERVAL = 1000

                OBJECT_REFRESH_LINE = width * 0.8
                MAGIC_NUM = 10

                # print(pking.hp)
                if (isPkingAlive)and(player_dino.score>pking_appearance_score):
                    isPkingTime=True
                else:
                    isPkingTime = False

                if isPkingTime:
                    if len(cacti) < 2:
                        if len(cacti) == 0:
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(game_speed, object_size[0], object_size[1]))
                    else:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(Cactus(game_speed, object_size[0], object_size[1]))

                    if len(fire_cacti) < 2:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL*5) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(fire_Cactus(game_speed, object_size[0], object_size[1]))

                    if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                        Cloud(width, random.randrange(height / 5, height / 2))

                    if (len(m_list)==0):
                        pass
                    else:
                        if (m.x>=pking.rect.left)and(m.x<=pking.rect.right)and(m.y>pking.rect.top)and(m.y<pking.rect.bottom):
                            isDown=True
                            boom=Obj()
                            boom.put_img("./sprites/boom.png")
                            boom.change_size(200,100)
                            boom.x=pking.rect.centerx-round(pking.rect.width)
                            boom.y=pking.rect.centery-round(pking.rect.height/2)
                            pking.life -= 1
                            m_list.remove(m)

                            if pking.life <= 0:
                                pking.kill()
                                isPkingAlive=False

                    #
                    if (len(pm_list)==0):
                        pass
                    else:
                        # print("x: ",pm.x,"y: ",pm.y)
                        for pm in pm_list:
                            if (pm.x>=player_dino.rect.left)and(pm.x<=player_dino.rect.right)and(pm.y>player_dino.rect.top)and(pm.y<player_dino.rect.bottom):
                                print("공격에 맞음.")
                                # if pygame.sprite.collide_mask(player_dino, pm):
                                player_dino.collision_immune = True
                                life -= 1
                                collision_time = pygame.time.get_ticks()
                                if life == 0:
                                    player_dino.is_dead = True
                                pm_list.remove(pm)
                    #
                else:
                    if len(cacti) < 2:
                        if len(cacti) == 0:
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(game_speed, object_size[0], object_size[1]))
                        else:
                            for l in last_obstacle:
                                if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL) == MAGIC_NUM:
                                    last_obstacle.empty()
                                    last_obstacle.add(Cactus(game_speed, object_size[0], object_size[1]))

                    if len(fire_cacti) < 2:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL * 5) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(fire_Cactus(game_speed, object_size[0], object_size[1]))

                    if len(stones) < 2:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(STONE_INTERVAL * 5) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(Stone(game_speed, object_size[0], object_size[1]))


                    if len(pteras) == 0 and random.randrange(PTERA_INTERVAL) == MAGIC_NUM and counter > PTERA_INTERVAL:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE:
                                last_obstacle.empty()
                                last_obstacle.add(Ptera(game_speed, ptera_size[0], ptera_size[1]))

                    if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                        Cloud(width, random.randrange(height / 5, height / 2))

                    if len(shield_items) < 0 and random.randrange(
                            SHIELD_INTERVAL) == MAGIC_NUM and counter > SHIELD_INTERVAL:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE:
                                last_obstacle.empty()
                                last_obstacle.add(ShieldItem(game_speed, object_size[0], object_size[1]))

                    if len(life_items) == 0 and random.randrange(
                            LIFE_INTERVAL) == MAGIC_NUM and counter > LIFE_INTERVAL * 2:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE:
                                last_obstacle.empty()
                                last_obstacle.add(LifeItem(game_speed, object_size[0], object_size[1]))

                    if len(slow_items) == 0 and random.randrange(SLOW_INTERVAL) == MAGIC_NUM and counter > SLOW_INTERVAL:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE:
                                last_obstacle.empty()
                                last_obstacle.add(SlowItem(game_speed, object_size[0], object_size[1]))

                player_dino.update()
                cacti.update()
                fire_cacti.update()
                stones.update()
                pteras.update()
                clouds.update()
                shield_items.update()
                life_items.update()

                new_ground.update()
                scb.update(player_dino.score)
                highsc.update(high_score)
                speed_indicator.update(game_speed - 3)
                heart.update(life)
                slow_items.update()

                # 보스몬스터 타임이면,
                if isPkingTime:
                    pking.update()
                #

                if pygame.display.get_surface() != None:
                    screen.fill(background_col)
                    new_ground.draw()
                    clouds.draw(screen)
                    scb.draw()
                    speed_indicator.draw()
                    screen.blit(speed_text, (width * 0.01, height * 0.13))
                    heart.draw()
                    if high_score != 0:
                        highsc.draw()
                        screen.blit(HI_image, HI_rect)
                    cacti.draw(screen)
                    fire_cacti.draw(screen)
                    stones.draw(screen)
                    pteras.draw(screen)
                    shield_items.draw(screen)
                    life_items.draw(screen)
                    slow_items.draw(screen)

                    # pkingtime이면, 보스몬스터를 보여줘라.
                    if isPkingTime:
                        # print(pking.pattern_idx)
                        pking.draw()
                        # 보스 익룡이 쏘는 미사일을 보여준다.
                        for pm in pm_list:
                            pm.show()
                    #

                   # 5. 미사일 배열에 저장된 미사일들을 게임 스크린에 그려줍니다.
                    for m in m_list:
                        m.show()
                        # print(type(mm.x))
                    if isDown :
                        boom.show()
                        boomCount+=1
                        # boomCount가 5가 될 때까지 boom이미지를 계속 보여준다.
                        if boomCount>10:
                            boomCount=0
                            isDown=False
                    #

                    player_dino.draw()
                    resized_screen.blit(
                        pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                        resized_screen_center)
                    pygame.display.update()
                clock.tick(FPS)

                if player_dino.is_dead:
                    game_over = True
                    pygame.mixer.music.stop()  # 죽으면 배경음악 멈춤
                    if player_dino.score > high_score:
                        high_score = player_dino.score

                if counter % speed_up_limit == speed_up_limit - 1:
                    new_ground.speed -= 1
                    game_speed += 1

                counter = (counter + 1)

        if game_quit:
            break

        while game_over:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                game_quit = True
                game_over = False
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
                            type_score(player_dino.score)
                            if not db.is_limit_data(player_dino.score):
                                db.query_db(
                                    f"insert into user(username, score) values ('{gamername}', '{player_dino.score}');")
                                db.commit()
                                board()
                            else:
                                board()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        game_over = False
                        game_quit = True
                        type_score(player_dino.score)
                        if not db.is_limit_data(player_dino.score):
                            db.query_db(
                                f"insert into user(username, score) values ('{gamername}', '{player_dino.score}');")
                            db.commit()
                            board()
                        else:
                            board()

                    if event.type == pygame.VIDEORESIZE:
                        check_scr_size(event.w, event.h)

            highsc.update(high_score)
            if pygame.display.get_surface() != None:
                disp_gameover_msg(game_over_image)
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image, HI_rect)
                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                    resized_screen_center)
                pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()


def board():
    global resized_screen
    game_quit = False
    scroll_y=0
    # 10
    max_per_screen = 10
    results = db.query_db("select username, score from user order by score desc;")
    screen_board_height = resized_screen.get_height()+(len(results)//max_per_screen)*resized_screen.get_height()
    screen_board = pygame.surface.Surface((
        resized_screen.get_width(),
        screen_board_height
        ))

    title_image, title_rect = load_image("ranking.png", 360, 75, -1)
    title_rect.centerx = width * 0.5
    title_rect.centery = height * 0.2

    # 버튼 이미지
    back_btn_image, back_btn_rect = load_image('back.png', 75, 30, -1)
    r_back_btn_image, r_back_btn_rect = load_image(*resize('back.png', 75, 30, -1))
    # 뒤로가기 버튼
    back_btn_rect =  (width * 0.05, height * 0.1)

    while not game_quit:
        if pygame.display.get_surface() is None:
            game_quit = True
        else:
            screen_board.fill(background_col)
            screen_board.blit(title_image, title_rect)

            for i, result in enumerate(results):
                top_i_surface = font.render(f"TOP {i + 1}", True, black)
                name_inform_surface = font.render("Name", True, black)
                score_inform_surface = font.render("Score", True, black)
                score_surface = font.render(str(result['score']), True, black)
                txt_surface = font.render(result['username'], True, black)

                screen_board.blit(top_i_surface, (width * 0.25, height * (0.55 + 0.1 * i)))
                screen_board.blit(name_inform_surface, (width * 0.4, height * 0.40))
                screen_board.blit(score_inform_surface, (width * 0.6, height * 0.40))
                screen_board.blit(txt_surface, (width*0.4, height * (0.55 + 0.1 * i)))
                screen_board.blit(score_surface, (width * 0.6, height * (0.55 + 0.1 * i)))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_quit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        game_quit = True
                        intro_screen()
                    if event.key == pygame.K_UP: scroll_y = min(scroll_y + 15, 0)
                    if event.key == pygame.K_DOWN: scroll_y = max(scroll_y - 15, -(len(results)//max_per_screen)*scr_size[1])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        x, y = event.pos
                        if r_back_btn_rect.collidepoint(x, y):
                            intro_screen()
                    if event.button == 4: scroll_y = min(scroll_y + 15, 0)
                    if event.button == 5: scroll_y = max(scroll_y - 15, -(len(results)//max_per_screen)*scr_size[1])
                    # if event.button == 1:
                    #     game_quit = True
                    #     intro_screen()
                if event.type == pygame.VIDEORESIZE:
                    check_scr_size(event.w, event.h)
            r_back_btn_rect.centerx, r_back_btn_rect.centery = resized_screen.get_width() * 0.075, resized_screen.get_height() * 0.1
            
            screen.blit(screen_board, (0, scroll_y))
            screen.blit(back_btn_image, back_btn_rect)
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())), resized_screen_center)
            pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

def gamerule():
    global resized_screen
    done = False
    btnpush_interval = 500

    largeText = pygame.font.Font('freesansbold.ttf', 60)
    TextSurf, TextRect = load_image("CONTROL.png", 350, 50, -1)

    TextRect.center = (width * 0.5, height * 0.2)

    # 버튼 이미지

    ##easy mode button
    easymoderule_btn_image, easymoderule_btn_rect = load_image('Easy-Mode.png', 150, 50, -1)
    r_easymoderule_btn_image, r_easyrule_btn_rect = load_image(*resize('Easy-Mode.png', 150, 50, -1))
    # hardmode button
    btn_hardmoderule, btn_hardmoderule_rect = load_image('Hard-Mode.png', 150, 50, -1)
    r_btn_hardmoderule, r_btn_hardmoderule_rect = load_image(*resize('Hard-Mode.png', 150, 50, -1))
    # runningmode button, 임시로 hardmode 이미지로 진행
    btn_runningmoderule, btn_runningmoderule_rect = load_image('PvP-Running.png', 150, 50, -1)
    r_btn_runningmoderule, r_btn_runningmoderule_rect = load_image(*resize('PvP-Running.png', 150, 50, -1))
    # battlemode button, 임시로 hardmode 이미지로 진행
    btn_battlemoderule, btn_battlemoderule_rect = load_image('PvP-Battle.png', 150, 50, -1)
    r_btn_battlemoderule, r_btn_battlemoderule_rect = load_image(*resize('PvP-Battle.png', 150, 50, -1))
    
    
    # 배경 이미지, 일단 인트로 사진으로 대체
    Background, Background_rect = load_image('winter.png', width, height, -1)

    # 이지, 하드모드 버튼
    easymoderule_btn_rect.center = (width * 0.66, height * 0.5)
    btn_hardmoderule_rect.center = (width * 0.66, height * 0.75)
    # 러닝, 배틀모드 버튼
    btn_runningmoderule_rect.center = (width * 0.33, height * 0.5)
    btn_battlemoderule_rect.center = (width * 0.33, height * 0.75)


    while not done:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                game_start = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    x, y = event.pos
                    if r_easyrule_btn_rect.collidepoint(x, y):
                        gamerule_image()

                    if r_btn_hardmoderule_rect.collidepoint(x, y):
                        gamerule_image()

                    if r_btn_runningmoderule_rect.collidepoint(x, y):
                        gamerule_image()
                    
                    if r_btn_battlemoderule_rect.collidepoint(x, y):
                        gamerule_image()

            if event.type == pygame.VIDEORESIZE:
                check_scr_size(event.w, event.h)

        r_easyrule_btn_rect.centerx, r_easyrule_btn_rect.centery = resized_screen.get_width() * 0.66, resized_screen.get_height() * 0.5
        r_btn_hardmoderule_rect.centerx, r_btn_hardmoderule_rect.centery = resized_screen.get_width() * 0.66, resized_screen.get_height() * (
                0.75)
        r_btn_runningmoderule_rect.centerx, r_btn_runningmoderule_rect.centery = resized_screen.get_width() * 0.33, resized_screen.get_height() * (
                0.5)
        r_btn_battlemoderule_rect.centerx, r_btn_battlemoderule_rect.centery = resized_screen.get_width() * 0.33, resized_screen.get_height() * (
                0.75)

        
        screen.blit(Background, Background_rect)
        screen.blit(TextSurf, TextRect)
        screen.blit(easymoderule_btn_image, easymoderule_btn_rect)
        screen.blit(btn_hardmoderule, btn_hardmoderule_rect)
        screen.blit(btn_runningmoderule, btn_runningmoderule_rect)
        screen.blit(btn_battlemoderule, btn_battlemoderule_rect)


        resized_screen.blit(
            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
            resized_screen_center)
        pygame.display.update()

        clock.tick(FPS)
    pygame.quit()
    quit()


def gamerule_image():
    global resized_screen
    game_quit = False
    max_per_screen = 10
    screen_board_height = resized_screen.get_height()
    screen_board = pygame.surface.Surface((
        resized_screen.get_width(),
        screen_board_height
        ))

    gamerule_image, gamerule_rect= load_image("gamerule.png",800,300,-1)
    gamerule_rect.centerx=width*0.5
    gamerule_rect.centery=height*0.5

    while not game_quit:
        if pygame.display.get_surface() is None:
            game_quit = True
        else:
            screen_board.fill(background_col)
            screen_board.blit(gamerule_image,gamerule_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_quit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        game_quit = True
                        # intro_screen()
                        option()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        game_quit = True
                        # intro_screen()
                        option()
                if event.type == pygame.VIDEORESIZE:
                    check_scr_size(event.w, event.h)

            screen.blit(screen_board, (0,0))
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())), resized_screen_center)
            pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

def pausing():
    global resized_screen
    game_quit = False
    pause_pic, pause_pic_rect = load_image('paused.png', 360, 75, -1)
    pause_pic_rect.centerx = width * 0.5
    pause_pic_rect.centery = height * 0.2

    pygame.mixer.music.pause()  # 일시정지상태가 되면 배경음악도 일시정지

    # BUTTON IMG LOAD
    retbutton_image, retbutton_rect = load_image('main_button.png', 70, 62, -1)
    resume_image, resume_rect = load_image('continue_button.png', 70, 62, -1)

    resized_retbutton_image, resized_retbutton_rect = load_image(*resize('main_button.png', 70, 62, -1))
    resized_resume_image, resized_resume_rect = load_image(*resize('continue_button.png', 70, 62, -1))

    # BUTTONPOS
    retbutton_rect.centerx = width * 0.4;
    retbutton_rect.top = height * 0.52
    resume_rect.centerx = width * 0.6;
    resume_rect.top = height * 0.52

    resized_retbutton_rect.centerx = resized_screen.get_width() * 0.4
    resized_retbutton_rect.top = resized_screen.get_height() * 0.52
    resized_resume_rect.centerx = resized_screen.get_width() * 0.6
    resized_resume_rect.top = resized_screen.get_height() * 0.52

    while not game_quit:
        if pygame.display.get_surface() is None:
            print("Couldn't load display surface")
            game_quit = True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_quit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.unpause()  # pausing상태에서 다시 esc누르면 배경음악 일시정지 해제
                        return False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        x, y = event.pos
                        if resized_retbutton_rect.collidepoint(x, y):
                            intro_screen()

                        if resized_resume_rect.collidepoint(x, y):
                            pygame.mixer.music.unpause()  # pausing상태에서 오른쪽의 아이콘 클릭하면 배경음악 일시정지 해제

                            return False

                if event.type == pygame.VIDEORESIZE:
                    check_scr_size(event.w, event.h)

            screen.fill(white)
            screen.blit(pause_pic, pause_pic_rect)
            screen.blit(retbutton_image, retbutton_rect)
            screen.blit(resume_image, resume_rect)
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                resized_screen_center)
            pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()


def type_score(score):
    global resized_screen
    global gamername
    global width, height
    done = False
    active = True

    message_pos = (width * 0.25, height * 0.3)
    score_pos = (width * 0.35, height * 0.4)
    inputbox_pos = (width * 0.43, height * 0.5)
    typebox_size = 100
    letternum_restriction = 3
    input_box = pygame.Rect(inputbox_pos[0], inputbox_pos[1], 500, 50)
    color = pygame.Color('dodgerblue2')

    text = ''
    text2 = font.render("플레이어 이름을 입력해주세요", True, black)
    text3 = font.render(f"CURRENT SCORE: {score}", True, black)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                intro_screen()
            if event.type == pygame.KEYDOWN:
                # if active:
                if event.key == pygame.K_RETURN:
                    gamername = text.upper()
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if event.unicode.isalpha() == True:
                        if len(text) < letternum_restriction:
                            text += event.unicode

            if event.type == pygame.VIDEORESIZE:
                check_scr_size(event.w, event.h)

        screen.fill(white)
        txt_surface = text_size(50).render(text.upper(), True, color)
        input_box.w = typebox_size
        screen.blit(txt_surface, (input_box.centerx - len(text) * 11 - 5, input_box.y))
        screen.blit(text2, message_pos)
        screen.blit(text3, score_pos)
        pygame.draw.rect(screen, color, input_box, 2)
        resized_screen.blit(
            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
            resized_screen_center)

        pygame.display.flip()
        clock.tick(FPS)


def credit():
    global resized_screen
    done = False
    creditimg, creditimg_rect = load_image('credit.png', width, height, -1)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                return False
            if event.type == pygame.VIDEORESIZE:
                check_scr_size(event.w, event.h)
        screen.fill(white)
        screen.blit(creditimg, creditimg_rect)
        resized_screen.blit(
            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
            resized_screen_center)
        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()
    quit()

# =====================================================================================================
