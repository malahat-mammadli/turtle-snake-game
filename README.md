## Turtle Parade (Snake Game)

A polished, visually engaging twist on the classic Snake game, built entirely with Python's turtle graphics. Lead a parade of baby turtles, manage your speed, and beat your high score!

## Features

Custom Game Loop: Built from scratch with grid-based collision detection and movement logic.

Difficulty Scaling: Choose between Easy, Medium, and Hard. The game speed dynamically increases as your parade grows.

Persistent High Scores: Saves your best runs locally using a JSON-based scoring system.

Dynamic UI: Real-time Heads-Up Display (HUD) tracking current score, lives, and all-time high score.

Modern Color Palette: Uses a curated selection of vibrant colors for the baby turtles.

## Installation & Running

This project uses only Python's standard library. No external dependencies are required.

Clone the repository:
```bash
git clone [https://github.com/malahat-mammadli/turtle-snake-game.git](https://github.com/malahat-mammadli/turtle-snake-game.git)
```

Run the game:
```bash
python main.py
```

## Controls

Arrow Keys: Change direction of the turtle parade.

Space: Play again (after Game Over).

Escape: Quit the application.

## Technical Details

Logic: Object-Oriented Programming (OOP) for game state management.

Data: highscores.json for persistence.

Graphics: Event-driven animation with the turtle.Screen().update() method.
