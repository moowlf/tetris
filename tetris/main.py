import pygame
from game.game import Game
from game.movement import Movement
from config import CONFIG
import random

class UI:

    def __init__(self) -> None:

        # Initialize tetris object
        self._game = Game(CONFIG.HORIZONTAL_SQUARES, CONFIG.VERTICAL_SQUARES)

        # Initialize pygame
        pygame.init()
        pygame.display.set_caption('Tetris')
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode((CONFIG.WINDOW_WIDTH, CONFIG.WINDOW_HEIGHT))

        # Print board
        self._draw_board()
    
    def run(self) -> None:
        
        # Draw the static parts of the game (side borders and bottom)
        self._draw_constants()
        
        self._running = True
        while self._running:
            self._clear_pieces_from_previous_frame()
            self._draw_board()

            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    self._running = False

                if event.type == pygame.KEYDOWN:
                     self._handle_keys(event)

            pygame.display.update() 
            self._clock.tick(60) 

    def _handle_keys(self, event):

        if event.key in [pygame.K_LEFT, pygame.K_a]:
            self._game.move_piece(Movement.LEFT)
        elif event.key in [pygame.K_RIGHT, pygame.K_d]:
            self._game.move_piece(Movement.RIGHT)
        elif event.key in [pygame.K_DOWN]:
            self._game.move_piece(Movement.DOWN)
        elif event.key in [pygame.K_r]:
            self._game.move_piece(Movement.ROTATE)

    def _draw_board(self) -> None:

        w_dimension = CONFIG.WINDOW_WIDTH // (CONFIG.HORIZONTAL_SQUARES + 2)
        h_dimension = CONFIG.WINDOW_HEIGHT // (CONFIG.VERTICAL_SQUARES + 1)

        board = self._game.next_state()
        for r in range(len(board)):
            for c in range(len(board[r])):
                
                if board[r][c] != 0:

                    x_coordinate = (c + 1) * w_dimension
                    y_coordinate = (r * h_dimension)

                    rect_pos = (x_coordinate, y_coordinate, w_dimension, h_dimension)
                    pygame.draw.rect(self._screen, (255, 255, 255), rect_pos)

    def _draw_constants(self) -> None:

        def round_down_to_multiple(val, multiple):
            if val % multiple == 0:
                return val
            return val - (val % multiple)

        w_dimension = CONFIG.WINDOW_WIDTH // (CONFIG.HORIZONTAL_SQUARES + 2)
        h_dimension = CONFIG.WINDOW_HEIGHT // (CONFIG.VERTICAL_SQUARES + 1)

        # Draw side borders
        r_origin = round_down_to_multiple(CONFIG.WINDOW_WIDTH, w_dimension)
        for r in range(CONFIG.VERTICAL_SQUARES):
            left =  (0, r * h_dimension, w_dimension, h_dimension)
            right = (r_origin - w_dimension, r * h_dimension, w_dimension, h_dimension)
            pygame.draw.rect(self._screen, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), left, 0)
            pygame.draw.rect(self._screen, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), right, 0)
        
        # Draw bottom line
        top_left = CONFIG.WINDOW_HEIGHT - h_dimension
        for c in range(CONFIG.HORIZONTAL_SQUARES + 2):
            left = (c * w_dimension, top_left, w_dimension, h_dimension)
            pygame.draw.rect(self._screen, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), left, 0)

    def _clear_pieces_from_previous_frame(self) -> None:

        w_dimension = 414 // (CONFIG.HORIZONTAL_SQUARES + 2)
        h_dimension = 736 // (CONFIG.VERTICAL_SQUARES + 1)

        color = (0, 0, 0)

        rect = (w_dimension, 0, CONFIG.HORIZONTAL_SQUARES * w_dimension, CONFIG.VERTICAL_SQUARES * h_dimension)
        self._screen.fill(color, rect)

if __name__=="__main__":
    # call the main function
    UI().run()