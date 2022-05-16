from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Courier", 15, "normal")
class Score_board(Turtle):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.color("white")
        self.penup()
        self.goto(0, 275)
        self.hideturtle()
        self.update_score()

    def update_score(self):
        self.write(f"Score: {self.count}", align=ALIGNMENT, font=FONT)

    def game_over(self):
        self.goto(0,0)
        self.write(f"GAME OVER", align=ALIGNMENT, font=FONT)

    def increase_score(self):
        self.count += 1
        self.clear()
        self.update_score()


