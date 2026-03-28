# 4주차 실습 정리
## 오늘 한 것
- 원형 / AABB / OBB Bounding Box 시각화
- 세 방식의 충돌 판정 차이 관찰


## 관찰 내용


### 원형 vs AABB
원형 충돌(circle)
중심점+반지름으로 판정, 판정 방식(두 중심 거리< 반지름 합 -> 충돌)
특징: 원형 충돌의 특징은 계산이 간단(거리만 계산), 회전 영향 X, 자연스러운 판정(특히 캐릭터)
단점: 네모 물체에는 부정확, 모서리 표현 못함

AABB충돌
축에 정렬돤 사각형, 판정 방식(X축 겹침 AND y축 겹침 -> 충돌)
특징: 매우 빠름, 구현 쉬움(colliderect), 대부분 게임에서 기본으로 사용
단점: 회전 불가능, 실제 모양과 안 맞을 수 있음

요약하자면 circle=자연스러움/AABB=정확하고 빠름


### AABB vs OBB
AABB
특징: 항상 기울지 않음, 계산 매우 빠름, colliderect()로 바로 처리
장점: 구현, 성능 최고, 대부분 기본 충돌에 사용
단점: 회전 표현 불가, 실제 모양보다 크게 잡힘 (부정확)

OBB
특징: 객체 회전에 맞춰 같이 회전, 꼭짓점 직접 계산 필요 ,SAT 알고리즘 사용
장점: 매우 정확한 충돌 판정, 회전 물체 대응 가능
단점: 계산 복잡(느림) 구현 어려움

요약하자면 AABB = 빠른 대충 검사 / OBB = 느리지만 정확한 검사

## AI와의 대화에서 배운 것
내부에 있는 정사각형은 돌아가지 않고 초록색 선만 돌아가게 해줘

좋아 👍 핵심은 회전은 OBB(초록 선)만 하고, 실제 회색 사각형은 회전시키지 않는 것이야.
즉, pygame.transform.rotate()를 제거하면 된다.

아래 코드로 바꿔주면 돼 👇

import pygame
import sys
import math

pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AABB + Circle + OBB")

clock = pygame.time.Clock()

# 색상
GRAY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# 공통 크기
size = 50
radius = size // 2

# 플레이어
player_x = 100
player_y = 100
speed = 5

# 고정 오브젝트 중심
fixed_center = [WIDTH // 2, HEIGHT // 2]

# 회전 변수
angle = 0
rotation_speed = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 키 입력
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= speed
    if keys[pygame.K_RIGHT]:
        player_x += speed
    if keys[pygame.K_UP]:
        player_y -= speed
    if keys[pygame.K_DOWN]:
        player_y += speed

    # Z키 → 회전 속도 증가
    if keys[pygame.K_z]:
        rotation_speed = 5
    else:
        rotation_speed = 1

    angle += rotation_speed

    # 화면 제한
    player_x = max(0, min(WIDTH - size, player_x))
    player_y = max(0, min(HEIGHT - size, player_y))

    # Rect (AABB)
    player_rect = pygame.Rect(player_x, player_y, size, size)

    fixed_rect = pygame.Rect(
        fixed_center[0] - size // 2,
        fixed_center[1] - size // 2,
        size, size
    )

    # 중심 좌표
    player_center = (player_x + radius, player_y + radius)

    # 원형 충돌
    dx = player_center[0] - fixed_center[0]
    dy = player_center[1] - fixed_center[1]
    distance = math.sqrt(dx**2 + dy**2)
    circle_collision = distance < (radius * 2)

    # 배경
    screen.fill(YELLOW if circle_collision else WHITE)

    # 플레이어
    pygame.draw.rect(screen, GRAY, player_rect)
    pygame.draw.rect(screen, RED, player_rect, 2)
    pygame.draw.circle(screen, BLUE, player_center, radius, 2)

    # 🔹 중앙 오브젝트 (회전 ❌)
    pygame.draw.rect(screen, GRAY, fixed_rect)

    # AABB
    pygame.draw.rect(screen, RED, fixed_rect, 2)

    # 원형 Bounding Box
    pygame.draw.circle(screen, BLUE, fixed_center, radius, 2)

    # -------- OBB만 회전 --------
    half = size / 2

    corners = [
        (-half, -half),
        (half, -half),
        (half, half),
        (-half, half)
    ]

    rad = math.radians(angle)

    obb_points = []
    for x, y in corners:
        rx = x * math.cos(rad) - y * math.sin(rad)
        ry = x * math.sin(rad) + y * math.cos(rad)
        obb_points.append((fixed_center[0] + rx, fixed_center[1] + ry))

    # 초록색 OBB만 회전해서 그림
    pygame.draw.polygon(screen, GREEN, obb_points, 2)

    pygame.display.flip()
    clock.tick(60)


## 내 게임에 적용한다면
미로의 함정에 움직이는 벽이나 돌아가는 벽으로 사용하면 좋을 것 같다는 생각이 들어
함정과 관련되어 적용할 것 같습니다.
