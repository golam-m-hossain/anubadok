# -*- coding: utf-8 -*-
#___________________________________________________________________
#
# Copyright (C) 2025, Golam Mortuza Hossain <gmhossain@gmail.com>
#
# This program is a part of the *python port* of Anubadok system
# which was originally written in Perl during 2005-2008. The python
# version is also released under the same license as given below.
#___________________________________________________________________
#
# This program is a part of "Anubadok: The Bengali Machine Translator",
# a free (as in freedom) machine translator package for Bengali (Bangla)
# developed by Golam Mortuza Hossain <gmhossain@gmail.com>.
#___________________________________________________________________
# 
# Copyright (C) 2005-2025, Golam Mortuza Hossain <gmhossain@gmail.com>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#___________________________________________________________________


def bn_verb_sondhi_preposition(sondhi_word1: str, sondhi_word2: str) -> str:
    """
    Apply Bengali sandhi rules for verb-preposition combinations
    """
    sondhi_word1 = sondhi_word1.rstrip()  # remove any trailing space

    if len(sondhi_word1) <= 1 or len(sondhi_word2) < 1:
        return sondhi_word1 + sondhi_word2

    sondhi_wds_array1 = list(sondhi_word1)
    sondhi_wds_array2 = list(sondhi_word2)

    if len(sondhi_word1) >= 3:
        # "XX_khol+te_YY => XX_khulte_YY
        if (check_bn_letter(sondhi_wds_array1[-3]) == 'consonant'
                and sondhi_wds_array1[-2] == get_bn_letter('okar')
                and check_bn_letter(sondhi_wds_array1[-1]) == 'consonant'
                and sondhi_wds_array2[0] == get_bn_letter('TA')
                and sondhi_wds_array2[1] == get_bn_letter('ekar')):
            sondhi_wds_array1[-2] = get_bn_letter('ukar')
            return ''.join(sondhi_wds_array1) + ''.join(sondhi_wds_array2)

        # "XX_patha+te_YY => XX_pathate_YY
        if (sondhi_wds_array1[-3] == get_bn_letter('akar')
                and check_bn_letter(sondhi_wds_array1[-2]) == 'consonant'
                and sondhi_wds_array1[-1] == get_bn_letter('akar')
                and sondhi_wds_array2[0] == get_bn_letter('TA')
                and sondhi_wds_array2[1] == get_bn_letter('ekar')):
            return sondhi_word1 + sondhi_word2

    # "XX_ne+ar_YY => XX_neoar_YY
    if (check_bn_letter(sondhi_wds_array1[-2]) == 'consonant'
            and (sondhi_wds_array1[-1] == get_bn_letter('ekar')
                 or sondhi_wds_array1[-1] == get_bn_letter('ikar'))
            and (sondhi_wds_array2[0] == get_bn_letter('akar')
                 or sondhi_wds_array2[0] == get_bn_letter('ekar'))
            and sondhi_wds_array2[1] == get_bn_letter('RA')):
        sondhi_wds_array1[-1] = get_bn_letter('ekar')
        sondhi_wds_array2[0] = get_bn_letter('akar')
        return (''.join(sondhi_wds_array1) + get_bn_letter('O') +
                get_bn_letter('YYA') + ''.join(sondhi_wds_array2))

    # "XX_pa+te_YY => XX_pete_YY
    if (check_bn_letter(sondhi_wds_array1[-2]) == 'consonant'
            and sondhi_wds_array1[-1] == get_bn_letter('akar')
            and sondhi_wds_array2[0] == get_bn_letter('TA')
            and sondhi_wds_array2[1] == get_bn_letter('ekar')):
        sondhi_wds_array1[-1] = get_bn_letter('ekar')
        return ''.join(sondhi_wds_array1) + ''.join(sondhi_wds_array2)

    # "XX_de+te_YY => XX_dite_YY
    if (check_bn_letter(sondhi_wds_array1[-2]) == 'consonant'
            and sondhi_wds_array1[-1] == get_bn_letter('ekar')
            and sondhi_wds_array2[0] == get_bn_letter('TA')
            and sondhi_wds_array2[1] == get_bn_letter('ekar')):
        sondhi_wds_array1[-1] = get_bn_letter('ikar')
        return ''.join(sondhi_wds_array1) + ''.join(sondhi_wds_array2)

    if (check_bn_letter(sondhi_wds_array1[-2]) == 'consonant'
            and check_bn_letter(sondhi_wds_array1[-1]) == 'consonant'
            and sondhi_wds_array2[0] == get_bn_letter('ekar')
            and sondhi_wds_array2[1] == get_bn_letter('RA')):
        sondhi_wds_array2[0] = get_bn_letter('akar')
        return ''.join(sondhi_wds_array1) + ''.join(sondhi_wds_array2)

    if (check_bn_letter(sondhi_wds_array1[-1]) == 'matra'
            and check_bn_letter(sondhi_wds_array2[0]) == 'matra'):
        sondhi_wds_array2.pop(0)
        return ''.join(sondhi_wds_array1) + ''.join(sondhi_wds_array2)

    return sondhi_word1 + sondhi_word2


