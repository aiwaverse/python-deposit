from turtle import *
from math import sqrt
from time import sleep

def t_square(turtle,side):
    for _ in range(4):
        turtle.forward(side)
        turtle.left(90)

wn = Screen()
luna = Turtle()
luna.shape("turtle")
luna.color("pink")
luna.speed(2)
luna.pensize(3)
sleep(5)

t_square(luna, 70)
luna.up()
luna.forward(20)
luna.left(90)
luna.forward(20)
luna.right(90)
luna.down()

t_square(luna,70)
luna.up()
luna.right(90)
luna.forward(20)
luna.right(90)
luna.forward(20)
luna.right(180)

luna.down()
luna.left(45)
luna.forward(20*sqrt(2))
luna.right(45)
luna.forward(70)
luna.right(90+45)
luna.forward(20*sqrt(2))
luna.left(180)
luna.forward(20*sqrt(2))

luna.left(45)
luna.forward(70)
luna.left(90+45)
luna.forward(20*sqrt(2))
luna.left(180)
luna.forward(20*sqrt(2))
luna.left(90+45)

luna.forward(70)
luna.left(45)
luna.forward(20*sqrt(2))
luna.hideturtle()
wn.exitonclick()