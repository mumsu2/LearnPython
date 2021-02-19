class Settings:
    """게임 세팅을 모두 저장하는 클래스"""
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 우주선 속도 세팅
        self.ship_speed = 1.5
        self.ship_limit = 3

        # 탄환 세팅
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # 외계인 세팅
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction이 1이면 오른쪽, -1이면 왼쪽
        self.fleet_direction = 1