import pygame
import sys
import math

# Pygame 초기화
pygame.init()

# 화면 설정
TILE_SIZE = 40
COLS = 20
ROWS = 15
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Bounce")
clock = pygame.time.Clock()

# 색상 정의 (RGB)
BG_COLOR = (15, 23, 42)  # slate-900
GRID_COLOR = (30, 41, 59) # slate-800
TEXT_COLOR = (248, 250, 252) # slate-50

PLAYER_COLOR = (56, 189, 248) # sky-400
PLAYER_GLOW = (2, 132, 199) # sky-600

BLOCK_COLOR = (148, 163, 184, 200) # slate-400
BLOCK_BORDER = (203, 213, 225) # slate-300

SPIKE_COLOR = (239, 68, 68) # red-500
SPIKE_GLOW = (185, 28, 28) # red-700

GOAL_COLOR = (74, 222, 128) # green-400
GOAL_GLOW = (22, 163, 74) # green-600

# 블록 타입 상수
EMPTY = 0
NORMAL = 1
SPIKE_UP = 2
SPIKE_DOWN = 3
SPIKE_LEFT = 4
SPIKE_RIGHT = 5
START = 8
GOAL = 9

class Player:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.radius = TILE_SIZE * 0.35
        self.vx = 0
        self.vy = 0
        self.speed = TILE_SIZE * 0.15
        self.gravity = TILE_SIZE * 0.02
        self.bounce_force = -TILE_SIZE * 0.35
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.vx = 0
        self.vy = 0
        self.update_rect()

    def update_rect(self):
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

    def update(self, keys):
        # 좌우 이동
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -self.speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = self.speed
        else:
            self.vx = 0

        # 중력 적용
        self.vy += self.gravity
        
        # 최고 낙하 속도 제한
        if self.vy > TILE_SIZE * 0.4:
            self.vy = TILE_SIZE * 0.4

        self.x += self.vx
        self.y += self.vy
        self.update_rect()

    def draw(self, surface):
        # 네온 효과 (바깥쪽 흐릿한 원)
        pygame.draw.circle(surface, PLAYER_GLOW, (int(self.x), int(self.y)), int(self.radius * 1.3))
        # 본체
        pygame.draw.circle(surface, PLAYER_COLOR, (int(self.x), int(self.y)), int(self.radius))
        # 하이라이트
        pygame.draw.circle(surface, (255, 255, 255, 128), (int(self.x - self.radius * 0.3), int(self.y - self.radius * 0.3)), int(self.radius * 0.2))

class Block:
    def __init__(self, x, y, b_type):
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.type = b_type
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface, time):
        if self.type == NORMAL:
            # 블록 본체
            pygame.draw.rect(surface, (100, 116, 139), self.rect)
            # 네온 엣지 효과
            pygame.draw.rect(surface, BLOCK_BORDER, self.rect, 2)
            inner_rect = pygame.Rect(self.x + 2, self.y + 2, self.width - 4, self.height - 4)
            pygame.draw.rect(surface, (148, 163, 184), inner_rect, 1)

        elif self.type in (SPIKE_UP, SPIKE_DOWN, SPIKE_LEFT, SPIKE_RIGHT):
            self.draw_spike(surface)

        elif self.type == GOAL:
            cx = self.x + self.width / 2
            cy = self.y + self.height / 2
            r = self.width * 0.4
            
            # 네온 글로우
            pygame.draw.circle(surface, GOAL_GLOW, (int(cx), int(cy)), int(r * 1.2))
            
            # 본체
            pygame.draw.circle(surface, GOAL_COLOR, (int(cx), int(cy)), int(r))
            pygame.draw.circle(surface, (255, 255, 255), (int(cx), int(cy)), int(r), 2)
            
            # 펄스 애니메이션
            pulse_r = r * 0.5 + math.sin(time * 0.005) * r * 0.2
            pygame.draw.circle(surface, (255, 255, 255), (int(cx), int(cy)), int(pulse_r))

    def draw_spike(self, surface):
        x, y, w, h = self.x, self.y, self.width, self.height
        points = []
        if self.type == SPIKE_UP:
            points = [(x, y + h), (x + w / 2, y), (x + w, y + h)]
        elif self.type == SPIKE_DOWN:
            points = [(x, y), (x + w / 2, y + h), (x + w, y)]
        elif self.type == SPIKE_LEFT:
            points = [(x + w, y), (x, y + h / 2), (x + w, y + h)]
        elif self.type == SPIKE_RIGHT:
            points = [(x, y), (x + w, y + h / 2), (x, y + h)]

        # 글로우 효과
        glow_points = points.copy() # 단순화를 위해 같은 크기로 그림 (실제로는 약간 더 커야 함)
        pygame.draw.polygon(surface, SPIKE_GLOW, glow_points)
        pygame.draw.polygon(surface, SPIKE_COLOR, points)

