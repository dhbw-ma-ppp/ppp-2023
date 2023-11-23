import matplotlib.pyplot as plt
import numpy as np

# Set up the game window
fig, ax = plt.subplots()
ax.set_xlim(0, 43)
ax.set_ylim(0, 23)
ax.set_aspect('equal')
ax.axis('off')

# Create the paddle
paddle_width = 2
paddle_height = 0.5
paddle_x = 4
paddle_y = 1
paddle = plt.Rectangle((paddle_x, paddle_y), paddle_width, paddle_height, color='blue')
ax.add_patch(paddle)

# Create the ball
ball_radius = 0.2
ball_x = 5
ball_y = 5
ball_dx = 0.1
ball_dy = 0.1
ball = plt.Circle((ball_x, ball_y), ball_radius, color='red')
ax.add_patch(ball)

# Game loop
while True:
    # Move the paddle
    paddle_x = plt.ginput(1)[0][0] - paddle_width / 2
    paddle.set_xy((paddle_x, paddle_y))

    # Move the ball
    ball_x += ball_dx
    ball_y += ball_dy
    ball.set_center((ball_x, ball_y))

    # Check for collision with paddle
    if paddle.contains_point((ball_x, ball_y - ball_radius)):
        ball_dy = -ball_dy

    # Check for collision with walls
    if ball_x - ball_radius < 0 or ball_x + ball_radius > 10:
        ball_dx = -ball_dx
    if ball_y - ball_radius < 0 or ball_y + ball_radius > 10:
        ball_dy = -ball_dy

    # Update the game window
    plt.pause(0.01)
    plt.draw()
