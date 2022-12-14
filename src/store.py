from src.item import *
from src.interface import *
from db.db_interface import InterfDB
from src.game_value import *
db = InterfDB("db/data.db")
import src.game

global user_font
user_font = pygame.font.Font('DungGeunMo.ttf', 16)


def store():
    global resized_screen
    game_start = False

    # 배경 이미지
    back_store, back_store_rect = load_image('intro_background.png', width, height)
    alpha_back, alpha_back_rect = alpha_image('alpha_back.png', width + ALPHA_MOVE, height)
    alpha_back_rect.left = -ALPHA_MOVE
    # 버튼 이미지
    item_btn_image, item_btn_rect = load_image('item_btn.png', INTRO_BTN_X, INTRO_BTN_Y, -1)
    r_item_btn_image, r_item_btn_rect = load_image(*resize('item_btn.png', INTRO_BTN_X, INTRO_BTN_Y, -1))
    # 뒤로 가기 버튼 이미지
    back_btn_image, back_btn_rect = load_image('back.png', BACK_BTN_X, BACK_BTN_Y, -1)
    r_back_btn_image, r_back_btn_rect = load_image(*resize('back.png', BACK_BTN_X, BACK_BTN_Y, -1))

    # 뒤로가기 버튼
    back_btn_rect =  (width * BACK_BTN_SIZE, height * BACK_BTN_SIZE)

    while not game_start:
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE and not full_screen:
                back_store_rect.bottomleft = (width * 0, height)
            if event.type == pygame.VIDEORESIZE:
                check_scr_size(event.w, event.h)
            if event.type == pygame.QUIT:
                game_start = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    x, y = pygame.mouse.get_pos()
                    if r_item_btn_rect.collidepoint(x, y):
                        item_store()
                    if r_back_btn_rect.collidepoint(x, y):
                        src.game.intro_screen()

        r_item_btn_rect.centerx = resized_screen.get_width() * (0.5)
        r_item_btn_rect.centery = resized_screen.get_height() * 0.5

        screen.blit(back_store, back_store_rect)
        screen.blit(alpha_back, alpha_back_rect)
        disp_store_buttons(item_btn_image, back_btn_image)
        resized_screen.blit(
            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
            resized_screen_center)
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    quit()


