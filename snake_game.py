import curses
import random
import time

def game_loop(window, game_speed):
    curses.curs_set(0)
    snake = [
        [10, 15],
        [9, 15],
        [8, 15],
        [7, 15]
    ]
    current_direction = curses.KEY_DOWN
    fruit = get_new_fruit(window)
    snake_ate_fruit = False
    score = 0

    while True:
        draw_screen(window)
        draw_snake(snake, window)
        draw_actor(fruit, window, curses.ACS_DIAMOND)
        direction = get_new_direction(window, game_speed)
        if direction is None or direction_is_opposite(direction, current_direction):
            direction = current_direction
        move_snake(snake, direction, snake_ate_fruit)
        if snake_hit_border(snake, window):
            break
        if snake_hit_itself(snake):
            break
        if snake_hit_fruit(snake, fruit):
            snake_ate_fruit = True
            fruit = get_new_fruit(window)
            score += 1
        else:
            snake_ate_fruit = False
        current_direction = direction

    finish_game(score, window)

def finish_game(score, window):
    height, width = window.getmaxyx()
    s = f"Você perdeu! Coletou {score} frutas!"
    y = int(height / 2)
    x = int((width - len(s)) / 2)
    window.addstr(y, x, s)
    window.refresh()
    time.sleep(2)

def direction_is_opposite(direction, current_direction):
    if direction == curses.KEY_UP and current_direction == curses.KEY_DOWN:
        return True
    if direction == curses.KEY_DOWN and current_direction == curses.KEY_UP:
        return True
    if direction == curses.KEY_LEFT and current_direction == curses.KEY_RIGHT:
        return True
    if direction == curses.KEY_RIGHT and current_direction == curses.KEY_LEFT:
        return True
    return False

def get_new_fruit(window):
    height, width = window.getmaxyx()
    return [random.randint(1, height - 2), random.randint(1, width - 2)]

def snake_hit_fruit(snake, fruit):
    return fruit in snake

def snake_hit_itself(snake):
    head = snake[0]
    body = snake[1:]
    return head in body

def snake_hit_border(snake, window):
    head = snake[0]
    return actor_hit_border(head, window)

def draw_screen(window):
    window.clear()
    window.border(0)

def draw_snake(snake, window):
    head = snake[0]
    draw_actor(head, window, "@")
    body = snake[1:]
    for body_part in body:
        draw_actor(body_part, window, "0")

def draw_actor(actor, window, char):
    window.addch(actor[0], actor[1], char)

def get_new_direction(window, timeout):
    window.timeout(timeout)
    direction = window.getch()
    if direction in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
        return direction
    else:
        return None

def move_snake(snake, direction, snake_ate_fruit):
    head = snake[0].copy()
    move_actor(head, direction)
    snake.insert(0, head)
    if not snake_ate_fruit:
        snake.pop()

def move_actor(actor, direction):
    match direction:
        case curses.KEY_UP:
            actor[0] -= 1
        case curses.KEY_DOWN:
            actor[0] += 1
        case curses.KEY_LEFT:
            actor[1] -= 1
        case curses.KEY_RIGHT:
            actor[1] += 1

def actor_hit_border(actor, window):
    height, width = window.getmaxyx()
    if actor[0] <= 0 or actor[0] >= height - 1:
        return True
    if actor[1] <= 0 or actor[1] >= width - 1:
        return True
    return False

def select_difficulty():
    difficulty = {
        "1": 1000,
        "2": 500,
        "3": 150,
        "4": 90,
        "5": 20
    }
    while True:
        answer = input("Selecione a dificuldade de 1 a 5:   ")
        game_speed = difficulty.get(answer)
        if game_speed is not None:
            return game_speed
        print("Escolha a dificuldade de 1 a 5:   ")

if __name__ == "__main__":
    curses.wrapper(game_loop, game_speed=select_difficulty())
    print("perdeu!")
