from ..hangul_automata import KeystrokeAutomata, JamoAutomata


def test_hangul_automata():
    am = JamoAutomata(False)
    assert am.convert('ㄱㅗㄱㅏㅁㅈㅏ') == '고감자'
    assert am.convert('ㄱㅗㄱㅏㅁㅁㅈㅏ') == 'ㄱㅗㄱㅏㅁㅁㅈㅏ'
    am = JamoAutomata(True)
    assert am.convert('ㄱㅗㄱㅏㅁㅁㅈㅏ') == '고감ㅁ자'

    kam = KeystrokeAutomata(False)
    assert kam.convert("rhrkawk") == '고감자'
    assert kam.convert("rhrkaawk") == 'rhrkaawk'
    kam = KeystrokeAutomata(True)
    assert kam.convert("rhrkaawk") == '고감ㅁ자'
