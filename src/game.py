from pygame.image import load
from src.dino import *
from src.obstacle import *
from src.item import *
from src.interface import *
# from src.option import *
import src.setting as setting
from src.game_value import *
from db.db_interface import InterfDB
from src.store import store
from src.pvp import *
from src.pvprunning import *
from time import sleep
import threading
import time
db = InterfDB("db/data.db")

## 시작 화면 ##
def intro_screen():
    global resized_screen
    global temp_dino
    global dino_type
    dino_type = ['ORIGINAL']
    global game_quit
    
    temp_dino = Dino(dino_size[0], dino_size[1])
    temp_dino.is_blinking = True
    game_start = False
    background, background_rect  = load_image('intro_background.png', width, height)
    # 버튼 이미지 (pvp모드에 대한 p 주석)
    r_btn_gamestart, r_btn_gamestart_rect = load_image(*resize('game_start.png', INTRO_BTN_X, INTRO_BTN_Y, -1))
    btn_gamestart, btn_gamestart_rect = load_image('game_start.png', INTRO_BTN_X,INTRO_BTN_Y, -1)
    r_btn_board, r_btn_board_rect = load_image(*resize('score_board.png', INTRO_BTN_X, INTRO_BTN_Y, -1))
    btn_board, btn_board_rect = load_image('score_board.png', INTRO_BTN_X, INTRO_BTN_Y, -1)
    r_btn_store, r_btn_store_rect = load_image(*resize('store.png', INTRO_BTN_X, INTRO_BTN_Y, -1))
    btn_store, btn_store_rect = load_image('store.png', INTRO_BTN_X, INTRO_BTN_Y, -1)
    r_btn_option, r_btn_option_rect = load_image(*resize('option.png', INTRO_BTN_X, INTRO_BTN_Y, -1))
    btn_option, btn_option_rect = load_image('option.png', INTRO_BTN_X, INTRO_BTN_Y, -1)
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
                        game_quit = True
                        intro_screen()
                    if event.key == pygame.K_r:
                        check_scr_size(799,399)
                        

                # 버튼 클릭했을 때 event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        x, y = event.pos
                        #game button
                        if r_btn_gamestart_rect.collidepoint(x, y):
                            temp_dino.movement[1] = -1 * temp_dino.jump_speed
                            game_start = True
                            select_mode()
                        #store button
                        if r_btn_store_rect.collidepoint(x, y):
                            store()
                        #board button
                        if r_btn_board_rect.collidepoint(x, y):
                            board()
                        # option button
                        if r_btn_option_rect.collidepoint(x, y):
                            option()
                # intro 화면 resize관련 부분 추가
                if event.type == pygame.VIDEORESIZE:
                    check_scr_size(event.w, event.h)

        # interface draw
        if pygame.display.get_surface() is not None:
            r_btn_gamestart_rect.centerx = resized_screen.get_width() * INTRO_RESIZE_X
            r_btn_board_rect.centerx = resized_screen.get_width() * INTRO_RESIZE_X
            r_btn_store_rect.centerx = resized_screen.get_width() * INTRO_RESIZE_X
            r_btn_option_rect.centerx = resized_screen.get_width() * INTRO_RESIZE_X

            r_btn_gamestart_rect.centery = resized_screen.get_height() * (INTRO_RESIZE_Y)
            r_btn_board_rect.centery = resized_screen.get_height() * (INTRO_RESIZE_Y + INTRO_RESIZE_INTERVER * button_offset)
            r_btn_store_rect.centery = resized_screen.get_height() * (INTRO_RESIZE_Y + 2*INTRO_RESIZE_INTERVER * button_offset)
            r_btn_option_rect.centery = resized_screen.get_height() * (INTRO_RESIZE_Y + 3*INTRO_RESIZE_INTERVER * button_offset)
            screen.blit(background, background_rect)
            disp_intro_buttons(btn_gamestart, btn_board, btn_store, btn_option)


            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())), resized_screen_center)
            pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()



