import pygame
import requests

FPS = 60
HEIGNT = 400
WIDTH = 600
FULLSCREN = False
REQ = "https://static-maps.yandex.ru/1.x/?ll=2.294494%2C48.858247&spn=0.001,0.001&l=map"


def main(fps, width, height, fullscreen=False):
    pygame.init()
    if not fullscreen:
        screen = pygame.display.set_mode((width, height))
    else:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    response = requests.get(REQ)
    if response:
        with open("aus.png", "wb") as f:
            f.write(response.content)
    running = True
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        img = pygame.image.load("aus.png")
        screen.blit(img, (0, 0))
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()


if __name__ == "__main__":
    main(FPS, WIDTH, HEIGNT, FULLSCREN)