def bn_sondhi_preposition(sondhi_word1: str, sondhi_word2: str) -> str:
    """
    Apply general Bengali sandhi rules for prepositions
    """
    sondhi_word1 = sondhi_word1.rstrip()  # remove any trailing space

    if len(sondhi_word1) <= 1 or len(sondhi_word2) < 1:
        return sondhi_word1 + sondhi_word2

    sondhi_wds_array1 = list(sondhi_word1)
    sondhi_wds_array2 = list(sondhi_word2)

    # Preprocessing starts here
    # Ex. 'lekh' => 'likh'
    if (len(sondhi_wds_array1) >= 3
            and sondhi_wds_array1[-3] == get_bn_letter('LA')
            and sondhi_wds_array1[-2] == get_bn_letter('ekar')
            and check_bn_letter(sondhi_wds_array1[-1]) == 'consonant'):
        sondhi_wds_array1[-2] = get_bn_letter('ikar')
        sondhi_word1 = ''.join(sondhi_wds_array1)

    # TO BE Checked and CONFIRMED that its alright
    # Ei+ti => Eti
    if (len(sondhi_wds_array1) >= 2
            and sondhi_wds_array1[-2] == get_bn_letter('E')
            and sondhi_wds_array1[-1] == get_bn_letter('I')
            and len(sondhi_wds_array2) >= 2
            and sondhi_wds_array2[0] == get_bn_letter('TA')
            and sondhi_wds_array2[1] == get_bn_letter('ikar')):
        sondhi_wds_array1.pop()
        return ''.join(sondhi_wds_array1) + ''.join(sondhi_wds_array2)

    # "XX_ke+er_YY => XX_ar_YY (ex. amake+er jonyo = amar + jonyo)
    if (len(sondhi_wds_array1) >= 2
            and sondhi_wds_array1[-2] == get_bn_letter('KA')
            and sondhi_wds_array1[-1] == get_bn_letter('ekar')
            and len(sondhi_wds_array2) >= 2
            and sondhi_wds_array2[0] == get_bn_letter('ekar')
            and sondhi_wds_array2[1] == get_bn_letter('RA')):
        sondhi_wds_array1 = sondhi_wds_array1[:-2]
        sondhi_wds_array2.pop(0)
        
        if sondhi_wds_array1 and sondhi_wds_array1[-1] == get_bn_letter('RA'):
            sondhi_wds_array1.pop()
            
        return ''.join(sondhi_wds_array1) + ''.join(sondhi_wds_array2)

    if (len(sondhi_wds_array1) >= 3
            and sondhi_wds_array1[-3] == ' '
            and check_bn_letter(sondhi_wds_array1[-2]) == 'consonant'
            and check_bn_letter(sondhi_wds_array1[-1]) == 'consonant'
            and len(sondhi_wds_array2) >= 2
            and sondhi_wds_array2[0] == get_bn_letter('ekar')
            and sondhi_wds_array2[1] == get_bn_letter('RA')):
        sondhi_wds_array2[0] = get_bn_letter('akar')
        return ''.join(sondhi_wds_array1) + ''.join(sondhi_wds_array2)

    if (len(sondhi_wds_array1) >= 2
            and (check_bn_letter(sondhi_wds_array1[-2]) in ['consonant', 'vowel', 'hasant', 'matra'])
            and check_bn_letter(sondhi_wds_array1[-1]) == 'consonant'
            and len(sondhi_wds_array2) >= 2
            and sondhi_wds_array2[0] == get_bn_letter('TA')
            and sondhi_wds_array2[1] == get_bn_letter('ekar')):
        sondhi_wds_array2.pop(0)
        return ''.join(sondhi_wds_array1) + ''.join(sondhi_wds_array2)

    if (check_bn_letter(sondhi_wds_array1[-1]) == 'matra'
            and check_bn_letter(sondhi_wds_array2[0]) == 'matra'):
        sondhi_wds_array2.pop(0)
        return ''.join(sondhi_wds_array1) + ''.join(sondhi_wds_array2)

    if (len(sondhi_wds_array2) >= 2
            and (sondhi_wds_array1[-1] == get_bn_letter('anusvar')
                 or check_bn_letter(sondhi_wds_array1[-1]) == sondhi_wds_array1[-1])
            and sondhi_wds_array2[0] == get_bn_letter('ekar')
            and sondhi_wds_array2[1] == get_bn_letter('RA')):
        sondhi_wds_array2[0] = get_bn_letter('E')
        return ''.join(sondhi_wds_array1) + ''.join(sondhi_wds_array2)

    return sondhi_word1 + sondhi_word2


