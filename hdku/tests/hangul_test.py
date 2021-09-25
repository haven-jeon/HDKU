from ..hangul import Hangul

def test_Hangul():
    h = Hangul()
    ret = h.convert_hangul_to_keystrokes('전희원', True, True)
    assert ret == 'ｗｊｓ｜ｇｍｌ｜ｄｎｊｓ｜'
    ret = h.convert_hangul_to_keystrokes('전희원', False, True)
    assert ret == 'wjs｜gml｜dnjs｜'
    ret = h.convert_hangul_to_keystrokes('전희원', False, False)
    assert ret == 'wjsgmldnjs'
    ret = h.convert_hangul_to_keystrokes('전희원', True, False)
    assert ret == 'ｗｊｓｇｍｌｄｎｊｓ'