def option():
    global on_pushtime
    global off_pushtime
    global bgm_on
    global hard_high_score
    global easy_high_score
    global resized_screen
    btnpush_interval = 500  # ms
    pygame.mixer.music.stop()
    done = False
    db_init = False
    large_text = pygame.font.Font('freesansbold.ttf', 60)
    text_surf, text_rect = load_image("option_word.png", 300, 75, -1)
    btn_bgm_on, btn_bgm_on_rect = load_image('btn_bgm_on.png', OPTION_BTN, OPTION_BTN, -1)
    btn_bgm_off, btn_bgm_off_rect = load_image('btn_bgm_off.png', OPTION_BTN, OPTION_BTN, -1)
    r_btn_bgm_on, r_btn_bgm_on_rect = load_image(*resize('btn_bgm_on.png', OPTION_BTN, OPTION_BTN, -1))
    init_btn_image, init_btn_rect = load_image('scorereset.png', OPTION_BTN, OPTION_BTN, -1)
    r_init_btn_image, r_init_btn_rect = load_image(*resize('scorereset.png', OPTION_BTN, OPTION_BTN, -1))
    btn_gamerule, btn_gamerule_rect = load_image('btn_gamerule.png', OPTION_BTN, OPTION_BTN, -1)
    r_btn_gamerule, r_btn_gamerule_rect = load_image(*resize('btn_gamerule.png', OPTION_BTN, OPTION_BTN, -1))
    btn_credit, btn_credit_rect = load_image('btn_credit.png', INTRO_BTN_X, INTRO_BTN_Y, -1)
    r_btn_credit, r_btn_credit_rect = load_image(*resize('btn_credit.png', INTRO_BTN_X, INTRO_BTN_Y, -1))
    # 버튼 이미지
    back_btn_image, back_btn_rect = load_image('back.png', BACK_BTN_X, BACK_BTN_Y, -1)
    r_back_btn_image, r_back_btn_rect = load_image(*resize('back.png', BACK_BTN_X, BACK_BTN_Y, -1))

    text_rect.center = (width * 0.5, height * 0.15)
    btn_bgm_on_rect.center = (width * 0.25, height * 0.5)
    init_btn_rect.center = (width * 0.5, height * 0.5)
    btn_gamerule_rect.center = (width * 0.75, height * 0.5)
    back_btn_rect =  (width * BACK_BTN_SIZE, height * BACK_BTN_SIZE)
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
                    if r_back_btn_rect.collidepoint(x, y):
                        intro_screen()

                    if r_btn_bgm_on_rect.collidepoint(x, y) and bgm_on:
                        off_pushtime = pygame.time.get_ticks()
                        if off_pushtime - on_pushtime > btnpush_interval:
                            bgm_on = False

                    if r_btn_bgm_on_rect.collidepoint(x, y) and not bgm_on:
                        on_pushtime = pygame.time.get_ticks()
                        if on_pushtime - off_pushtime > btnpush_interval:
                            bgm_on = True

                    if r_init_btn_rect.collidepoint(x, y):
                        db.query_db("delete from hard_mode;")
                        db.query_db("delete from easy_mode")
                        db.commit()
                        easy_high_score = 0
                        hard_high_score = 0
                        db_init = True

                    if r_btn_gamerule_rect.collidepoint(x, y):
                        gamerule()

                    if r_btn_credit_rect.collidepoint(x, y):
                        credit()

            if event.type == pygame.VIDEORESIZE:
                check_scr_size(event.w, event.h)

        r_init_btn_rect.centerx = resized_screen.get_width() * 0.5
        r_init_btn_rect.centery = resized_screen.get_height() * 0.5
        r_btn_gamerule_rect.centerx = resized_screen.get_width() * 0.75
        r_btn_gamerule_rect.centery = resized_screen.get_height() * 0.5
        r_btn_credit_rect.centerx = resized_screen.get_width() * 0.9
        r_btn_credit_rect.centery = resized_screen.get_height() * 0.85
        r_back_btn_rect.centerx, r_back_btn_rect.centery = resized_screen.get_width() * BACK_BTN_RECT, resized_screen.get_height() * BACK_BTN_SIZE

        screen.fill(background_col)
        screen.blit(text_surf, text_rect)
        screen.blit(init_btn_image, init_btn_rect)
        screen.blit(btn_gamerule, btn_gamerule_rect)
        screen.blit(back_btn_image, back_btn_rect)
        screen.blit(btn_credit, btn_credit_rect)

        if bgm_on:
            screen.blit(btn_bgm_on, btn_bgm_on_rect)
            r_btn_bgm_on_rect.centerx = resized_screen.get_width() * 0.25
            r_btn_bgm_on_rect.centery = resized_screen.get_height() * 0.5
        if not bgm_on:
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
    back_btn_image, back_btn_rect = load_image('back.png', BACK_BTN_X, BACK_BTN_Y, -1)
    r_back_btn_image, r_back_btn_rect = load_image(*resize('back.png', BACK_BTN_X, BACK_BTN_Y, -1))
    ##easy mode button
    easymode_btn_image, easymode_btn_rect = load_image('easy_mode.png', INTRO_BTN_X, INTRO_BTN_Y, -1)
    r_easymode_btn_image, r_easy_btn_rect = load_image(*resize('easy_mode.png', INTRO_BTN_X, INTRO_BTN_Y, -1))
    # hardmode button
    btn_hardmode, btn_hardmode_rect = load_image('hard_mode.png', INTRO_BTN_X, INTRO_BTN_Y, -1)
    r_btn_hardmode, r_btn_hardmode_rect = load_image(*resize('hard_mode.png', INTRO_BTN_X, INTRO_BTN_Y, -1))
    # runningmode button, 임시로 hardmode 이미지로 진행
    btn_runningmode, btn_runningmode_rect = load_image('pvp_running.png', INTRO_BTN_X, INTRO_BTN_Y, -1)
    r_btn_runningmode, r_btn_runningmode_rect = load_image(*resize('pvp_running.png', INTRO_BTN_X, INTRO_BTN_Y, -1))
    # battlemode button, 임시로 hardmode 이미지로 진행
    btn_battlemode, btn_battlemode_rect = load_image('pvp_battle.png', INTRO_BTN_X, INTRO_BTN_Y, -1)
    r_btn_battlemode, r_btn_battlemode_rect = load_image(*resize('pvp_battle.png', INTRO_BTN_X, INTRO_BTN_Y, -1))
    
     
    # 배경 이미지
    Background, Background_rect = load_image('intro_background.png', width, height, -1)

    # 뒤로가기 버튼
    back_btn_rect =  (width * BACK_BTN_SIZE, height * BACK_BTN_SIZE)
    # 이지, 하드모드 버튼
    easymode_btn_rect.center = (width * SINGLE_BTN_SIZE_X, height * SELECT_BTN_H * 2)
    btn_hardmode_rect.center = (width * SINGLE_BTN_SIZE_X, height * SELECT_BTN_H * 3)
    # 러닝, 배틀모드 버튼
    btn_runningmode_rect.center = (width * MULTI_BTN_SIZE_X, height * SELECT_BTN_H * 2)
    btn_battlemode_rect.center = (width * MULTI_BTN_SIZE_X, height * SELECT_BTN_H * 3)


    while not game_start:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                game_start = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    intro_screen()
                if event.key == pygame.K_r:
                    pvp_check_scr_size(1200,400)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    x, y = event.pos
                    if r_back_btn_rect.collidepoint(x, y):
                        intro_screen()

                    if r_easy_btn_rect.collidepoint(x, y):
                        gameplay_easy()
                    if r_btn_hardmode_rect.collidepoint(x, y):
                        gameplay_hard()

                    if r_btn_runningmode_rect.collidepoint(x, y):
                        pvprunning()
                    
                    if r_btn_battlemode_rect.collidepoint(x, y):
                        resized_screen.blit(
                            pygame.transform.scale(screen, (1200,400)),
                            resized_screen_center)
                        pygame.display.update()
                        pvp()
                        

            if event.type == pygame.VIDEORESIZE:
                check_scr_size(event.w, event.h)
        r_back_btn_rect.centerx, r_back_btn_rect.centery = resized_screen.get_width() * BACK_BTN_RECT, resized_screen.get_height() * BACK_BTN_SIZE
        r_easy_btn_rect.centerx, r_easy_btn_rect.centery = resized_screen.get_width() * SINGLE_BTN_SIZE_X, resized_screen.get_height() * SELECT_BTN_H*2
        r_btn_hardmode_rect.centerx, r_btn_hardmode_rect.centery = resized_screen.get_width() * SINGLE_BTN_SIZE_X, resized_screen.get_height() * (
                SELECT_BTN_H*3)
        r_btn_runningmode_rect.centerx, r_btn_runningmode_rect.centery = resized_screen.get_width() * MULTI_BTN_SIZE_X, resized_screen.get_height() * (
                SELECT_BTN_H*2)
        r_btn_battlemode_rect.centerx, r_btn_battlemode_rect.centery = resized_screen.get_width() * MULTI_BTN_SIZE_X, resized_screen.get_height() * (
                SELECT_BTN_H*3)

        
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
    global easy_high_score
    spring_image, spring_rect = load_image('ex_spring.png', EASY_BACK_W, EASY_BACK_H, -1)
    r_spring_image, r_spring_rect = load_image(*resize('ex_spring.png', EASY_BACK_W, EASY_BACK_H, -1))
    screen.blit(spring_image, spring_rect)
    result = None
    result = db.query_db("select score from easy_mode order by score desc;", one=True)
    if result is not None:
        easy_high_score = result['score']
    if bgm_on:
        pygame.mixer.music.play(-1) # 배경음악 실행
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

    counter = 0

    cacti = pygame.sprite.Group()
    fire_cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    stones = pygame.sprite.Group()

    last_obstacle = pygame.sprite.Group()
    # shield_items = pygame.sprite.Group()
    life_items = pygame.sprite.Group()
    slow_items = pygame.sprite.Group()
    # highjump_items = pygame.sprite.Group()
    # 아이템 추가 11/08
    # mask_items = pygame.sprite.Group()

    Stone.containers = stones
    Cactus.containers = cacti
    fire_Cactus.containers = fire_cacti
    Ptera.containers = pteras
    Cloud.containers = clouds
    # ShieldItem.containers = shield_items
    LifeItem.containers = life_items
    SlowItem.containers = slow_items

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
                            if player_dino.rect.bottom == int(DEFAULT_HEIGHT * height):
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
                        if pygame.mouse.get_pressed() == (1, 0, 0) and player_dino.rect.bottom == int(DEFAULT_HEIGHT * height):
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
                # shield_items.update()
                life_items.update()
                new_ground.update()
                scb.update(player_dino.score)
                highsc.update(easy_high_score)
                heart.update(life)
                slow_items.update()
                stones.update()

                if pygame.display.get_surface() != None:
                    screen.fill(background_col)
                    new_ground.draw()
                    clouds.draw(screen)
                    scb.draw()

                    heart.draw()
                    if easy_high_score != 0:
                        highsc.draw()
                        screen.blit(high_image, high_rect)
                    cacti.draw(screen)
                    stones.draw(screen)
                    fire_cacti.draw(screen)
                    pteras.draw(screen)
                    # shield_items.draw(screen)
                    life_items.draw(screen)
                    slow_items.draw(screen)
                    player_dino.draw()
                    resized_screen.blit(
                        pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                        resized_screen_center)
                    pygame.display.update()
                clock.tick(FPS)

                if player_dino.is_dead:
                    game_over = True
                    pygame.mixer.music.stop()  # 죽으면 배경음악 멈춤
                    if player_dino.score > easy_high_score:
                        easy_high_score = player_dino.score
                        

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
                            if easy_high_score > player_dino.score:
                                type_score(player_dino.score)
                                if not db.is_limit_data(player_dino.score, mode = "easy"):
                                    db.query_db(
                                        f"insert into easy_mode (username, score) values ('{gamer_name}', '{player_dino.score}');")
                                    db.commit()
                                    board("easy")
                                else:
                                    board("easy")
                            else:
                                highscore_page(player_dino, "easy")

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        game_over = False
                        game_quit = True
                        if easy_high_score > player_dino.score:
                            type_score(player_dino.score)
                            if not db.is_limit_data(player_dino.score, mode = "easy"):
                                db.query_db(
                                    f"insert into easy_mode (username, score) values ('{gamer_name}', '{player_dino.score}');")
                                db.commit()
                                board("easy")
                            else:
                                board("easy")
                        else:
                            highscore_page(player_dino, "easy")

                    if event.type == pygame.VIDEORESIZE:
                        check_scr_size(event.w, event.h)

            highsc.update(easy_high_score)
            if pygame.display.get_surface() != None:
                disp_gameover_msg(game_over_image)
                if easy_high_score != 0:
                        highsc.draw()
                        screen.blit(high_image, high_rect)
                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                    resized_screen_center)
                pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()

