from typing import List
import pygame

import logging
from rich.logging import RichHandler

from sys import exit

from random import randint, choice

# Initialise Logger
logging.basicConfig(level=logging.INFO, format="[{asctime}] - {funcName} - {message}", style='{', handlers=[RichHandler()])
logger = logging.getLogger("Runner")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(80,300))
        self.gravity = 0
        player_walk_1_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2_surface = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_jump_surface = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.player_walk_surfaces_list = [player_walk_1_surface, player_walk_2_surface]
        self.player_walk_index = 0

        self.image = self.player_walk_surfaces_list[self.player_walk_index]

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump_surface
        else:
            self.player_walk_index += 0.1
            if self.player_walk_index >=  len(self.player_walk_surfaces_list) :
                self.player_walk_index = 0
            self.image = self.player_walk_surfaces_list[int(self.player_walk_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_surface_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_surface_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_surface_1, fly_surface_2]
            y_pos = 210
        else:
            snail_surface_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_surface_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_surface_1, snail_surface_2]
            y_pos = 300          

        self.animation_index = 0

        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index  >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def collision_sprite(player, obstacle_group):
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False ):
        obstacle_group.empty()
        return False
    else:
        return True

    
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



def main() -> None:
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
        # background music
        bg_music = pygame.mixer.Sound('audio/music.wav')
        bg_music.set_volume(0.2)
        bg_music.play(loops = -1)

        # game active flag
        game_active = True

        # start time for score
        start_time = 0

        # create sky regular surface
        sky_surface = pygame.image.load('graphics/sky.png').convert()
        # create ground regular surface
        ground_surface = pygame.image.load('graphics/ground.png').convert()


        # Player
        player = pygame.sprite.GroupSingle()
        player.add(Player())

        # obstacles
        obstacle_group = pygame.sprite.Group()

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

        # Timer - obstacle generation
        obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(obstacle_timer, 2000)

        # Timer - snail animator
        snail_animation_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(snail_animation_timer, 500)
        
        # Timer - fly animator
        fly_animation_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(fly_animation_timer, 200)
        
        logger.info(f"[green]Initialised Runner[/green]", extra={"markup": True})
 
        while True:
            # check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logger.info(f"[purple]Quitting Runner[/purple]", extra={"markup": True})
                    pygame.quit()  # Opposite of .init()
 
                    # Ensure pygame ends 
                    exit()

                if game_active:
                    if event.type == obstacle_timer:
                        obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            game_active = True
                            start_time = int(pygame.time.get_ticks()/1000)
                    
            if game_active:
                # blit - Block Image Transfer i.e put a regular surface on top of display surface
                screen.blit(sky_surface,(0,0))
                screen.blit(ground_surface,(0,300))

                player.draw(screen)
                player.update()

                obstacle_group.draw(screen)
                obstacle_group.update()

                # display score
                score = display_score(screen, start_time)

                # collison
                game_active = collision_sprite(player, obstacle_group)
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

            # Control speed , set maximum frame rate - while loop must not run 
            # more than 60 times per second
            clock.tick(60)

    except Exception as error:
        logger.error(f"[red]{error}[/red]", extra={"markup": True})


if __name__ == "__main__":
    try:
        main()

    except Exception as error:
        logger.error(f"[red]{error}[/red]", extra={"markup": True})