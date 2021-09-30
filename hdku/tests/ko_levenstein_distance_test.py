from ..ko_levenstein_distance import KoLevensteinDistance


def test_kolevensteindistance():
    dist = KoLevensteinDistance()
    #  a capital letter <=> a small letter
    assert dist.get_dubeolsik_distance("rhrkawk", "rhrkaWk") == 0.3
    #  a small letter <=> a small letter within 1 keybord space
    assert dist.get_dubeolsik_distance("rhrkawk", "rhrkaqk") == 0.5
    # delete
    assert dist.get_dubeolsik_distance("rhrkawk", "rhrkawkk") == 1
    # insert
    assert dist.get_dubeolsik_distance("rhrkawk", "rhrkaw") == 1
    # space insert
    assert dist.get_dubeolsik_distance("rhrkawk ", "rhrkawk") == 1
    # space delete
    assert dist.get_dubeolsik_distance("rhrkawk", "rhrkawk ") == 0.5
    # number  : 'insert' => 2
    assert dist.get_dubeolsik_distance("rhrkawk", "rhrkawk1") == 2
    # number  : 'delete' => 2
    assert dist.get_dubeolsik_distance("1", "") == 1
    assert dist.get_dubeolsik_distance("", "1") == 1
    assert dist.get_dubeolsik_distance("d", "") == 1
    assert dist.get_dubeolsik_distance("dd", "") == 2
    assert dist.get_dubeolsik_distance("DD", "") == 2
    # phonetic distance
    assert dist.get_dubeolsik_distance("z", "r") == 0.5
