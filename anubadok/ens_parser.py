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


def english_sentence_parser(sentence_input):
    """
    Parse a given sentence into sub-sentences
    
    Args:
        sentence_input: List of word\tTAG\tlemma strings
        
    Returns:
        List of parsed sentence components
    """
    sentence_block = []
    sentence_output = []
    empty_sent = "\tSENT\t"

    for word in sentence_input:
        words_array = word.split('\t')
        
        if len(words_array) > 1 and words_array[1] in ["SENT", "LBLM"]:
            if sentence_block:
                sentence_output.extend(english_sentence_parser_sub(sentence_block))
            sentence_output.append(word)
            sentence_block = []
        else:
            sentence_block.append(word)
    
    if sentence_block:
        sentence_output.extend(sentence_block)
    
    return sentence_output

def english_sentence_parser_sub(sentence_input):
    """
    Parse each block of the sentence into further blocks
    
    Args:
        sentence_input: List of word\tTAG\tlemma strings
        
    Returns:
        List of parsed sentence components
    """
    # Currently just returns the input as-is
    return sentence_input.copy()

def insert_logical_block_marker(sentence_input):
    """
    Insert logical block markers into the sentence
    
    Args:
        sentence_input: List of word\tTAG\tlemma strings
        
    Returns:
        List with logical block markers inserted
    """
    sentence_output = []
    logical_block_marker = "\tLBLM\t"
    empty_sent = "\tSENT\t"
    word_position = 0
    no_of_penn_tag = 0
    preposition_ind = False

    for sts in sentence_input:
        wds_array = sts.split('\t')
        # Ensure array has at least 3 elements
        wds_array += [''] * (3 - len(wds_array))
        
        tag = wds_array[1]
        word = wds_array[0].lower() if wds_array[0] else ''

        if tag == "CC":  # coordinating conjunction
            tmp_array = get_string_in_between(
                word_position + 1,
                "SENT",
                sentence_input
            )
            
            if check_for_verb(sentence_input[word_position + 1]):
                sentence_output.extend([
                    logical_block_marker,
                    sts,
                    logical_block_marker
                ])
            elif (check_for_verb_without_preposition(sentence_output) and 
                  (check_for_verb_without_preposition(tmp_array) or 
                   check_for_listed_preposition(tmp_array))):
                sentence_output.extend([
                    empty_sent,
                    sts,
                    empty_sent
                ])
            else:
                sentence_output.append(sts)
                
        elif tag == ",":  # comma
            tmp_array = get_string_in_between(
                word_position + 1,
                "SENT",
                sentence_input
            )
            
            if check_for_given_tag("CC", sentence_input[word_position + 1]):
                sentence_output.extend([
                    empty_sent,
                    sts,
                    empty_sent
                ])
            elif (check_for_verb_without_preposition(tmp_array) or 
                  check_for_listed_preposition(tmp_array)):
                sentence_output.extend([
                    logical_block_marker,
                    sts,
                    logical_block_marker
                ])
            else:
                sentence_output.append(sts)
                
        elif word == ";":  # semicolon
            sentence_output.extend([
                empty_sent,
                sts,
                empty_sent
            ])
            
        elif (tag == ":" or  # colon
              word in ["(", ")", "[", "]", '"'] or
              word == "then" or
              (word == "that" and tag == "IN") or
              word == "because"):
            sentence_output.extend([
                logical_block_marker,
                sts,
                logical_block_marker
            ])
            preposition_ind = False
            
        elif (no_of_penn_tag > 1 and 
              (tag in ["WDT", "WPT", "WP", "WP$", "WRB"] or
               word in ["so", "if"])):
            sentence_output.extend([
                logical_block_marker,
                sts
            ])
            preposition_ind = False
            
        elif tag in ["IN", "TO"]:  # preposition or 'to'
            sentence_output.append(sts)
            preposition_ind = True
            
        else:
            sentence_output.append(sts)
            if tag:  # If it has a tag
                preposition_ind = False
                
        if tag:
            no_of_penn_tag += 1
            
        word_position += 1
        
    return sentence_output

