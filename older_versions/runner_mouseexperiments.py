import pygame

import logging
from rich.logging import RichHandler

from sys import exit

# Initialise Logger
logging.basicConfig(level=logging.INFO, format="[{asctime}] - {funcName} - {message}", style='{', handlers=[RichHandler()])
logger = logging.getLogger("Runner")

def main()-> None:
    try:
        # raise Exception("Testing exception logger")

        logger.info(f"[bold purple]WELCOME TO RUNNER !!![/bold purple]", extra={"markup": True})

        logger.info(f"[blue]Initialising Runner[/blue]", extra={"markup": True})

        pygame.init()
        # create display surface - width,height
        screen = pygame.display.set_mode((800,400))
        # Set window title
        pygame.display.set_caption('Runner')
        # create clock for controlling fps
        clock = pygame.time.Clock()

        # create sky regular surface
        sky_surface = pygame.image.load('graphics/sky.png').convert()
        # create ground regular surface
        ground_surface = pygame.image.load('graphics/ground.png').convert()
        # Create on screen caption - None defaults to pygame font
        caption_font= pygame.font.Font('fonts/Pixeltype.ttf', 30)
        # Text, Anti Aliaisingt to smooth out edges, 
        caption_surface = caption_font.render('Runner', False, 'Purple')

        # Snail
        snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
        snail_rectangle = snail_surface.get_rect(topleft=(700, 265))
        snail_speed = 4
        # Player
        player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_rectangle = player_surface.get_rect(midbottom=(80,300))
        player_speed = 1
        
        logger.info(f"[green]Initialised Runner[/green]", extra={"markup": True})
 
        while True:
            # check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logger.info(f"[purple]Quitting Runner[/purple]", extra={"markup": True})
                    pygame.quit() # Opposite of .init()
 
                    # Ensure pygame ends 
                    exit()

                if event.type == pygame.MOUSEMOTION:
                    if player_rectangle.collidepoint(event.pos) :
                        print('Mouse collided with player')
                    

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Mouse Down")

                if event.type == pygame.MOUSEBUTTONUP:
                    print("Mouse Up")

            # blit - Block Image Transfer i.e put a regular surface on top of display surface
            screen.blit(sky_surface,(0,0))
            screen.blit(ground_surface,(0,300))
            screen.blit(caption_surface,(350,10))

            screen.blit(snail_surface,snail_rectangle)
            snail_rectangle.x = snail_rectangle.x - snail_speed if snail_rectangle.right > 0 else 800
            screen.blit(player_surface,player_rectangle)
            # player_rectangle.x = player_rectangle.x + player_speed if player_rectangle.right < 800 else 80

            # if player_rectangle.colliderect(snail_rectangle) # check collision using rectangles only
            if player_rectangle.collidepoint(pygame.mouse.get_pos()) :
                print(pygame.mouse.get_pressed())

            # Writeupdates to display surface
            pygame.display.update()

            # Control speed , set maximum frame rate - while loop must not run more than 60 times per second
            clock.tick(60)

    except Exception as error:
        logger.error(f"[red]{error}[/red]", extra={"markup": True})

if __name__=="__main__":
    try:
        main()

    except Exception as error:
        logger.error(f"[red]{error}[/red]", extra={"markup": True})