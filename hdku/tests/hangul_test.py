from ..hangul import Hangul


def test_Hangul():
    h = Hangul()
    # convert_hangul_to_keystrokes
    ret = h.convert_hangul_to_keystrokes('전희원', True, True)
    assert ret == 'ｗｊｓ｜ｇｍｌ｜ｄｎｊｓ｜'
    ret = h.convert_hangul_to_keystrokes('전희원', False, True)
    assert ret == 'wjs｜gml｜dnjs｜'
    ret = h.convert_hangul_to_keystrokes('전희원', False, False)
    assert ret == 'wjsgmldnjs'
    ret = h.convert_hangul_to_keystrokes('전희원', True, False)
    assert ret == 'ｗｊｓｇｍｌｄｎｊｓ'
    # convert_hangul_to_jamos
    ret = h.convert_hangul_to_jamos("전희원", False)
    assert ret == 'ㅈㅓㄴㅎㅢㅇㅝㄴ'
    ret = h.convert_hangul_to_jamos("전희원", True)
    assert ret == 'ㅈㅓㄴ｜ㅎㅢ｜ㅇㅝㄴ｜'
    # is_moeum
    assert h.is_moeum('ㅒ')
    assert h.is_moeum('ㅣ')
    assert h.is_moeum('ㅈ') is False
    assert h.is_moeum('A') is False
    # is_ascii
    assert h.is_ascii('asdasvABA')
    assert h.is_ascii('sㄱasvABA') is False
    # is_jaeum
    assert h.is_jaeum('ㄲㅇ')
    assert h.is_jaeum('ㄲ ㅇ') is False
    assert h.is_jaeum('ㄲㅐㅇ') is False
    # is_hangul
    assert h.is_hangul('ㄲㅐㅇ크게놀자')
    assert h.is_hangul('ㄲㅐ ㅇ크게놀자') is False
    assert h.is_hangul('ㄲㅐaㅇB게놀자') is False
    # is_jamo
    assert h.is_jamo('ㄲㅐaㅇB게놀자') is False
    assert h.is_jamo('ㄲㅐ게놀자') is False
    assert h.is_jamo('ㄲㅐ')