def item_store():
    global resized_screen
    image_space = 0.3
    game_start = False
    # 배경 이미지
    back_store, back_store_rect = load_image('no_name_background.png', width, height)
    alpha_back, alpha_back_rect = alpha_image('alpha_back.png', width + ALPHA_MOVE, height)
    alpha_back_rect.left = -ALPHA_MOVE
    # 코인 이미지
    coin2_image, _ = load_sprite_sheet('coin.png', 1, 7, -1, -1, -1)
    coin2_image = transform.scale(coin2_image[0], (COIN_SIZE, COIN_SIZE))
    coin2_rect = coin2_image.get_rect()
    coin3_image, _ = load_sprite_sheet('coin.png', 1, 7, -1, -1, -1)
    coin3_image = transform.scale(coin3_image[0], (COIN_SIZE, COIN_SIZE))
    coin3_rect = coin3_image.get_rect()
    # 아이템 이미지
    life_image, life_rect = load_image('love-shield.png', ITEM_SIZE, ITEM_SIZE, -1)
    time_image, _ = load_sprite_sheet('slow_pic.png', 2, 1, -1, -1, -1)
    time_image = transform.scale(time_image[0], (ITEM_SIZE, ITEM_SIZE))
    time_rect = time_image.get_rect()
    # # user가 가지고 있는 아이템 노출을 위한 이미지
    user_life_image, user_life_rect = load_image('love-shield.png', USER_ITEM_SIZE, USER_ITEM_SIZE, -1)
    user_time_image, _ = load_sprite_sheet('slow_pic.png', 2, 1, -1, -1, -1)
    user_time_image = transform.scale(user_time_image[0], (USER_ITEM_SIZE, USER_ITEM_SIZE))
    user_time_rect = user_time_image.get_rect()
    user_coin_image, _ = load_sprite_sheet('coin.png', 1, 7, -1, -1, -1)
    user_coin_image = transform.scale(user_coin_image[0], (USER_ITEM_SIZE, USER_ITEM_SIZE))
    user_coin_rect = user_coin_image.get_rect()
    
    # item store 버튼 이미지
    buy_btn2_image, buy_btn2_rect = load_image('buy.png', STORE_BTN_X, STORE_BTN_Y, -1)
    r_buy_btn2_image, r_buy_btn2_rect = load_image(*resize('buy.png', STORE_BTN_X, STORE_BTN_Y, -1))
    buy_btn3_image, buy_btn3_rect = load_image('buy.png', STORE_BTN_X, STORE_BTN_Y, -1)
    r_buy_btn3_image, r_buy_btn3_rect = load_image(*resize('buy.png', STORE_BTN_X, STORE_BTN_Y, -1))
    no_money2_image, no_money2_rect = load_image('X.png', STORE_BTN_X, STORE_BTN_Y, -1)
    no_money3_image, no_money3_rect = load_image('X.png', STORE_BTN_X, STORE_BTN_Y, -1)
    
    # 뒤로 가기 버튼 이미지
    back_btn_image, back_btn_rect = load_image('back.png', BACK_BTN_X, BACK_BTN_Y, -1)
    r_back_btn_image, r_back_btn_rect = load_image(*resize('back.png', BACK_BTN_X, BACK_BTN_Y, -1))

    # 뒤로가기 버튼
    back_btn_rect =  (width * BACK_BTN_SIZE, height * BACK_BTN_SIZE)

    # 아이템
    life_item_count = db.query_db("select count from item where name='life';", one=True)['count']
    slow_item_count = db.query_db("select count from item where name='slow';", one=True)['count']
    coin_item_count = db.query_db("select count from item where name='coin';", one=True)['count']
    
    # 가격
    l_price = db.query_db("SELECT price from item where name = 'life'", one=True)['price']
    t_price = db.query_db("SELECT price from item where name = 'slow'", one=True)['price']
    
    # 폰트
    my_font = pygame.font.Font('DungGeunMo.ttf', 18)

    # user_font = pygame.font.Font('DungGeunMo.ttf', 16)
    life_price = my_font.render(f'x {l_price}', True, black)
    time_price = my_font.render(f'x {t_price}', True, black)
    
    # info = my_font.render(f"[YOU HAVE]", True, black)
    user_life = user_font.render(f'X{life_item_count}', True, black)
    user_time = user_font.render(f'X{slow_item_count}', True, black)
    user_coin = user_font.render(f'X{coin_item_count}', True, black)

    # 배치
    (life_rect.centerx, life_rect.centery) = (width * (STORE_ITEM_X), height * STORE_ITEM_Y)
    (coin2_rect.centerx, coin2_rect.centery) = (width * (STORE_ITEM_X-0.02), height * (STORE_ITEM_Y + item_price_offset))
    life_price_rect = life_price.get_rect(center=(width * (STORE_ITEM_X+0.03), height * (STORE_ITEM_Y + item_price_offset)))
    (buy_btn2_rect.centerx, buy_btn2_rect.centery) = (width * (STORE_ITEM_X), height * (STORE_ITEM_Y + item_btn_offset))
    (no_money2_rect.centerx, no_money2_rect.centery) = (width * (STORE_ITEM_X), height * (STORE_ITEM_Y + item_btn_offset))

    (time_rect.centerx, time_rect.centery) = (width * (STORE_ITEM_X + btn_offset), height * STORE_ITEM_Y)
    (coin3_rect.centerx, coin3_rect.centery) = (width * (STORE_ITEM_X -0.02 + btn_offset), height * (STORE_ITEM_Y + item_price_offset))
    time_price_rect = time_price.get_rect(center=(width * (STORE_ITEM_X + 0.03 + btn_offset), height * (STORE_ITEM_Y + item_price_offset)))
    (buy_btn3_rect.centerx, buy_btn3_rect.centery) = (
                                                    width * (STORE_ITEM_X + btn_offset), height * (STORE_ITEM_Y + item_btn_offset))
    (no_money3_rect.centerx, no_money3_rect.centery) = (
                                                    width * (STORE_ITEM_X + btn_offset), height * (STORE_ITEM_Y + item_btn_offset))
    #
    user_count_offset = 0.04
    user_btn_offset = 0.09
    (user_life_rect.centerx, user_life_rect.centery) = (width * (STORE_ITEM2_X + user_btn_offset), height * STORE_ITEM2_Y)
    user_l_rect = user_life.get_rect(center=(width * (STORE_ITEM2_X + user_btn_offset + user_count_offset), height * STORE_ITEM2_Y))
    (user_time_rect.centerx, user_time_rect.centery) = (width * (STORE_ITEM2_X + 2 * user_btn_offset), height * STORE_ITEM2_Y)
    user_t_rect = user_time.get_rect(center=(width * (STORE_ITEM2_X + (2 * user_btn_offset) + user_count_offset), height * STORE_ITEM2_Y))
    (user_coin_rect.centerx, user_coin_rect.centery) = (width * (STORE_ITEM2_X + 3 * user_btn_offset), height * STORE_ITEM2_Y)
    user_c_rect = user_coin.get_rect(center=(width * (STORE_ITEM2_X + (3 * user_btn_offset) + user_count_offset), height * STORE_ITEM2_Y))

    while not game_start:
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE and not full_screen:
                back_store_rect.bottomleft = (width * 0, height)
            if event.type == pygame.VIDEORESIZE:
                check_scr_size(event.w, event.h)
            if event.type == pygame.QUIT:
                game_start = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if pygame.mouse.get_pressed() == (1, 0, 0):
                x, y = pygame.mouse.get_pos()
                if r_back_btn_rect.collidepoint(x, y):
                    store()
                if r_buy_btn2_rect.collidepoint(x, y) and coin_item_count >= l_price:
                    db.query_db(
                        f"UPDATE item SET count = {life_item_count + 1} where name = 'life'"
                    )
                    db.query_db(
                        f"UPDATE item SET count = {coin_item_count - l_price} where name = 'coin'"
                    )
                    db.commit()
                if r_buy_btn3_rect.collidepoint(x, y) and coin_item_count >= t_price:
                    db.query_db(
                        f"UPDATE item SET count = {slow_item_count + 1} where name = 'slow'"
                    )
                    db.query_db(
                        f"UPDATE item SET count = {coin_item_count - t_price} where name = 'coin'"
                    )
                    db.commit()
        (r_buy_btn2_rect.centerx, r_buy_btn2_rect.centery) = (resized_screen.get_width() * (STORE_ITEM_X),
                                                          resized_screen.get_height() * (STORE_ITEM_Y + item_btn_offset))
        (r_buy_btn3_rect.centerx, r_buy_btn3_rect.centery) = (resized_screen.get_width() * (STORE_ITEM_X + btn_offset),
                                                          resized_screen.get_height() * (STORE_ITEM_Y + item_btn_offset))

        life_item_count = db.query_db("select count from item where name='life';", one=True)['count']
        slow_item_count = db.query_db("select count from item where name='slow';", one=True)['count']
        coin_item_count = db.query_db("select count from item where name='coin';", one=True)['count']

        user_life = user_font.render(f'X{life_item_count}', True, black)
        user_time = user_font.render(f'X{slow_item_count}', True, black)
        user_coin = user_font.render(f'X{coin_item_count}', True, black)

        screen.blit(back_store, back_store_rect)
        screen.blit(alpha_back, alpha_back_rect)

        screen.blit(coin2_image, coin2_rect)
        screen.blit(coin3_image, coin3_rect)

        screen.blit(life_image, life_rect)
        screen.blit(time_image, time_rect)

        screen.blit(user_life_image, user_life_rect)
        screen.blit(user_life, user_l_rect)
        screen.blit(user_time_image, user_time_rect)
        screen.blit(user_time, user_t_rect)
        screen.blit(user_coin_image, user_coin_rect)
        screen.blit(user_coin, user_c_rect)


        if (coin_item_count >= l_price):
            screen.blit(buy_btn2_image, buy_btn2_rect)
        else:
            screen.blit(no_money2_image, no_money2_rect)
        if (coin_item_count >= t_price):
            screen.blit(buy_btn3_image, buy_btn3_rect)
        else:
            screen.blit(no_money3_image, no_money3_rect)
        screen.blit(life_price, life_price_rect)
        screen.blit(time_price, time_price_rect)
        screen.blit(back_btn_image, back_btn_rect)
        resized_screen.blit(
            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
            resized_screen_center)
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    quit()
