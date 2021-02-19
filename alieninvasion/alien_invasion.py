import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button

class AlienInvasion:
    """게임 전체의 자원과 동작을 관리하는 클래스"""

    def __init__(self):
        """게임을 초기화하고 게임 자원을 생성"""
        pygame.init() # pygame을 초기화
        self.settings = Settings()

        # 게임 창 크기 설정
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        # 전체화면 설정
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # 게임 기록을 저장할 인스턴스를 만듦
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # 플레이 버튼 생성
        self.play_button = Button(self, "Play")

        # 배경색을 설정
        self.bg_color = (self.settings.bg_color)


    def run_game(self):
        """게임의 메인 루프를 시작"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

            # 사라진 탄환을 제거
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            print(len(self.bullets))


    def _check_events(self):
        """키 입력과 마우스 이벤트에 반응"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        """키 입력에 반응"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        """키에서 손을 뗄 때 반응"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_q:
            sys.exit()


    def _fire_bullet(self):
        """새 탄환을 생성하고 bullets 그룹에 추가함"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """탄환 위치를 업데이트하고 사라진 탄환을 제거"""
        # 탄환 위치를 업데이트
        self.bullets.update()

        # 사라진 탄환을 제거
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        """탄환과 외계인의 충돌에 반응"""
        # 충돌한 탄환과 외계인 제거
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # 남아있는 탄환을 파괴하고 새 함대를 만듦
            self.bullets.empty()
            self._create_fleet()


    def _create_fleet(self):
        """외계인 함대를 만듦"""
        # 외계인 하나를 만들고 한 줄에 몇이 들어갈지 정함
        # 외계인 사이의 공간은 외계인 하나의 너비와 같음
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # 화면 높이에 알맞은 외계인 줄 수를 결정
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # 외계인 함대 생성
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
        """외계인을 만들고 줄에 배치"""
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)


    def _check_fleet_edges(self):
        """외계인이 경계에 닿았다면 그에 맞게 반응"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """함대 전체를 아래로 내리고 방향을 바꿈"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """우주선이 외계인과 충돌했을때 반응"""
        if self.stats.ships_left > 0:
            # ship_left를 줄임
            self.stats.ships_left -= 1

            # 남아있는 외계인과 탄환을 제거
            self.aliens.empty()
            self.bullets.empty()

            # 새 함대를 만들고 우주선을 배치
            self._create_fleet()
            self.ship.center_ship()

            # 일시정지
            sleep(0.5)
        else:
            self.stats.game_active = False


    def _check_aliens_bottom(self):
        """화면 아래쪽에 닿은 외계인이 있는지 체크"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 우주선이 공격당했을 때와 마찬가지로 반응
                self._ship_hit()
                break

    def _update_aliens(self):
        """함대가 가장자리에 있는지 확인한 다음 함대에 있는 모든 외계인의 위치를 업데이트함"""
        self._check_fleet_edges()
        self.aliens.update()

        # 외계인과 우주선이 충돌했는지 확인
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 화면 아래쪽에 닿은 외계인이 있는지 체크
        self._check_aliens_bottom()


    def _update_screen(self):
        # 루프의 반복마다 화면을 표시
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 게임이 비활성 상태이면 플레이 버튼을 그림
        if not self.stats.game_active:
            self.play_button.draw_button()

        # 가장 최근에 그려진 화면을 표시
        pygame.display.flip()

if __name__ == '__main__':
    # 게임 인스턴스를 만들고 게임을 실행
    ai = AlienInvasion()
    ai.run_game()