stages = [
    # Stage 1: Basic Jump
    [
        "00000000000000000000",
        "00000000000000000000",
        "00000000000000000000",
        "00000000000000000000",
        "00000000000000000000",
        "00000000000000000000",
        "00000000000000000000",
        "00000000000000000000",
        "00000000000000000000",
        "00800000000000000090",
        "00000000000000000000",
        "11100111001110011111",
        "00000000000000000000",
        "00000000000000000000",
        "00000000000000000000"
    ],
    # Stage 2: Spikes introduction
    [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00800000000000000090",
                "00000000000000000000",
                "11110001111000111111",
                "11112221111222111111",
                "11111111111111111111",
                "00000000000000000000"
    ],
    # Stage 3: Height change
    [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000090",
                "00000000000000001111",
                "00000000000000000000",
                "00000000000011110000",
                "00000000000000000000",
                "00000000111100000000",
                "00000000000000000000",
                "00001111000000000000",
                "00800000000000000000",
                "11110000000000000000",
                "00000000000000000000",
                "00000000000000000000"
    ],
    # Stage 4: Spike Tunnel
    [
                "11111111111111111111",
                "11111111111111111111",
                "33333333333333333333",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00800000000000000090",
                "00000012210002200000",
                "11111211111211111111",
                "11111111111111111111",
                "11111111111111111111",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
    ],
    # Stage 5: ZigZag
    [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000090",
                "00800000000000000111",
                "00000000000000000000",
                "01100011000110001100",
                "01100011000110001100",
                "01100011000110001100",
                "00000000000000000000"
    ],
    # Stage 6: Precision Jumps
    [
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000090",
                "00000000011100001111",
                "00001100001100000000",
                "00000000001100000000",
                "00800001101100000000",
                "00000000001100000000",
                "11111100001111111111",
                "11111122221111111111",
                "11111111111111111111",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
    ],
    # Stage 7: Wall of Spikes
    [
                "00000000000000000000",
                "11111111111111111111",
                "11111111111111111111",
                "33333333333333333333",
                "00000333000333000000",
                "00000030000030000000",
                "00800000000000000090",
                "00000000000000000000",
                "11111111111111111111",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000",
                "00000000000000000000"
    ],
     # Stage 8: Stairs
    [
                "00800000000000000000",
                "11100000000000000000",
                "00000000000000000000",
                "00000400000000000000",
                "00000110000000000000",
                "00000000040000000000",
                "00000000011000000000",
                "00000000000004000000",
                "00000000000001100000",
                "00000000000000000000",
                "00000000000000000090",
                "00000000000000000111",
                "22222222222222222111",
                "11111111111111111111",
                "00000000000000000000"
    ],
    # Stage 9: Tight Squeeze
    [
                "00000000000000000000",
                "11111111111111110090",
                "00000000000000000111",
                "00000000000000000000",
                "00111111111111111111",
                "10000000000000000000",
                "00000000000000000000",
                "11111111111111111000",
                "00000000000000000100",
                "00000000000000000000",
                "00011111111111111111",
                "00800000000000000000",
                "11110000000000000000",
                "22222222222222222222",
                "11111111111111111111"
    ],
    # Stage 10: The Finale
    [
                "00000000000000000000",
                "00000000000000000090",
                "00000000000000000111",
                "00000000000002200000",
                "00000000000011110000",
                "00000000020000000000",
                "00000000110000000000",
                "00000200000000000000",
                "00001100000000000000",
                "00800000000000000000",
                "11110000000000000000",
                "22222222222222222222",
                "11111111111111111111",
                "00000000000000000000",
                "00000000000000000000"
    ]
]

def rect_circle_colliding(circle_x, circle_y, radius, rect):
    # 가장 가까운 점 찾기
    closest_x = max(rect.left, min(circle_x, rect.right))
    closest_y = max(rect.top, min(circle_y, rect.bottom))

    # 거리 계산
    distance_x = circle_x - closest_x
    distance_y = circle_y - closest_y

    # 피타고라스 정리로 반지름 이내인지 확인
    return (distance_x ** 2 + distance_y ** 2) < (radius ** 2)

