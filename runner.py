import pygame

import logging
from rich.logging import RichHandler

from sys import exit

# Initialise Logger
logging.basicConfig(level=logging.INFO, format="[{asctime}] - {funcName} - {message}", style='{', handlers=[RichHandler()])
logger = logging.getLogger("Runner")


def display_score(screen: pygame.display, start_time: int) -> int:
    current_time = int(pygame.time.get_ticks()/1000) - start_time

    # Create on screen caption - None defaults to pygame font
    score_font = pygame.font.Font('fonts/Pixeltype.ttf', 30)
    # Text, Anti Aliaising to smooth out edges, 
    score_surface = score_font.render(f'Score : {current_time}', False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center=(400, 50))

    # Score board
    pygame.draw.rect(screen,'#c0e8ec',score_rectangle,6)
    pygame.draw.rect(screen,'#c0e8ec',score_rectangle)
    screen.blit(score_surface,score_rectangle)

    return current_time


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

        # game active flag
        game_active = True

        # start time for score
        start_time = 0

        # create sky regular surface
        sky_surface = pygame.image.load('graphics/sky.png').convert()
        # create ground regular surface
        ground_surface = pygame.image.load('graphics/ground.png').convert()

        # Snail
        snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
        snail_rectangle = snail_surface.get_rect(topleft=(700, 265))
        snail_speed = 4

        # Player
        player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_rectangle = player_surface.get_rect(midbottom=(80,300))
        player_gravity = 0

        # Game end screen
        # - Standing player
        player_stand_surface = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
        player_stand_surface = pygame.transform.rotozoom(player_stand_surface, 45, 2)
        player_stand_rectangle = player_stand_surface.get_rect(center=(400,200))
        # - Caption
        game_font = pygame.font.SysFont('timesnewroman',  20)
        game_name_surface = game_font.render('Pixel Runner', False, (64, 64, 64))
        game_name_rectangle = game_name_surface.get_rect(center=(400, 80))
        # Instructions
        game_instructions_surface = game_font.render('Press space for another game ...', False, (104,0,104))
        game_instructions_rectangle = game_instructions_surface.get_rect(center=(400,350))
        
        logger.info(f"[green]Initialised Runner[/green]", extra={"markup": True})
 
        while True:
            # check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logger.info(f"[purple]Quitting Runner[/purple]", extra={"markup": True})
                    pygame.quit() # Opposite of .init()
 
                    # Ensure pygame ends 
                    exit()

                if game_active :
                    if event.type == pygame.MOUSEBUTTONDOWN :
                        if player_rectangle.collidepoint(event.pos):
                            if player_rectangle.bottom == 300:
                                player_gravity = -20
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if player_rectangle.bottom == 300:
                                player_gravity = -20
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            game_active = True
                            snail_rectangle.left = 800
                            start_time = int(pygame.time.get_ticks()/1000)
                    
            if game_active :
                # blit - Block Image Transfer i.e put a regular surface on top of display surface
                screen.blit(sky_surface,(0,0))
                screen.blit(ground_surface,(0,300))

                # snail
                screen.blit(snail_surface,snail_rectangle)
                snail_rectangle.x = snail_rectangle.x - snail_speed if snail_rectangle.right > 0 else 800

                # player
                player_gravity += 1
                player_rectangle.y += player_gravity
                if player_rectangle.bottom > 300 :
                    player_rectangle.bottom = 300
                screen.blit(player_surface,player_rectangle)

                # display score
                score = display_score( screen,start_time )

                # collison
                if snail_rectangle.colliderect(player_rectangle) :
                    logger.info(f"[red]COLLISION - EndingGame[/red]", extra={"markup": True})
                    game_active = False
            else:
                screen.fill('Purple')
                screen.blit(player_stand_surface, player_stand_rectangle)
                screen.blit(game_name_surface, game_name_rectangle)
                screen.blit(game_instructions_surface, game_instructions_rectangle)
                # Final score
                end_game_score_surface = game_font.render(f'Score : {score}', False, (104, 0, 104))
                end_game_score_rectangle = end_game_score_surface.get_rect(center=(400,100))
                screen.blit(end_game_score_surface, end_game_score_rectangle)

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