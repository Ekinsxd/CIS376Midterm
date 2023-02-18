import pygame

WIDTH = 800
HEIGHT = 600
BACKGROUND = (0, 0, 0)


def main():
    # hello world pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