class Game:
    def __init__(self):
        self.state = 'menu' # menu, playing, gameover, clear, allclear
        self.current_stage = 0
        self.deaths = 0
        self.player = None
        self.blocks = []
        
        # 폰트 설정 (기본 폰트 사용)
        self.font_large = pygame.font.SysFont('arial', 64, bold=True)
        self.font_medium = pygame.font.SysFont('arial', 32, bold=True)
        self.font_small = pygame.font.SysFont('arial', 24)

    def load_stage(self, stage_index):
        self.blocks = []
        layout = stages[stage_index]
        
        for y, row in enumerate(layout):
            for x, char in enumerate(row):
                b_type = int(char)
                if b_type == START:
                    self.player = Player(x * TILE_SIZE + TILE_SIZE / 2, y * TILE_SIZE + TILE_SIZE / 2)
                elif b_type != EMPTY:
                    self.blocks.append(Block(x, y, b_type))

    def draw_text(self, text, font, color, y, shadow_color=None):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(WIDTH/2, y))
        
        if shadow_color:
            shadow_surface = font.render(text, True, shadow_color)
            shadow_rect = shadow_surface.get_rect(center=(WIDTH/2, y))
            # 네온 그림자 효과 (여러 번 그려서 흐리게)
            for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                screen.blit(shadow_surface, shadow_rect.move(offset))
                
        screen.blit(text_surface, text_rect)

    def draw_ui(self):
        if self.state == 'playing':
            stage_text = self.font_small.render(f"Stage {self.current_stage + 1}", True, TEXT_COLOR)
            death_text = self.font_small.render(f"Deaths: {self.deaths}", True, TEXT_COLOR)
            screen.blit(stage_text, (20, 20))
            screen.blit(death_text, (WIDTH - 120, 20))

        elif self.state == 'menu':
            # 반투명 오버레이
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((15, 23, 42, 200))
            screen.blit(overlay, (0, 0))
            
            self.draw_text("NEON BOUNCE", self.font_large, PLAYER_COLOR, HEIGHT / 2 - 50, PLAYER_GLOW)
            self.draw_text("Press SPACE to Start", self.font_medium, TEXT_COLOR, HEIGHT / 2 + 50)

        elif self.state == 'gameover':
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((15, 23, 42, 200))
            screen.blit(overlay, (0, 0))
            
            self.draw_text("GAME OVER", self.font_large, SPIKE_COLOR, HEIGHT / 2 - 50, SPIKE_GLOW)
            self.draw_text("Press SPACE to Retry", self.font_medium, TEXT_COLOR, HEIGHT / 2 + 50)

        elif self.state == 'clear':
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((15, 23, 42, 200))
            screen.blit(overlay, (0, 0))
            
            self.draw_text("STAGE CLEAR!", self.font_large, GOAL_COLOR, HEIGHT / 2 - 50, GOAL_GLOW)
            self.draw_text("Press SPACE to Next Stage", self.font_medium, TEXT_COLOR, HEIGHT / 2 + 50)

        elif self.state == 'allclear':
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((15, 23, 42, 200))
            screen.blit(overlay, (0, 0))
            
            self.draw_text("ALL CLEAR!", self.font_large, (250, 204, 21), (202, 138, 4), HEIGHT / 2 - 80)
            self.draw_text(f"Total Deaths: {self.deaths}", self.font_medium, TEXT_COLOR, HEIGHT / 2)
            self.draw_text("Press SPACE to Main Menu", self.font_medium, TEXT_COLOR, HEIGHT / 2 + 80)

def main():
    game = Game()
    running = True

    while running:
        time = pygame.time.get_ticks()
        
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game.state == 'menu':
                        game.state = 'playing'
                        game.current_stage = 0
                        game.deaths = 0
                        game.load_stage(game.current_stage)
                    elif game.state == 'gameover':
                        game.state = 'playing'
                        game.player.reset()
                    elif game.state == 'clear':
                        game.current_stage += 1
                        game.state = 'playing'
                        game.load_stage(game.current_stage)
                    elif game.state == 'allclear':
                        game.state = 'menu'

        keys = pygame.key.get_pressed()

        # 업데이트 로직
        if game.state == 'playing':
            game.player.update(keys)

            # 화면 밖으로 떨어지면 사망
            if game.player.y - game.player.radius > HEIGHT:
                game.state = 'gameover'
                game.deaths += 1

            # 충돌 처리
            if game.state == 'playing':
                prev_y = game.player.y - game.player.vy
                prev_x = game.player.x - game.player.vx

                for block in game.blocks:
                    if rect_circle_colliding(game.player.x, game.player.y, game.player.radius, block.rect):
                        
                        # 목표 도착
                        if block.type == GOAL:
                            if game.current_stage < len(stages) - 1:
                                game.state = 'clear'
                            else:
                                game.state = 'allclear'
                            break
                        
                        # 가시 충돌
                        if block.type in (SPIKE_UP, SPIKE_DOWN, SPIKE_LEFT, SPIKE_RIGHT):
                            game.state = 'gameover'
                            game.deaths += 1
                            break

                        # 일반 블록 바운스
                        if block.type == NORMAL:
                            # 위에서 충돌
                            if prev_y + game.player.radius <= block.rect.top + 5:
                                game.player.y = block.rect.top - game.player.radius
                                game.player.vy = game.player.bounce_force
                            # 아래에서 충돌
                            elif prev_y - game.player.radius >= block.rect.bottom - 5:
                                game.player.y = block.rect.bottom + game.player.radius
                                game.player.vy = 0
                            # 측면 충돌
                            else:
                                if prev_x < block.rect.left:
                                    game.player.x = block.rect.left - game.player.radius
                                elif prev_x > block.rect.right:
                                    game.player.x = block.rect.right + game.player.radius
                            
                            game.player.update_rect()

        # 그리기
        screen.fill(BG_COLOR)
        
        # 격자 배경 (선택적)
        for x in range(0, WIDTH, TILE_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILE_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

        if game.state != 'menu':
            for block in game.blocks:
                block.draw(screen, time)
            if game.player:
                game.player.draw(screen)

        game.draw_ui()

        pygame.display.flip()
        clock.tick(60) # 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
