import sys
import pygame
import os
from threading import Thread

import functional
from classes import Bullet, MyShip, EShip, Colors, Pattern

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Client")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


def menu():
    menus = ["Single Player", "Multiplayer", "Exit"]
    myFont = pygame.font.Font(None, 30)
    SelectedFont = pygame.font.Font(None, 40)
    pointer = 0
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                key_event = pygame.key.get_pressed()
                if key_event[pygame.K_ESCAPE]:
                    sys.exit()

                elif key_event[pygame.K_UP]:
                    pointer -= 1
                    if pointer < 0:
                        pointer = 0

                elif key_event[pygame.K_DOWN]:
                    pointer += 1
                    if pointer > 2:
                        pointer = 2

                elif key_event[pygame.K_RETURN] or key_event[pygame.K_SPACE]:
                    run = False
        background_a = pygame.image.load('./img/background.jpg')
        background_a = pygame.transform.scale(background_a, (900, 900))
        screen.fill(Colors.black)
        screen.blit(background_a, (0, 0))
        background = pygame.image.load('./img/start.png')
        background = pygame.transform.scale(background, (450, 300))
        screen.blit(background, (250, 100))
        for i in range(3):
            if i == pointer:
                text_Title = SelectedFont.render(menus[i], True, Colors.green)
            else:
                text_Title = myFont.render(menus[i], True, Colors.white)
            screen.blit(text_Title, [100, 300 + 100 * (i + 1)])
        pygame.display.flip()

    if pointer == 0:
        return main()
    elif pointer == 1:
        return multi_menu()
    else:
        return


