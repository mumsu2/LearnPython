class Settings:
    """게임 세팅을 모두 저장하는 클래스"""
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 우주선 속도 세팅
        self.ship_limit = 3

        # 탄환 세팅
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # 외계인 세팅
        self.fleet_drop_speed = 10

        # 게임이 빨라지는 정도
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """게임을 진행하며 바뀌는 세팅을 초기화"""
        self.sheep_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction이 1이면 오른쪽, -1이면 왼쪽
        self.fleet_direction = 1

        # 점수 기록하기
        self.alien_points = 50



    def increase_speed(self):
        """속도 세팅을 올림"""
        self.sheep_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale