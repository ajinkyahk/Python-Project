import random
from turtle import Turtle, Screen


screen = Screen()

screen.setup(width=500, height=400)
user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a colour: ")
colors = ["red","orange","yellow","blue","purple","green"]
is_race_on=False
tim = Turtle(shape="turtle")

tim.penup()
tim.goto(x=-230, y=-100)
tim1 = tim.clone()
tim1.goto(x=-230, y=-50)
tim2 = tim.clone()
tim2.goto(x=-230, y=50)
tim3 = tim.clone()
tim3.goto(x=-230, y=100)
tim4 = tim.clone()
tim4.goto(x=-230, y=0)
tim5 = tim.clone()
tim5.goto(x=-230, y=150)

turtle_list = [tim,tim1,tim2,tim3,tim4,tim5]
count=0
for turtles in turtle_list:
    turtles.color(colors[count])
    count +=1

if user_bet:
    is_race_on=True

while is_race_on:
    for turtles in turtle_list:
        if turtles.xcor()>230:
            is_race_on=False
            winning_color = turtles.pencolor()
            if winning_color == user_bet:
                print(f"You've won! The {winning_color} is the winner")
            else:
                print(f"You've lost! The {winning_color} is the winner")
        rand_dist = random.randint(0,10)
        turtles.forward(rand_dist)
screen.exitonclick()