def bn_sondhi(sondhi_word1: str, sondhi_word2: str) -> str:
    """
    Main Bengali sandhi engine
    """
    sondhi_word1 = sondhi_word1.rstrip()  # remove any trailing space
    sondhi_word2 = sondhi_word2.lstrip()  # remove space at the beginning

    if len(sondhi_word1) <= 1 or len(sondhi_word2) < 1:
        return sondhi_word1 + sondhi_word2

    sondhi_wds_array1 = list(sondhi_word1)
    sondhi_wds_array2 = list(sondhi_word2)

    if (len(sondhi_wds_array1) >= 2
            and check_bn_letter(sondhi_wds_array1[-2]) == 'matra'
            and check_bn_letter(sondhi_wds_array1[-1]) == 'consonant'
            and len(sondhi_wds_array2) >= 2
            and sondhi_wds_array2[0] == get_bn_letter('TA')
            and sondhi_wds_array2[1] == get_bn_letter('ekar')):
        sondhi_wds_array2.pop(0)
        return ''.join(sondhi_wds_array1) + ''.join(sondhi_wds_array2)

    if (check_bn_letter(sondhi_wds_array1[-1]) == 'matra'
            and len(sondhi_wds_array2) > 0
            and check_bn_letter(sondhi_wds_array2[0]) == 'matra'):
        sondhi_wds_array2.pop(0)
        return ''.join(sondhi_wds_array1) + ''.join(sondhi_wds_array2)

    return sondhi_word1 + sondhi_word2


def bn_sondhi_possessive(sondhi_word1: str, sondhi_word2: str) -> str:
    """
    Apply Bengali sandhi rules for possessive tags
    """
    sondhi_word1 = sondhi_word1.rstrip()  # remove any trailing space
    sondhi_word2 = sondhi_word2.lstrip()  # remove space at the beginning

    if len(sondhi_word1) <= 1 or len(sondhi_word2) < 1:
        return sondhi_word1 + sondhi_word2

    sondhi_wds_array1 = list(sondhi_word1)
    sondhi_wds_array2 = list(sondhi_word2)

    if check_bn_letter(sondhi_wds_array1[-1]) == 'matra':
        sondhi_wds_array2.pop(0)
        return ''.join(sondhi_wds_array1) + ''.join(sondhi_wds_array2)
    
    return sondhi_word1 + sondhi_word2


