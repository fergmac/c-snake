from astar import astar


class Board:
    def __init__(self, board_data):
        self.height = board_data["height"]
        self.width = board_data["width"]


class Coordinate:
    def __init__(self, coordinate_data):
        self.x = coordinate_data["x"]
        self.y = coordinate_data["y"]

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def as_tuple(self):
        return self.x, self.y


class SnakeBody(Coordinate):
    pass


class Snake:
    def __init__(self, snake_data):
        self.id = snake_data["id"]
        self.name = snake_data["name"]
        self.health = snake_data["health"]
        self.body = [SnakeBody(body_data) for body_data in snake_data["body"]]

    def get_head(self):
        return self.body[0]

    def get_tail(self):
        return self.body[-1]


class Food(Coordinate):
    pass


class GameState:
    UP = "up"
    LEFT = "left"
    DOWN = "down"
    RIGHT = "right"

    def __init__(self, data):
        self.turn = data["turn"]
        self.board = Board(data["board"])
        self.you = Snake(data["you"])
        self.snakes = [Snake(snake) for snake in data["board"]["snakes"]]
        self.food = [Food(food) for food in data["board"]["food"]]

        self.invalid_spaces = self.populate_invalid_spaces()

    def populate_invalid_spaces(self):
        # TODO - Include possible moves from snakes bigger than you
        invalid_spaces = []
        for snake in self.snakes:
            for body in snake.body:
                self.invalid_spaces.append(body)
        return invalid_spaces

    def is_bigger_than(self, snake):
        # TODO - Return is bigger than a given snake
        raise NotImplemented

    def move_to_snake_head(self, snake):
        # TODO - Return a move to target the head of a specific snake
        raise NotImplemented

    def move_to_food(self):
        # TODO - Select the closest food, not just the first in the array
        return self.determine_route_to_target(self.food[0])

    def move_to_tail(self):
        return self.determine_route_to_target(self.you.get_tail())

    def determine_route_to_target(self, target):
        route = astar(
            invalid_spaces=[space.as_tuple() for space in self.invalid_spaces],
            width=self.board.width,
            height=self.board.height,
            start=self.you.get_head().as_tuple(),
            end=target.as_tuple()
        )

        x_diff = route[1][0] - route[0][0]
        y_diff = route[1][1] - route[0][1]

        if x_diff == -1 and y_diff == 0:
            return self.LEFT
        elif x_diff == 1 and y_diff == 0:
            return self.RIGHT
        elif x_diff == 0 and y_diff == -1:
            return self.DOWN
        elif x_diff == 0 and y_diff == 1:
            return self.UP
        else:
            print("FUCK WHAT DO WE DO")
            return self.UP
