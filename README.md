# Turtle Race

## Overview

Turtle Race is a fun, interactive game that allows players to bet on which turtle will win a race. Initially inspired by a Python course project using the Turtle package, this project evolved into a full-fledged game using Pygame and Pygbag, making it deployable on the web for anyone to play.

## Why I Built This

The inspiration for this project came from my ongoing journey to master Python. After creating a simple Turtle Race using the Turtle package, I wanted to make the game accessible to a wider audience. This led me to explore Pygame for game development and Pygbag for deploying Python games on the web. The game you're about to experience is a recreation of that Turtle Race but with a more generalised approach using Pygame.

## Features

- Interactive Gameplay: Players can place bets on which turtle (represented by colored squares) they think will win the race.
- Randomised Race Mechanics: The race outcome is randomised, making each game unique.
- Responsive Design: The game scales well to different screen sizes.
- Web Deployment: Using Pygbag, the game can be played directly in a web browser without the need for any installations.

## Installation

To run the game locally, you'll need Python installed on your machine along with the required dependencies. Follow these steps:

1 Clone the Repository:

```bash
git clone https://github.com/AlanaBF/Turtle-Race
cd turtle-race
```

2 Install Dependencies: Ensure you have Python installed, and then install the dependencies:

```bash
pip install pygame asyncio
```

3 Run the Game: Execute the Python script to start the game:

```bash
python main.py
```

## How to Play

1 Place Your Bet: At the start of the game, you will be prompted to choose a color representing one of the turtles. Type your choice and submit it.

2 Watch the Race: The turtles will race across the screen, with the winner being declared at the end.

3 Play Again: After the race, you’ll be given the option to play again or exit the game.

## Deployment

The game is also deployable on the web using Pygbag. Follow these steps to deploy the game on GitHub Pages:

1 Prepare the Project for Web Deployment:

- Install Pygbag:

```bash
pip install pygbag
```

- Build the project for the web:

```bash
pygbag main.py
```

2 Deploy to GitHub Pages:

- Commit the built files (located in the build/web directory) to the gh-pages branch of your GitHub repository.
- Go to the repository settings on GitHub and enable GitHub Pages, selecting the gh-pages branch as the source.

3 Access the Game:

- Once deployed, your game will be accessible at https://yourusername.github.io/turtle-race/.

## Example Code

Here is the initial Turtle Race code that inspired this project:

```python
import random
from turtle import Turtle, Screen
from tkinter import messagebox
import asyncio

async def main():
    def start_race():
        is_race_on = False
        screen = Screen()
        screen.setup(width=500, height=400)
        user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Choose a color: ")
        colors = ["red", "orange", "yellow", "green", "blue", "purple"]
        y_positions = [-100, -50, 0, 50, 100, 150]
        all_turtles = []

        for turtle_index in range(0, 6):
            new_turtle = Turtle(shape="turtle")
            new_turtle.color(colors[turtle_index])
            new_turtle.penup()
            new_turtle.goto(x=-230, y=y_positions[turtle_index])
            all_turtles.append(new_turtle)
            
        if user_bet:
            is_race_on = True

        while is_race_on:
            for turtle in all_turtles:
                if turtle.xcor() > 230:
                    is_race_on = False
                    winning_color = turtle.pencolor()
                    if winning_color == user_bet:
                        print(f"You've won! The {winning_color} turtle is the winner!")
                        messagebox.showinfo("You've won", f"The {winning_color} turtle is the winner!")
                    else:
                        print(f"You've lost! The {winning_color} turtle is the winner!")
                        messagebox.showinfo("You've lost", f"The {winning_color} turtle is the winner!")
                    play_again = messagebox.askyesno("Game Over", "Do you want to play again?")
                    if play_again:
                        screen.clearscreen()
                        start_race()
                    else:
                        screen.bye()
                    break
                random_distance = random.randint(0, 10)
                turtle.forward(random_distance)

        screen.exitonclick()

    start_race()
    await asyncio.sleep(0)  # Very important, and keep it 0
asyncio.run(main())
```

## Future Improvements

- Add More Visual Effects: Enhance the race with animations and visual effects.
- Improve User Interface: Create a more polished user interface with additional interaction elements.
- Mobile Compatibility: Optimize the game for mobile devices.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

Special thanks to the developers of Pygame and Pygbag for making game development and deployment accessible.
Thanks to my course instructors and the Python community for ongoing support and resources.