def bn_verb_sondhi_basic(sondhi_word1: str, sondhi_word2: str) -> str:
    """
    Apply basic Bengali verb sandhi rules
    """
    sondhi_word1 = sondhi_word1.rstrip()
    sondhi_word2 = sondhi_word2.lstrip()

    if len(sondhi_word1) <= 1 or len(sondhi_word2) < 1:
        return sondhi_word1 + sondhi_word2

    sondhi_wds_array1 = list(sondhi_word1)
    sondhi_wds_array2 = list(sondhi_word2)

    if sondhi_wds_array1[-1] == get_bn_letter('ikar'):
        sondhi_wds_array1[-1] = get_bn_letter('ekar')
        return (''.join(sondhi_wds_array1) + get_bn_letter('O') + 
                get_bn_letter('YYA') + ''.join(sondhi_wds_array2))

    return sondhi_word1 + sondhi_word2


def bn_verb_sondhi_passive(sondhi_word1: str, sondhi_word2: str) -> str:
    """
    Apply Bengali verb sandhi rules for passive sentences
    """
    sondhi_word1 = sondhi_word1.rstrip()
    sondhi_word2 = sondhi_word2.lstrip()

    if len(sondhi_word1) <= 1 or len(sondhi_word2) < 1:
        return sondhi_word1 + sondhi_word2

    # pad-up by 3 spaces to avoid array index problems
    sondhi_word1 = "   " + sondhi_word1
    sondhi_wds_array1 = list(sondhi_word1)
    sondhi_wds_array2 = list(sondhi_word2)

    if ((check_bn_letter(sondhi_wds_array1[-2]) == 'consonant' and 
         check_bn_letter(sondhi_wds_array1[-1]) == 'consonant') or
        (check_bn_letter(sondhi_wds_array1[-2]) == 'matra' and 
         check_bn_letter(sondhi_wds_array1[-1]) == 'consonant')):
        return sondhi_word1[3:] + sondhi_word2  # Remove padding before returning
    else:
        if sondhi_wds_array1[-1] == get_bn_letter('ikar'):
            sondhi_wds_array1[-1] = get_bn_letter('ekar')
            sondhi_word1 = ''.join(sondhi_wds_array1)
        return (sondhi_word1[3:] + get_bn_letter('O') +  # Remove padding
                get_bn_letter('YYA') + sondhi_word2)


