import tkinter as tk
import random
import math

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500
# Amount of pieces for each group.
PIECES = 50
# Delay must be an interger.
# 20ms delay is equal to 50 FPS.
DELAY = 20
# Speed of items.
SPEED = 2

root = tk.Tk()
root.title("Rock Paper Scissors Simulator")

canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
canvas.pack()

leaderboard_text = tk.StringVar()
leaderboard_label = tk.Label(root, textvariable=leaderboard_text)
leaderboard_label.pack()

rock_image = tk.PhotoImage(file="rock.png")
paper_image = tk.PhotoImage(file="paper.png")
scissors_image = tk.PhotoImage(file="scissors.png")

items = []

for _ in range(PIECES):
    items.append(canvas.create_image((random.randint(0, CANVAS_WIDTH), random.randint(0, CANVAS_HEIGHT)), image=rock_image, tags=("rock", random.randint(0, 360))))
    items.append(canvas.create_image((random.randint(0, CANVAS_WIDTH), random.randint(0, CANVAS_HEIGHT)), image=paper_image, tags=("paper", random.randint(0, 360))))
    items.append(canvas.create_image((random.randint(0, CANVAS_WIDTH), random.randint(0, CANVAS_HEIGHT)), image=scissors_image, tags=("scissors", random.randint(0, 360))))

# Used for bouncing items off walls.
def reflect_angle(normal_angle, incident_angle):
    reflected_angle = 2 * normal_angle - incident_angle
    reflected_angle %= 360
    return reflected_angle

def game_loop():
    rock_count = 0
    paper_count = 0
    scissors_count = 0

    for item in items:
        tags = canvas.gettags(item)

        direction = int(tags[1])
        radians = math.radians(direction)
        dx = SPEED * math.cos(radians)
        dy = SPEED * math.sin(radians)
        canvas.move(item, dx, dy)

        left, top, right, bottom = canvas.bbox(item)

        if left < 0:
            direction = reflect_angle(90, direction)
            canvas.moveto(item, x=0)
        elif right > CANVAS_WIDTH:
            direction = reflect_angle(270, direction)
            canvas.moveto(item, x=CANVAS_WIDTH-20)
        elif top < 0:
            direction = reflect_angle(0, direction)
            canvas.moveto(item, y=0)
        elif bottom > CANVAS_HEIGHT:
            direction = reflect_angle(180, direction)
            canvas.moveto(item, y=CANVAS_HEIGHT-20)

        item_type = tags[0]

        if item_type == "rock":
            rock_count += 1
        elif item_type == "paper":
            paper_count += 1
        else:
            scissors_count += 1

        for collided in canvas.find_overlapping(left, top, right, bottom):
            if item_type == "rock" and canvas.gettags(collided)[0] == "paper":
                canvas.itemconfigure(item, image=paper_image, tags=("paper", direction))
                break
            elif item_type == "paper" and canvas.gettags(collided)[0] == "scissors":
                canvas.itemconfigure(item, image=scissors_image, tags=("scissors", direction))
                break
            elif item_type == "scissors" and canvas.gettags(collided)[0] == "rock":
                canvas.itemconfigure(item, image=rock_image, tags=("rock", direction))
                break
        else:
            canvas.itemconfig(item, tags=(item_type, direction))

    leaderboard_text.set(f"Rock: {rock_count} Paper: {paper_count} Scissors: {scissors_count}")

    root.after(DELAY, game_loop)

game_loop()

root.mainloop()
