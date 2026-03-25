import turtle
import random
import time
import json
import os


SETTINGS: dict = {
    "easy":   {"speed": 0.18, "label": "EASY",   "color": "lime green"},
    "medium": {"speed": 0.12, "label": "MEDIUM",  "color": "orange"},
    "hard":   {"speed": 0.07, "label": "HARD",    "color": "red"},
}

GRID_SIZE: int = 20
GRID_W:    int = 30
GRID_H:    int = 28
WIN_W:     int = GRID_W * GRID_SIZE   
WIN_H:     int = GRID_H * GRID_SIZE   
PANEL_H:   int = 60

DIRECTIONS: tuple = (
    ("Up",    ( 0,  1)),
    ("Down",  ( 0, -1)),
    ("Left",  (-1,  0)),
    ("Right", ( 1,  0)),
)
DIR_MAP: dict = {name: vec for name, vec in DIRECTIONS}

BABY_COLORS: list = [
    c for c in ["#FFE66D", "#4ECDC4", "#A78BFA", "#F97316",
                "#EC4899", "#06B6D4", "#84CC16", "#FF6B6B"]
]

NUM_BABIES: int = 4   
SCORE_FILE: str = os.path.join(os.path.dirname(__file__), "highscores.json")

def load_highscore() -> int:    
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            data: dict = json.load(f)
            return data.get("highscore", 0)
    return 0

def save_highscore(score: int) -> None:    
    with open(SCORE_FILE, "w") as f:
        json.dump({"highscore": score}, f, indent=2)

def setup_screen() -> turtle._Screen:    
    screen = turtle.Screen()
    screen.title("🐢  Turtle Parade  –  Arrow Keys to Lead!")
    screen.bgcolor("#1A0D12")
    screen.setup(width=WIN_W, height=WIN_H + PANEL_H)
    screen.tracer(0)   
    return screen

def make_t(shape: str = "turtle",
           color: str = "white",
           size: float = 1.0,
           visible: bool = True) -> turtle.Turtle:
    t = turtle.Turtle()
    t.shape(shape)
    t.color(color)
    t.shapesize(size, size)
    t.penup()
    t.speed(0)
    if not visible:
        t.hideturtle()
    return t


def make_writer() -> turtle.Turtle:
    w = turtle.Turtle()
    w.hideturtle()
    w.penup()
    w.color("white")
    w.speed(0)
    return w

def grid_to_px(gx: int, gy: int) -> tuple:
    px = gx * GRID_SIZE - WIN_W // 2 + GRID_SIZE // 2
    py = gy * GRID_SIZE - WIN_H // 2 + GRID_SIZE // 2 - PANEL_H // 2
    return px, py


def random_free_cell(occupied: set) -> tuple:
    while True:
        cell = (random.randint(1, GRID_W - 2),
                random.randint(1, GRID_H - 2))
        if cell not in occupied:
            return cell
    return cell  


def dir_to_heading(dx: int, dy: int) -> float:
    if dx == 1:  return 0.0
    if dx == -1: return 180.0
    if dy == 1:  return 90.0
    return 270.0

def draw_border(pen: turtle.Turtle) -> None:
    pen.hideturtle()
    pen.penup()
    pen.color("#FF69B4")
    pen.pensize(3)
    x0, y0 = grid_to_px(0, 0)
    x1, y1 = grid_to_px(GRID_W, GRID_H)
    pen.goto(x0, y0)
    pen.pendown()
    for corner in [(x1, y0), (x1, y1), (x0, y1), (x0, y0)]:
        pen.goto(*corner)
    pen.penup()

def show_difficulty_menu(screen: turtle._Screen,
                          writer: turtle.Turtle) -> str:

    writer.clear()

    writer.goto(0, 90)
    writer.color("#FF69B4")
    writer.write("🐢  TURTLE PARADE", align="center",
                 font=("Courier", 26, "bold"))

    writer.goto(0, 48)
    writer.color("white")
    writer.write("Collect baby turtles – they join your parade!",
                 align="center", font=("Courier", 10, "normal"))

    writer.goto(0, 12)
    writer.color("#AAAAAA")
    writer.write("Choose Difficulty:", align="center",
                 font=("Courier", 13, "normal"))

    for i, (key, cfg) in enumerate(SETTINGS.items()):
        writer.goto(0, -16 - i * 28)
        writer.color(cfg["color"])
        writer.write(f"  {i+1}.  {cfg['label']}", align="center",
                     font=("Courier", 13, "bold"))

    writer.goto(0, -115)
    writer.color("#666666")
    writer.write("(type 1, 2 or 3 then press OK)", align="center",
                 font=("Courier", 10, "normal"))

    screen.update()

    choice_map: dict = {"1": "easy", "2": "medium", "3": "hard"}
    while True:
        answer = screen.textinput("Difficulty",
                                  "Enter 1 (Easy)  2 (Medium)  3 (Hard):")
        if answer in choice_map:
            return choice_map[answer]
        if answer is None:
            return "medium"
    return "medium" 