def bn_verb_sondhi_active(sondhi_word1: str, sondhi_word2: str, 
                         imperative_sentence_ind: int = 0) -> str:
    """
    Apply Bengali verb sandhi rules for active sentences
    """
    sondhi_word1 = sondhi_word1.rstrip()
    sondhi_word2 = sondhi_word2.lstrip()

    if len(sondhi_word1) <= 1 or len(sondhi_word2) < 1:
        return sondhi_word1 + sondhi_word2

    # pad-up by 3 spaces to avoid array index problems
    sondhi_word1 = "   " + sondhi_word1

    if sondhi_word2 == get_bn_letter('okar'):
        return bn_verb_sondhi_active_suffix_okar(sondhi_word1[3:], sondhi_word2)

    sondhi_wds_array1 = list(sondhi_word1)
    sondhi_wds_array2 = list(sondhi_word2)

    # Ex. 'de' => 'di'
    if (check_bn_letter(sondhi_wds_array1[-2]) == 'consonant' and 
        sondhi_wds_array1[-1] == get_bn_letter('ekar')):
        sondhi_wds_array1[-1] = get_bn_letter('ikar')
        sondhi_word1 = ''.join(sondhi_wds_array1)

    # Ex. 'lekh' => 'likh'
    if (len(sondhi_wds_array1) >= 3 and 
        sondhi_wds_array1[-3] == get_bn_letter('LA') and 
        sondhi_wds_array1[-2] == get_bn_letter('ekar') and 
        check_bn_letter(sondhi_wds_array1[-1]) == 'consonant'):
        sondhi_wds_array1[-2] = get_bn_letter('ikar')
        sondhi_word1 = ''.join(sondhi_wds_array1)

    # 3rd person, present simple - XX + 'ekar'
    if sondhi_word2 == get_bn_letter('ekar'):
        # Ex. 'likh' => 'lekh' (reversal)
        if (len(sondhi_wds_array1) >= 3 and 
            sondhi_wds_array1[-3] == get_bn_letter('LA') and 
            sondhi_wds_array1[-2] == get_bn_letter('ikar') and 
            check_bn_letter(sondhi_wds_array1[-1]) == 'consonant'):
            sondhi_wds_array1[-2] = get_bn_letter('ekar')
            sondhi_word1 = ''.join(sondhi_wds_array1)
        
        # Ex. 'di' => 'de'
        if (len(sondhi_wds_array1) >= 2 and 
            check_bn_letter(sondhi_wds_array1[-2]) == 'consonant' and 
            sondhi_wds_array1[-1] == get_bn_letter('ikar')):
            sondhi_wds_array1[-1] = get_bn_letter('ekar')
            sondhi_word1 = ''.join(sondhi_wds_array1)

        if ((check_bn_letter(sondhi_wds_array1[-2]) == 'consonant' or 
            check_bn_letter(sondhi_wds_array1[-2]) == 'matra') and 
            check_bn_letter(sondhi_wds_array1[-1]) == 'consonant'):
            return sondhi_word1[3:] + sondhi_word2  # Remove padding
        else:
            return sondhi_word1[3:] + map_to_proper_bn_letter(sondhi_word2)

    # 2nd person, present simple - XX + 'ekar NA'
    if sondhi_word2 == get_bn_letter('ekar') + get_bn_letter('NA'):
        # Ex. 'likh' => 'lekh' (reversal)
        if (len(sondhi_wds_array1) >= 3 and 
            sondhi_wds_array1[-3] == get_bn_letter('LA') and 
            sondhi_wds_array1[-2] == get_bn_letter('ikar') and 
            check_bn_letter(sondhi_wds_array1[-1]) == 'consonant'):
            sondhi_wds_array1[-2] = get_bn_letter('ekar')
            sondhi_word1 = ''.join(sondhi_wds_array1)

        if ((check_bn_letter(sondhi_wds_array1[-2]) == 'consonant' or 
             check_bn_letter(sondhi_wds_array1[-2]) == 'vowel' or 
             sondhi_wds_array1[-2] == get_bn_letter('ekar')) and 
            check_bn_letter(sondhi_wds_array1[-1]) == 'consonant'):
            if imperative_sentence_ind == 1:
                sondhi_wds_array2[0] = get_bn_letter('ukar')
            return sondhi_word1[3:] + ''.join(sondhi_wds_array2)
        elif (check_bn_letter(sondhi_wds_array1[-2]) == 'matra' and 
              check_bn_letter(sondhi_wds_array1[-1]) == 'consonant'):
            return sondhi_word1[3:] + sondhi_word2
        else:
            return sondhi_word1[3:] + map_to_proper_bn_letter(sondhi_word2)

    # Future simple - XX + 'BA', 'be', 'ben'
    if len(sondhi_wds_array2) > 0 and sondhi_wds_array2[0] == get_bn_letter('BA'):
        if len(sondhi_wds_array1) > 0 and sondhi_wds_array1[-1] == get_bn_letter('ikar'):
            sondhi_wds_array1[-1] = get_bn_letter('ekar')
            return ''.join(sondhi_wds_array1)[3:] + ''.join(sondhi_wds_array2)
        else:
            return sondhi_word1[3:] + sondhi_word2

    # Past simple - XX + 'lam', 'len', 'la'
    if (sondhi_word2 == get_bn_letter('LA') or 
        sondhi_word2 == get_bn_letter('LA') + get_bn_letter('akar') + get_bn_letter('MA') or 
        sondhi_word2 == get_bn_letter('LA') + get_bn_letter('ekar') + get_bn_letter('NA')):
        # YA akar + LA = GA akar + LA
        if (len(sondhi_wds_array1) >= 3 and 
            sondhi_wds_array1[-3] == " " and 
            sondhi_wds_array1[-2] == get_bn_letter('YA') and 
            sondhi_wds_array1[-1] == get_bn_letter('akar')):
            sondhi_wds_array1[-2] = get_bn_letter('GA')
            sondhi_word1 = ''.join(sondhi_wds_array1)

        if len(sondhi_wds_array1) > 0 and sondhi_wds_array1[-1] == get_bn_letter('akar'):
            sondhi_wds_array1[-1] = get_bn_letter('ekar')
            return ''.join(sondhi_wds_array1)[3:] + sondhi_word2
        else:
            return sondhi_word1[3:] + sondhi_word2

    # 1st person, present simple - XX + 'ikar'
    if sondhi_word2 == get_bn_letter('ikar'):
        # Ex. 'lekh' => 'likh'
        if (len(sondhi_wds_array1) >= 3 and 
            sondhi_wds_array1[-3] == get_bn_letter('LA') and 
            sondhi_wds_array1[-2] == get_bn_letter('ekar') and 
            check_bn_letter(sondhi_wds_array1[-1]) == 'consonant'):
            sondhi_wds_array1[-2] = get_bn_letter('ikar')
            sondhi_word1 = ''.join(sondhi_wds_array1)

        if ((check_bn_letter(sondhi_wds_array1[-2]) == 'consonant' or 
              check_bn_letter(sondhi_wds_array1[-2]) == 'matra') and 
            check_bn_letter(sondhi_wds_array1[-1]) == 'consonant'):
            return sondhi_word1[3:] + sondhi_word2
        else:  # Ex. kha + akar + ikar => kha + akar + I
            return sondhi_word1[3:] + map_to_proper_bn_letter(sondhi_word2)

    # Present/past continuous - XX + 'chi', 'che', 'chen'
    if (len(sondhi_wds_array2) >= 2 and 
        sondhi_wds_array2[0] == get_bn_letter('CHA') and 
        (sondhi_wds_array2[1] == get_bn_letter('ikar') or 
         sondhi_wds_array2[1] == get_bn_letter('ekar'))):
        if (len(sondhi_wds_array1) >= 2 and 
            sondhi_wds_array1[-2] != " " and 
            check_bn_letter(sondhi_wds_array1[-1]) == 'consonant'):
            return sondhi_word1[3:] + sondhi_word2
        else:
            # ...kh+ akar + chh + ... => ...kh + akar + ch+ chh..
            return (sondhi_word1[3:] + get_bn_letter('CA') + 
                    get_bn_letter('hasant') + sondhi_word2)

    # Present/past perfect - XX + 'echhi', 'echhe', 'echhen'
    if (len(sondhi_wds_array2) >= 3 and 
        sondhi_wds_array2[0] == get_bn_letter('ekar') and 
        sondhi_wds_array2[1] == get_bn_letter('CHA') and 
        (sondhi_wds_array2[2] == get_bn_letter('ekar') or 
         sondhi_wds_array2[2] == get_bn_letter('ikar'))):
        # YA akar + LA = GA ikar + LA
        if (len(sondhi_wds_array1) >= 3 and 
            sondhi_wds_array1[-3] == " " and 
            sondhi_wds_array1[-2] == get_bn_letter('YA') and 
            sondhi_wds_array1[-1] == get_bn_letter('akar')):
            sondhi_wds_array1[-2] = get_bn_letter('GA')
            sondhi_wds_array1[-1] = get_bn_letter('ikar')
            sondhi_word1 = ''.join(sondhi_wds_array1)

        # Ex. 'bas' => 'bes'
        if (len(sondhi_wds_array1) >= 3 and 
            check_bn_letter(sondhi_wds_array1[-3]) == 'consonant' and 
            sondhi_wds_array1[-2] == get_bn_letter('akar') and 
            check_bn_letter(sondhi_wds_array1[-1]) == 'consonant'):
            sondhi_wds_array1[-2] = get_bn_letter('ekar')
            sondhi_word1 = ''.join(sondhi_wds_array1)

        # ...ha + ekar ... => ...ha + Ya+ ekar ..
        if (len(sondhi_wds_array1) >= 2 and 
            sondhi_wds_array1[-2] == " " and 
            check_bn_letter(sondhi_wds_array1[-1]) == 'consonant'):
            return sondhi_word1[3:] + get_bn_letter('YYA') + sondhi_word2
        elif (len(sondhi_wds_array1) >= 2 and 
              check_bn_letter(sondhi_wds_array1[-2]) == 'consonant' and 
              sondhi_wds_array1[-1] == get_bn_letter('ikar')):
            return sondhi_word1[3:] + get_bn_letter('YYA') + sondhi_word2
        elif (len(sondhi_wds_array1) >= 3 and 
              (check_bn_letter(sondhi_wds_array1[-3]) == 'consonant' or 
              check_bn_letter(sondhi_wds_array1[-3]) == 'matra') and 
              check_bn_letter(sondhi_wds_array1[-2]) == 'consonant' and 
              sondhi_wds_array1[-1] == get_bn_letter('akar')):
            if len(sondhi_wds_array1) >= 3 and sondhi_wds_array1[-3] == get_bn_letter('okar'):
                sondhi_wds_array1[-3] = get_bn_letter('ukar')
            sondhi_wds_array1[-1] = get_bn_letter('ikar')
            return (''.join(sondhi_wds_array1)[3:] + 
                    get_bn_letter('YYA') + sondhi_word2)
        elif len(sondhi_wds_array1) > 0 and sondhi_wds_array1[-1] == get_bn_letter('akar'):
            sondhi_wds_array1[-1] = get_bn_letter('ekar')
            return (''.join(sondhi_wds_array1)[3:] + 
                    get_bn_letter('YYA') + sondhi_word2)
        else:
            return sondhi_word1[3:] + sondhi_word2

    return sondhi_word1[3:] + sondhi_word2  # Remove padding before returning


