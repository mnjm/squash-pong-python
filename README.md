# Squash Pong Game in Python

A simple squash pong game built using python.

![Squash-pong python](https://github.com/mnjm/squash-pong_python/blob/assets/squash_pong.gif?raw=true)

### Installation
- Install python3 (v3.5 or above) and pip3
- Run 
```shell 
pip3 install -r requirements.txt
```

### Options

```text
usage: squash_pong.py [-h] [-screen_size SCREEN_SIZE]
                      [-wall_thickness WALL_THICKNESS]
                      [-ball_radius BALL_RADIUS] [-paddle_size PADDLE_SIZE]
                      [-score_canvas_height SCORE_CANVAS_HEIGHT]
                      [-screen_color SCREEN_COLOR] [-wall_color WALL_COLOR]
                      [-ball_color BALL_COLOR] [-paddle_color PADDLE_COLOR]
                      [-score_color SCORE_COLOR] [-ball_speed BALL_SPEED]
                      [-paddle_speed PADDLE_SPEED] [-font_size FONT_SIZE]
                      [--opencv_display] [--no_score_board] [--debug]

simple squash-pong game built from python

options:
  -h, --help            show this help message and exit
  -screen_size SCREEN_SIZE
                        Screen size fmt:"w,h" (default: 700,500)
  -wall_thickness WALL_THICKNESS
                        Wall thickness in pxls (default: 30)
  -ball_radius BALL_RADIUS
                        Ball's radius in pxls (default: 40)
  -paddle_size PADDLE_SIZE
                        Paddle size in pxls fmt:"w,h" (default: 15,60)
  -score_canvas_height SCORE_CANVAS_HEIGHT
                        Score canvas height in pxls (default: 80)
  -screen_color SCREEN_COLOR
                        Scene background color fmt:"r,g,b" (default: 0,0,0)
  -wall_color WALL_COLOR
                        Wall color fmt:"r,g,b" (default: 255,255,255)
  -ball_color BALL_COLOR
                        Ball color fmt:"r,g,b" (default: 255,0,0)
  -paddle_color PADDLE_COLOR
                        Paddle color fmt:"r,g,b" (default: 0,255,0)
  -score_color SCORE_COLOR
                        Score font color fmt:"r,g,b" (default: 0,127,127)
  -ball_speed BALL_SPEED
                        Ball speed in pxls (default: 5)
  -paddle_speed PADDLE_SPEED
                        Paddle speed in pxls (default: 5)
  -font_size FONT_SIZE  Score font size in pxls (default: 32)
  --opencv_display      Use opencv's display functions (default: False)
  --no_score_board      Dont display scoreboard (default: False)
  --debug               Display debug info (default: False)
```