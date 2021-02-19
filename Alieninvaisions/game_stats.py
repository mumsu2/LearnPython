class GameStats:
    """게임 기록 저장"""

    def __init__(self, ai_game):
        """기록 초기화"""
        self.settings = ai_game.settings
        self.reset_stats()
        # 게임을 비활성 상태로 시작
        self.game_active = False


    def reset_stats(self):
        """게임을 진행하는 동안 바뀔 수 있는 기록 초기화"""
        self.ships_left = self.settings.ship_limit
