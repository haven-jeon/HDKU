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


class KoLevensteinDistance:
    """
    < cost table explaination >
    1) 'insert', 'delete'   =>   1
    'space'  : 'insert', 'delete' => 0.5
    number  : 'insert', 'delete' => 2

    2) a small letter <=> a small letter within 1 keybord space           =>   0.5

    3) a small letter <=> a small letter within 2 keybord space           =>   1

    4) a small letter <=> a small letter within 3 keybord space           =>   1.5

    5) a small letter <=> a small letter over 3 keybord space             =>   2

    6) a capital letter <=> a capital letter within 1 keybord space	=>   0.5

    7) a capital letter <=> a small letter within 1 keybord space	        =>   0.5

    6) a capital letter <=> a small letter                                =>   0.3

    7) letter           <=> number		                        =>   1.5

    8) letter           <=> space		                                =>   1.5

    9) space            <=> number                        	        =>   1.5

    10)number           <=> number	                  		=>   2

    11) 'ㄸ' <=> 'ㅌ' , 'ㅋ' <=> 'ㄱ'                                	     => 0.5 (phonetic distance)
    12) a small letter <=> a capital letter over 3 keyboard space  =>   *3*


    //09.01.05
    //{a,A,b,B,c,C,d,D,e,E,f,F,g,G,h,H,i,I,j,J,k,K,l,L,m,M,n,N,o,O,p,P,q,Q,r,R,s,S,t,T,u,U,v,V,w,W,x,X,y,Y,z,Z,0,1,2,3,4,5,6,7,8,9,_,$,#,delete},
    """
    COST_TABLE_SIZE: int = 66
    a_ascii = ord('a')
    z_ascii = ord('z')
    A_ascii = ord('A')
    Z_ascii = ord('Z')

    # cost table for 2 bul keyboard
    cost: List = [
        [
            0, 0.3, 2, 3, 1.5, 3, 1, 3, 1, 1, 1.5, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3,
            2, 3, 2, 3, 2, 3, 2, 2, 2, 2, 0.5, 0.5, 1.5, 1.5, 0.5, 0.5, 2, 2, 2, 3,
            2, 3, 0.5, 0.5, 1, 3, 2, 3, 0.5, 0.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            0.3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0.5, 0.5, 3, 3,
            0.5, 0.5, 3, 3, 3, 3, 3, 3, 0.5, 0.5, 3, 3, 3, 3, 0.5,
            0.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 100, 100, 1
        ],
        [
            2, 3, 0, 0.3, 1, 3, 1.5, 3, 2, 2, 1, 3, 0.5, 0.5, 0.5,
            0.5, 1.5, 3, 1, 3, 1.5, 3, 2, 3, 1, 3, 0.5, 0.5, 2, 2, 2,
            2, 2, 2, 1.5, 1.5, 2, 3, 1, 1, 1, 3, 0.5, 0.5, 2, 2, 1.5,
            3, 1, 3, 2, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            3, 3, 0.3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0.5, 0.5, 0.5, 0.5,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0.5, 0.5, 3, 3, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 0.5, 0.5, 3, 3, 3, 3, 3, 3, 3, 3,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            100, 100, 1
        ],
        [
            1.5, 3, 1, 3, 0, 0.3, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 1, 3,
            1.5, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 1.5, 3, 2, 2, 2, 2,
            2, 2, 1, 1, 1, 3, 0.5, 0.5, 2, 3, 3, 3, 0.5, 0.5, 0.5,
            0.5, 1.5, 3, 1, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            3, 3, 3, 3, 0.3, 0, 0.5, 0.5, 3, 3, 0.5, 0.5, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0.5, 0.5, 3, 3, 3, 3,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            100, 100, 1
        ],
        [
            1, 3, 1.5, 3, 0.5, 0.5, 0, 0.3, 0.5, 0.5, 0.5, 0.5, 1, 3,
            1.5, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 2, 2, 2,
            1.5, 1.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 2, 3, 0.5, 0.5, 1, 1,
            0.5, 0.5, 1.5, 3, 1, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            3, 3, 3, 3, 0.5, 0.5, 0.3, 0, 0.5, 0.5, 0.5, 0.5, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 0.5, 0.5, 0.5, 0.5, 3, 3, 3, 3, 0.5, 0.5, 3, 3, 0.5,
            0.5, 3, 3, 3, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            1, 3, 2, 3, 0.5, 3, 0.5, 3, 0, 0.3, 1, 3, 1.5, 3, 2, 3,
            2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 2, 2, 2, 1, 1,
            0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 2, 3, 1.5, 3, 0.5, 0.5,
            0.5, 3, 1.5, 3, 1, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            1, 3, 2, 3, 1, 3, 0.5, 0.5, 0.3, 0, 1, 3, 1.5, 3, 2, 3,
            2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 2, 2, 2, 1, 1,
            0.5, 0.5, 0.5, 0.5, 1, 1, 2, 3, 1.5, 3, 0.5, 0.5, 0.5, 3,
            1.5, 3, 1, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            1.5, 3, 1, 3, 0.5, 0.5, 0.5, 0.5, 1, 1, 0, 0.3, 0.5, 0.5,
            1, 3, 2, 3, 1.5, 3, 2, 3, 2, 3, 2, 3, 1.5, 3, 2, 2, 2, 2,
            2, 2, 0.5, 0.5, 1, 3, 0.5, 0.5, 1.5, 3, 0.5, 0.5, 1.5,
            1.5, 1, 3, 1, 3, 1.5, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            3, 3, 3, 3, 0.5, 0.5, 0.5, 0.5, 3, 3, 0.3, 0, 0.5, 0.5,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 0.5, 0.5, 3, 3, 0.5, 0.5, 3, 3, 0.5, 0.5, 3, 3, 3, 3,
            3, 3, 3, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 100, 100, 1
        ],
        [
            2, 3, 0.5, 0.5, 1, 3, 1, 3, 1.5, 1.5, 0.5, 0.5, 0, 0.3,
            0.5, 0.5, 1.5, 3, 1, 3, 1.5, 3, 2, 3, 1.5, 3, 1, 3, 2, 2,
            2, 2, 2, 2, 1, 1, 1.5, 3, 0.5, 0.5, 1, 3, 0.5, 0.5, 2, 2,
            1.5, 3, 0.5, 0.5, 2, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            3, 3, 0.5, 0.5, 3, 3, 3, 3, 3, 3, 0.5, 0.5, 0.3, 0, 0.5,
            0.5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 0.5, 0.5, 3, 3, 0.5, 0.5, 3, 3, 3, 3, 0.5,
            0.5, 3, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 100, 100, 1
        ],
        [
            2, 3, 0.5, 0.5, 1.5, 3, 1.5, 3, 2, 2, 1, 3, 0.5, 0.5, 0,
            0.3, 1, 3, 0.5, 0.5, 1, 3, 1.5, 3, 1, 3, 0.5, 0.5, 1.5,
            1.5, 2, 2, 2, 2, 1.5, 1.5, 2, 3, 1, 1, 0.5, 0.5, 1, 3, 2,
            2, 2, 3, 0.5, 0.5, 2, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            3, 3, 0.5, 0.5, 3, 3, 3, 3, 3, 3, 3, 3, 0.5, 0.5, 0.3, 0,
            3, 3, 0.5, 0.5, 3, 3, 3, 3, 3, 3, 0.5, 0.5, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 0.5, 0.5, 3, 3, 3, 3, 3, 3, 0.5,
            0.5, 3, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 100, 100, 1
        ],
        [
            2, 3, 1.5, 3, 2, 3, 2, 3, 2, 2, 2, 3, 1.5, 3, 1, 3, 0,
            0.3, 0.5, 0.5, 0.5, 0.5, 1, 3, 1, 3, 1, 3, 0.5, 0.5, 1,
            1, 2, 2, 2, 2, 2, 3, 1.5, 1.5, 0.5, 0.5, 2, 3, 2, 2, 2,
            3, 1, 3, 2, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0.3, 0,
            0.5, 0.5, 0.5, 0.5, 3, 3, 3, 3, 3, 3, 0.5, 0.5, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 0.5, 0.5, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            100, 100, 1
        ],
        [
            2, 3, 1, 3, 2, 3, 2, 3, 2, 2, 1.5, 3, 1, 3, 0.5, 0.5,
            0.5, 0.5, 0, 0.3, 0.5, 0.5, 1, 3, 0.5, 0.5, 0.5, 0.5, 1,
            1, 1, 1.5, 2, 2, 2, 2, 2, 3, 1.5, 1.5, 0.5, 0.5, 1.5, 3,
            2, 2, 2, 3, 1, 3, 2, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0.5, 0.5, 0.5,
            0.5, 0.3, 0, 0.5, 0.5, 3, 3, 0.5, 0.5, 0.5, 0.5, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 0.5, 0.5, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 100, 100, 1
        ],
        [
            2, 3, 1.5, 3, 2, 3, 2, 3, 2, 2, 2, 3, 1.5, 3, 1, 3, 0.5,
            3, 0.5, 0.5, 0, 0.3, 0.5, 0.5, 0.5, 0.5, 1, 3, 0.5, 0.5,
            1, 1, 2, 2, 2, 2, 2, 3, 2, 2, 1, 3, 2, 3, 2, 2, 2, 3,
            1.5, 3, 2, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0.5, 0.5,
            0.5, 0.5, 0.3, 0, 0.5, 0.5, 0.5, 0.5, 3, 3, 0.5, 0.5, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 100, 100, 1
        ],
        [
            2, 3, 2, 3, 2, 3, 2, 3, 2, 2, 2, 3, 2, 3, 1.5, 3, 1, 3,
            1, 3, 0.5, 0.5, 0, 0.3, 1, 3, 1.5, 3, 0.5, 0.5, 0.5, 0.5,
            2, 2, 2, 2, 2, 3, 2, 2, 1.5, 3, 2, 3, 2, 2, 2, 3, 2, 3,
            2, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 100, 100, 1
        ],
        [
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 0.5, 0.5, 0.3, 0, 3, 3, 3, 3, 0.5, 0.5, 0.5, 0.5, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            100, 100, 1
        ],
        [
            2, 3, 1, 3, 2, 3, 2, 3, 2, 2, 2, 3, 1.5, 3, 1, 3, 1, 3,
            0.5, 0.5, 0.5, 0.5, 1, 3, 0, 0.3, 0.5, 0.5, 1, 1, 1.5,
            1.5, 2, 2, 2, 2, 2, 3, 2, 2, 1, 3, 1.5, 3, 2, 2, 2, 3,
            1.5, 3, 2, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            0.5, 0.5, 0.5, 0.5, 3, 3, 0.3, 0, 0.5, 0.5, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            100, 100, 1
        ],
        [
            2, 3, 0.5, 0.5, 1.5, 3, 2, 3, 2, 2, 1.5, 3, 1, 3, 0.5,
            0.5, 1, 3, 0.5, 0.5, 1, 3, 1.5, 3, 0.5, 0.5, 0, 0.3, 1.5,
            1.5, 2, 2, 2, 2, 2, 2, 2, 3, 1.5, 1.5, 1, 3, 1, 3, 2, 2,
            2, 3, 1, 3, 2, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            3, 3, 0.5, 0.5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0.5, 0.5,
            3, 3, 0.5, 0.5, 3, 3, 3, 3, 0.5, 0.5, 0.3, 0, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            100, 100, 1
        ],
        [
            2, 3, 2, 3, 2, 3, 2, 3, 2, 2, 2, 3, 2, 3, 1.5, 3, 0.5,
            0.5, 1, 3, 0.5, 0.5, 0.5, 0.5, 1, 3, 1.5, 3, 0, 0.3, 0.5,
            0.5, 2, 2, 2, 2, 2, 3, 2, 2, 1, 3, 2, 3, 2, 2, 2, 3, 1.5,
            3, 2, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 100, 100, 1
        ],
        [
            2, 3, 2, 3, 2, 3, 2, 3, 2, 2, 2, 3, 2, 3, 1.5, 3, 0.5,
            0.5, 1, 3, 0.5, 0.5, 0.5, 0.5, 1, 3, 1.5, 3, 0.3, 0, 0.5,
            0.5, 2, 2, 2, 2, 2, 3, 2, 2, 1, 3, 2, 3, 2, 2, 2, 3, 1.5,
            3, 2, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 100, 100, 1
        ],
        [
            2, 3, 2, 3, 2, 3, 2, 3, 2, 2, 2, 3, 2, 3, 2, 3, 1, 3, 1,
            3, 1, 3, 0.5, 0.5, 1.5, 3, 2, 3, 0.5, 0.5, 0, 0.3, 2, 2,
            2, 2, 2, 3, 2, 2, 1.5, 3, 2, 3, 2, 2, 2, 3, 2, 3, 2, 3,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            100, 100, 1
        ],
        [
            2, 3, 2, 3, 2, 3, 2, 3, 2, 2, 2, 3, 2, 3, 2, 3, 1, 3,
            1.5, 3, 1, 3, 0.5, 0.5, 1.5, 3, 2, 3, 0.5, 0.5, 0.3, 0,
            2, 2, 2, 2, 2, 3, 2, 2, 1.5, 3, 2, 3, 2, 2, 2, 3, 2, 3,
            2, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 100, 100, 1
        ],
        [
            0.5, 0.5, 2, 3, 2, 3, 1.5, 3, 1, 1, 2, 3, 2, 3, 2, 3, 2,
            3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 2, 2, 2, 0, 0.3, 1.5,
            1.5, 1, 3, 2, 2, 2, 3, 0.5, 3, 0.5, 0.5, 1.5, 3, 2, 3, 1,
            3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            100, 100, 1
        ],
        [
            0.5, 0.5, 2, 3, 2, 3, 1.5, 3, 1, 1, 2, 3, 2, 3, 2, 3, 2,
            3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 2, 2, 2, 0.3, 0, 1.5,
            1.5, 1, 3, 2, 2, 2, 3, 0.5, 3, 0.5, 0.5, 1.5, 3, 2, 3, 1,
            3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            100, 100, 1
        ],
        [
            1.5, 3, 1.5, 3, 1, 3, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 3,
            1.5, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 2, 2, 2,
            1.5, 1.5, 0, 0.3, 1, 3, 0.5, 0.5, 1.5, 3, 1, 3, 1, 1, 1,
            3, 1, 3, 0.5, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            1.5, 3, 1.5, 3, 1, 3, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 3,
            1.5, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 2, 2, 2,
            1.5, 1.5, 0.3, 0, 1, 3, 0.5, 0.5, 1.5, 3, 1, 3, 1, 1, 1,
            3, 1, 3, 0.5, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            0.5, 0.5, 2, 3, 1, 3, 0.5, 0.5, 0.5, 0.5, 1, 3, 1.5, 3,
            2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 2, 2, 2, 1,
            1, 1, 1, 0, 0.3, 1.5, 1.5, 2, 3, 1.5, 3, 0.5, 0.5, 0.5,
            0.5, 2, 3, 0.5, 0.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            0.5, 0.5, 3, 3, 3, 3, 0.5, 0.5, 0.5, 0.5, 3, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 0.3, 0, 3, 3, 3, 3, 3, 3, 0.5, 0.5, 0.5, 0.5, 3, 3,
            0.5, 0.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 100, 100, 1
        ],
        [
            2, 3, 1, 3, 0.5, 3, 1, 3, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 1,
            3, 1.5, 3, 1.5, 3, 2, 3, 2, 3, 2, 3, 1.5, 3, 2, 2, 2, 2,
            2, 2, 0.5, 0.5, 1.5, 3, 0, 0.3, 1, 3, 1, 3, 0.5, 1.5,
            0.5, 3, 0.5, 0.5, 2, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            2, 3, 1, 3, 0.5, 3, 1, 3, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 1,
            3, 1.5, 3, 1.5, 3, 2, 3, 2, 3, 2, 3, 1.5, 3, 2, 2, 2, 2,
            2, 2, 0.5, 0.5, 1.5, 3, 0.3, 0, 1, 3, 1, 3, 0.5, 1.5,
            0.5, 3, 0.5, 0.5, 2, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            2, 3, 1, 3, 2, 3, 2, 3, 2, 2, 1.5, 3, 1, 3, 0.5, 0.5,
            0.5, 0.5, 0.5, 0.5, 1, 3, 1.5, 3, 1, 3, 1, 3, 1, 1, 1.5,
            1.5, 2, 2, 1.5, 1.5, 2, 3, 1, 1, 0, 0.3, 1.5, 3, 2, 2, 2,
            3, 0.5, 0.5, 2, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0.5, 0.5, 0.5,
            0.5, 0.5, 0.5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 0.3, 0, 3, 3, 3, 3, 3, 3, 0.5, 0.5, 3,
            3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            100, 100, 1
        ],
        [
            2, 3, 0.5, 0.5, 0.5, 0.5, 1, 3, 1.5, 1.5, 0.5, 0.5, 0.5,
            0.5, 1, 3, 2, 3, 1.5, 3, 2, 3, 2, 3, 1.5, 3, 1, 3, 2, 2,
            2, 2, 0.5, 0.5, 1, 1, 1.5, 3, 1, 1, 1.5, 3, 0, 0.3, 2, 2,
            1, 3, 1, 3, 1.5, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            3, 3, 0.5, 0.5, 0.5, 0.5, 3, 3, 3, 3, 0.5, 0.5, 0.5, 0.5,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 0.3, 0, 3, 3, 3, 3, 3, 3, 3,
            3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            100, 100, 1
        ],
        [
            0.5, 0.5, 2, 3, 0.5, 3, 1, 3, 0.5, 0.5, 1.5, 3, 2, 3, 2,
            3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 2, 2, 2, 0.5,
            0.5, 1, 1, 0.5, 0.5, 0.5, 0.5, 2, 3, 2, 3, 0, 0.3, 0.5,
            3, 2, 3, 1, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            0.5, 0.5, 2, 3, 0.5, 3, 1, 3, 0.5, 0.5, 1.5, 3, 2, 3, 2,
            3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 2, 2, 2, 0.5,
            0.5, 1, 1, 0.5, 0.5, 1.5, 1.5, 2, 3, 2, 3, 0.3, 0, 1, 3,
            2, 3, 1, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 100, 100, 1
        ],
        [
            1, 3, 1.5, 3, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 3, 1.5, 3,
            2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 2, 2, 2,
            1.5, 1.5, 1, 1, 0.5, 0.5, 0.5, 0.5, 2, 3, 1, 3, 0.5, 1,
            0, 0.3, 2, 3, 0.5, 0.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            3, 3, 3, 3, 0.5, 0.5, 0.5, 0.5, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 0.5, 0.5, 3, 3, 3, 3, 3, 3, 3, 3, 0.3, 0, 3, 3, 0.5,
            0.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 100, 100, 1
        ],
        [
            2, 3, 1, 3, 1.5, 3, 1.5, 3, 1.5, 1.5, 1, 3, 0.5, 0.5,
            0.5, 0.5, 1, 3, 1, 3, 1.5, 3, 2, 3, 1.5, 3, 1, 3, 1.5,
            1.5, 2, 2, 2, 2, 1, 1, 2, 3, 0.5, 0.5, 0.5, 0.5, 1, 3, 2,
            2, 2, 3, 0, 0.3, 2, 3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 100, 100, 1
        ],
        [
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0.5, 0.5, 0.5, 0.5,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3, 0.5, 0.5, 0.5, 0.5, 3, 3, 3, 3, 3, 3, 0.3, 0, 3,
            3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            100, 100, 1
        ],
        [
            0.5, 0.5, 2, 3, 1, 3, 1, 3, 1, 1, 1.5, 3, 2, 3, 2, 3, 2,
            3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 2, 2, 2, 1, 1, 0.5,
            0.5, 0.5, 0.5, 2, 2, 2, 3, 1.5, 3, 1, 1, 0.5, 0.5, 2, 3,
            0, 0.3, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 100, 100, 1
        ],
        [
            0.5, 0.5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            0.5, 0.5, 3, 3, 3, 3, 3, 3, 3, 3, 0.5, 0.5, 3, 3, 0.3, 0,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            100, 100, 1
        ],
        [
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 0, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 1.5, 100, 100, 2
        ],
        [
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2, 0, 2, 2, 2, 2,
            2, 2, 2, 2, 1.5, 100, 100, 2
        ],
        [
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2, 2, 0, 2, 2, 2,
            2, 2, 2, 2, 1.5, 100, 100, 2
        ],
        [
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2, 2, 2, 0, 2, 2,
            2, 2, 2, 2, 1.5, 100, 100, 2
        ],
        [
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2, 2, 2, 2, 0, 2,
            2, 2, 2, 2, 1.5, 100, 100, 2
        ],
        [
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2, 2, 2, 2, 2, 0,
            2, 2, 2, 2, 1.5, 100, 100, 2
        ],
        [
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2, 2, 2, 2, 2, 2,
            0, 2, 2, 2, 1.5, 100, 100, 2
        ],
        [
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2, 2, 2, 2, 2, 2,
            2, 0, 2, 2, 1.5, 100, 100, 2
        ],
        [
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2, 2, 2, 2, 2, 2,
            2, 2, 0, 2, 1.5, 100, 100, 2
        ],
        [
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 0, 1.5, 100, 100, 2
        ],
        [
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5,
            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 0, 100, 100, 0.5
        ],
        [
            100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
            100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
            100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
            100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
            100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
            100, 100, 100, 100, 100, 100, 100, 100, 0, 100, 0.15
        ],
        [
            100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
            100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
            100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
            100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
            100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
            100, 100, 100, 100, 100, 100, 100, 100, 100, 0, 0.2
        ],
        [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 0.5, 0.15, 0.2, 1
        ]
    ]

    def __init__(self) -> None:
        pass

    def insertCost(self, ch: str) -> float:
        c: int = ord(ch)
        cost_sum: float = 0
        if c >= KoLevensteinDistance.a_ascii and c <= KoLevensteinDistance.z_ascii:
            cost_sum = KoLevensteinDistance.cost[
                (c - KoLevensteinDistance.a_ascii) *
                2][KoLevensteinDistance.COST_TABLE_SIZE - 1]
        elif c >= KoLevensteinDistance.A_ascii and c <= KoLevensteinDistance.Z_ascii:
            cost_sum = KoLevensteinDistance.cost[
                (c - KoLevensteinDistance.A_ascii) * 2 +
                1][KoLevensteinDistance.COST_TABLE_SIZE - 1]
        elif c >= 48 and c <= 57:
            cost_sum = KoLevensteinDistance.cost[c + 4][
                KoLevensteinDistance.COST_TABLE_SIZE - 1]
        elif c == 32:
            cost_sum = KoLevensteinDistance.cost[62][
                KoLevensteinDistance.COST_TABLE_SIZE - 1]
        else:
            assert False
        return cost_sum

    def deleteCost(self, ch: str) -> float:
        c: int = ord(ch)
        cost_sum: float = 0
        if c >= KoLevensteinDistance.a_ascii and c <= KoLevensteinDistance.z_ascii:
            cost_sum = KoLevensteinDistance.cost[
                KoLevensteinDistance.COST_TABLE_SIZE -
                1][(c - KoLevensteinDistance.a_ascii) * 2]
        elif c >= KoLevensteinDistance.A_ascii and c <= KoLevensteinDistance.Z_ascii:
            cost_sum = KoLevensteinDistance.cost[
                KoLevensteinDistance.COST_TABLE_SIZE -
                1][(c - KoLevensteinDistance.A_ascii) * 2 + 1]
        elif c >= 48 and c <= 57:
            cost_sum = KoLevensteinDistance.cost[
                KoLevensteinDistance.COST_TABLE_SIZE - 1][c + 4]
        elif c == 32:
            cost_sum = KoLevensteinDistance.cost[
                KoLevensteinDistance.COST_TABLE_SIZE - 1][62]
        else:
            assert False
        return cost_sum

    def transCost(self, sc: str, tc: str) -> float:
        s: int = ord(sc)
        t: int = ord(tc)
        if s == t:
            return 0
        cost_sum: float = 0
        if s >= KoLevensteinDistance.a_ascii and s <= KoLevensteinDistance.z_ascii:
            if t >= KoLevensteinDistance.a_ascii and t <= KoLevensteinDistance.z_ascii:
                cost_sum = KoLevensteinDistance.cost[
                    (s - KoLevensteinDistance.a_ascii) *
                    2][(t - KoLevensteinDistance.a_ascii) * 2]
            elif t >= KoLevensteinDistance.A_ascii and t <= KoLevensteinDistance.Z_ascii:
                cost_sum = KoLevensteinDistance.cost[
                    (s - KoLevensteinDistance.a_ascii) *
                    2][(t - KoLevensteinDistance.A_ascii) * 2 + 1]
            elif t >= 48 and t <= 57:
                cost_sum = KoLevensteinDistance.cost[
                    (s - KoLevensteinDistance.a_ascii) * 2][t + 4]
            elif t == 32:
                cost_sum = KoLevensteinDistance.cost[
                    (s - KoLevensteinDistance.a_ascii) * 2][62]
            else:
                assert False
        elif s >= KoLevensteinDistance.A_ascii and s <= KoLevensteinDistance.Z_ascii:
            if t >= KoLevensteinDistance.a_ascii and t <= KoLevensteinDistance.z_ascii:
                cost_sum = KoLevensteinDistance.cost[
                    (s - KoLevensteinDistance.A_ascii) * 2 +
                    1][(t - KoLevensteinDistance.a_ascii) * 2]
            elif t >= KoLevensteinDistance.A_ascii and t <= KoLevensteinDistance.Z_ascii:
                cost_sum = KoLevensteinDistance.cost[
                    (s - KoLevensteinDistance.A_ascii) * 2 +
                    1][(t - KoLevensteinDistance.A_ascii) * 2 + 1]
            elif t >= 48 and t <= 57:
                cost_sum = KoLevensteinDistance.cost[
                    (s - KoLevensteinDistance.A_ascii) * 2 + 1][t + 4]
            elif t == 32:
                cost_sum = KoLevensteinDistance.cost[
                    (s - KoLevensteinDistance.A_ascii) * 2 + 1][62]
            else:
                assert False
        elif s >= 48 and s <= 57:
            if t >= KoLevensteinDistance.a_ascii and t <= KoLevensteinDistance.z_ascii:
                cost_sum = KoLevensteinDistance.cost[
                    s + 4][(t - KoLevensteinDistance.a_ascii) * 2]
            elif t >= KoLevensteinDistance.A_ascii and t <= KoLevensteinDistance.Z_ascii:
                cost_sum = KoLevensteinDistance.cost[
                    s + 4][(t - KoLevensteinDistance.A_ascii) * 2 + 1]
            elif t >= 48 and t <= 57:
                cost_sum = KoLevensteinDistance.cost[s + 4][t + 4]
            elif t == 32:
                cost_sum = KoLevensteinDistance.cost[s + 4][62]
            else:
                assert False
        elif s == 32:
            if t >= KoLevensteinDistance.a_ascii and t <= KoLevensteinDistance.z_ascii:
                cost_sum = KoLevensteinDistance.cost[62][
                    (t - KoLevensteinDistance.a_ascii) * 2]
            elif t >= KoLevensteinDistance.A_ascii and t <= KoLevensteinDistance.Z_ascii:
                cost_sum = KoLevensteinDistance.cost[62][
                    (t - KoLevensteinDistance.A_ascii) * 2 + 1]
            elif t >= 48 and t <= 57:
                cost_sum = KoLevensteinDistance.cost[62][t + 4]
            elif t == 32:
                cost_sum = KoLevensteinDistance.cost[62][62]
            else:
                assert False
        else:
            assert False
        return cost_sum

    def getDistance(self, target: str, other: str) -> float:
        sa = target
        n: int = len(sa)
        p: List[float] = [None] * (n + 1
                                   )  # 'previous' cost array, horizontally
        d: List[float] = [None] * (n + 1)  # cost array, horizontally
        _d: List[float] = [None]  # placeholder to assist in swapping p and d

        m: int = len(other)
        if n == 0 or m == 0:
            if n == m:
                return 1
            else:
                return 0
        # indexes into strings s and t
        # i: int = 0  # iterates through s
        # j: int = 1  # iterates through t
        t_j: str = ''  # jth character of t

        cost: float = 0  # cost

        for i in range(n + 1):
            p[i] = i

        for j in range(1, m + 1):
            t_j = other[j - 1]
            d[0] = j

            for i in range(1, n + 1):
                cost = 0 if sa[i -
                               1] == t_j else self.transCost(sa[i - 1], t_j)
                # minimum of cell to the left+1, to the top+1, diagonally left
                # and up +cost
                d[i] = min(
                    min(d[i - 1] + self.insertCost(t_j),
                        p[i] + self.deleteCost(t_j)), p[i - 1] + cost)
            # copy current distance counts to 'previous row' distance counts
            _d = p
            p = d
            d = _d
        # our last action in the above loop was to switch d and p, so p now
        # actually has the most recent cost counts
        # return 1.0f - ((float) p[n] / Math.max(other.length(), sa.length))
        return p[n]
