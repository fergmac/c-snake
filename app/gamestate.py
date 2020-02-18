from .astar import astar


class Board:
    def __init__(self, board_data):
        self.height = board_data["height"]
        self.width = board_data["width"]


def up(coord):
    return coord[0], coord[1] - 1


def down(coord):
    return coord[0], coord[1] + 1


def left(coord):
    return coord[0] - 1, coord[1]


def right(coord):
    return coord[0] + 1, coord[1]


class Snake:
    def __init__(self, snake_data, is_you=False):
        self.id = snake_data["id"]
        self.name = snake_data["name"]
        self.health = snake_data["health"]
        self.body = [(body_data["x"], body_data["y"]) for body_data in snake_data["body"]]

    def get_head(self):
        return self.body[0]

    def get_tail(self):
        return self.body[-1]


class Move:
    UP = "up"
    LEFT = "left"
    DOWN = "down"
    RIGHT = "right"

    def __init__(self, direction, distance):
        self.direction = direction
        self.distance = distance


class GameState:
    NO_PATH = 10000

    def __init__(self, data):
        self.turn = data["turn"]
        self.board = Board(data["board"])
        self.you = Snake(data["you"])
        self.snakes = [Snake(snake) for snake in data["board"]["snakes"]]
        self.food = [(food["x"], food["y"]) for food in data["board"]["food"]]

        self.invalid_spaces = self.populate_invalid_spaces()

    def populate_invalid_spaces(self):
        # TODO - Only include possible moves from snakes bigger than you
        invalid_spaces = []
        for snake in self.snakes:
            snake_body = snake.body
            if snake.id == self.you.id:
                snake_body = snake_body[:-1]
            for body in snake_body:
                if body not in invalid_spaces:
                    invalid_spaces.append(body)

            # TODO - Do this better
            if snake.id != self.you.id:
                head = snake.get_head()
                if left(head) not in invalid_spaces:
                    invalid_spaces.append(left(head))
                if right(head) not in invalid_spaces:
                    invalid_spaces.append(right(head))
                if up(head) not in invalid_spaces:
                    invalid_spaces.append(up(head))
                if down(head) not in invalid_spaces:
                    invalid_spaces.append(down(head))

        return invalid_spaces

    def is_bigger_than(self, snake):
        # TODO - Return is bigger than a given snake
        raise NotImplemented

    def move_to_snake_head(self, snake):
        # TODO - Return a move to target the head of a specific snake
        raise NotImplemented

    def move_to_closest_food(self):
        best_move = None

        # TODO - Handle no food case

        for food in self.food:
            possible_move = self.determine_route_to_target(food)
            if not best_move or possible_move.distance < best_move.distance:
                best_move = possible_move

        return best_move.direction

    def move_to_tail(self):
        # TODO - Handle first few turns
        return self.determine_route_to_target(self.you.get_tail()).direction

    def determine_route_to_target(self, target):
        print(f"\nInvalid spaces: {self.invalid_spaces}"
              f"\nWidth: {self.board.width}",
              f"\nHeight: {self.board.height}",
              f"\nStart: {self.you.get_head()}",
              f"\nTarget: {target}\n")
        route = astar(
            invalid_spaces=self.invalid_spaces,
            width=self.board.width,
            height=self.board.height,
            start=self.you.get_head(),
            end=target
        )

        print(f"\nRoute found: {route}\n")
        if not route:
            print("Something went wrong!")
            return Move(Move.UP, self.NO_PATH)

        distance = len(route) if route else self.NO_PATH

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
            print("Something went wrong!")
            return Move(Move.UP, self.NO_PATH)
