# "Learning Python by building five games" youtube tutorial
# game 1: pong

# importing a module turtle, so that we can use the class Turtle for graphics
import turtle
# us mac commands
import os

# creating a window
wn = turtle.Screen()
wn.title("Pong by Noosh")
wn.bgcolor("black")
wn.setup(width = 800, height = 600) # center is 0, 0
wn.tracer(0)

# VARIABLES
score_a = 0
score_b = 0

# OBJECTS
# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0) # speed of animation set to max
paddle_a.shape("square") # one of the basic shapes, 20x20
paddle_a.color("white")
paddle_a.shapesize(stretch_wid = 5, stretch_len = 1)
paddle_a.penup() # it won't draw lines
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0) # speed of animation set to max
paddle_b.shape("square") # one of the basic shapes, 20x20
paddle_b.color("white")
paddle_b.shapesize(stretch_wid = 5, stretch_len = 1)
paddle_b.penup() # it won't draw lines
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0) # speed of animation set to max
ball.shape("square") # one of the basic shapes, 20x20
ball.color("white")
ball.penup() # it won't draw lines
ball.goto(0, 0)
ball.dx = 2.5 # moves by 2.5 pixels
ball.dy = 2.5

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align = "center", font = ("Courier", 24, "normal"))


# FUNCTIONS
def paddle_a_up():
    y = paddle_a.ycor() # returns y coordinate
    y += 20
    paddle_a.sety(y)

def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)

def paddle_b_up():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)


# KEYBOARD BINDINGS
wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")


# Main game loop
while True:
    wn.update()

    # move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # border checks
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1 # reverses direction
        os.system("afplay bounce.wav&")

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
        os.system("afplay bounce.wav&")
    
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align = "center", font = ("Courier", 24, "normal"))

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align = "center", font = ("Courier", 24, "normal"))

    # Paddle and ball collisions
    if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() - 50):
        ball.setx(340)
        ball.dx *= -1
        os.system("afplay bounce.wav&")
    
    if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() - 50):
        ball.setx(-340)
        ball.dx *= -1
        os.system("afplay bounce.wav&")
