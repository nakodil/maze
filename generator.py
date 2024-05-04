import random

WALL = '█'
EMPTY = '░'
BORDER = '█'
ENTER = '@'
EXIT = 'X'
KEY = 'K'


class Maze:
    '''
    Лабиринт - двухмерный список строк вида:
    [
        [WALL, WALL, WALL],
        [WALL, WALL, WALL],
    ]
    В лабиринте должно быть всегда нечетное число рядов и колонн!
    Внутренний (без границ) лабиринт создается
    из (rows - 2) рядов и (cols - 2 колонн) и полностью заполняется тенами;
    Затем бульдозер ломает внутренние стены, пока лабиринт не станет проходим;
    Потом вокруг внутреннего лабиринта создаются границы из стен;
    В границах всерху и снизу пробиваются вход и выход;
    В одну из свободных клеток помещается ключ.
    '''
    def __init__(self, rows: int = 11, cols: int = 25) -> None:
        self.rows = rows - 2  # оставляем 2 стены для границ лабиринта
        self.cols = cols - 2  # оставляем 2 стены для границ лабиринта
        self.map = None
        self.is_ready = False
        self.bulldozer_col = None
        self.bulldozer_row = None
        self.bulldozer_direction = None
        self.generate()
        self.make_path()
        self.make_borders()
        self.make_enter_exit()
        self.make_key()
        self.rows += 2
        self.cols += 2

    def generate(self) -> None:
        '''Заполняет внутренний лабиринт стенами полностью'''
        self.map = [
            [WALL for _ in range(self.cols)] for _ in range(self.rows)
        ]

    def check(self) -> None:
        '''Лабиринт готов, если на четных клетках нет стен'''
        for row in range(self.rows):
            for col in range(self.cols):
                if row % 2 == 0 and col % 2 == 0:
                    if self.map[row][col] == WALL:
                        self.is_ready = False
                        return
        self.is_ready = True

    def make_path(self) -> None:
        '''
        Ставит бульдозер в случайную четную клетку внутреннего лабиринта;
        Запускает цикл, в котором бульдозер ломает стены в своем напрвлении;
        Каждую итерацию бульдозер выбирает случайное направление из возможных;
        В конце итерации проверяется, стал ли лабиринт проходим.
        '''
        self.bulldozer_row = random.choice(range(2, self.rows, 2))
        self.bulldozer_col = random.choice(range(2, self.cols, 2))
        self.map[self.bulldozer_row][self.bulldozer_col] = EMPTY

        while not self.is_ready:
            directions = []
            if self.bulldozer_col > 0:
                directions.append((0, -2))
            if self.bulldozer_col < self.cols - 2:
                directions.append((0, 2))
            if self.bulldozer_row > 0:
                directions.append((-2, 0))
            if self.bulldozer_row < self.rows - 2:
                directions.append((2, 0))

            self.bulldozer_direction = random.choice(directions)
            self.break_walls()
            self.check()

    def break_walls(self) -> None:
        '''
        Ломает стену в соседней с бульдозером клетке и в следующей за ней,
        если через 2 клетки в направлении бульдозера есть стена;
        Меняет координаты бульдозера независимо от тогро, были ли сломаны стены
        за этот ход
        '''
        row = self.bulldozer_row
        col = self.bulldozer_col
        d_row = self.bulldozer_direction[0]
        d_col = self.bulldozer_direction[1]
        if self.map[row + d_row][col + d_col] == WALL:
            self.map[row + d_row // 2][col + d_col // 2] = EMPTY
            self.map[row + d_row][col + d_col] = EMPTY
        self.bulldozer_row += d_row
        self.bulldozer_col += d_col

    def make_borders(self) -> None:
        '''Окружает лабиринт сплошной границей с каждой стороны'''
        self.map.insert(0, [BORDER] * (self.cols))
        self.map.append([BORDER] * (self.cols))
        for row in self.map:
            row.insert(0, BORDER)
            row.append(BORDER)

    def make_enter_exit(self) -> None:
        '''Пробивает вход и выход в первом и последнем рядах карты лабиринта'''
        self.map[0][-2] = EXIT
        self.map[-1][1] = ENTER

    def make_key(self) -> None:
        '''Кладет ключ в любую свободную клетку внутри лаюбиринта'''
        key_row = random.choice(range(1, self.rows, 2))
        key_col = random.choice(range(1, self.cols, 2))
        self.map[key_row][key_col] = KEY

    def get_map(self) -> list[str]:
        '''
        Возвращает карту лабиринта в виде списка строк:
        одна строка для одного ряда
        '''
        map = [''.join(row) for row in self.map]
        return map

    def __str__(self) -> str:
        map_str = ''
        for row in self.map:
            map_str += ''.join(row) + '\n'
        return map_str


maze = Maze(rows=27, cols=47)
print(maze)
