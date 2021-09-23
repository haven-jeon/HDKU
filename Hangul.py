# Copyright 2011 Heewon Jeon(madjakarta@gmail.com)

# This file is part of KoNLP.

# KoNLP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# KoNLP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with JHanNanum.  If not, see <http://www.gnu.org/licenses/>

from typing import List, Dict, FrozenSet


class Hangul:
    MAX_KEYSTROKE_SIZE: int = 100
    HANGUL_SYLLABLE_START: int = 0xAC00
    HANGUL_SYLLABLE_END: int = 0xD7A3

    DIVIDER: str = '｜'  # 65372
    ASCII_DIVIDER: str = '|'  # 124

    KO_HANGUL_SUCCESS: int = 1
    KO_HANGUL_ERROR: int = -1
    KO_HANGUL_NOT_ENOUGH_SPACE: int = -2
    KO_HANGUL_CONTAIN_ASCII: int = -3
    KO_HANGUL_NOT_CONVERTIBLE: int = -4

    JAMO_LEN_PER_SYLLABLE: int = 3
    # define Jamo mapping table
    # code to Keystrokes
    jamo_to_key: Dict[str, str] = {
        "ㄱ": "r",
        "ㄲ": "R",
        "ㄳ": "rt",
        "ㄴ": "s",
        "ㄵ": "sw",
        "ㄶ": "sg",
        "ㄷ": "e",
        "ㄸ": "E",
        "ㄹ": "f",
        "ㄺ": "fr",
        "ㄻ": "fa",
        "ㄼ": "fq",
        "ㄽ": "ft",
        "ㄾ": "fx",
        "ㄿ": "fv",
        "ㅀ": "fg",
        "ㅁ": "a",
        "ㅂ": "q",
        "ㅃ": "Q",
        "ㅄ": "qt",
        "ㅅ": "t",
        "ㅆ": "T",
        "ㅇ": "d",
        "ㅈ": "w",
        "ㅉ": "W",
        "ㅊ": "c",
        "ㅋ": "z",
        "ㅌ": "x",
        "ㅍ": "v",
        "ㅎ": "g",
        "ㅏ": "k",
        "ㅐ": "o",
        "ㅑ": "i",
        "ㅒ": "O",
        "ㅓ": "j",
        "ㅔ": "p",
        "ㅕ": "u",
        "ㅖ": "P",
        "ㅗ": "h",
        "ㅘ": "hk",
        "ㅙ": "ho",
        "ㅚ": "hl",
        "ㅛ": "y",
        "ㅜ": "n",
        "ㅝ": "nj",
        "ㅞ": "np",
        "ㅟ": "nl",
        "ㅠ": "b",
        "ㅡ": "m",
        "ㅢ": "ml",
        "ㅣ": "l",
        "": ""
    }
    # Keystroke to code
    key_to_jamo: Dict[str, str] = {
        "r": "ㄱ",
        "R": "ㄲ",
        "rt": "ㄳ",
        "s": "ㄴ",
        "sw": "ㄵ",
        "sg": "ㄶ",
        "e": "ㄷ",
        "E": "ㄸ",
        "f": "ㄹ",
        "fr": "ㄺ",
        "fa": "ㄻ",
        "fq": "ㄼ",
        "ft": "ㄽ",
        "fx": "ㄾ",
        "fv": "ㄿ",
        "fg": "ㅀ",
        "a": "ㅁ",
        "q": "ㅂ",
        "Q": "ㅃ",
        "qt": "ㅄ",
        "t": "ㅅ",
        "T": "ㅆ",
        "d": "ㅇ",
        "w": "ㅈ",
        "W": "ㅉ",
        "c": "ㅊ",
        "z": "ㅋ",
        "x": "ㅌ",
        "v": "ㅍ",
        "g": "ㅎ",
        "k": "ㅏ",
        "o": "ㅐ",
        "i": "ㅑ",
        "O": "ㅒ",
        "j": "ㅓ",
        "p": "ㅔ",
        "u": "ㅕ",
        "P": "ㅖ",
        "h": "ㅗ",
        "hk": "ㅘ",
        "ho": "ㅙ",
        "hl": "ㅚ",
        "y": "ㅛ",
        "n": "ㅜ",
        "nj": "ㅝ",
        "np": "ㅞ",
        "nl": "ㅟ",
        "b": "ㅠ",
        "m": "ㅡ",
        "ml": "ㅢ",
        "l": "ㅣ",
        "": "",
    }

    multi_jamo_to_one: Dict[str, str] = {
        "ㄱㅅ": "ㄳ",
        "ㄴㅈ": "ㄵ",
        "ㄴㅎ": "ㄶ",
        "ㄹㄱ": "ㄺ",
        "ㄹㅁ": "ㄻ",
        "ㄹㅂ": "ㄼ",
        "ㄹㅅ": "ㄽ",
        "ㄹㅌ": "ㄾ",
        "ㄹㅍ": "ㄿ",
        "ㄹㅎ": "ㅀ",
        "ㅂㅅ": "ㅄ",
        "ㅗㅏ": "ㅘ",
        "ㅗㅐ": "ㅙ",
        "ㅗㅣ": "ㅚ",
        "ㅜㅓ": "ㅝ",
        "ㅜㅔ": "ㅞ",
        "ㅜㅣ": "ㅟ",
        "ㅡㅣ": "ㅢ",
        "": "",
    }

    # ㄱ ㄲ ㄴ ㄷ ㄸ ㄹ ㅁ ㅂ ㅃ ㅅ ㅆ ㅇ ㅈ ㅉ ㅊ ㅋ ㅌ ㅍ ㅎ
    chosung_idx: Dict[str, int] = {
        "ㄱ": 0,
        "ㄲ": 1,
        "ㄴ": 2,
        "ㄷ": 3,
        "ㄸ": 4,
        "ㄹ": 5,
        "ㅁ": 6,
        "ㅂ": 7,
        "ㅃ": 8,
        "ㅅ": 9,
        "ㅆ": 10,
        "ㅇ": 11,
        "ㅈ": 12,
        "ㅉ": 13,
        "ㅊ": 14,
        "ㅋ": 15,
        "ㅌ": 16,
        "ㅍ": 17,
        "ㅎ": 18,
    }

    chosung: Dict[int, str] = {v: k for k, v in chosung_idx.items()}

    # ㅏ ㅐ ㅑ ㅒ ㅓ ㅔ ㅕ ㅖ ㅗ ㅘ ㅙ ㅚ ㅛ ㅜ ㅝ ㅞ ㅟ ㅠ ㅡ ㅢ ㅣ
    jwungsung_idx: Dict[str, int] = {
        "ㅏ": 0,
        "ㅐ": 1,
        "ㅑ": 2,
        "ㅒ": 3,
        "ㅓ": 4,
        "ㅔ": 5,
        "ㅕ": 6,
        "ㅖ": 7,
        "ㅗ": 8,
        "ㅘ": 9,
        "ㅙ": 10,
        "ㅚ": 11,
        "ㅛ": 12,
        "ㅜ": 13,
        "ㅝ": 14,
        "ㅞ": 15,
        "ㅟ": 16,
        "ㅠ": 17,
        "ㅡ": 18,
        "ㅢ": 19,
        "ㅣ": 20,
    }

    jwungsung: Dict[int, str] = {v: k for k, v in jwungsung_idx.items()}

    # ㄱ ㄲ ㄳ ㄴ ㄵ ㄶ ㄷ ㄹ ㄺ ㄻ ㄼ ㄽ ㄾ ㄿ ㅀ ㅁ ㅂ ㅄ ㅅ ㅆ ㅇ ㅈ ㅊ ㅋ ㅌ ㅍ ㅎ
    jongsung_idx: Dict[str, int] = {
        "": 0,
        "ㄱ": 1,
        "ㄲ": 2,
        "ㄳ": 3,
        "ㄴ": 4,
        "ㄵ": 5,
        "ㄶ": 6,
        "ㄷ": 7,
        "ㄹ": 8,
        "ㄺ": 9,
        "ㄻ": 10,
        "ㄼ": 11,
        "ㄽ": 12,
        "ㄾ": 13,
        "ㄿ": 14,
        "ㅀ": 15,
        "ㅁ": 16,
        "ㅂ": 17,
        "ㅄ": 18,
        "ㅅ": 19,
        "ㅆ": 20,
        "ㅇ": 21,
        "ㅈ": 22,
        "ㅊ": 23,
        "ㅋ": 24,
        "ㅌ": 25,
        "ㅍ": 26,
        "ㅎ": 27
    }

    jongsung: Dict[int, str] = {v: k for k, v in jongsung_idx.items()}

    jaeum: FrozenSet[str] = {
        "ㄱ",
        "ㄲ",
        "ㄳ",
        "ㄴ",
        "ㄵ",
        "ㄶ",
        "ㄷ",
        "ㄸ",
        "ㄹ",
        "ㄺ",
        "ㄻ",
        "ㄼ",
        "ㄽ",
        "ㄾ",
        "ㄿ",
        "ㅀ",
        "ㅁ",
        "ㅂ",
        "ㅃ",
        "ㅄ",
        "ㅅ",
        "ㅆ",
        "ㅇ",
        "ㅈ",
        "ㅉ",
        "ㅊ",
        "ㅋ",
        "ㅌ",
        "ㅍ",
        "ㅎ",
    }

    moeum: FrozenSet[str] = set(jwungsung_idx.keys())

    def __init__(self) -> None:
        pass

    def _in_jamokey(self, code: str) -> bool:
        ## isInCodeKey
        return code in Hangul.jamo_to_key

    def _in_keyjamo(self, key: str) -> bool:
        ## isInKeyCode
        return key in Hangul.key_to_jamo

    def _get_jamo_from_key(self, key: str) -> str:
        ## getCodefromKey
        return Hangul.key_to_jamo[key]

    def _in_multijamo(self, jamos: str) -> bool:
        ## isInMultiJamo
        return jamos in Hangul.multi_jamo_to_one

    def _get_multijamo_to_one(self, jamos: str) -> str:
        ## getMultiJamo
        return Hangul.multi_jamo_to_one[jamos]

    def _get_key_from_jamo(self, jamo: str) -> str:
        ## getKeyfromCode
        return Hangul.jamo_to_key[jamo]

    def _get_chosung_idx(self, ch: str) -> int:
        return Hangul.chosung_idx[ch]

    def _get_jwungsung_idx(self, ch: str) -> int:
        return Hangul.jwungsung_idx[ch]

    def _get_jongsung_idx(self, ch: str) -> int:
        return Hangul.jongsung_idx[ch]

    def _is_hangul(self, ch: str) -> bool:
        return ((Hangul.HANGUL_SYLLABLE_START <= ord(ch) and ord(ch) <= Hangul.HANGUL_SYLLABLE_END) or self.is_jamo(ch))

    def _convert_halfwidth_to_fullwidth(self, ch: str) -> str:
        return chr((ord(ch) - 0x41) + 0xFF21)

    def is_jamo(self, input: str) -> bool:
        if len(input) == 0:
            return False
        for ch in input:
            if not (self.is_jaeum(ch) or self.is_moeum(ch)):
                return False
        return True

    def is_hangul(self, input: str) -> bool:
        if len(input) == 0:
            return False
        for ch in input:
            if not self._is_hangul(ch):
                return False
        return True

    def is_jaeum(self, input: str) -> bool:
        ## isJaeumString
        if len(input) == 0:
            return False
        for ch in input:
            if ch not in Hangul.jaeum:
                return False
        return True

    def is_ascii(self, input: str) -> bool:
        ## isAsciiString
        if len(input) == 0:
            return False
        for ch in input:
            if not ord(ch) < 128:
                return False
        return True

    def is_moeum(self, input: str) -> bool:
        ## isMoeumString
        if len(input) == 0:
            return False
        for ch in input:
            if ch not in Hangul.moeum:
                return False
        return True

    def convert_jamos_to_syllable(self, jamos: str) -> str:
        """
        가 = 0xAC00 + 0(ㄱ)*588 + 0(ㅏ)*28 + 0(none) = 0xAC00
        Args:
            jamos (str): [description]

        Returns:
            str: [description]
        """
        if len(jamos) != Hangul.JAMO_LEN_PER_SYLLABLE:
            return ''
        if ord(jamos[0]) == 0 or ord(jamos[1]) == 0:
            return jamos[0] if ord(jamos[0]) != 0 else jamos[1]
        return chr(
            Hangul.HANGUL_SYLLABLE_START +
            self._get_chosung_idx(jamos[0]) * 588 +
            self._get_jwungsung_idx(jamos[1]) * 28 +
            self._get_jongsung_idx(jamos[2])
        )

    def convert_syllable_to_jamos(self, syllable: str) -> str:
        assert len(syllable) == 1
        jamo_buf1: int = 0
        jamo_buf2: int = 0
        jamo_buf3: int = 0
        jamos: List[str] = [chr(0)] * 3

        if self.is_jaeum(syllable):
            jamos[0] = syllable
            return ''.join(jamos)
        if self.is_moeum(syllable):
            jamos[1] = syllable
            return ''.join(jamos)

        jamo_buf3 = ord(syllable) - Hangul.HANGUL_SYLLABLE_START
        jamo_buf1 = jamo_buf3 // (21 * 28)
        jamo_buf3 = jamo_buf3 % (21 * 28)
        jamo_buf2 = jamo_buf3 // 28
        jamo_buf3 = jamo_buf3 % 28

        jamos[0] = Hangul.chosung[jamo_buf1]
        jamos[1] = Hangul.jwungsung[jamo_buf2]
        jamos[2] = Hangul.jongsung[jamo_buf3]
        return ''.join(jamos)

    def convert_hangul_to_jamos(self, syllables: str, div: bool = False) -> str:
        sb: List[str] = []
        for ch in syllables:
            if not self.is_hangul(ch):
                sb.append(ch)
            else:
                jamos: str = self.convert_syllable_to_jamos(ch)
                assert len(jamos) == Hangul.JAMO_LEN_PER_SYLLABLE
                for j in jamos:
                    if ord(j) == 0:
                        continue
                    sb.append(j)
            # insert divider at the end of each Syllable
            if div:
                sb.append(Hangul.DIVIDER)
        return ''.join(sb)

    def convert_hangul_to_keystrokes(self, syllables: str, fullwidth: bool = False, div: bool = False) -> str:
        keystrokes: List[str] = []

        for ch in syllables:
            if self.is_hangul(ch):
                jamos: str = self.convert_syllable_to_jamos(ch)
                for jamo in jamos:
                    key: str = self._get_key_from_jamo(jamo)
                    for k in key:
                        if fullwidth:
                            keystrokes.append(self._convert_halfwidth_to_fullwidth(k))
                        else:
                            keystrokes.append(k)
            else:
                keystrokes.append(ch)
            if div:
                keystrokes.append(Hangul.DIVIDER)
        return ''.join(keystrokes)


if __name__ == '__main__':
    h = Hangul()
    ret = h.convert_hangul_to_keystrokes('전희원', True, True)
    print(ret)
