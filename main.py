import sys
import pygame
from threading import Thread

import functional
from classes import Bullet, MyShip, EShip, Colors, Pattern

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900

pygame.init()
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

                if key_event[pygame.K_UP]:
                    pointer -= 1
                    if pointer < 0:
                        pointer = 0

                if key_event[pygame.K_DOWN]:
                    pointer += 1
                    if pointer > 2:
                        pointer = 2

                if key_event[pygame.K_RETURN] or key_event[pygame.K_SPACE]:
                    run = False

        screen.fill(Colors.black)
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
    while True:
        screen.fill(Colors.black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                key_event = pygame.key.get_pressed()
                if key_event[pygame.K_ESCAPE]:
                    sys.exit()

                if key_event[pygame.K_UP]:
                    pointer -= 1
                    if pointer < 0:
                        pointer = 0

                if key_event[pygame.K_DOWN]:
                    pointer += 1
                    if pointer > 2:
                        pointer = 2

                if key_event[pygame.K_RETURN] or key_event[pygame.K_SPACE]:
                    run = False
        text_Title = myFont.render("Number of Players", True, Colors.white)
        screen.blit(text_Title, [100, 200])


def main(player=1):
    t1 = Thread(target=functional.start_server, args=[player])
    t1.daemon = True

    bullet_delay = 10
    client_num = 0
    client = functional.Client()
    client.init()

    if player == 1:
        t1.start()

    client.connect_server()
    client_num = int(client.recieve())

    myFont = pygame.font.Font(None, 30)

    def display():
        life = 10
        cnt, tick = 0, 0
        myships, bullets, ships, destroyed, life_c, score = client.download()
        destro = []
        while True:
            text_Title = myFont.render("Pygame Text Test", True, Colors.black)
            cnt += 1
            tick += 1
            clock.tick(60)
            bullets = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            key_event = pygame.key.get_pressed()
            if key_event[pygame.K_ESCAPE]:
                sys.exit()

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

            background = pygame.image.load('./img/background.jpg')
            background = pygame.transform.scale(background, (900, 900))
            screen.blit(background, (0, 0))

            client.upload(myships[client_num], bullets)
            myships, bullets, ships, destroyed, life_c, score = client.download()
            temp = []
            for i in destroyed:
                destro.append([i[0], i[1], tick])
            for i in destro:
                if tick - i[2] < 20 or 40 < tick - i[2] < 60:
                    img = pygame.image.load('./img/fire.png')
                    img = pygame.transform.scale(img, (50, 30))
                    screen.blit(img, (i[0] - 15, i[1] - 15))
                if tick - i[2] > 60:
                    temp.append(i)
            for i in temp:
                destro.remove(i)
            for i in ships + bullets + myships:
                i.draw(screen)
            img = pygame.image.load('./img/life.png')
            img = pygame.transform.scale(img, (20, 20))
            life -= life_c
            for i in range(life):
                screen.blit(img, (30 + i * 30, 850))

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

    display()


menu()
