# Week 3 실습 기록

## 목표
플레이어 캐릭터를 키보드로 움직이기 구현

## AI 대화 기록

Q1:import pygame
import sys
pygame.init() screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Pygame") WHITE = (255, 255, 255) BLUE = (0, 0, 255)
clock = pygame.time.Clock() running = True 3 while running: for event in pygame.event.get():
if event.type == pygame.QUIT: running = False screen.fill(WHITE)
pygame.draw.circle(screen, BLUE, (400, 300), 50) pygame.display.flip()
clock.tick(60) pygame.quit() sys.exit()
이 코딩식에서 오류를 고쳐줘

AI의 답: 문제점은 3개가 있습니다.
1. 3이라는 쓸모없는 숫자 한줄
2.white 아래 들여쓰기 없음
3.for,if도 들여쓰기가 없습니다.
수정된 코드 드립니다.
수정된 코드 적용결과 오류 없이 성공

Q2:키보드 w는 위로 a는 왼쪽으로 s는 뒤로 d는 오른쪽으로 이동할 수 있게 해줘


AI의 답:  # 키 입력 확인
keys = pygame.key.get_pressed()
if keys[pygame.K_w]:
y -= speed
if keys[pygame.K_s]:
y += speed
if keys[pygame.K_a]:
x -= speed
if keys[pygame.K_d]:
x += speed
위 코드를 넣은 결과 wasd를 이용하여 움직이기 성공


Q3: 움직이는 원이 화면 밖으로 나가지 않게 해줘


AI의 답: 원을 화면 밖으로 못 나가게 하려면 좌표 x, y의 범위를 제한하면 됩니다.
원 반지름이 50이므로 화면 경계도 그만큼 고려해야 합니다.
# 화면 경계 제한
 if x < radius:
x = radius
if x > 800 - radius:
x = 800 - radius
 if y < radius:
 y = radius
 if y > 600 - radius:
  y = 600 - radius

  위 코드를 적용하자 원이 화면 밖으로 이탈하지 않음
## 시행착오 및 해결과정
첫 질문을 할 때는 무엇을 해야할 지 명확하게 말하지 않아 원하는 대로 나오지 않는 경우가 많았다.
이를 해결하기 위해 내가 원하는 것이 무엇인지에 대하여 AI에게 정확히 알려주니 원하는 것이 오류없이 나오기 시작했다.


##배운점
AI를 이용하는 경우에도 AI에게 명확하게 알려줘야 오류없이 원하는 것을 얻을수 있다는 것을 배웠다
