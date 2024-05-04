import tkinter
import random
from maps import maps

WINDOW_TITLE = 'Лабиринт'
WINDOW_BG = 'black'
CANVAS_BG = 'pink'
PLAYER_COLOR = 'lime'

FONT_NAME = 'Impact'
FONT_COLOR = 'gold'

KEY_QUIT = 'Escape'
KEY_UP = 'Up'
KEY_DOWN = 'Down'
KEY_LEFT = 'Left'
KEY_RIGHT = 'Right'
KEY_PLAY = 'Return'

WALL = '█'
EMPTY = '░'
PLAYER = '@'
EXIT = 'X'
KEY = 'K'

MAZE_COLORS = {
    WALL: 'maroon',
    EMPTY: 'black',
    KEY: 'dark orange',
    EXIT: 'RED',
    PLAYER: 'medium sea green'
}


class Game:
    def __init__(self) -> None:
        self.window = tkinter.Tk()
        self.window.title = WINDOW_TITLE
        self.window.attributes('-fullscreen', True)
        self.window['bg'] = WINDOW_BG

        self.cols = len(maps[0][0])
        self.rows = len(maps[0])

        self.tile_size = min(
            self.window.winfo_screenwidth() // self.cols,
            self.window.winfo_screenheight() // self.rows
        )

        self.canvas = tkinter.Canvas(
            self.window,
            width=self.cols * self.tile_size,
            height=self.rows * self.tile_size,
            bg=CANVAS_BG,
            highlightthickness=0
        )

        self.canvas.pack(expand=True)
        self.canvas.focus_set()
        self.canvas.bind('<Key>', self.on_key)
        self.canvas.update()  # До апдейта размер виджетов будет 1 1
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        self.font_size = int(min((self.width, self.height)) * 0.05)

        self.player = None
        self.maze = None
        self.exit_id = None
        self.key_id = None
        self.is_running = False
        self.run()
        self.window.mainloop()

    def show_victory(self) -> None:
        self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text='Победа!\nENTER - новый лабиринт\nESCAPE - выход',
            font=(FONT_NAME, self.font_size),
            fill=FONT_COLOR,
            justify='center',
            tag='victory'
        )
        self.canvas.bind(f'<{KEY_PLAY}>', lambda _: self.run())

    def run(self) -> None:
        self.canvas.unbind(f'<{KEY_PLAY}>')
        self.canvas.delete('all')
        self.maze = random.choice(maps)
        self.draw_maze()

        self.player = Player(
            self,
            1,
            self.rows - 2,
            PLAYER_COLOR
        )

        self.is_running = True
        self.player.draw()

    def on_key(self, event: tkinter.Event) -> None:
        '''Диспетчер клавиш'''
        if event.keysym == KEY_QUIT:
            self.window.destroy()
        elif event.keysym == KEY_RIGHT:
            self.player.move(1, 0)
        elif event.keysym == KEY_LEFT:
            self.player.move(-1, 0)
        elif event.keysym == KEY_UP:
            self.player.move(0, -1)
        elif event.keysym == KEY_DOWN:
            self.player.move(0, 1)

    def draw_maze(self) -> None:
        for row_idx, row in enumerate(self.maze):
            for col_idx, col in enumerate(row):
                id = self.canvas.create_rectangle(
                    col_idx * self.tile_size,
                    row_idx * self.tile_size,
                    col_idx * self.tile_size + self.tile_size,
                    row_idx * self.tile_size + self.tile_size,
                    fill=MAZE_COLORS[col],
                    outline=''
                )
                if col == EXIT:
                    self.exit_id = id
                elif col == KEY:
                    self.key_id = id


class Player:
    '''Игрок'''
    def __init__(
            self,
            game: Game,
            col: int,
            row: int,
            color: str,
    ) -> None:
        self.game = game
        self.canvas = self.game.canvas
        self.maze = self.game.maze
        self.col = col
        self.row = row
        self.size = self.game.tile_size
        self.color = color
        self.outline = ''
        self.tag = 'player'
        self.has_key = False
        self.exit_col = (len(self.maze[0]) - 2)
        self.exit_row = 0

    def draw(self) -> None:
        '''Рисует игрока'''
        self.canvas.delete(self.tag)
        self.canvas.create_rectangle(
            self.col * self.size,
            self.row * self.size,
            self.col * self.size + self.size,
            self.row * self.size + self.size,
            fill=PLAYER_COLOR,
            outline=self.outline,
            tags=self.tag,
        )

    def move(self, dx: int, dy: int) -> None:
        if not self.game.is_running:
            return

        new_col = self.col + dx
        new_row = self.row + dy

        if self.maze[new_row][new_col] == WALL:
            return

        if self.maze[new_row][new_col] == EXIT and not self.has_key:
            return

        if self.maze[new_row][new_col] == EXIT and self.has_key:
            self.game.is_running = False
            self.game.show_victory()

        if self.maze[new_row][new_col] == KEY:
            if not self.has_key:
                self.has_key = True
                self.outline = MAZE_COLORS[KEY]
                self.canvas.itemconfig(
                    self.game.key_id, fill=MAZE_COLORS[EMPTY]
                )
                self.canvas.itemconfig(self.game.exit_id, fill='green')

        self.col = new_col
        self.row = new_row
        self.draw()


if __name__ == '__main__':
    Game()
