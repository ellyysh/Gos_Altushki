import socket
import pygame
import sys
import random
import subprocess

pygame.init()
pygame.mixer.init()
global SERVER
PORT = 6040
HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MSG = "disc"
screen = pygame.display.set_mode((1100, 600))
pygame.display.set_caption("GosAlt")

icon_sprite = pygame.image.load("img/icon.jpg")
icon_sprite = pygame.transform.scale(icon_sprite, (500, 300))
sprite_array = ["img/1.jpg", "img/2.jpg", "img/3.jpg", "img/4.jpg", "img/5.jpg", "img/6.jpg", "img/7.jpg", "img/8.jpg"]
button_sprite = pygame.image.load("img/button.png")
button_sprite = pygame.transform.scale(button_sprite, (400, 100))
button_left1 = pygame.image.load("img/rightb.png")
button_left1 = pygame.transform.scale(button_left1, (270, 70))
button_right1 = pygame.image.load("img/leftb.png")
button_right1 = pygame.transform.scale(button_right1, (270, 70))
button_left_rect = button_left1.get_rect(center=(420, 400))
button_right_rect = button_right1.get_rect(center=(720, 400))

button_sound = pygame.mixer.Sound("music/button.mp3")
change_sound = pygame.mixer.Sound("music/change.mp3")

font = pygame.font.Font("font/Lato-Medium.ttf", 26)


def write_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def connection(ADDR):
    server_started = False
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while not server_started:
        screen.fill((255, 255, 255))
        write_text('Загрузка...', font, (0, 0, 0), 500, 300)
        pygame.display.flip()
        try:
            s.connect(ADDR)
            server_started = True
        except ConnectionRefusedError:
            pass
    return s

def connectionSelection():

    while True:
        write_text('Выбери тип подключения:', font, (0, 0, 0), 300, 200)
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (button_left_rect.collidepoint(event.pos)):
                    button_sound.play(0)
                    subprocess.Popen("python main.py", shell=True)
                    SERVER = socket.gethostbyname(socket.gethostname())
                    client = connection((SERVER, PORT))
                    menu(client, SERVER)
                if button_right_rect.collidepoint(event.pos):
                    button_sound.play(0)
                    find_ip()

        screen.blit(button_left1, button_left_rect)
        write_text('Создать выдачу', font, (255, 255, 255), 315, 385)
        screen.blit(button_right1, button_right_rect)
        write_text('Найти выдачу', font, (255, 255, 255), 615, 385)
        screen.blit(icon_sprite, (350, 70))
        pygame.display.flip()
def find_ip():
    SERVER = ""
    while True:
        screen.fill((255, 255, 255))
        screen.blit(icon_sprite, (350, 100))
        write_text('Введите IP выдачи:', font, (0, 0, 0), 300, 400)
        write_text(SERVER, font, (0, 0, 0), 600, 400)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    client = connection((SERVER, PORT))
                    menu(client, SERVER)
                elif event.key == pygame.K_BACKSPACE:
                    SERVER = SERVER[:-1]
                else:
                    SERVER += event.unicode


        pygame.display.flip()
def menu(client, SERVER):
    screen.fill((255, 255, 255))
    screen.blit(icon_sprite, (350, 100))
    while True:

        write_text('Ваш адрес: ' + SERVER, font, (0, 0, 0), 70, 550)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (button_left_rect.collidepoint(event.pos)):
                    button_sound.play(0)
                    register(client)
                elif button_right_rect.collidepoint(event.pos):
                    button_sound.play(0)
                    altushka(client)
        screen.blit(button_left1, button_left_rect)
        write_text('Регистрация', font, (255, 255, 255), 315, 385)
        screen.blit(button_right1, button_right_rect)
        write_text('Получить альтушку', font, (255, 255, 255), 615, 385)
        pygame.display.flip()

def register(client):

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_sprite.get_rect(center=(520, 420)).collidepoint(event.pos):
                    client.send("change".encode(FORMAT))
                    print("sent")
        # Отображение кнопки
        screen.fill((255, 255, 255))
        screen.blit(button_sprite, (400, 400))
        screen.blit(icon_sprite, (350, 100))
        pygame.display.flip()

def altushka(client):

    screen.fill((255, 255, 255))
    random_sprite_path = random.choice(sprite_array)
    sprite = pygame.image.load(random_sprite_path)
    sprite = pygame.transform.scale(sprite, (1000, 500))


    client.setblocking(False)  # Устанавливаем соединение в неблокирующий режим

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        try:
            received = client.recv(HEADER).decode(FORMAT)
            if received == "change":
                random_sprite_path = random.choice(sprite_array)
                sprite = pygame.image.load(random_sprite_path)
                sprite = pygame.transform.scale(sprite, (1000, 600))
                print("change")
                change_sound.play()
        except socket.error as e:
            pass

        # Отображение спрайта
        screen.fill((220, 220, 220))
        screen.blit(sprite, (50, 50))
        pygame.display.flip()
connectionSelection()