def check_for_verb_without_preposition(sentence_input):
    """
    Check if the string contains any verb without any preposition
    
    Args:
        sentence_input: List of word\tTAG\tlemma strings
        
    Returns:
        bool: True if verb without preposition is found
    """
    preposition_ind = False
    
    for sts in sentence_input:
        wds_array = sts.split('\t')
        wds_array += [''] * (3 - len(wds_array))
        tag = wds_array[1]
        
        if tag in ["IN", "TO"]:
            preposition_ind = True
            
        if tag in ["NN", "NNS", "NP", "NPS", "PP", "PPS", "DT", "CD"]:
            preposition_ind = False
        elif not preposition_ind and check_for_mainverb(sts):
            return True
        elif not preposition_ind and check_for_aux_verb(sts):
            return True
            
    return False

def get_string_in_between(starting_position, end_TAG, sentence_input):
    """
    Return the string between the position and given TAG or SENT
    
    Args:
        starting_position: Starting index
        end_TAG: Tag to look for
        sentence_input: List of word\tTAG\tlemma strings
        
    Returns:
        List of words between positions
    """
    sentence_output = []
    
    for word_position in range(starting_position, len(sentence_input)):
        sts = sentence_input[word_position]
        wds_array = sts.split('\t')
        tag = wds_array[1] if len(wds_array) > 1 else ''
        word = wds_array[0].lower() if wds_array[0] else ''
        
        if (tag in ["SENT", ","] or 
            word in ["that", "then"] or 
            tag == "CC" or 
            tag == end_TAG):
            sentence_output.append(sts)
            return sentence_output
            
        sentence_output.append(sts)
        
    return sentence_output

def check_for_verb(word):
    """
    Check if the word is a verb (main or auxiliary)
    
    Args:
        word: word\tTAG\tlemma string
        
    Returns:
        bool: True if word is a verb
    """
    return check_for_mainverb(word) or check_for_aux_verb(word)

def check_for_mainverb(word):
    """
    Check if the word is a main verb
    
    Args:
        word: word\tTAG\tlemma string
        
    Returns:
        bool: True if word is a main verb
    """
    if isinstance(word, list):
        sentence_input = word
    else:
        sentence_input = [word]
    
    for sts in sentence_input:
        wds_array = sts.split('\t')
        wds_array += [''] * (3 - len(wds_array))
        
        if len(wds_array) > 2 and wds_array[2] == "do":
            return False
            
        if wds_array[1] in ["VV", "VVD", "VVG", "VVN", "VVP", "VVZ"]:
            return True
            
    return False

def check_for_aux_verb(word):
    """
    Check if the word is an auxiliary verb
    
    Args:
        word: word\tTAG\tlemma string
        
    Returns:
        bool: True if word is an auxiliary verb
    """
    if isinstance(word, list):
        sentence_input = word
    else:
        sentence_input = [word]
    
    for sts in sentence_input:
        wds_array = sts.split('\t')
        tag = wds_array[1] if len(wds_array) > 1 else ''
        
        if tag in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ",
                   "VH", "VHD", "VHG", "VHN", "VHP", "VHZ"]:
            return True
            
    return False

def check_for_listed_preposition(sentence_input):
    """
    Check if the string contains listed prepositions
    
    Args:
        sentence_input: List of word\tTAG\tlemma strings
        
    Returns:
        bool: True if listed preposition is found
    """
    for sts in sentence_input:
        wds_array = sts.split('\t')
        word = wds_array[0].lower() if wds_array[0] else ''
        
        if word in ["as", "since", "of", "consist.of"]:
            return True
            
    return False

def check_for_given_tag(tag, word):
    """
    Check if the word has the given tag
    
    Args:
        tag: Tag to check for
        word: word\tTAG\tlemma string
        
    Returns:
        bool: True if word has the specified tag
    """
    words_array = word.split('\t')
    word_tag = words_array[1] if len(words_array) > 1 else ''
    
    return word_tag == tag
