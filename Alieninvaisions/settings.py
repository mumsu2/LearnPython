class Settings:
    """게임 세팅을 모두 저장하는 클래스"""
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 우주선 속도 세팅
        self.ship_speed = 1.5

        # 탄환 세팅
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3