def bn_verb_sondhi_active_suffix_okar(sondhi_word1: str, sondhi_word2: str) -> str:
    """
    Apply Bengali sandhi rules when suffix is 'okar'
    """
    sondhi_wds_array1 = list(sondhi_word1)
    sondhi_wds_array2 = list(sondhi_word2)
    
    if check_bn_letter(sondhi_wds_array1[-1]) == 'matra':
        if sondhi_wds_array1[-1] == get_bn_letter('ekar'):
            sondhi_wds_array1[-1] = get_bn_letter('akar')
            sondhi_word1 = ''.join(sondhi_wds_array1)
        return sondhi_word1 + get_bn_letter('O')
    
    return sondhi_word1 + sondhi_word2


def map_to_proper_bn_letter(bn_letter: str) -> str:
    """
    Return corresponding Bengali letter for a given letter
    """
    bn_letter_table = {
        'ি': 'ই',
        'ে': 'য়',
        'েন': 'ন',
    }
    
    return bn_letter_table.get(bn_letter, bn_letter)


def get_bn_letter(bn_letter: str) -> str:
    """
    Return Unicode Bengali letter for the given key
    """
    bn_letter_table = {
        'chandrabindu': 'ঁ',
        'anusvar': 'ং',
        ':': '0',
        
        'A': 'অ',
        'AA': 'আ',
        'I': 'ই',
        'II': 'ঈ',
        'U': 'উ',
        'UU': 'ঊ',
        'RI': 'ঋ',
        'E': 'এ',
        'AI': 'ঐ',
        'O': 'ও',
        'AU': 'ঔ',
        
        'KA': 'ক',
        'KHA': 'খ',
        'GA': 'গ',
        'GHA': 'ঘ',
        'NGA': 'ঙ',
        'CA': 'চ',
        'CHA': 'ছ',
        'JA': 'জ',
        'JHA': 'ঝ',
        'NYA': 'ঞ',
        'TTA': 'ট',
        'TTHA': 'ঠ',
        'DDA': 'ড',
        'DDHA': 'ঢ',
        'NNA': 'ণ',
        'TA': 'ত',
        'THA': 'থ',
        'DA': 'দ',
        'DHA': 'ধ',
        'NA': 'ন',
        'PA': 'প',
        'PHA': 'ফ',
        'BA': 'ব',
        'BHA': 'ভ',
        'MA': 'ম',
        'YA': 'য',
        'RA': 'র',
        'LA': 'ল',
        'SHA': 'শ',
        'SSA': 'ষ',
        'SA': 'স',
        'HA': 'হ',
        'RRA': 'ড়',
        'RHA': 'ঢ়',
        'YYA': 'য়',
        
        'akar': 'া',
        'ikar': 'ি',
        'iikar': 'ী',
        'ukar': 'ু',
        'uukar': 'ূ',
        'rikar': 'ৃ',
        'ekar': 'ে',
        'oikar': 'ৈ',
        'okar': 'ো',
        'aukar': 'ৌ',
        
        'hasant': '্'
    }
    
    return bn_letter_table.get(bn_letter, bn_letter)


