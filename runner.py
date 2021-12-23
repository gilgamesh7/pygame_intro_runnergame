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
        
        logger.info(f"[green]Initialised Runner[/green]", extra={"markup": True})
 
        while True:
            # check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logger.info(f"[purple]Quitting Runner[/purple]", extra={"markup": True})
                    pygame.quit() # Opposite of .init()
 
                    # Ensure pygame ends 
                    exit()

            # Writeupdates to g=display surface
            pygame.display.update()

    except Exception as error:
        logger.error(f"[red]{error}[/red]", extra={"markup": True})

if __name__=="__main__":
    try:
        main()

    except Exception as error:
        logger.error(f"[red]{error}[/red]", extra={"markup": True})