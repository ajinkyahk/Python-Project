import turtle

screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)


#print(answer_state.title())
count=0
import pandas
data = pandas.read_csv("50_states.csv")
guessed_states = []

while count<51:
    answer_state = screen.textinput(title=f"Guess the State {count}/50", prompt="What's another state's name?")
    if answer_state == "Exit":
        # states to learn
        states_to_learn = [state for state in data.state if state not in guessed_states]
        df = pandas.DataFrame(states_to_learn)
        df.to_csv("missing_state.csv")
        break
    if answer_state.title() in data["state"].values:
        in_state = data[data["state"] == answer_state.title()]
        xcor = int(in_state["x"].values)
        ycor = int(in_state.y.values)
        state_name = str(in_state["state"].item())
        guessed_states.append(state_name)
        count +=1
        tim = turtle.Turtle()
        tim.hideturtle()
        tim.penup()
        tim.goto(xcor, ycor)
        tim.color("black")
        tim.write(f"{state_name}", align="center", font=("arial", 10, "normal"))

