import pygame
import sys
import math

pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Debug")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# 색상
GRAY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)  # 🔥 추가

# 크기
size = 50
radius = size // 2

# 플레이어
player_x = 100
player_y = 100
speed = 5

# 중앙 오브젝트
fixed_center = [WIDTH // 2, HEIGHT // 2]

# 회전
angle = 0
base_speed = 1.5
boost_speed = 4

# -------- SAT 함수 --------
def get_axes(points):
    axes = []
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]
        edge = (p2[0] - p1[0], p2[1] - p1[1])
        normal = (-edge[1], edge[0])
        length = math.sqrt(normal[0]**2 + normal[1]**2)
        axes.append((normal[0]/length, normal[1]/length))
    return axes

def project(points, axis):
    dots = [p[0]*axis[0] + p[1]*axis[1] for p in points]
    return min(dots), max(dots)

def sat_collision(poly1, poly2):
    axes = get_axes(poly1) + get_axes(poly2)
    for axis in axes:
        min1, max1 = project(poly1, axis)
        min2, max2 = project(poly2, axis)
        if max1 < min2 or max2 < min1:
            return False
    return True

# -------- 메인 루프 --------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # 이동
    if keys[pygame.K_LEFT]:
        player_x -= speed
    if keys[pygame.K_RIGHT]:
        player_x += speed
    if keys[pygame.K_UP]:
        player_y -= speed
    if keys[pygame.K_DOWN]:
        player_y += speed

    # 회전 속도
    if keys[pygame.K_z]:
        rotation_speed = base_speed + boost_speed
    else:
        rotation_speed = base_speed

    angle += rotation_speed

    # 화면 제한
    player_x = max(0, min(WIDTH - size, player_x))
    player_y = max(0, min(HEIGHT - size, player_y))

    # Rect
    player_rect = pygame.Rect(player_x, player_y, size, size)
    fixed_rect = pygame.Rect(
        fixed_center[0] - size//2,
        fixed_center[1] - size//2,
        size, size
    )

    # 중심
    player_center = player_rect.center

    # -------- Circle 충돌 --------
    dx = player_center[0] - fixed_center[0]
    dy = player_center[1] - fixed_center[1]
    distance = math.sqrt(dx**2 + dy**2)
    circle_hit = distance < (radius * 2)

    # -------- AABB 충돌 --------
    aabb_hit = player_rect.colliderect(fixed_rect)

    # -------- OBB (회전) --------
    half = size / 2
    corners = [(-half,-half),(half,-half),(half,half),(-half,half)]
    rad = math.radians(angle)

    obb_points = []
    for x, y in corners:
        rx = x * math.cos(rad) - y * math.sin(rad)
        ry = x * math.sin(rad) + y * math.cos(rad)
        obb_points.append((fixed_center[0] + rx, fixed_center[1] + ry))

    player_points = [
        (player_rect.left, player_rect.top),
        (player_rect.right, player_rect.top),
        (player_rect.right, player_rect.bottom),
        (player_rect.left, player_rect.bottom)
    ]

    obb_hit = sat_collision(player_points, obb_points)

    # 배경
    if circle_hit or aabb_hit or obb_hit:
        screen.fill(RED)
    else:
        screen.fill(WHITE)

    # 오브젝트
    pygame.draw.rect(screen, GRAY, player_rect)
    pygame.draw.rect(screen, RED, player_rect, 2)
    pygame.draw.circle(screen, BLUE, player_center, radius, 2)

    pygame.draw.rect(screen, GRAY, fixed_rect)
    pygame.draw.rect(screen, RED, fixed_rect, 2)
    pygame.draw.circle(screen, BLUE, fixed_center, radius, 2)

    pygame.draw.polygon(screen, GREEN, obb_points, 2)

    # 텍스트
    circle_text = f"Circle: {'HIT' if circle_hit else 'MISS'}"
    aabb_text = f"AABB: {'HIT' if aabb_hit else 'MISS'}"
    obb_text = f"OBB: {'HIT' if obb_hit else 'MISS'}"

    screen.blit(font.render(circle_text, True, BLUE), (10, 10))
    screen.blit(font.render(aabb_text, True, YELLOW), (10, 40))  # 🔥 변경됨
    screen.blit(font.render(obb_text, True, GREEN), (10, 70))

    pygame.display.flip()
    clock.tick(60)