def gameplay_hard():
    global resized_screen
    global hard_high_score
    global game_over
    global paused
    result = None
    result = db.query_db("select score from hard_mode order by score desc;", one=True)
    if result is not None:
        hard_high_score = result['score']

    # HERE: REMOVE SOUND!!    
    if bgm_on:
        pygame.mixer.music.play(-1)  # 배경음악 실행
    
    game_speed = GAME_SPEED
    startMenu = False
    game_over = False
    game_quit = False
    paused = False
    global is_super_time
    global super_rest_time
    is_super_time = False
    super_rest_time = ITEM_TIME


    ###
    stage = 1
    life = LIFE
    pking_life = PKING_LIFE # 보스 목숨
    life_item_count = db.query_db("select count from item where name='life';", one=True)['count']
    slow_item_count = db.query_db("select count from item where name='slow';", one=True)['count']
    coin_item_count = db.query_db("select count from item where name='coin';", one=True)['count']


    type_idx = 0
    type_idx2 = 0
    player_dino = Dino(dino_size[0], dino_size[1],type=dino_type[type_idx])
    #배경 변경하는 코드
    
    if type_idx2 ==0:
        new_background = ImgBack(-1 * game_speed, "spring")
    new_ground = Ground(-1 * game_speed)

    scb = Scoreboard( y = height * SCB_HEIGHT)
    highsc = Scoreboard(width * SCB_WIDTH, height * SCB_HEIGHT)
    heart = HeartIndicator(player_dino.life)
    speed_indicator = Scoreboard(width * INDICATOR_X, height * INDICATOR_Y)
    counter = 0
    speed_text = font.render("SPEED", True, black)

    item_back, item_back_rect = alpha_image('item_back.png', ITEM_BACK_WIDTH *0.75, ITEM_BACK_HEIGHT, -1)
    (item_back_rect.centerx, item_back_rect.top) = (width * ITEM_BACK_X, ITEM_BACK_Y)
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()
    # shield_items = pygame.sprite.Group()
    life_items = pygame.sprite.Group()
    slow_items = pygame.sprite.Group()
    coin_items = pygame.sprite.Group()

    obst_container(type_idx2)
    Ptera.containers = pteras
    Cloud.containers = clouds
    # ShieldItem.containers = shield_items
    LifeItem.containers = life_items
    SlowItem.containers = slow_items
    CoinItem.containers = coin_items

    # BUTTON IMG LOAD
    game_over_image, game_over_rect = load_image('game_over.png', OVER_X, OVER_Y, -1)
    heart_item_image, heart_item_rect = load_image('love-shield.png', GAME_ITEM_DISP, GAME_ITEM_DISP, -1)
    slow_item_image, slow_item_rect = load_sprite_sheet('slow_pic.png', 2, 1, GAME_ITEM_DISP, GAME_ITEM_DISP, -1)
    coin_image, coin_rect = load_sprite_sheet('coin.png', 1, 7, GAME_ITEM_DISP, GAME_ITEM_DISP, -1)
    
    my_font = pygame.font.Font('DungGeunMo.ttf', 30)
    high_image = my_font.render('HI', True, black)
    high_rect = high_image.get_rect()
    high_rect.top = height * HARD_HI_HEIGHT
    high_rect.left = width * HARD_HI_WIDTH

    # 1. 미사일 발사.
    space_go=False
    m_list=[]
    bk=0
    # 익룡이 격추되었을때
    is_down=False
    boom_count=0
    # 방향키 구현
    go_left=False
    go_right=False
    
    # 보스몬스터 변수설정
    is_pking_time=False
    is_pking_alive=True
    pking=PteraKing()

    pm_list = []
    pm_vector = []
    pm_pattern0_count = 0
    pm_pattern1_count = 0
    global rest_time
    rest_time = REST_TIME_10
    pking_appear()
    
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
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:  
                            # 스페이스 누르는 시점에 공룡이 땅에 닿아있으면 점프한다.
                            if player_dino.rect.bottom == int(DEFAULT_HEIGHT * height):
                                player_dino.is_jumping = True
                                if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                                player_dino.movement[1] = -1 * player_dino.jump_speed
                        if event.key == pygame.K_DOWN:  
                            # 아래방향키를 누르는 시점에 공룡이 점프중이지 않으면 숙인다.
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

                        # life item
                        if event.key == pygame.K_w:
                            if life_item_count > 0 and player_dino.life < LIFE:
                                # if pygame.mixer.get_init() is not None:
                                    # check_point_sound.play()
                                player_dino.increase_life()
                                life_item_count -= 1
                        # slow item
                        if event.key == pygame.K_e:
                            if slow_item_count > 0 and game_speed > 4:
                                # if pygame.mixer.get_init() is not None:
                                    # check_point_sound.play()
                                game_speed -= SPEED_RATE
                                new_ground.speed += SPEED_RATE
                                new_background.speed += SPEED_RATE
                                slow_item_count -= 1

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            player_dino.is_ducking = False
                        # 3.a키에서 손을 떼면, 미사일이 발사 되지 않습니다.
                        if event.key == pygame.K_a:
                            space_go = False
                        # 방향키 추가
                        if event.key == pygame.K_LEFT:
                            go_left=False
                        if event.key == pygame.K_RIGHT:
                            go_right=False
                        ## jumgpingx2
                        if event.key == pygame.K_s:
                            jumpingx2 = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed() == (1, 0, 0) and player_dino.rect.bottom == int(DEFAULT_HEIGHT * height):
                            player_dino.is_jumping = True
                            if pygame.mixer.get_init() != None:
                                jump_sound.play()
                            player_dino.movement[1] = -1 * player_dino.jump_speed
                        if pygame.mouse.get_pressed() == (0, 0, 1):
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
                    mm.put_img("./sprites/red_bullet.png")
                    mm.change_size(10,10)
                    
                    
                    if player_dino.is_ducking ==False:
                        mm.x = round(player_dino.rect.centerx)
                        mm.y = round(player_dino.rect.top*1.035)
                    if player_dino.is_ducking ==True:
                        mm.x = round(player_dino.rect.centerx)
                        mm.y = round(player_dino.rect.centery*1.01)
                    mm.move = 15
                    m_list.append(mm)
                bk = bk + 1
                d_list=[]
                for i in range(len(m_list)):
                    m = m_list[i]
                    m.x += m.move
                    if m.x > width:
                        d_list.append(i)
                d_list.reverse()
                for d in d_list:
                    del m_list[d]

                if jumpingx2 :
                    if  player_dino.rect.bottom == int(height * DEFAULT_HEIGHT):
                        player_dino.is_jumping = True
                        player_dino.movement[1] = -1 * player_dino.super_jump_speed

                # 보스 몬스터 패턴0(위에서 가만히 있는 패턴): 보스 익룡이 쏘는 미사일.
                if (is_pking_time) and (pking.pattern_idx == 0) and (int(pm_pattern0_count % 20) == 0):
                    pm=Obj()
                    pm.put_img("./sprites/orange_bullet.png")
                    pm.change_size(12,12)
                    pm.x = round(pking.rect.centerx)
                    pm.y = round(pking.rect.centery)
                    pm.x_move = random.randint(0, 15)
                    pm.y_move = random.randint(1, 3)
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
                # 보스 몬스터 패턴1(좌우로 왔다갔다 하는 패턴): 보스 익룡이 쏘는 미사일.
                if (is_pking_time) and (pking.pattern_idx == 1) and (int(pm_pattern1_count % 20) == 0):
                    pm=Obj()
                    pm.put_img("./sprites/orange_bullet.png")
                    pm.change_size(12,12)
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
                # 장애물1
                for o in obst1:
                    o.movement[0] = -1 * game_speed
                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, o):
                            player_dino.collision_immune = True
                            player_dino.decrease_life()
                            collision_time = pygame.time.get_ticks()
                            if player_dino.is_life_zero():
                                player_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()
                    elif not player_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player_dino.collision_immune = False
                for o in obst2:
                    o.movement[0] = -1 * game_speed
                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, o):
                            player_dino.collision_immune = True
                            player_dino.decrease_life()
                            collision_time = pygame.time.get_ticks()
                            if player_dino.is_life_zero():
                                player_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()
                    elif not player_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player_dino.collision_immune = False
                for o in obst3:
                    o.movement[0] = -1 * game_speed
                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, o):
                            player_dino.collision_immune = True
                            player_dino.decrease_life()
                            collision_time = pygame.time.get_ticks()
                            if player_dino.is_life_zero():
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

                    if not player_dino.collision_immune:
                        if pygame.sprite.collide_mask(player_dino, p):
                            player_dino.collision_immune = True
                            player_dino.decrease_life()
                            collision_time = pygame.time.get_ticks()
                            if player_dino.is_life_zero():
                                player_dino.is_dead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not player_dino.is_super:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            player_dino.collision_immune = False
                for c in coin_items:
                    c.movement[0] = -1 * game_speed
                    if pygame.sprite.collide_mask(player_dino, c):
                        # if pygame.mixer.get_init() is not None:
                        #     check_point_sound.play()
                        coin_item_count += 1
                        c.kill()
                    elif l.rect.right < 0:
                        c.kill()

                for c in life_items:
                    c.movement[0] = -1 * game_speed
                    if pygame.sprite.collide_mask(player_dino, c):
                        # if pygame.mixer.get_init() is not None:
                        #     check_point_sound.play()
                        life_item_count += 1
                        c.kill()
                    elif l.rect.right < 0:
                        c.kill()

                if is_pking_alive and (rest_time <= PKING_APPEARANCE_TIME):
                    is_pking_time = True
                else:
                    is_pking_time = False

                if len(coin_items) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(COIN_INTERVAL) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(CoinItem(game_speed, object_size[0], object_size[1]))                

                if len(life_items) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(LIFEITEM_INTERVAL) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(LifeItem(game_speed, object_size[0], object_size[1]))
                
                
                
                if is_pking_time:
                    if len(obst1) < 2:
                        # 하나도 안들어있으면
                        if len(obst1) == 0:
                            # last_obstacle 비우고
                            last_obstacle.empty()
                            # 장애물 1 넣는다. (사이즈는 object_size로 지정)
                            last_obstacle.add(obst(type_idx2, 1, game_speed))
                        else:
                            # 장애물1이 한개 들어있으면
                            for l in last_obstacle:
                                # refreshLine 후에 오고, rand.randrange(인터벌 == magicnum이면 비우고 다시 하나 넣기
                                if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(OBST1_INTERVAL) == MAGIC_NUM:
                                    last_obstacle.empty()
                                    last_obstacle.add(obst(type_idx2, 1, game_speed))

                    if len(obst2) < 2:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(OBST2_INTERVAL * 5) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(obst(type_idx2, 2, game_speed))

                    if len(obst3) < 2:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(OBST3_INTERVAL * 3) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(obst(type_idx2, 3, game_speed))
                    # 봄, 가을, 겨울에는 구름 아이콘이 나타나지 않게 한다.
                    if type_idx2 == 0:
                        if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                            Cloud(width, random.randrange(height / 5, height / 2))
                    if len(m_list) == 0:
                        pass
                    else:
                        if (m.x >= pking.rect.left) and (m.x <= pking.rect.right) and (m.y > pking.rect.top) and (
                                m.y < pking.rect.bottom):
                            is_down = True
                            boom = Obj()
                            boom.put_img("./sprites/boom.png")
                            boom.change_size(200, 100)
                            boom.x = pking.rect.centerx - round(pking.rect.width)
                            boom.y = pking.rect.centery - round(pking.rect.height / 2)
                            pking.decrease_life()
                            m_list.remove(m)
                            if pking.life <= 0:
                                pking.kill()
                                stage += 1
                                rest_time = REST_TIME_10
                                new_ground.speed -= SPEED_RATE
                                new_background.speed -= SPEED_RATE
                                game_speed += SPEED_RATE
                                pking_life *= PKING_LIFE_INCREASE_RATE
                                pking_life = int(pking_life)
                                pking = PteraKing(life=pking_life)

                    if len(pm_list) == 0:
                        pass
                    else:
                        for pm in pm_list:
                            if (pm.x >= player_dino.rect.left) and (pm.x <= player_dino.rect.right) and (
                                    pm.y > player_dino.rect.top) and (pm.y < player_dino.rect.bottom):
                                if not player_dino.collision_immune:
                                    player_dino.collision_immune = True
                                    player_dino.decrease_life()
                                    collision_time = pygame.time.get_ticks()
                                    if player_dino.is_life_zero():
                                        player_dino.is_dead = True
                                    if pygame.mixer.get_init() is not None:
                                        die_sound.play()
                                elif not player_dino.is_super:
                                    immune_time = pygame.time.get_ticks()
                                    if immune_time - collision_time > collision_immune_time:
                                        player_dino.collision_immune = False
                                pm_list.remove(pm)
                else:
                    # 장애물1
                    if len(obst1) < 2:
                        # 하나도 안들어있으면
                        if len(obst1) == 0:
                            # last_obstacle 비우고
                            last_obstacle.empty()
                            # 장애물 1 넣는다. (사이즈는 object_size로 지정)
                            last_obstacle.add(obst(type_idx2, 1, game_speed))
                        else:
                            # 장애물1이 한개 들어있으면
                            for l in last_obstacle:
                                # refreshLine 후에 오고, rand.randrange(인터벌 == magicnum이면 비우고 다시 하나 넣기
                                if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(OBST1_INTERVAL) == MAGIC_NUM:
                                    last_obstacle.empty()
                                    last_obstacle.add(obst(type_idx2, 1, game_speed))

                    if len(obst2) < 2:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(OBST2_INTERVAL * 5) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(obst(type_idx2, 2, game_speed))

                    if len(obst3) < 2:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(OBST3_INTERVAL * 3) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(obst(type_idx2, 3, game_speed))
                    if len(pteras) == 0 and random.randrange(PTERA_INTERVAL) == MAGIC_NUM and counter > PTERA_INTERVAL:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE:
                                last_obstacle.empty()
                                last_obstacle.add(Ptera(game_speed, ptera_size[0], ptera_size[1]))
                    # 봄, 가을, 겨울에는 구름 아이콘이 나타나지 않게 한다.
                    if type_idx2 == 0:
                        if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                            Cloud(width, random.randrange(height / 5, height / 2))
                player_dino.update()
                obst1.update()
                obst2.update()
                obst3.update()
                pteras.update()
                if type_idx2 == 0:
                    clouds.update()
                # shield_items.update()
                life_items.update()
                new_background.update()
                new_ground.update()
                scb.update(player_dino.score)
                highsc.update(hard_high_score)
                speed_indicator.update(game_speed - 3)
                heart.update(player_dino.life)
                slow_items.update()
                coin_items.update()

                if is_super_time:
                    player_dino.is_super = True
                if super_rest_time ==0:
                    is_super_time = False
                    player_dino.add_score = False

                # 보스몬스터 타임이면,
                if is_pking_time:
                    pking.update()
                if pygame.display.get_surface() != None:
                    screen.fill(background_col)
                    new_background.draw()
                    new_ground.draw()
                    clouds.draw(screen)
                    scb.draw()
                    speed_indicator.draw()
                    screen.blit(speed_text, (width * 0.01, height * 0.15))
                    screen.blit(item_back, item_back_rect)
                    screen.blit(coin_image[0], (width * 0.35, height * HARD_ITEM_HEIGHT))
                    screen.blit(heart_item_image, (width * (0.35 + HARD_ITEM_OFF), height * HARD_ITEM_HEIGHT))
                    screen.blit(slow_item_image[0], (width * (0.35 + 2 * HARD_ITEM_OFF), height * HARD_ITEM_HEIGHT))

                    life_item_count_text = small_font.render(f"x{life_item_count}", True, black)
                    soldout_life_text = small_font.render(f"x{life_item_count}", True, deep_red)
                    slow_item_count_text = small_font.render(f"x{slow_item_count}", True, black)
                    soldout_slow_text = small_font.render(f"x{slow_item_count}", True, deep_red)
                    coin_count_text = small_font.render(f"x{coin_item_count}", True, black)
                    
                    screen.blit(coin_count_text, (width * 0.39, height * 0.02))
                    if life_item_count == 0:
                        screen.blit(soldout_life_text, (width * (0.39 + HARD_ITEM_OFF ),
                                                        height * HARD_ITEM_HEIGHT))
                    else:
                        screen.blit(life_item_count_text, (width * (0.39 + HARD_ITEM_OFF),
                                                           height * HARD_ITEM_HEIGHT))
                    if slow_item_count == 0:
                        screen.blit(soldout_slow_text, (width * (0.39 + 2 * HARD_ITEM_OFF ),
                                                        height * HARD_ITEM_HEIGHT))
                    else:
                        screen.blit(slow_item_count_text, (width * (0.39 +2* HARD_ITEM_OFF ),
                                                           height * HARD_ITEM_HEIGHT))
                    heart.draw()
  
                    if hard_high_score != 0:
                        highsc.draw()
                        screen.blit(high_image, high_rect)
                    obst1.draw(screen)
                    obst2.draw(screen)
                    obst3.draw(screen)
                    pteras.draw(screen)
                    life_items.draw(screen)
                    slow_items.draw(screen)
                    coin_items.draw(screen)
                    # pkingtime이면, 보스몬스터를 보여줘라.
                    if is_pking_time:
                        # print(pking.pattern_idx)
                        pking.draw()
                        # 보스 익룡이 쏘는 미사일을 보여준다.
                        for pm in pm_list:
                            pm.show()
                    # 5. 미사일 배열에 저장된 미사일들을 게임 스크린에 그려줍니다.
                    for m in m_list:
                        m.show()
                        # print(type(mm.x))
                    if is_down:
                        boom.show()
                        boom_count += 1
                        # boom_count가 5가 될 때까지 boom이미지를 계속 보여준다.
                        if boom_count > 10:
                            boom_count = 0
                            is_down = False
                    player_dino.draw()
                    resized_screen.blit(
                        pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                        resized_screen_center)
                    pygame.display.update()
                clock.tick(FPS)
                if player_dino.is_dead:
                    game_over = True
                    pygame.mixer.music.stop()  # 죽으면 배경음악 멈춤
                    if player_dino.score > hard_high_score:
                        hard_high_score = player_dino.score
                counter += 1

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
                            game_over = False
                            intro_screen()

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or pygame.MOUSEBUTTONDOWN:
                            game_over = False
                            game_quit = True
                            rest_time = REST_TIME_10
                            if not db.is_limit_data(player_dino.score, mode="hard"):
                                db.query_db(
                                    f"UPDATE item set count = {life_item_count} where name ='life';"
                                )
                                db.query_db(
                                    f"UPDATE item SET count = {slow_item_count} where name ='slow';"
                                )
                                db.query_db(
                                    f"UPDATE item SET count = {coin_item_count} where name= 'coin';"
                                )
                                db.commit()
                                if hard_high_score > player_dino.score:
                                    type_score(player_dino.score)
                                    if not db.is_limit_data(player_dino.score, mode = "hard"):
                                        db.query_db(
                                            f"insert into hard_mode (username, score) values ('{gamer_name}', '{player_dino.score}');")
                                        db.commit()
                                        board("hard")
                                    else:
                                        board("hard")
                                else:
                                    highscore_page(player_dino, "hard")
                            else:
                                board("hard")

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            rest_time = 1
                            x, y = event.pos
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or pygame.MOUSEBUTTONDOWN:
                                if not db.is_limit_data(player_dino.score, mode="hard"):
                                    # db.query_db(
                                    #     f" UPDATE item set count = {shield_item_count} where name ='shield';")
                                    db.query_db(
                                        f"UPDATE item set count = {life_item_count} where name ='life';"
                                    )
                                    db.query_db(
                                        f"UPDATE item SET count = {slow_item_count} where name ='slow';"
                                    )
                                    db.query_db(
                                        f"UPDATE item SET count = {coin_item_count} where name= 'coin';"
                                    )
                                    db.commit()
                                    if hard_high_score > player_dino.score:
                                        type_score(player_dino.score)
                                        if not db.is_limit_data(player_dino.score, mode = "hard"):
                                            db.query_db(
                                                f"insert into hard_mode (username, score) values ('{gamer_name}', '{player_dino.score}');")
                                            db.commit()
                                            board("hard")
                                        else:
                                            board("hard")
                                    else:
                                        highscore_page(player_dino, "hard")
                                else:
                                    board("hard")
        

                    if event.type == pygame.VIDEORESIZE:
                        check_scr_size(event.w, event.h)

            highsc.update(hard_high_score)
            if pygame.display.get_surface() != None:
                disp_gameover_msg(game_over_image)
                if high_score != 0:
                    highsc.draw()
                    screen.blit(high_image, high_rect)
                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                    resized_screen_center)
                pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()
