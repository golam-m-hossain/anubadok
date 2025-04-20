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



def check_for_imperative_sentence(sentence_input):
    """
    Check whether the sentence is imperative
    
    Args:
        sentence_input: List of word\tTAG\tlemma strings
        
    Returns:
        bool: True if sentence is imperative
    """
    word_position = 0
    imperative_sentence_ind = False
    last_word_was_you = False

    for word in sentence_input:
        words_array = word.split('\t')
        
        if len(words_array) > 1 and words_array[1]:
            word_position += 1

        if word_position == 1:
            if (words_array[1] in ["VV", "VVP"] or 
                words_array[0].lower() == "please"):
                imperative_sentence_ind = True
                break
            elif words_array[0].lower() == "you":
                last_word_was_you = True
            else:
                break
        elif word_position == 2:
            if (last_word_was_you and 
                words_array[1] in ["VV", "VVP"]):
                imperative_sentence_ind = True
            break

    return imperative_sentence_ind

def check_for_interrogative_sentence(sentence_input):
    """
    Check whether the sentence is interrogative
    
    Args:
        sentence_input: List of word\tTAG\tlemma strings
        
    Returns:
        tuple: (question_mark, non_wh_question_mark)
               Both are bool indicating question type
    """
    question_mark = False
    non_wh_question_mark = False
    word_position = 0
    first_word_is_do = False

    wh_tags = {'WDT', 'WRB', 'WP$', 'WP'}
    aux_verbs = {
        'MD', 'VB', 'VBP', 'VBZ', 'VBG', 'VBD', 'VBN',
        'VH', 'VHP', 'VHZ', 'VHG', 'VHD', 'VHN'
    }

    for word in sentence_input:
        words_array = word.split('\t')
        if len(words_array) > 1 and words_array[1]:
            word_position += 1
        else:
            words_array.append('')  # Ensure tag exists

        # Wh-interrogation
        if (word_position == 1 and 
            words_array[1] in wh_tags):
            return (True, False)

        # Auxiliary verbs at the beginning
        elif (word_position == 1 and 
              words_array[1] in aux_verbs):
            return (True, True)

        # Do verb at the beginning
        elif (word_position == 1 and 
              len(words_array) > 2 and 
              words_array[2].lower() == 'do'):
            if words_array[0].lower() != 'do':
                return (True, True)
            else:
                first_word_is_do = True

        elif (word_position == 2 and first_word_is_do and
              words_array[0].lower() not in ['it', 'this']):
            return (True, True)

        elif word_position > 2:
            break

    return (question_mark, non_wh_question_mark)

def find_out_tense_details(sentence_input):
    """
    Determine tense and other grammatical features of a sentence
    
    Args:
        sentence_input: List of word\tTAG\tlemma strings
        
    Returns:
        tuple: (tense, tense_desc, passive_sentence_ind)
               - tense: 'present', 'past', or 'future'
               - tense_desc: 's' (simple), 'c' (continuous), 
                            'p' (perfect), 'pc' (perfect continuous)
               - passive_sentence_ind: bool
    """
    tense = "present"
    tense_desc = "s"
    tense_determined = False
    tense_desc_determined = False

    past_participle_of_be_ind = False
    past_participle_of_verb_ind = False
    have_has_had_ind = False
    passive_sentence_ind = False

    for wds in sentence_input:
        wds_array = wds.split('\t')
        
        if len(wds_array) > 2 and wds_array[2] == "have.to":
            passive_sentence_ind = True

        if len(wds_array) <= 1:
            wds_array.append('')  # Ensure tag exists

        tag = wds_array[1]

        if tag == "TO":  # to
            continue
        elif tag in ["VBP", "VBZ"]:  # am, are, is
            if not tense_determined:
                tense = 'present'
                tense_determined = True
        elif tag == "VBD":  # was, were
            if not tense_determined:
                tense = 'past'
                tense_determined = True
        elif tag == "MD":  # shall, will, would, must
            if (not tense_determined and 
                len(wds_array) > 2 and 
                wds_array[2].lower() in ['shall', 'will', 'would', 'must']):
                tense = 'future'
                tense_determined = True
        elif tag in ["VVP", "VVZ"]:  # tell, tells
            if not tense_determined:
                tense = 'present'
                tense_determined = True
            if not tense_desc_determined:
                tense_desc = 's'
                tense_desc_determined = True
        elif tag == "VVD":  # told
            if not tense_determined:
                tense = 'past'
                tense_determined = True
            if not tense_desc_determined:
                tense_desc = 's'
                tense_desc_determined = True
        elif tag in ["VBG", "VVG", "VHG"]:  # being, telling, having
            tense_desc = 'c'
            tense_desc_determined = True
        elif tag == "VBN":  # been
            past_participle_of_be_ind = True
        elif tag in ["VVN", "VHN"]:  # past participle of verb
            past_participle_of_verb_ind = True
        elif tag in ["VHZ", "VH", "VHP"]:  # has, have
            have_has_had_ind = True
            if not tense_determined:
                tense = 'present'
                tense_determined = True
            if not tense_desc_determined:
                tense_desc = 'p'
                tense_desc_determined = True
        elif tag == "VHD":  # had
            have_has_had_ind = True
            if not tense_determined:
                tense = 'past'
                tense_determined = True
            if not tense_desc_determined:
                tense_desc = 'p'
                tense_desc_determined = True

    # Determine passive voice
    if (not have_has_had_ind and 
        (past_participle_of_be_ind or past_participle_of_verb_ind)):
        passive_sentence_ind = True

    # Handle perfect continuous
    if have_has_had_ind and tense_desc == 'c':
        tense_desc = 'pc'

    # Additional passive check
    if (have_has_had_ind and 
        past_participle_of_be_ind and 
        past_participle_of_verb_ind):
        passive_sentence_ind = True

    return (tense, tense_desc, passive_sentence_ind)
