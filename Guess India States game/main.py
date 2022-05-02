import turtle
import pandas
screen = turtle.Screen()
image = "india.gif"
screen.screensize(canvheight=800, canvwidth=900)
screen.setup(800,900)
screen.addshape(image)
turtle.shape(image)

#def get_mouse_click_coor(x, y):
#    print(x,y)
#turtle.onscreenclick(get_mouse_click_coor)
count=0
while count<35:
    input_state = screen.textinput(title=f"Guess states {count}/34", prompt="Enter the Next State Name?")
    data = pandas.read_csv("indian_states.csv")
    if input_state.title() in data.state.values:
        count +=1
        is_state=data[data["state"]==input_state.title()]
        xcor = int(is_state.x.values)
        ycor = int(is_state.y.values)
        state_name = is_state.state.item()
        # print(is_state.state.item(), xcor,ycor)
        tim = turtle.Turtle()
        tim.hideturtle()
        tim.penup()
        tim.color("red")
        tim.goto(xcor,ycor)
        tim.write(f"{state_name}", align="left", font=("arial",8,"normal"))

screen.exitonclick()