def multi_menu():
    myFont = pygame.font.Font(None, 30)
    SelectedFont = pygame.font.Font(None, 40)
    run = True
    mode = [0, 0]
    pointer = 0
    player_cnt = 2
    flag = False
    menu_ = ["Host", "Join", "Return"]
    ip_addr = "127.0.0.1"
    port = "1234"
    tick = 0
    while run:
        clock.tick(60)
        background_a = pygame.image.load('./img/background.jpg')
        background_a = pygame.transform.scale(background_a, (900, 900))
        screen.fill(Colors.black)
        screen.blit(background_a, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                key_event = pygame.key.get_pressed()
                if key_event[pygame.K_UP]:
                    mode[pointer] -= 1
                    if mode[pointer] < 0:
                        mode[pointer] = 0

                if key_event[pygame.K_DOWN]:
                    mode[pointer] += 1
                    if pointer > 0:
                        if mode[pointer] > 2:
                            mode[pointer] = 2

                if key_event[pygame.K_RETURN]:
                    if pointer == 0:
                        pointer = 1
                    if mode[0] == 2:
                        run = False
                    if pointer == 1 and mode[1] == 2 and port.replace("|", "").isnumeric():
                        run = False

                if key_event[pygame.K_BACKSPACE]:
                    if mode[0] == 1:
                        if mode[1] == 0:
                            ip_addr = ip_addr[:-1]
                        else:
                            port = port[:-1]

                    if mode[0] == 0:
                        port = port[:-1]

                if key_event[pygame.K_ESCAPE]:
                    mode[1] = 0
                    if pointer == 1:
                        pointer -= 1
                    else:
                        run = False

                if key_event[pygame.K_RIGHT] and pointer == 1 and mode[0] == 0 and mode[1] == 1:
                    player_cnt += 1
                    if player_cnt > 4:
                        player_cnt = 4

                if key_event[pygame.K_LEFT] and pointer == 1 and mode[0] == 0 and mode[1] == 1:
                    player_cnt -= 1
                    if player_cnt < 2:
                        player_cnt = 2

            if event.type == pygame.TEXTINPUT and pointer == 1:
                if mode[0] == 1:
                    if mode[1] == 0:
                        ip_addr += event.text
                    else:
                        port += event.text

                if mode[0] == 0:
                    port += event.text

        for i in range(len(menu_)):
            if i == mode[0]:
                if pointer == 0:
                    text_Title = SelectedFont.render(menu_[i], True, Colors.green)
                else:
                    text_Title = SelectedFont.render(menu_[i], True, Colors.blue)
            else:
                text_Title = myFont.render(menu_[i], True, Colors.white)
            screen.blit(text_Title, [200, 100 * (i + 1)])

        if pointer == 1:
            tick += 1
            if mode[0] < 2:
                ip_addr = ip_addr.replace("|", "")
                port = port.replace("|", "")
                if mode[0] == 1:
                    if mode[1] == 0:
                        if flag: ip_addr += "|"
                    if mode[1] == 1:
                        if flag: port += "|"
                else:
                    if mode[1] == 0:
                        if flag: port += "|"
            if tick > 30:
                flag = not flag
                tick = 0

            if mode[0] == 1:
                text_Title = myFont.render("HOST: " + ip_addr, True, Colors.white)
                if mode[1] == 0:
                    text_Title = myFont.render("HOST: " + ip_addr, True, Colors.green)
                screen.blit(text_Title, [400, 100])
                text_Title = myFont.render("PORT: " + port, True, Colors.white)
                if mode[1] == 1:
                    text_Title = myFont.render("PORT: " + port, True, Colors.green)
                    if not port.replace("|", "").isnumeric():
                        text_Title = myFont.render("PORT: " + port, True, Colors.red)
                screen.blit(text_Title, [400, 200])
            if mode[0] == 0:
                text_Title = myFont.render("PORT: " + port, True, Colors.white)
                if mode[1] == 0:
                    text_Title = myFont.render("PORT: " + port, True, Colors.green)
                    if not port.replace("|", "").isnumeric():
                        text_Title = myFont.render("PORT: " + port, True, Colors.red)
                screen.blit(text_Title, [400, 100])
                text_Title = myFont.render("Players: < " + str(player_cnt) + ' >', True, Colors.white)
                if mode[1] == 1:
                    text_Title = myFont.render("Players: < " + str(player_cnt) + ' >', True, Colors.green)
                screen.blit(text_Title, [400, 200])

            text_Title = myFont.render("OKAY", True, Colors.white)
            if mode[1] == 2:
                text_Title = myFont.render("OKAY", True, Colors.green)
            screen.blit(text_Title, [400, 300])

        pygame.display.flip()

    if mode[0] == 2:
        return menu()

    port = port.replace("|", "")
    port = int(port)
    ip_addr = ip_addr.replace("|", "")
    if mode[0] == 0:
        return main(player=player_cnt, port=port, server=True)
    if mode[0] == 1:
        return main(host=ip_addr, port=port)


def main(player=1, host="127.0.0.1", port=1234, server=False):
    t1 = Thread(target=functional.start_server, args=[player, port])
    t1.daemon = True

    bullet_delay = 10
    client_num = 0
    client = functional.Client(host, port)

    myFont = pygame.font.Font(None, 30)
    background_a = pygame.image.load('./img/background.jpg')
    background_a = pygame.transform.scale(background_a, (900, 900))
    screen.fill(Colors.black)
    screen.blit(background_a, (0, 0))
    text_Title = myFont.render("Waiting for connection", True, Colors.green)
    screen.blit(text_Title, [400, 300])
    pygame.display.flip()

    if player == 1:
        t1.start()
    else:
        if server:
            t1.start()

    client.connect_server()
    client_num = int(client.recieve())

    life = 10
    cnt, tick = 0, 0
    myships, bullets, ships, destroyed, life_c, score = client.download()
    destro = []
    pygame.mixer.music.load('./sounds/shot.wav')

    expload = pygame.image.load('./img/fire.png')
    expload = pygame.transform.scale(expload, (50, 30))

    life_img = pygame.image.load('./img/life.png')
    life_img = pygame.transform.scale(life_img, (20, 20))
    run = True
    while run:
        cnt += 1
        tick += 1
        clock.tick(60)
        bullets = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        key_event = pygame.key.get_pressed()
        if key_event[pygame.K_ESCAPE]:
            run = False

        if key_event[pygame.K_LEFT]:
            myships[client_num].change_position(-2, 0)

        if key_event[pygame.K_RIGHT]:
            myships[client_num].change_position(2, 0)

        if key_event[pygame.K_UP]:
            myships[client_num].change_position(0, -2)

        if key_event[pygame.K_DOWN]:
            myships[client_num].change_position(0, 2)

        if key_event[pygame.K_SPACE] and cnt > bullet_delay:
            cnt = 0
            bullets.append(Bullet(myships[client_num].get_pos_x(), myships[client_num].get_pos_y(), -3))

        screen.blit(background_a, (0, 0))

        client.upload(myships[client_num], bullets)
        temp_score = score
        myships, bullets, ships, destroyed, life_c, score = client.download()
        if life_c != 0:
            pygame.mixer.music.play(1)
        if temp_score != score:
            pygame.mixer.music.play(1)
        temp = []
        for i in destroyed:
            destro.append([i[0], i[1], tick])
        for i in destro:
            if tick - i[2] < 20 or 40 < tick - i[2] < 60:
                screen.blit(expload, (i[0] - 15, i[1] - 15))
            if tick - i[2] > 60:
                temp.append(i)
        for i in temp:
            destro.remove(i)
        for i in ships + bullets + myships:
            i.draw(screen)

        life -= life_c
        for i in range(life):
            screen.blit(life_img, (30 + i * 30, 850))

        text_Title = myFont.render("SCORE:" + str(len(score)), True, Colors.white)
        screen.blit(text_Title, [50, 50])

        pygame.display.flip()
        if life <= 0:
            text_Title = myFont.render("GAME OVER\n RETRY? \nPRESS Y / N", True, Colors.white)
            screen.blit(text_Title, [400, 400])
            if key_event[pygame.K_y]:
                menu()
            elif key_event[pygame.K_n]:
                sys.exit()

    client.close()
    os.execl(sys.executable, sys.executable, *sys.argv)




menu()
