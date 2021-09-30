__all__ = ['KoDubeolsikDistance']


class KoDubeolsikDistance:

    def __init__(self) -> None:
        from . import Hangul
        from . import KoLevensteinDistance
        self.hangul = Hangul()
        self.dubul_levelstein = KoLevensteinDistance()

    def get_distance(self, src: str, target: str) -> float:
        src_key: str = self.hangul.convert_hangul_to_keystrokes(src)
        target_key: str = self.hangul.convert_hangul_to_keystrokes(target)
        cost = self.dubul_levelstein.get_dubeolsik_distance(src_key, target_key)
        return cost
