from ..utils import KoDubeolsikDistance


def test_KoDubeolsikDistance():
    kdd = KoDubeolsikDistance()
    assert kdd.get_distance("안녕하세요", "안녕하세요") == 0
    assert kdd.get_distance("안녕하세요", "안녕허세요") == 0.5
    assert kdd.get_distance("안녕하세요", "안녕허ㅓ세요") == 1.5
    assert kdd.get_distance("안녕하세요", "안녕하셈") == 2
    assert kdd.get_distance("아주 바뻐요", "아주 바빠요") == 0.5
    assert kdd.get_distance("아버지가 방에 들어가셨다.", "아버지 가방에 들어가셨다.") == 1.5
    assert kdd.get_distance("찡그린 상판때기가 너무 보기 싫어", "찡그린 상판떼기가 너무 보기 싫어") == 0.5
    assert kdd.get_distance("찡그린 상판때기가 너무 보기 싫어", "찡그린 상판때기게 너무 보기 싫어") == 1.0