def board(mode=""):
    global resized_screen
    game_quit = False
    scroll_y=0
    max_per_screen = 5
    length = 0
    results = ""
    if mode == "":
        easy_mode_results = db.query_db(f"select username, score from easy_mode order by score desc;")
        hard_mode_results = db.query_db(f"select username, score from hard_mode order by score desc;")
        length = len(easy_mode_results) if len(easy_mode_results) > len(hard_mode_results) else len(hard_mode_results)
    else:
        results = db.query_db(f"select username, score from {mode}_mode order by score desc;")
        length = len(results)
    screen_board_height = resized_screen.get_height() + (length // max_per_screen) * resized_screen.get_height()
    screen_board = pygame.surface.Surface((
        resized_screen.get_width(),
        screen_board_height
    ))

    title_image, title_rect = load_image("ranking.png", RANKING_WIDTH, RANKING_HEIGHT, -1)
    title_rect.centerx = width * RANKING_X
    title_rect.centery = height * RANKING_Y

    # 버튼 이미지
    btn_back, btn_back_rect = load_image('back.png', BACK_BTN_X, BACK_BTN_Y, -1)
    r_btn_back, r_btn_back_rect = load_image(*resize('back.png', BACK_BTN_X, BACK_BTN_Y, -1))

    while not game_quit:
        if pygame.display.get_surface() is None:
            game_quit = True
        else:
            screen_board.fill(background_col)
            screen_board.blit(title_image, title_rect)
            screen_board.blit(btn_back, btn_back_rect)

            if results:
                for i, result in enumerate(results):
                    top_i_surface = font.render(f"TOP {i + 1}", True, dark_pink)
                    name_inform_surface = font.render("Name", True, black)
                    score_inform_surface = font.render("Score", True, black)
                    score_surface = font.render(str(result['score']), True, black)
                    txt_surface = font.render(result['username'], True, black)

                    screen_board.blit(top_i_surface, (width * 0.25, height * (0.55 + RESULT_OFF * i)))
                    screen_board.blit(name_inform_surface, (width * 0.4, height * 0.40))
                    screen_board.blit(score_inform_surface, (width * 0.6, height * 0.40))
                    screen_board.blit(txt_surface, (width * 0.4, height * (0.55 + RESULT_OFF * i)))
                    screen_board.blit(score_surface, (width * 0.6, height * (0.55 + RESULT_OFF * i)))
            else:
                easy_mode_surface = font.render(f"[Easy Mode]", True, black)
                hard_mode_surface = font.render(f"[Hard Mode]", True, black)
                screen_board.blit(easy_mode_surface, (width * 0.2, height * 0.35))
                screen_board.blit(hard_mode_surface, (width * 0.62, height * 0.35))
                for i, result in enumerate(easy_mode_results):
                    top_i_surface = font.render(f"TOP {i + 1}", True, dark_pink)
                    name_inform_surface = font.render("Name", True, black)
                    score_inform_surface = font.render("Score", True, black)
                    score_surface = font.render(str(result['score']), True, black)
                    txt_surface = font.render(result['username'], True, black)

                    screen_board.blit(top_i_surface, (width * 0.05, height * (0.55 + RESULT_OFF * i)))
                    screen_board.blit(name_inform_surface, (width * 0.2, height * RESULT_HEIGHT))
                    screen_board.blit(score_inform_surface, (width * (0.2 + RESULT_X_OFF), height * RESULT_HEIGHT))
                    screen_board.blit(txt_surface, (width * 0.2, height * (0.55 + RESULT_OFF * i)))
                    screen_board.blit(score_surface, (width * (0.2 + RESULT_X_OFF), height * (0.55 + RESULT_OFF * i)))

                for i, result in enumerate(hard_mode_results):
                    top_i_surface = font.render(f"TOP {i + 1}", True, dark_blue)
                    name_inform_surface = font.render("Name", True, black)
                    score_inform_surface = font.render("Score", True, black)
                    score_surface = font.render(str(result['score']), True, black)
                    txt_surface = font.render(result['username'], True, black)

                    screen_board.blit(top_i_surface, (width * 0.5, height * (0.55 + RESULT_OFF * i)))
                    screen_board.blit(name_inform_surface, (width * 0.62, height * RESULT_HEIGHT))
                    screen_board.blit(score_inform_surface, (width * (0.62 + RESULT_X_OFF), height *RESULT_HEIGHT))
                    screen_board.blit(txt_surface, (width * 0.62, height * (0.55 + 0.1 * i)))
                    screen_board.blit(score_surface, (width * (0.62 + RESULT_X_OFF), height * (0.55 + RESULT_OFF * i)))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_quit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        intro_screen()
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        game_quit = True
                        intro_screen()
                    if event.key == pygame.K_UP:
                        scroll_y = min(scroll_y + SCROLL, 0)
                    if event.key == pygame.K_DOWN:
                        scroll_y = max(scroll_y - SCROLL, -(length // max_per_screen) * scr_size[1])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        x, y = event.pos
                        if r_btn_back_rect.collidepoint(x, y):
                            intro_screen()
                    if event.button == 4:
                        scroll_y = min(scroll_y + SCROLL, 0)
                    if event.button == 5:
                        scroll_y = max(scroll_y - SCROLL, -(length // max_per_screen) * scr_size[1])

                if event.type == pygame.VIDEORESIZE:
                    check_scr_size(event.w, event.h)
            
            btn_back_rect =  (width * BACK_BTN_SIZE, height * BACK_BTN_SIZE)
            r_btn_back_rect.center = (resized_screen.get_width() * BACK_BTN_RECT,resized_screen.get_height() * BACK_BTN_SIZE)
            
            score_board(btn_back)
            screen.blit(btn_back, btn_back_rect)
            screen.blit(screen_board, (0, scroll_y))
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                resized_screen_center)
            pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

def gamerule():
    global resized_screen
    done = False
    btnpush_interval = 500

    largeText = pygame.font.Font('freesansbold.ttf', 60)
    TextSurf, TextRect = load_image("control_word.png", 350, 75, -1)

    TextRect.center = (width * 0.5, height * 0.2)

    # 버튼 이미지

    ##easy mode button
    easymoderule_btn_image, easymoderule_btn_rect = load_image('easy_mode.png', INTRO_BTN_X, INTRO_BTN_Y, -1)
    r_easymoderule_btn_image, r_easyrule_btn_rect = load_image(*resize('easy_mode.png', INTRO_BTN_X, INTRO_BTN_Y, -1))
    # hardmode button
    btn_hardmoderule, btn_hardmoderule_rect = load_image('hard_mode.png', INTRO_BTN_X, INTRO_BTN_Y, -1)
    r_btn_hardmoderule, r_btn_hardmoderule_rect = load_image(*resize('hard_mode.png', INTRO_BTN_X, INTRO_BTN_Y, -1))
    # runningmode button, 임시로 hardmode 이미지로 진행
    btn_runningmoderule, btn_runningmoderule_rect = load_image('pvp_running.png', INTRO_BTN_X, INTRO_BTN_Y, -1)
    r_btn_runningmoderule, r_btn_runningmoderule_rect = load_image(*resize('pvp_running.png', INTRO_BTN_X, INTRO_BTN_Y, -1))
    # battlemode button, 임시로 hardmode 이미지로 진행
    btn_battlemoderule, btn_battlemoderule_rect = load_image('pvp_battle.png', INTRO_BTN_X, INTRO_BTN_Y, -1)
    r_btn_battlemoderule, r_btn_battlemoderule_rect = load_image(*resize('pvp_battle.png', INTRO_BTN_X, INTRO_BTN_Y, -1))
    #back 버튼
    btn_home, btn_home_rect = load_image('back.png', BACK_BTN_X, BACK_BTN_Y, -1)
    r_btn_home, r_btn_home_rect = load_image(*resize('back.png', BACK_BTN_X, BACK_BTN_Y, -1))
    
    # 배경 이미지, 일단 인트로 사진으로 대체
    Background, Background_rect = load_image('no_name_background.png', width, height)

    # 이지, 하드모드 버튼
    easymoderule_btn_rect.center = (width * SINGLE_BTN_SIZE_X, height * SELECT_BTN_H*2)
    btn_hardmoderule_rect.center = (width * SINGLE_BTN_SIZE_X, height * SELECT_BTN_H*3)
    # 러닝, 배틀모드 버튼
    btn_runningmoderule_rect.center = (width * MULTI_BTN_SIZE_X, height * SELECT_BTN_H*2)
    btn_battlemoderule_rect.center = (width * MULTI_BTN_SIZE_X, height * SELECT_BTN_H*3)
    btn_home_rect = (width * BACK_BTN_SIZE, height * BACK_BTN_SIZE)

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
                    if r_btn_home_rect.collidepoint(x, y):
                        option()

                    if r_easyrule_btn_rect.collidepoint(x, y):
                        gamerule_image("easy")

                    if r_btn_hardmoderule_rect.collidepoint(x, y):
                        gamerule_image("hard")

                    if r_btn_runningmoderule_rect.collidepoint(x, y):
                        gamerule_image("running")
                    
                    if r_btn_battlemoderule_rect.collidepoint(x, y):
                        gamerule_image("battle")

            if event.type == pygame.VIDEORESIZE:
                check_scr_size(event.w, event.h)

        r_easyrule_btn_rect.centerx, r_easyrule_btn_rect.centery = resized_screen.get_width() * SINGLE_BTN_SIZE_X, resized_screen.get_height() * SELECT_BTN_H*2
        r_btn_hardmoderule_rect.centerx, r_btn_hardmoderule_rect.centery = resized_screen.get_width() * SINGLE_BTN_SIZE_X, resized_screen.get_height() * (
                SELECT_BTN_H*3)
        r_btn_runningmoderule_rect.centerx, r_btn_runningmoderule_rect.centery = resized_screen.get_width() * MULTI_BTN_SIZE_X, resized_screen.get_height() * (
                SELECT_BTN_H*2)
        r_btn_battlemoderule_rect.centerx, r_btn_battlemoderule_rect.centery = resized_screen.get_width() * MULTI_BTN_SIZE_X, resized_screen.get_height() * (
                SELECT_BTN_H*3)
        r_btn_home_rect.center = (resized_screen.get_width() * BACK_BTN_RECT,resized_screen.get_height() * BACK_BTN_SIZE)
        
        
        screen.blit(Background, Background_rect)
        screen.blit(TextSurf, TextRect)
        screen.blit(easymoderule_btn_image, easymoderule_btn_rect)
        screen.blit(btn_hardmoderule, btn_hardmoderule_rect)
        screen.blit(btn_runningmoderule, btn_runningmoderule_rect)
        screen.blit(btn_battlemoderule, btn_battlemoderule_rect)
        screen.blit(btn_home, btn_home_rect)

        resized_screen.blit(
            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
            resized_screen_center)
        pygame.display.update()

        clock.tick(FPS)
    pygame.quit()
    quit()


def gamerule_image(mode = ""):
    global resized_screen
    game_quit = False
    screen_board_height = resized_screen.get_height()
    screen_board = pygame.surface.Surface((
        resized_screen.get_width(),
        screen_board_height
        ))
    if mode == "easy":
        gamerule_image, gamerule_rect= load_image("easy_mode_rule.png",800,400,-1)
    elif mode == "hard":
        gamerule_image, gamerule_rect= load_image("hard_mode_rule.png",800,400,-1)
    elif mode == "battle":
        gamerule_image, gamerule_rect= load_image("pvp_battle_rule.png",800,400,-1)
    elif mode == "running":
        gamerule_image, gamerule_rect= load_image("pvp_running_rule.png",800,400,-1)
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
                        if mode == "easy":
                            gamerule()
                        elif mode == "hard":
                            gamerule_image2("hard")
                        elif mode == "battle":
                            gamerule_image2("battle")
                        elif mode == "running":
                            gamerule_image2("running")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        game_quit = True
                        if mode == "easy":
                            print(mode)
                            gamerule()
                        else:
                            gamerule_image2(mode)
                if event.type == pygame.VIDEORESIZE:
                    check_scr_size(event.w, event.h)

            screen.blit(screen_board, (0,0))
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())), resized_screen_center)
            pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()


def gamerule_image2(mode = ""):
    global resized_screen
    game_quit = False
    screen_board_height = resized_screen.get_height()
    screen_board = pygame.surface.Surface((
        resized_screen.get_width(),
        screen_board_height
        ))

    if mode == "battle":
        gamerule_image, gamerule_rect= load_image("pvp_battle_rule_item.png",800,400,-1)
    elif mode == "running":
        gamerule_image, gamerule_rect= load_image("pvp_running_rule_item.png",800,400,-1)
    elif mode == "hard":
        gamerule_image, gamerule_rect= load_image("hard_mode_rule_item.png",800,400,-1)
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
                        gamerule()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        game_quit = True
                        gamerule()
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
    global game_start
    game_quit = False
    pause_pic, pause_pic_rect = load_image('paused.png', 360, 75, -1)
    pause_pic_rect.centerx = width * 0.5
    pause_pic_rect.centery = height * 0.2

    pygame.mixer.music.pause()  # 일시정지상태가 되면 배경음악도 일시정지
    # 배경 이미지
    back_store, back_store_rect = load_image('mode_background.png', width, height)
    alpha_back, alpha_back_rect = alpha_image('alpha_back.png', width + ALPHA_MOVE, height)
    alpha_back_rect.left = -ALPHA_MOVE
    # BUTTON IMG LOAD
    retbutton_image, retbutton_rect = load_image('home_btn.png', 150, 55, -1)
    resume_image, resume_rect = load_image('resume_button.png', 150, 55, -1)

    resized_retbutton_image, resized_retbutton_rect = load_image(*resize('home_btn.png', 150, 55, -1))
    resized_resume_image, resized_resume_rect = load_image(*resize('resume_button.png', 150, 55, -1))

    # BUTTONPOS
    retbutton_rect.centerx = width * 0.35
    retbutton_rect.top = height * 0.52
    resume_rect.centerx = width * 0.65
    resume_rect.top = height * 0.52

    resized_retbutton_rect.centerx = resized_screen.get_width() * 0.35
    resized_retbutton_rect.top = resized_screen.get_height() * 0.52
    resized_resume_rect.centerx = resized_screen.get_width() * 0.65
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
                            game_start = False
                            intro_screen()

                        if resized_resume_rect.collidepoint(x, y):
                            pygame.mixer.music.unpause()  # pausing상태에서 오른쪽의 아이콘 클릭하면 배경음악 일시정지 해제

                            return False

                if event.type == pygame.VIDEORESIZE:
                    check_scr_size(event.w, event.h)

            screen.blit(back_store, back_store_rect)
            screen.blit(alpha_back, alpha_back_rect)
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
    global gamer_name
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
                    gamer_name = text.upper()
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

def pking_appear():
        global game_over
        global paused
        if game_over:
            return
        if paused:
            return
        threading.Timer(ONE_SECOND,pking_appear).start()
        global rest_time
        rest_time -= 1
        if rest_time <= 0:
            rest_time = 0

# 스킨별 컨테이너 반환
def obst_container(type_idx):
    # 장애물 osbt1 obst2 obst3
    global obst1
    global obst2
    global obst3
    obst1 = pygame.sprite.Group()
    obst2 = pygame.sprite.Group()
    obst3 = pygame.sprite.Group()
    
    Cactus.containers = obst1
    FireCactus.containers = obst2
    Stone.containers = obst3


# 스킨별 장애물 반환
def obst(type_idx, obst_num, game_speed):
    if obst_num == 1:
        return Cactus(game_speed, object_size[0], object_size[1])
    elif obst_num == 2:
        return FireCactus(game_speed, object_size[0], object_size[1])
    else:
        return Stone(game_speed, object_size[0], object_size[1])

def highscore_page(player_dino, mode):
    global resized_screen
    game_quit = False
    max_per_screen = 10
    score_pos = (width * 0.3, height * 0.6)
    screen_board_height = resized_screen.get_height()
    screen_board = pygame.surface.Surface((
        resized_screen.get_width(),
        screen_board_height
        ))

    text = font.render(f"NEW HIGH SCORE : {player_dino.score}", True, black)

    highsc_image, highsc_rect = load_image("new-score.png",450,100,-1)
    highsc_rect.centerx=width*0.5
    highsc_rect.centery=height*0.25

    while not game_quit:
        if pygame.display.get_surface() is None:
            game_quit = True
        else:
            screen_board.fill(background_col)
            screen_board.blit(highsc_image,highsc_rect)
            screen_board.blit(text, score_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_quit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        game_quit = True
                        # intro_screen()
                        if mode == "easy":
                            type_score(player_dino.score)
                            db.query_db(
                                    f"insert into easy_mode (username, score) values ('{gamer_name}', '{player_dino.score}');")
                            db.commit()
                            board("easy")
                        elif mode == "hard":
                            type_score(player_dino.score)
                            db.query_db(
                                    f"insert into hard_mode (username, score) values ('{gamer_name}', '{player_dino.score}');")
                            db.commit()
                            board("hard")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        game_quit = True
                        # intro_screen()
                        if mode == "easy":
                            type_score(player_dino.score)
                            db.query_db(
                                    f"insert into easy_mode (username, score) values ('{gamer_name}', '{player_dino.score}');")
                            db.commit()
                            board("easy")
                        elif mode == "hard":
                            type_score(player_dino.score)
                            db.query_db(
                                    f"insert into hard_mode (username, score) values ('{gamer_name}', '{player_dino.score}');")
                            db.commit()
                            board("hard")
                if event.type == pygame.VIDEORESIZE:
                    check_scr_size(event.w, event.h)

            screen.blit(screen_board, (0,0))
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())), resized_screen_center)
            pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()
# =====================================================================================================
def super_appear():
        global game_over
        global paused
        global is_super_time
        if game_over:
            return
        if paused:
            return
        if  is_super_time == False:
            return
        
        threading.Timer(ONE_SECOND,super_appear).start()
        global super_rest_time
        super_rest_time -= 1
        if super_rest_time <= 0:
            super_rest_time = 0