def update_hud(writer: turtle.Turtle,
               score: int, high: int,
               difficulty: str, lives: int,
               parade_len: int) -> None:
    writer.clear()

    writer.goto(-WIN_W // 2 + 10, WIN_H // 2 - PANEL_H + 14)
    writer.color("#FF69B4")
    writer.write(f"SCORE: {score:04d}  🐢x{parade_len}",
                 align="left", font=("Courier", 12, "bold"))

    writer.goto(0, WIN_H // 2 - PANEL_H + 14)
    writer.color("#FFE66D")
    writer.write(f"BEST: {high:04d}", align="center",
                 font=("Courier", 12, "bold"))

    cfg = SETTINGS[difficulty]
    writer.goto(WIN_W // 2 - 10, WIN_H // 2 - PANEL_H + 14)
    writer.color(cfg["color"])
    writer.write(f"{cfg['label']}  {'v' * lives}", align="right",
                 font=("Courier", 12, "bold"))

    writer.goto(-WIN_W // 2, WIN_H // 2 - PANEL_H + 4)
    writer.color("#3A1A2A")
    writer.write("-" * 60, align="left",
                 font=("Courier", 11, "normal"))


def show_game_over(writer: turtle.Turtle,
                   score: int, high: int,
                   new_record: bool) -> None:
    writer.clear()

    writer.goto(0, 60)
    writer.color("#FF6B6B")
    writer.write("GAME  OVER", align="center",
                 font=("Courier", 32, "bold"))

    writer.goto(0, 10)
    writer.color("white")
    writer.write(f"Your Score: {score}", align="center",
                 font=("Courier", 16, "normal"))

    if new_record:
        writer.goto(0, -28)
        writer.color("#FFE66D")
        writer.write("NEW HIGH SCORE!", align="center",
                     font=("Courier", 14, "bold"))
    else:
        writer.goto(0, -28)
        writer.color("#888888")
        writer.write(f"Best: {high}", align="center",
                     font=("Courier", 13, "normal"))

    writer.goto(0, -68)
    writer.color("#FF69B4")
    writer.write("SPACE to play again  |  ESC to quit",
                 align="center", font=("Courier", 11, "normal"))


class TurtleParadeGame:
    def __init__(self, screen: turtle._Screen,
                 difficulty: str = "medium") -> None:
        self.screen     = screen
        self.difficulty = difficulty
        self.delay      = SETTINGS[difficulty]["speed"]
        self.score      = 0
        self.lives      = 3
        self.highscore  = load_highscore()
        self.running    = True
        self.paused     = False
        self.new_record = False

        sx, sy = GRID_W // 2, GRID_H // 2
        self.body: list       = [(sx, sy), (sx - 1, sy), (sx - 2, sy)]
        self.direction: tuple = DIR_MAP["Right"]
        self.occupied: set    = set(self.body)

        self.segments: list = []
        self._build_segments()

        self.babies: dict = {}
        self.rand_color = lambda: random.choice(BABY_COLORS)
        self._spawn_babies()

        border_pen = make_t(shape="square", visible=False)
        draw_border(border_pen)

        self.writer = make_writer()
        update_hud(self.writer, self.score, self.highscore,
                   self.difficulty, self.lives, len(self.body))

        self._bind_keys()

    def _build_segments(self) -> None:
        dx, dy  = self.direction
        heading = dir_to_heading(dx, dy)

        for i, (gx, gy) in enumerate(self.body):
            color = "#FF69B4" if i == 0 else "#C2185B"
            size  = 0.9      if i == 0 else 0.7
            seg   = make_t("turtle", color, size)
            seg.setheading(heading)
            seg.goto(*grid_to_px(gx, gy))
            self.segments.append(seg)

    def _spawn_babies(self) -> None:
        all_taken: set = self.occupied | set(self.babies.keys())

        while len(self.babies) < NUM_BABIES:
            cell  = random_free_cell(all_taken)
            bt    = make_t("turtle", self.rand_color(), 0.55)
            bt.setheading(random.choice([0, 90, 180, 270]))
            bt.goto(*grid_to_px(*cell))
            self.babies[cell] = bt
            all_taken.add(cell)

    def _bind_keys(self) -> None:
        for key, vec in DIR_MAP.items():
            self.screen.onkey(lambda v=vec: self._turn(v), key)  # type: ignore[arg-type]
        self.screen.onkey(self._toggle_pause, "p")
        self.screen.onkey(self._toggle_pause, "P")
        self.screen.listen()

    def _turn(self, new_dir: tuple) -> None:
        dx, dy   = self.direction
        ndx, ndy = new_dir
        if (dx + ndx, dy + ndy) != (0, 0):
            self.direction = new_dir

    def _toggle_pause(self) -> None:
        self.paused = not self.paused

    def _step(self) -> bool:        
        head_x, head_y = self.body[0]
        dx, dy         = self.direction

        nhx = (head_x + dx) % GRID_W
        nhy = (head_y + dy) % GRID_H
        new_head = (nhx, nhy)

        if new_head in self.occupied:
            return False

        collected = new_head in self.babies

        self.body.insert(0, new_head)
        self.occupied.add(new_head)

        heading  = dir_to_heading(dx, dy)
        head_seg = make_t("turtle", "#FF69B4", 0.9)
        head_seg.setheading(heading)
        head_seg.goto(*grid_to_px(*new_head))
        self.segments.insert(0, head_seg)

        if len(self.segments) > 1:
            self.segments[1].color("#C2185B")
            self.segments[1].shapesize(0.7, 0.7)

        if collected:
            baby_t = self.babies.pop(new_head)
            baby_t.hideturtle()
            del baby_t

            self.score += 10
            self.delay  = max(0.04, self.delay * 0.99)
            if self.score > self.highscore:
                self.highscore  = self.score
                self.new_record = True

            self._spawn_babies()   
        else:
            tail    = self.body.pop()
            self.occupied.discard(tail)
            old_seg = self.segments.pop()
            old_seg.hideturtle()
            del old_seg

        headings: list = [
            dir_to_heading(
                self.body[i-1][0] - self.body[i][0],
                self.body[i-1][1] - self.body[i][1]
            )
            for i in range(1, len(self.body))
        ]
        for i, h in enumerate(headings):
            self.segments[i + 1].setheading(h)

        return True

    def _respawn(self) -> None:
        for seg in self.segments:
            seg.hideturtle()
        self.segments.clear()
        self.body.clear()
        self.occupied.clear()

        sx, sy         = GRID_W // 2, GRID_H // 2
        self.body      = [(sx, sy), (sx - 1, sy), (sx - 2, sy)]
        self.occupied  = set(self.body)
        self.direction = DIR_MAP["Right"]
        self._build_segments()

    def run(self) -> None:
        while self.running:
            self.screen.update()

            if self.paused:
                time.sleep(0.05)
                continue

            alive = self._step()
            update_hud(self.writer, self.score, self.highscore,
                       self.difficulty, self.lives, len(self.body))
            self.screen.update()

            if not alive:
                self.lives -= 1
                if self.lives > 0:
                    for _ in range(6):
                        self.screen.bgcolor("#3D0020")
                        self.screen.update()
                        time.sleep(0.07)
                        self.screen.bgcolor("#1A0D12")
                        self.screen.update()
                        time.sleep(0.07)
                    self._respawn()
                else:
                    save_highscore(self.highscore)
                    self.writer.clear()
                    show_game_over(self.writer, self.score,
                                   self.highscore, self.new_record)
                    self.screen.update()
                    self.running = False

            time.sleep(self.delay)

    def cleanup(self) -> None:
        for seg in self.segments:
            seg.hideturtle()
        for bt in self.babies.values():
            bt.hideturtle()
        self.writer.clear()


def main() -> None:
    screen      = setup_screen()
    menu_writer = make_writer()
    play_again  = True

    while play_again:
        difficulty = show_difficulty_menu(screen, menu_writer)
        menu_writer.clear()
        screen.update()

        game = TurtleParadeGame(screen, difficulty)
        game.run()

        replay_flag = [False]
        quit_flag   = [False]

        screen.onkey(lambda: replay_flag.__setitem__(0, True), "space")
        screen.onkey(lambda: quit_flag.__setitem__(0, True),   "Escape")
        screen.listen()

        while not replay_flag[0] and not quit_flag[0]:
            screen.update()
            time.sleep(0.05)

        game.cleanup()
        screen.onkey(None, "space")    # type: ignore[arg-type]
        screen.onkey(None, "Escape")  # type: ignore[arg-type]

        play_again = replay_flag[0]

    screen.bye()


if __name__ == "__main__":
    main()