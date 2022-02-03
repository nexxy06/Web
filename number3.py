import pygame
import requests

FPS = 60
HEIGHT = 400
WIDTH = 600
FULLSCREEN = False


def main(fps, width, height, fullscreen=False):
    a = 133
    b = 25
    running = True
    while running:
        pygame.init()
        REQ = 'https://static-maps.yandex.ru/1.x/?ll={}%2C-{}&spn=20.1,20.1&l=map'.format(a, b)
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
                b += 2
            if keys[pygame.K_UP]:
                b -= 2
            if keys[pygame.K_LEFT]:
                a -= 2
            if keys[pygame.K_RIGHT]:
                a += 2
        img = pygame.image.load('aus.png')
        screen.blit(img, (0, 0))
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()


if __name__ == '__main__':
    main(FPS, WIDTH, HEIGHT, FULLSCREEN)
