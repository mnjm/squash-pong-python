import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, cv2
import numpy as np
from config_parser import parse_args
# This program was ment to provide images to train a simple RL-ML model

class Ball:

    def __init__(self, config):
        self.config = config
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(self.config.screen_size[0]//2 - self.config.ball_radius,
                self.config.screen_size[1]//2 - self.config.ball_radius,
                self.config.ball_radius//2, self.config.ball_radius//2)
        self.velocity_x = self.config.ball_speed * np.random.choice([-1,1])
        self.velocity_y = self.config.ball_speed * np.random.choice([-1,1])

    def update(self, paddle):
        point = 0
        # wall bounce
        x1, y1 = self.rect.x, self.rect.y
        x2, y2 = self.rect.x + self.rect.width, self.rect.y + self.rect.height
        screen_wo_wall = self.config.screen_size[1] - self.config.wall_thickness
        if x1 <= self.config.wall_thickness:
            self.velocity_x *= -1
        if y1 <= self.config.wall_thickness or y2 >= screen_wo_wall:
            self.velocity_y *= -1
        # paddle bounce
        new_rect = pygame.Rect(x1 - 1, y1 - 1, self.rect.width + 2, self.rect.height + 2)
        # if self.rect.colliderect(paddle.rect):
        if new_rect.colliderect(paddle.rect):
            self.velocity_x *= -1
            point = +1
        elif x2 >= self.config.screen_size[0]:
            point = -1
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        return point

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.config.ball_color, self.rect)

class Paddle:

    def __init__(self, config):
        self.config = config
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(self.config.screen_size[0] - self.config.paddle_size[0],
                self.config.screen_size[1]//2 - self.config.paddle_size[1]//2,
                self.config.paddle_size[0], self.config.paddle_size[1])
        self.velocity = 0

    def update(self):
        self.rect.y += self.velocity
        if self.rect.y <= self.config.wall_thickness:
            self.rect.y = self.config.wall_thickness
        elif (self.rect.y + self.rect.height) >= (self.config.screen_size[1] - self.config.wall_thickness):
            self.rect.y = self.config.screen_size[1] - self.config.wall_thickness - self.config.paddle_size[1]

    def draw(self, screen):
        pygame.draw.rect(screen, self.config.paddle_color, self.rect)

class SquashPong:
    # Actions
    PADDLE_UP = 0
    PADDLE_DOWN = 1
    PADDLE_STAY = 2

    def __init__(self, config, display_live=False, render_score=False):
        self.config = config
        pygame.init()
        self.display_live = display_live
        extra_height = self.config.score_canvas_height if render_score else 0
        if display_live:
            self.screen = pygame.display.set_mode((self.config.screen_size[0], self.config.screen_size[1] + extra_height))
            pygame.display.set_caption("SquashPong")
        else:
            self.screen = pygame.Surface((self.config.screen_size[0], self.config.screen_size[1] + extra_height))
        self.render_score = render_score
        if self.render_score:
            self.font = pygame.font.Font("freesansbold.ttf", self.config.font_size)
        self.walls_rect = [pygame.Rect(0, 0, self.config.screen_size[0], self.config.wall_thickness),
            pygame.Rect(0, self.config.screen_size[1] - self.config.wall_thickness, self.config.screen_size[0], self.config.wall_thickness),
            pygame.Rect(0, self.config.wall_thickness, self.config.wall_thickness, self.config.screen_size[1] - self.config.wall_thickness)]
        self.ball = Ball(config)
        self.paddle = Paddle(config)
        self.score = 0

    def render_score_board(self):
        if self.render_score:
            text_render = self.font.render("Score: %d"%(self.score), True, self.config.score_color)
            text_rect = text_render.get_rect()
            text_rect.center = (self.config.screen_size[0]//2,
                    self.config.screen_size[1] + self.config.score_canvas_height//2)
            self.screen.blit(text_render, text_rect)

    def update(self, action):
        # Update action and collect reward
        # Returns reward and the img. img can be used to train RLML models
        if action == SquashPong.PADDLE_UP:
            self.paddle.velocity = -self.config.paddle_speed
        elif action == SquashPong.PADDLE_DOWN:
            self.paddle.velocity = +self.config.paddle_speed
        elif action == SquashPong.PADDLE_STAY:
            self.paddle.velocity = 0
        self.paddle.update()
        reward = self.ball.update(self.paddle)
        self.score += reward
        # reset the game if lost
        if reward < 0:
            self.paddle.reset()
            self.ball.reset()
            self.score = 0
        # draw
        self.screen.fill(self.config.screen_color)
        for rect in self.walls_rect:
            pygame.draw.rect(self.screen, self.config.wall_color, rect)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        if self.render_score: self.render_score_board()
        # get image
        temp_buffer = pygame.surfarray.pixels3d(self.screen)
        img = temp_buffer.copy() # Deep copy
        del temp_buffer # Free the ref to redraw
        img = np.swapaxes(img, 0, 1)[:self.config.screen_size[1],...] # get swap axes and remove score board if rendered
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return reward, img

    def quit(self):
        if self.display_live: pygame.quit()

def run_squash_pong_live(config):
    squashpong = SquashPong(config, display_live = True, render_score = (not config.no_score_board))
    clock = pygame.time.Clock()
    exit_flag = False
    action = SquashPong.PADDLE_STAY
    while not exit_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_flag = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    action = SquashPong.PADDLE_UP
                elif event.key == pygame.K_DOWN:
                    action = SquashPong.PADDLE_DOWN
            elif event.type == pygame.KEYUP  and (event.key == pygame.K_UP or event.key == pygame.K_DOWN):
                action = SquashPong.PADDLE_STAY
        if not exit_flag: reward, img = squashpong.update(action) # img can be used to train RLML models
        pygame.display.flip()
        clock.tick(60)
    squashpong.quit()

if __name__ == '__main__':
    config = parse_args()
    run_squash_pong_live(config)
