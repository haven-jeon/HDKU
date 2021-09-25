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

from typing import List
from abc import ABCMeta, abstractmethod

from .hangul import Hangul

__all__ = ['JamoAutomata', 'KeystrokeAutomata']


class HangulAutomata(metaclass=ABCMeta):
    # 0, 1,2 can be value
    # 0 mean truly false
    # 1 mean truly true
    # 2 mean act as if true
    def __init__(self, force: bool) -> None:
        self.word_valid: int = 1
        self.chosung: str = '\x00'
        self.jwungsung: str = '\x00'
        self.jongsung: str = '\x00'
        self.__force_convert: bool = force
        self.hangul_buffer: List[str] = []
        self.syllables: List[str] = []
        self.raw_char: List[str] = []
        self.hangul_util = Hangul()

    def clear_comp(self) -> None:
        self.chosung = '\x00'
        self.jwungsung = '\x00'
        self.jongsung = '\x00'

    def push_comp(self) -> None:
        if not(self.chosung != '\x00' and self.jwungsung != '\x00'):
            self.word_valid = 0
        jamos: str = self.chosung + self.jwungsung + self.jongsung
        self.syllables.append(self.hangul_util.convert_jamos_to_syllable(jamos))
        self.clear_comp()

    def finalization(self) -> int:
        r: int = 0
        rjio: List[str] = []
        if self.chosung != '\x00' or self.jwungsung != '\x00' or self.jongsung != '\x00':
            self.push_comp()
        if self.__force_convert:
            self.word_valid = 2

        if len(self.raw_char) != 0 or len(self.syllables) != 0:
            if self.word_valid == 1:
                rjio += self.syllables
                r = 0
            elif self.word_valid == 2:
                rjio += self.syllables
                r = 2
            else:
                rjio += self.raw_char
                r = 1
            self.word_valid = 1
            self.raw_char = []
            self.syllables = []
            if len(rjio) != 0:
                self.hangul_buffer += rjio
                return r
        return 0

    def clear(self) -> None:
        self.hangul_buffer = []
        self.raw_char = []
        self.syllables = []
        self.word_valid = 1
        self.clear_comp()

    @property
    def force_convert(self) -> bool:
        return self.__force_convert

    @force_convert.setter
    def force_convert(self, force: bool) -> None:
        self.__force_convert = force

    def convert(self, keystroke: str) -> str:
        self.clear()
        for k in keystroke:
            self.feed(k)

        is_uncompleted: int = self.finalization()
        if is_uncompleted == 1 and not self.force_convert:
            return keystroke
        sb: List[str] = []
        for i in self.hangul_buffer:
            sb.append(i)
        self.clear()
        return ''.join(sb)

    @abstractmethod
    def feed(self, ch: str) -> None:
        pass


class JamoAutomata(HangulAutomata):
    def __init__(self, force: bool) -> None:
        super().__init__(force)

    def feed(self, ch: str) -> None:
        self.raw_char.append(ch)
        if self.hangul_util.is_jamo(ch):
            if self.hangul_util.is_jaeum(ch):
                if self.chosung == '\x00':
                    if self.jwungsung != '\x00' or self.jongsung != '\x00':
                        if self.force_convert:
                            self.push_comp()
                            self.chosung = ch
                        else:
                            self.word_valid = 0
                    else:
                        self.chosung = ch
                elif self.jwungsung == '\x00':
                    # chosung 1 jwungsung 0
                    if self.jongsung != '\x00':
                        self.word_valid = 0
                    else:
                        self.push_comp()
                        self.chosung = ch
                elif self.jongsung == '\x00':
                    # chosung 1 jungsung 1 jongsung 0
                    if self.hangul_util._get_chosung_idx(ch) is None:
                        self.push_comp()
                        self.chosung = ch
                    else:
                        self.jongsung = ch
                else:  # full
                    jong: str = self.hangul_util._get_key_from_jamo(self.jongsung)
                    jl: int = len(jong)
                    if jl == 1:
                        trymul: str = jong + self.hangul_util._get_key_from_jamo(ch)
                        if self.hangul_util._in_keyjamo(trymul):
                            self.jongsung = self.hangul_util._get_jamo_from_key(trymul)  # can be multi jongsung
                        else:
                            self.push_comp()
                            self.chosung = ch
                    elif jl == 2:
                        self.push_comp()
                        self.chosung = ch
                    else:
                        assert False
            else:  # Moeum
                if self.jongsung == '\x00':
                    # jongsung 0
                    if self.jwungsung == '\x00':
                        self.jwungsung = ch
                    else:
                        # jongsung 0 jwungsung 1
                        trymul: str = self.hangul_util._get_key_from_jamo(self.jwungsung) + self.hangul_util._get_key_from_jamo(ch)
                        if self.hangul_util._in_keyjamo(trymul):
                            self.jwungsung = self.hangul_util._get_jamo_from_key(trymul)
                        else:
                            self.push_comp()
                            self.jwungsung = ch
                else:  # jongsung 1
                    jong: str = self.hangul_util._get_key_from_jamo(self.jongsung)
                    l: int = len(jong)
                    assert l > 0 and l < 3  # must be 1 or 2
                    if l > 1:
                        ojong: str = self.hangul_util._get_jamo_from_key(jong[0])
                        ncho: str = self.hangul_util._get_jamo_from_key(jong[1])
                        self.jongsung = ojong
                        self.push_comp()
                        self.chosung = ncho
                        self.jwungsung = ch
                    else:
                        njong: str = self.jongsung
                        self.jongsung = '\x00'
                        self.push_comp()
                        self.chosung = njong
                        self.jwungsung = ch
        else:  # invalid key code
            is_uncompleted: int = self.finalization()
            if is_uncompleted == 0 or is_uncompleted == 2:
                self.hangul_buffer += ch


