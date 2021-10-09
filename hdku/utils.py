from typing import List, Dict
import string

import numpy as np

__all__ = ['KoDubeolsikDistance']


class KoDubeolsikDistance:
    """[summary]
    """

    def __init__(self) -> None:
        from . import Hangul
        from . import KoLevensteinDistance
        from . import KeystrokeAutomata
        self.hangul = Hangul()
        self.dubul_levelstein = KoLevensteinDistance()
        self.automata = KeystrokeAutomata(force=True)

    def get_distance(self, src: str, target: str) -> float:
        src_key: str = self.hangul.convert_hangul_to_keystrokes(src)
        target_key: str = self.hangul.convert_hangul_to_keystrokes(target)
        cost = self.dubul_levelstein.get_dubeolsik_distance(src_key, target_key)
        return cost

    def _construct_string_from_mixedkeystroke(self, mixkey: str) -> str:
        """[summary]

        Args:
            mixkey (str): keystroke with divider '｜'

        Returns:
            str: syllable string
        """
        rmed_sylla_keys: List[str] = mixkey.split(self.hangul.DIVIDER)
        rmed_sylla: List[str] = []
        for sylla in rmed_sylla_keys:
            if sylla == '':
                continue
            # if hangul
            if self.hangul.is_keystroke_fullwidth(sylla):
                halfkey: str = self.hangul._convert_fullwidth_to_halfwidth(sylla)
                rmed_sylla.append(self.automata.convert(halfkey))
            else:
                rmed_sylla.append(sylla)
        return ''.join(rmed_sylla)

    def _any_fullwidth(self, s: str) -> bool:
        for i in s:
            if self.hangul.is_keystroke_fullwidth(i):
                return True
        return False

    # def get_edx_samples(self, reference: str, ed_cost: List[float] = [1.0, 1.5, 1.5],
    #                     downsample: bool = True) -> Dict[str, str]:
    #     """generate all sentences below editdistance cost

    #     Args:
    #         reference (str): [description]
    #         ed_cost (float, optional): [description]. Defaults to 0.5.

    #     Returns:
    #         List[str]: [description]
    #     """
    #     # insert, delete, trans
    #     rml: List[str] = []
    #     adl: List[str] = []
    #     tra: List[str] = []
    #     key_strokes: str = self.hangul.convert_hangul_to_keystrokes(reference, fullwidth=True, div=True)
    #     rl: int = len(key_strokes)
    #     d_cost, i_cost, tr_cost = ed_cost
    #     # delete any position
    #     for i in range(rl):
    #         if self.hangul.DIVIDER == key_strokes[i]:
    #             continue
    #         # delete
    #         rmed_key: str = key_strokes[:i] + key_strokes[(i + 1):]
    #         rmed_sylla = self._construct_string_from_mixedkeystroke(rmed_key)
    #         cost: float = self.get_distance(reference, rmed_sylla)
    #         if cost > d_cost and key_strokes[i] != ' ':
    #             continue
    #         rml.append([cost, rmed_sylla])

    #         # insert any position any ascii
    #         if self.hangul.is_keystroke_fullwidth(key_strokes[i]):
    #             if ord(key_strokes[i]) >= 65 and ord(key_strokes[i]) <= 90:  # A-Z
    #                 letters = string.ascii_uppercase
    #             else:
    #                 letters = string.ascii_lowercase
    #             for letter in self.hangul._convert_halfwidth_to_fullwidth(letters) + ' ':
    #                 if letter == ' ':
    #                     letter = ' ' + self.hangul.DIVIDER
    #                 added_key: str = key_strokes[:i] + letter + key_strokes[i:]
    #                 added_sylla = self._construct_string_from_mixedkeystroke(added_key)
    #                 cost: float = self.get_distance(reference, added_sylla)
    #                 if cost > i_cost and letter != ' ' + self.hangul.DIVIDER:
    #                     continue
    #                 adl.append([cost, added_sylla])
    #         # elif ord(key_strokes[i]) >= 48 and ord(key_strokes[i]) <= 57:  # number
    #         #     for number in string.digits + ' ':
    #         #         if number == ' ':
    #         #             number = ' ' + self.hangul.DIVIDER
    #         #         added_key: str = key_strokes[:i] + number + key_strokes[i:]
    #         #         added_sylla = self._construct_string_from_mixedkeystroke(added_key)
    #         #         cost: float = self.get_distance(reference, added_sylla)
    #         #         if cost > i_cost and number != ' ' + self.hangul.DIVIDER:
    #         #             continue
    #         #         adl.append([cost, added_sylla])
    #         elif ord(key_strokes[i]) >= 65 and ord(key_strokes[i]) <= 90:  # A-Z
    #             for letter in string.ascii_uppercase + ' ':
    #                 if letter == ' ':
    #                     letter = ' ' + self.hangul.DIVIDER
    #                 added_key: str = key_strokes[:i] + letter + key_strokes[i:]
    #                 added_sylla = self._construct_string_from_mixedkeystroke(added_key)
    #                 cost: float = self.get_distance(reference, added_sylla)
    #                 if cost > i_cost and letter != ' ' + self.hangul.DIVIDER:
    #                     continue
    #                 adl.append([cost, added_sylla])
    #         elif ord(key_strokes[i]) >= 97 and ord(key_strokes[i]) <= 122:  # a-z
    #             for letter in string.ascii_lowercase + ' ':
    #                 if letter == ' ':
    #                     letter = ' ' + self.hangul.DIVIDER
    #                 added_key: str = key_strokes[:i] + letter + key_strokes[i:]
    #                 added_sylla = self._construct_string_from_mixedkeystroke(added_key)
    #                 cost: float = self.get_distance(reference, added_sylla)
    #                 if cost > i_cost and letter != ' ' + self.hangul.DIVIDER:
    #                     continue
    #                 adl.append([cost, added_sylla])
    #         # replace any position any ascii
    #         if self.hangul.is_keystroke_fullwidth(key_strokes[i]):
    #             if ord(key_strokes[i]) >= 65 and ord(key_strokes[i]) <= 90:  # A-Z
    #                 letters = string.ascii_uppercase
    #             else:
    #                 letters = string.ascii_lowercase
    #             for letter in self.hangul._convert_halfwidth_to_fullwidth(letters) + ' ':
    #                 if letter == ' ':
    #                     letter += self.hangul.DIVIDER
    #                 trans_key: str = key_strokes[:(i - 1)] + letter + key_strokes[i:]
    #                 trans_sylla = self._construct_string_from_mixedkeystroke(trans_key)
    #                 cost: float = self.get_distance(reference, trans_sylla)
    #                 if cost > tr_cost and letter != ' ' + self.hangul.DIVIDER:
    #                     continue
    #                 tra.append([cost, trans_sylla])
    #         # elif ord(key_strokes[i]) >= 48 and ord(key_strokes[i]) <= 57:  # number
    #         #     for number in string.digits + ' ':
    #         #         if number == ' ':
    #         #             number = ' ' + self.hangul.DIVIDER
    #         #         trans_key: str = key_strokes[: (i - 1)] + number + key_strokes[i:]
    #         #         trans_sylla = self._construct_string_from_mixedkeystroke(trans_key)
    #         #         cost: float = self.get_distance(reference, trans_sylla)
    #         #         if cost > tr_cost and number != ' ' + self.hangul.DIVIDER:
    #         #             continue
    #         #         tra.append([cost, trans_sylla])
    #         elif ord(key_strokes[i]) >= 65 and ord(key_strokes[i]) <= 90:  # A-Z
    #             for letter in string.ascii_uppercase + ' ':
    #                 if letter == ' ':
    #                     letter = ' ' + self.hangul.DIVIDER
    #                 trans_key: str = key_strokes[:(i - 1)] + letter + key_strokes[i:]
    #                 trans_sylla = self._construct_string_from_mixedkeystroke(trans_key)
    #                 cost: float = self.get_distance(reference, trans_sylla)
    #                 if cost > tr_cost and letter != ' ' + self.hangul.DIVIDER:
    #                     continue
    #                 tra.append([cost, trans_sylla])
    #         elif ord(key_strokes[i]) >= 97 and ord(key_strokes[i]) <= 122 or key_strokes[i] == ' ':  # a-z
    #             for letter in string.ascii_lowercase + ' ':
    #                 if letter == ' ':
    #                     letter = ' ' + self.hangul.DIVIDER
    #                 trans_key: str = key_strokes[:(i - 1)] + letter + key_strokes[i:]
    #                 trans_sylla = self._construct_string_from_mixedkeystroke(trans_key)
    #                 cost: float = self.get_distance(reference, trans_sylla)
    #                 if cost > tr_cost and letter != ' ' + self.hangul.DIVIDER:
    #                     continue
    #                 tra.append([cost, trans_sylla])

    #     result = {'delete': [(c, v) for c, v in rml if c > 0 and not self._any_fullwidth(v)],
    #               'insert': [(c, v) for c, v in adl if c > 0 and not self._any_fullwidth(v)],
    #               'transition': [(c, v) for c, v in tra if c > 0 and not self._any_fullwidth(v)]}
    #     if downsample:
    #         min_cnt = min([len(v) for _, v in result.items()])
    #         for k, v in result.items():
    #             vl = len(v)
    #             weight = np.array([1.0 / w for w, _ in v])
    #             p = weight / np.sum(weight)
    #             sel_vl = np.random.choice(vl, size=min_cnt, p=p, replace=False)
    #             result[k] = np.array(v)[sel_vl].tolist()
    #     return result
