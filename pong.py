import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, cv2
import numpy as np

SCREEN_SIZE = (700, 500)
WALL_THICKNESS = 30
PADDLE_SIZE = (15, 60)
SCREEN_COLOR = (0, 0, 0)
WALL_COLOR = (255, 255, 255)
BALL_COLOR = (255, 0, 0)
PADDLE_COLOR = (0, 255, 0)
BALL_SPEED = 5
PADDLE_SPEED = 5
BALL_RADIUS = 40
SCORE_CANVAS_HEIGHT = 80
FONT_SIZE = 32

class Ball:

    def __init__(self):
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(SCREEN_SIZE[0]//2 - BALL_RADIUS, SCREEN_SIZE[1]//2 - BALL_RADIUS,
                BALL_RADIUS//2, BALL_RADIUS//2)
        self.velocity_x = BALL_SPEED * np.random.choice([-1,1])
        self.velocity_y = BALL_SPEED * np.random.choice([-1,1])

    def update(self, paddle):
        point = 0
        # wall bounce
        if self.rect.x <= WALL_THICKNESS:
            self.velocity_x *= -1
        if self.rect.y <= WALL_THICKNESS or (self.rect.y + self.rect.height) >= (SCREEN_SIZE[1] - WALL_THICKNESS):
            self.velocity_y *= -1
        # paddle bounce
        if self.rect.colliderect(paddle.rect):
            self.velocity_x *= -1
            point = +1
        elif (self.rect.x + self.rect.width) >= SCREEN_SIZE[0]:
            point = -1
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        return point
    
    def draw(self, screen):
        pygame.draw.ellipse(screen, BALL_COLOR, self.rect)

class Paddle:

    def __init__(self):
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(SCREEN_SIZE[0] - PADDLE_SIZE[0], SCREEN_SIZE[1]//2 - PADDLE_SIZE[1]//2,
                PADDLE_SIZE[0], PADDLE_SIZE[1])
        self.velocity = 0

    def update_and_draw(self, screen):
        self.rect.y += self.velocity
        if self.rect.y <= WALL_THICKNESS:
            self.rect.y = WALL_THICKNESS
        elif (self.rect.y + self.rect.height) >= (SCREEN_SIZE[1] - WALL_THICKNESS):
            self.rect.y = SCREEN_SIZE[1] - WALL_THICKNESS - PADDLE_SIZE[1]
        pygame.draw.rect(screen, PADDLE_COLOR, self.rect)

def render_score_board(points_scored, points_lost, screen):
    global font
    text = font.render("Points lost: %d"%(points_lost), True, WALL_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_SIZE[0]//4, SCREEN_SIZE[1] + SCORE_CANVAS_HEIGHT//2)
    screen.blit(text, text_rect)
    text = font.render("Points scored: %d"%(points_scored), True, WALL_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_SIZE[0]//4 + SCREEN_SIZE[0]//2, SCREEN_SIZE[1] + SCORE_CANVAS_HEIGHT//2)
    screen.blit(text, text_rect)

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1] + SCORE_CANVAS_HEIGHT))
pygame.display.set_caption("Squash_Pong")
font = pygame.font.Font('freesansbold.ttf', FONT_SIZE) 
exit_flag = False
clock = pygame.time.Clock()

walls_rect = [pygame.Rect(0, 0, SCREEN_SIZE[0], WALL_THICKNESS),
        pygame.Rect(0, SCREEN_SIZE[1] - WALL_THICKNESS, SCREEN_SIZE[0], WALL_THICKNESS),
        pygame.Rect(0, WALL_THICKNESS, WALL_THICKNESS, SCREEN_SIZE[1] - WALL_THICKNESS)]

ball = Ball()
paddle = Paddle()
points_scored = 0
points_lost = 0

cv2.namedWindow("Show", cv2.WINDOW_NORMAL)
dilate_kernel = np.ones((5,5), dtype=np.uint8)

while not exit_flag:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_flag = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                paddle.velocity = -PADDLE_SPEED
            elif event.key == pygame.K_DOWN:
                paddle.velocity = +PADDLE_SPEED
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                paddle.velocity = 0
            elif event.key == pygame.K_DOWN:
                paddle.velocity = 0

    screen.fill(SCREEN_COLOR)
    for rect in walls_rect:
        pygame.draw.rect(screen, WALL_COLOR, rect)
    paddle.update_and_draw(screen)
    current_point = ball.update(paddle)
    if current_point < 0:
        points_lost -= current_point
        paddle.reset()
        ball.reset()
    elif current_point > 0: points_scored += current_point
    ball.draw(screen)
    render_score_board(points_scored, points_lost, screen)

    # temp = pygame.surfarray.pixels3d(screen)
    # img = temp.copy()
    # del temp
    # img = np.swapaxes(img, 0, 1)[:SCREEN_SIZE[1],...]
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # img = cv2.dilate(img, dilate_kernel, iterations=2)
    # img = cv2.resize(img, (24, 24))
    # cv2.imshow("Show", img)
    # cv2.waitKey(1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
