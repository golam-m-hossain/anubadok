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


def match_pattern_and_modify_as_directed(no_p, *args):
    """
    Match pattern and modify as directed in a POS tagged sentence
    
    Args:
        no_p: Number of patterns to match
        *args: Contains:
            - First no_p elements: patterns to match
            - Next no_p elements: patterns to substitute
            - Remaining elements: sentence output to process
            
    Returns:
        Modified sentence as a list
    """
    # Split args into patterns to match, substitute, and sentence output
    pattern_to_match = list(args[:no_p])
    pattern_to_substitute = list(args[no_p:2*no_p])
    sentence_output = list(args[2*no_p:])
    
    total_words = len(sentence_output)
    
    
    i = 0
    while i <= total_words - no_p:
        match = True
        
        # Check if patterns match
        for j in range(no_p):
            if not compare_two_patterns(pattern_to_match[j], sentence_output[i + j]):
                match = False
                break
        
        if match:
            # Process matched patterns
            for j in range(no_p - 1, -1, -1):  # Process in reverse order
                sub_pattern = pattern_to_substitute[j] if j < len(pattern_to_substitute) else ""

                if "__REMOVE__" in str(sub_pattern):
                    del sentence_output[i + j]
                    total_words -= 1
                elif "__CONCAT__" in str(sub_pattern):
                    parts = str(sub_pattern).split('\t')
                    given_tag = parts[1] if len(parts) > 1 else ""
                    k = int(parts[2]) if len(parts) > 0 else 0
                    combo = sentence_output[i + j]
                    
                    for l in range(1, k):
                        combo = concatenate_given_two_patterns(
                            sentence_output[i + j - l], 
                            combo, 
                            given_tag
                        )
                    
                    sentence_output[i + j] = combo
                elif sub_pattern != "__KEEP__":
                    sentence_output[i + j] = generate_final_pattern(
                        sentence_output[i + j], 
                        sub_pattern
                    )
        
        i += 1
    
    return sentence_output


def compare_two_patterns(pattern1, pattern2):
    """
    Compare two given word\tTAG\tlemma patterns
    
    Args:
        pattern1: First pattern to compare
        pattern2: Second pattern to compare
        
    Returns:
        bool: True if patterns match according to comparison rules
    """
    words_array_1 = str(pattern1).split('\t')
    words_array_2 = str(pattern2).split('\t')
    
    # Ensure array has at least 3 elements
    words_array_1 += [''] * (3 - len(words_array_1))
    words_array_2 += [''] * (3 - len(words_array_2))
    
    # Compare word (case insensitive)
    if words_array_1[0] and words_array_1[0].lower() != words_array_2[0].lower():
        return False
    
    # Compare tag (case sensitive)
    if words_array_1[1] and words_array_1[1] != words_array_2[1]:
        return False
    
    # Compare lemma (case insensitive)
    if words_array_1[2] and words_array_1[2].lower() != words_array_2[2].lower():
        return False
    
    return True


def concatenate_given_two_patterns(pattern1, pattern2, given_tag):
    """
    Generate final pattern after concatenating two given patterns
    
    Args:
        pattern1: First pattern (word\tTAG\tlemma)
        pattern2: Second pattern (word\tTAG\tlemma)
        given_tag: Tag to use for the concatenated result
        
    Returns:
        Concatenated pattern as string
    """
    parts1 = str(pattern1).split('\t')
    parts2 = str(pattern2).split('\t')
    
    # Ensure we have at least word, tag, lemma for both patterns
    parts1 += [''] * (3 - len(parts1))
    parts2 += [''] * (3 - len(parts2))
    
    word1, tag1, lemma1 = parts1[0], parts1[1], parts1[2]
    word2, tag2, lemma2 = parts2[0], parts2[1], parts2[2]
    
    return f"{word1}.{word2}\t{given_tag}\t{lemma1}.{lemma2}"


def generate_final_pattern(original_pattern, modification_pattern):
    """
    Generate final pattern by applying modifications
    
    Args:
        original_pattern: Original pattern (word\tTAG\tlemma)
        modification_pattern: Modification pattern (word\tTAG\tlemma)
        
    Returns:
        Modified pattern as string
    """
    orig_parts = str(original_pattern).split('\t')
    mod_parts = str(modification_pattern).split('\t')
    
    # Ensure we have at least word, tag, lemma for original
    orig_parts += [''] * (3 - len(orig_parts))
    word, tag, lemma = orig_parts[0], orig_parts[1], orig_parts[2]
    
    # Apply modifications if specified
    if len(mod_parts) > 0 and mod_parts[0]:
        word = mod_parts[0]
    if len(mod_parts) > 1 and mod_parts[1]:
        tag = mod_parts[1]
    if len(mod_parts) > 2 and mod_parts[2]:
        lemma = mod_parts[2]
    
    return f"{word}\t{tag}\t{lemma}"