def check_bn_letter(bn_letter: str) -> str:
    """
    Check the type of Bengali letter (vowel, consonant, matra, hasant)
    """
    bn_letter_table = {
        'ঁ': '0',
        'ং': '0',
        ':': '0',
        
        'অ': '1',
        'আ': '1',
        'ই': '1',
        'ঈ': '1',
        'উ': '1',
        'ঊ': '1',
        'ঋ': '1',
        'এ': '1',
        'ঐ': '1',
        'ও': '1',
        'ঔ': '1',
        
        'ক': '2',
        'খ': '2',
        'গ': '2',
        'ঘ': '2',
        'ঙ': '2',
        'চ': '2',
        'ছ': '2',
        'জ': '2',
        'ঝ': '2',
        'ঞ': '2',
        'ট': '2',
        'ঠ': '2',
        'ড': '2',
        'ঢ': '2',
        'ণ': '2',
        'ত': '2',
        'থ': '2',
        'দ': '2',
        'ধ': '2',
        'ন': '2',
        'প': '2',
        'ফ': '2',
        'ব': '2',
        'ভ': '2',
        'ম': '2',
        'য': '2',
        'র': '2',
        'ল': '2',
        'শ': '2',
        'ষ': '2',
        'স': '2',
        'হ': '2',
        'ড়': '2',
        'ঢ়': '2',
        'য়': '2',
        
        'া': '3',
        'ি': '3',
        'ী': '3',
        'ু': '3',
        'ূ': '3',
        'ৃ': '3',
        'ে': '3',
        'ৈ': '3',
        'ো': '3',
        'ৌ': '3',
        
        '্': '4'
    }
    
    bn_lt = bn_letter_table.get(bn_letter, None)
    
    if bn_lt is None:
        return bn_letter  # default
    elif bn_lt == "1":
        return 'vowel'
    elif bn_lt == "2":
        return 'consonant'
    elif bn_lt == "3":
        return 'matra'
    elif bn_lt == "4":
        return 'hasant'
    return bn_letter
    

