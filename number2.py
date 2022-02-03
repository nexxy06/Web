import pygame
import requests, random

FPS = 60
HEIGHT = 400
WIDTH = 600
FULLSCREEN = False


def main(fps, width, height, fullscreen=False):
    A = 25
    B = 25
    running = True
    while running:
        pygame.init()
        REQ = 'https://static-maps.yandex.ru/1.x/?ll=133.282109%2C-26.327176&spn={},{}&l=map'.format(
            A,
            B)
        if not fullscreen:
            screen = pygame.display.set_mode((width, height))
        else:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        clock = pygame.time.Clock()
        response = requests.get(REQ)
        if response:
            with open('aus.png', 'wb') as f:
                f.write(response.content)
        screen.fill((255, 255, 255))
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if keys[pygame.K_DOWN]:
                if A + 5 < 200 and B + 5 < 200:
                    A += 5
                    B += 5
                    print(1)
            if keys[pygame.K_UP]:
                if A - 5 > 0 and B - 5 > 0:
                    A -= 5
                    B -= 5
                    print(2)
        img = pygame.image.load('aus.png')
        screen.blit(img, (0, 0))
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()


if __name__ == '__main__':
    main(FPS, WIDTH, HEIGHT, FULLSCREEN)