class KeystrokeAutomata(HangulAutomata):
    def __init__(self, force: bool) -> None:
        super().__init__(force)

    def feed(self, ch: str) -> None:
        self.raw_char.append(ch)
        if self.hangul_util._in_keyjamo(ch):
            code: str = self.hangul_util._get_jamo_from_key(ch)
            if self.hangul_util.is_jaeum(code):
                if self.chosung == '\x00':
                    if self.jwungsung != '\x00' or self.jongsung != '\x00':
                        if self.force_convert:
                            self.push_comp()
                            self.chosung = code
                        else:
                            self.word_valid = 0
                    else:
                        self.chosung = code
                elif self.jwungsung == '\x00':  # chosung 1 jwungsung 0
                    if self.jongsung != '\x00':
                        self.word_valid = 0
                    else:
                        self.push_comp()
                        self.chosung = code
                elif self.jongsung == '\x00':  # chosung 1 jungsung 1 jongsung 0
                    if self.hangul_util._get_jongsung_idx(code) is None:
                        self.push_comp()
                        self.chosung = code
                    else:
                        self.jongsung = code
                else:  # full
                    jong: str = self.hangul_util._get_key_from_jamo(self.jongsung)
                    jl: int = len(jong)
                    if jl == 1:
                        trymul: str = jong + ch
                        if self.hangul_util._in_keyjamo(trymul):
                            self.jongsung = self.hangul_util._get_jamo_from_key(trymul)  # can be multi jongsung
                        else:
                            self.push_comp()
                            self.chosung = code
                    elif jl == 2:
                        self.push_comp()
                        self.chosung = code
                    else:
                        assert False
            else:  # MOEUM
                if self.jongsung == '\x00':
                    if self.jwungsung == '\x00':
                        self.jwungsung = code
                    else:
                        trymul: str = self.hangul_util._get_key_from_jamo(self.jwungsung) + ch
                        if self.hangul_util._in_keyjamo(trymul):  # multi jwungsung
                            self.jwungsung = self.hangul_util._get_jamo_from_key(trymul)
                        else:
                            self.push_comp()
                            self.jwungsung = code
                else:  # jongsung 1
                    jong: str = self.hangul_util._get_key_from_jamo(self.jongsung)
                    jl: int = len(jong)
                    assert jl > 0 and jl < 3  # must be 1 or 2
                    if jl > 1:
                        ojong: str = self.hangul_util._get_jamo_from_key(jong[0])
                        ncho: str = self.hangul_util._get_jamo_from_key(jong[1])
                        self.jongsung = ojong
                        self.push_comp()
                        self.chosung = ncho
                        self.jwungsung = code
                    else:
                        njong: str = self.jongsung
                        self.jongsung = '\x00'
                        self.push_comp()
                        self.chosung = njong
                        self.jwungsung = code
        else:  # invalid key code
            is_uncompleted: int = self.finalization()
            if is_uncompleted == 0 or is_uncompleted == 2:
                self.hangul_buffer += ch


if __name__ == '__main__':
    am = JamoAutomata(False)
    print(am.convert('ㅈㅓㄴㅎㅡㅣㅇㅜㅓㄴ'))
    print(am.convert('"ㅇㅏㄹㅁ'))
    print(am.convert("sksms wjdakf glaemfdj"))

    kam = KeystrokeAutomata(False)
    print(kam.convert("wjsgmldnjsdkfa"))
