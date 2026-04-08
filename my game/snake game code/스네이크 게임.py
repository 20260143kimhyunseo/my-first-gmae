import pygame
import random
import sys

pygame.init()

def get_korean_font(size):
    candidates = ["malgungothic", "applegothic", "nanumgothic", "notosanscjk"]
    available = pygame.font.get_fonts()
    for name in candidates:
        if name.lower() in available:
            return pygame.font.SysFont(name, size)
    return pygame.font.SysFont(None, size)

WIDTH, HEIGHT = 800, 600
CELL = 20

WHITE = (255, 255, 255)
GREEN = (50, 200, 50)
DARK = (30, 150, 30)
RED = (220, 50, 50)
GRAY = (40, 40, 40)
PURPLE = (180, 50, 200)
BLUE = (50, 150, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = get_korean_font(36)
font_big = get_korean_font(72)

LEVELS = {
    1: {"speed": 18, "label": "Easy", "obs_time": 3, "time": 120, "bonus": 3},
    2: {"speed": 18, "label": "Normal", "obs_time": 5, "time": 90, "bonus": 3},
    3: {"speed": 18, "label": "Hard", "obs_time": 7, "time": 60, "bonus": 5},
}

def new_pos(snake, obstacles, bonus_blocks):
    while True:
        pos = (
            random.randrange(0, WIDTH // CELL) * CELL,
            random.randrange(0, HEIGHT // CELL) * CELL,
        )
        if (pos not in snake and
            all(pos != o["pos"] for o in obstacles) and
            all(pos != b["pos"] for b in bonus_blocks)):
            return pos

def draw_snake(snake):
    for i, seg in enumerate(snake):
        color = DARK if i == 0 else GREEN
        pygame.draw.rect(screen, color, (*seg, CELL, CELL))

def draw_hud(score, level, time_left):
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Level: {LEVELS[level]['label']}", True, WHITE), (10, 40))
    t = font.render(f"Time: {time_left}s", True, RED)
    screen.blit(t, (WIDTH - t.get_width() - 10, 10))

def game_over_screen(score):
    screen.fill(GRAY)
    screen.blit(font_big.render("GAME OVER", True, RED), (220, 220))
    screen.blit(font.render(f"Score: {score}", True, WHITE), (350, 310))
    screen.blit(font.render("R: Restart   Q: Quit", True, WHITE), (270, 360))
    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: return True
                if e.key == pygame.K_q: return False

def level_select_screen():
    screen.fill(GRAY)
    screen.blit(font_big.render("SNAKE", True, GREEN), (310, 160))
    for lv, info in LEVELS.items():
        screen.blit(font.render(f"{lv}: {info['label']}", True, WHITE),
                    (340, 250 + lv * 40))
    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    return int(e.unicode)

def main():
    while True:
        level = level_select_screen()

        snake = [(WIDTH // 2, HEIGHT // 2)]
        direction = (CELL, 0)
        next_direction = direction

        obstacles = []
        bonus_blocks = []

        food = new_pos(snake, obstacles, bonus_blocks)
        score = 0
        speed = LEVELS[level]["speed"]
        obs_duration = LEVELS[level]["obs_time"] * 1000

        start_time = pygame.time.get_ticks()
        time_limit = LEVELS[level]["time"] * 1000

        obs_timer = 0
        bonus_timer = 0

        running = True
        while running:
            dt = clock.tick(speed)
            obs_timer += dt
            bonus_timer += dt

            current_time = pygame.time.get_ticks()
            time_left = max(0, (time_limit - (current_time - start_time)) // 1000)

            if current_time - start_time >= time_limit:
                if not game_over_screen(score):
                    pygame.quit(); sys.exit()
                break

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP and direction != (0, CELL):
                        next_direction = (0, -CELL)
                    elif e.key == pygame.K_DOWN and direction != (0, -CELL):
                        next_direction = (0, CELL)
                    elif e.key == pygame.K_LEFT and direction != (CELL, 0):
                        next_direction = (-CELL, 0)
                    elif e.key == pygame.K_RIGHT and direction != (-CELL, 0):
                        next_direction = (CELL, 0)

            direction = next_direction

            head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

            # 벽 통과
            x, y = head
            if x < 0: x = WIDTH - CELL
            elif x >= WIDTH: x = 0
            if y < 0: y = HEIGHT - CELL
            elif y >= HEIGHT: y = 0
            head = (x, y)

            # 장애물 충돌
            for o in obstacles:
                if head == o["pos"]:
                    if not game_over_screen(score):
                        pygame.quit(); sys.exit()
                    running = False
                    break
            if not running:
                break

            # 자기 몸 충돌
            if head in snake:
                if not game_over_screen(score):
                    pygame.quit(); sys.exit()
                break

            snake.insert(0, head)

            # 🔥 보너스 블럭 먹기 (시간 + 점수)
            for b in bonus_blocks[:]:
                if head == b["pos"]:
                    time_limit += LEVELS[level]["bonus"] * 1000
                    score += 50  # ⭐ 추가된 부분
                    bonus_blocks.remove(b)

            if head == food:
                score += 10
                food = new_pos(snake, obstacles, bonus_blocks)
            else:
                snake.pop()

            # 장애물 생성
            if obs_timer > 3000:
                obs_timer = 0
                pos = new_pos(snake, obstacles, bonus_blocks)
                obstacles.append({"pos": pos, "time": pygame.time.get_ticks()})

            # 장애물 삭제
            for o in obstacles[:]:
                if pygame.time.get_ticks() - o["time"] > obs_duration:
                    obstacles.remove(o)

            # 보너스 블럭 생성
            if bonus_timer > 5000:
                bonus_timer = 0
                pos = new_pos(snake, obstacles, bonus_blocks)
                bonus_blocks.append({"pos": pos, "time": pygame.time.get_ticks()})

            # 보너스 블럭 삭제
            for b in bonus_blocks[:]:
                if pygame.time.get_ticks() - b["time"] > 3000:
                    bonus_blocks.remove(b)

            screen.fill(GRAY)

            pygame.draw.rect(screen, RED, (*food, CELL, CELL))

            for o in obstacles:
                pygame.draw.rect(screen, PURPLE, (*o["pos"], CELL, CELL))

            for b in bonus_blocks:
                pygame.draw.rect(screen, BLUE, (*b["pos"], CELL, CELL))

            draw_snake(snake)
            draw_hud(score, level, time_left)

            pygame.display.flip()

main()