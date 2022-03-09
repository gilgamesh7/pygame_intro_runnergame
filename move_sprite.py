import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(700,300))

    def update(self, event_type):
        if event_type == 1 :
            if self.rect.x > 400 :
                self.rect.x -= 6
        if event_type == 2 :
            if self.rect.x < 700 :
                self.rect.x += 6


if __name__ == "__main__":
    pygame.init()
    
    screen = pygame.display.set_mode((800,400))
    screen.fill((255, 255, 255))

    clock = pygame.time.Clock()

    obstacle = pygame.sprite.GroupSingle()
    obstacle.add(Obstacle())

    animation_timer1 = pygame.USEREVENT + 2
    pygame.time.set_timer(animation_timer1, 2000,2)

    animation_timer2 = pygame.USEREVENT + 3
    pygame.time.set_timer(animation_timer2, 3000,2)

    event_type = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  
                exit()

            if event.type == animation_timer1:
                event_type = 1
                print("timer 1 fired")

            if event.type == animation_timer2:
                event_type = 2
                print("timer 2 fired")

        screen.fill((255, 255, 255))

        obstacle.draw(screen)
        obstacle.update(event_type)


        pygame.display.update()

        clock.tick(60)
   
