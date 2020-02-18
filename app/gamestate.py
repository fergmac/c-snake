from .astar import astar


class Board:
    def __init__(self, board_data):
        self.height = board_data["height"]
        self.width = board_data["width"]


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def as_tuple(self):
        return self.x, self.y

    def up(self):
        return self.x, self.y - 1

    def down(self):
        return self.x, self.y + 1

    def left(self):
        return self.x - 1, self.y

    def right(self):
        return self.x + 1, self.y

class SnakeBody(Coordinate):
    pass


class Snake:
    def __init__(self, snake_data):
        self.id = snake_data["id"]
        self.name = snake_data["name"]
        self.health = snake_data["health"]
        self.body = [SnakeBody(body_data["x"], body_data["y"]) for body_data in snake_data["body"]]

    def get_head(self):
        return self.body[0]

    def get_tail(self):
        return self.body[-1]


class Food(Coordinate):
    pass

class Move:
    UP = "up"
    LEFT = "left"
    DOWN = "down"
    RIGHT = "right"

    def __init__(self, direction, distance):
        self.direction = direction
        self.distance = distance

class GameState:

    def __init__(self, data):
        self.turn = data["turn"]
        self.board = Board(data["board"])
        self.you = Snake(data["you"])
        self.snakes = [Snake(snake) for snake in data["board"]["snakes"]]
        self.food = [Food(food["x"], food["y"]) for food in data["board"]["food"]]

        self.invalid_spaces = self.populate_invalid_spaces()

    def populate_invalid_spaces(self):
        # TODO - Only include possible moves from snakes bigger than you
        invalid_spaces = []
        for snake in self.snakes:
            for body in snake.body:
                if body not in invalid_spaces:
                    invalid_spaces.append(body)
            # TODO - Do this better
            head = snake.get_head()
            if head.left() not in invalid_spaces:
                invalid_spaces.append(head.left())
            if head.right() not in invalid_spaces:
                invalid_spaces.append(head.right())
            if head.up() not in invalid_spaces:
                invalid_spaces.append(head.up())
            if head.down() not in invalid_spaces:
                invalid_spaces.append(head.down())

        return invalid_spaces

    def is_bigger_than(self, snake):
        # TODO - Return is bigger than a given snake
        raise NotImplemented

    def move_to_snake_head(self, snake):
        # TODO - Return a move to target the head of a specific snake
        raise NotImplemented

    def move_to_closest_food(self):
        best_move = None

        for food in self.food:
            possible_move = self.determine_route_to_target(food)
            if not best_move or possible_move.distance < best_move:
                best_move = possible_move

        return best_move.direction

    def move_to_tail(self):
        return self.determine_route_to_target(self.you.get_tail()).direction

    def determine_route_to_target(self, target):
        print(f"\nInvalid spaces: {self.invalid_spaces}"
              f"\nWidth: {self.board.width}",
              f"\nHeight: {self.board.height}",
              f"\nStart: {self.you.get_head().as_tuple()}",
              f"\nTarget: {target.as_tuple()}\n")
        route = astar(
            invalid_spaces=[space.as_tuple() for space in self.invalid_spaces],
            width=self.board.width,
            height=self.board.height,
            start=self.you.get_head().as_tuple(),
            end=target.as_tuple()
        )

        distance = len(route)
        print(f"\nRoute found: {route}\n")

        x_diff = route[1][0] - route[0][0]
        y_diff = route[1][1] - route[0][1]

        if x_diff == -1 and y_diff == 0:
            return Move(Move.LEFT, distance)
        elif x_diff == 1 and y_diff == 0:
            return Move(Move.RIGHT, distance)
        elif x_diff == 0 and y_diff == -1:
            return Move(Move.UP, distance)
        elif x_diff == 0 and y_diff == 1:
            return Move(Move.DOWN, distance)
        else:
            print("FUCK WHAT DO WE DO")
            return Move(Move.UP, 100000)
