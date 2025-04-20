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


from anubadok import context
from anubadok import ens_parser
from anubadok import bn_dict
from anubadok.en_tools import match_pattern_and_modify_as_directed


def english_sentence_preprocessor(input_text: str) -> list:
    """
    Top-level processor for English sentences
    """
    sentence_input = input_text.split('\n')
    sentence = []
    sentence_output = []
    
    wds_array = []
    tmp_string = ""
    empty_sent = "\tSENT\t"
    remove_ind = False
    
    # Add empty sent to ensure processing stops
    sentence_input.append(empty_sent)
    
    # Remove marked portions
    temp_output = []
    for sts in sentence_input:
        if "<__ANUBADOK__REMOVE__START__>" in sts:
            remove_ind = True
        elif "<__ANUBADOK__REMOVE__END__>" in sts:
            remove_ind = False
        elif not remove_ind:
            temp_output.append(sts)
    
    sentence_input = temp_output

    for sts in sentence_input:
        sts = sts.replace("<__ANUBADOK__EMPTY__SENT__>", empty_sent)
        
        wds_array = sts.split('\t')
        wds_array.extend([''] * (3 - len(wds_array)))  # Ensure at least 3 elements
        
        if wds_array[1] == "SENT":
            sentence.append(sts)
            sentence_output.extend(
                english_sentence_preprocessor_sub(sentence)
            )
            sentence = []
        else:
            sentence.append(sts)
    
    sentence_output.extend(sentence)
    return sentence_output


def english_sentence_preprocessor_sub(sentence: list) -> list:
    """
    Process each sentence individually
    """
    # Treat known cases where words together mean something
    sentence = concatenate_set_of_two_given_words(sentence)
    sentence = concatenate_set_of_three_given_words(sentence)
    
    # Match patterns and modify them
    sentence = match_pattern_and_modify_as_directed(
        2, "\t\thow", "\t\tbe", "\t\thow.be", "__KEEP__", *sentence
    )
    sentence = match_pattern_and_modify_as_directed(
        2, "\t\thow", "\t\tdo", "\t\thow.do", "__KEEP__", *sentence
    )
    sentence = match_pattern_and_modify_as_directed(
        2, "\t\thow", "\tMD\t", "\t\thow.do", "__KEEP__", *sentence
    )
    sentence = match_pattern_and_modify_as_directed(
        2, "\t\thow", "\t\tto", "\t\thow.to", "\t\tto", *sentence
    )
    sentence = match_pattern_and_modify_as_directed(
        2, "\t\thow", "\t\tnot.to", "\t\thow.to", "\t\tnot.to", *sentence
    )
    sentence = match_pattern_and_modify_as_directed(
        2, "\t\thave", "\t\tto", "\t\thave.to", "\t\tto", *sentence
    )
    
    # Disambiguate contextual meanings of preposition
    sentence = context.disambiguate_prepositions(sentence)

    # Noun processing
    sentence = process_for_adjective_noun_adjustment(sentence)
    sentence = process_for_noun_concatenation("NP", "NPS", sentence)
    sentence = concatenate_NP_of_NP_and_tag_it_NP(sentence)
    
    # Verb tag adjustments
    sentence = process_for_vvg_tag_adjustment(sentence)
    sentence = process_for_vvn_tag_adjustment(sentence)
    
    # Phrasal verb processing
    sentence = process_for_phrasal_adjustment(sentence)
    sentence = process_for_phrasal_verb(sentence)
    
    # Other adjustments
    sentence = process_for_interrogation_adjustment(sentence)
    sentence = process_for_make_verb_adjustment(sentence)
    
    # Insert logical blocks and parse
    sentence = ens_parser.insert_logical_block_marker(sentence)
    sentence = ens_parser.english_sentence_parser(sentence)
    
    return sentence


def concatenate_set_of_three_given_words(sentence: list) -> list:
    """
    Concatenate set of three given words and assign a new tag
    """
    wordlist_array = [
        # Prepositions
        "as", "far", "as", "IN",
        "as", "well", "as", "IN",
        "by", "mean", "of", "IN",
        "by", "means", "of", "IN",
        "in", "accordance", "with", "IN",
        "in", "addition", "to", "IN",
        "in", "case", "of", "IN",
        "in", "front", "of", "IN",
        "in", "lieu", "of", "IN",
        "in", "place", "of", "IN",
        "in", "spite", "of", "IN",
        "on", "account", "of", "IN",
        "on", "behalf", "of", "IN",
        "on", "top", "of", "IN",
        "with", "respect", "to", "IN",
        # Others
        "on", "the", "fly", "RB",
    ]
    
    total_no = len(wordlist_array)
    
    for i in range(0, total_no - 3, 4):
        word_1 = wordlist_array[i]
        word_2 = wordlist_array[i + 1]
        word_3 = wordlist_array[i + 2]
        given_tag = wordlist_array[i + 3]
        
        sentence = match_pattern_and_modify_as_directed(
            3, f"\t\t{word_1}", f"\t\t{word_2}", f"\t\t{word_3}",
            "__REMOVE__", "__REMOVE__",
            f"__CONCAT__\t{given_tag}\t3", *sentence
        )
    
    return sentence


def concatenate_set_of_two_given_words(sentence: list) -> list:
    """
    Concatenate set of two given words and assign a new tag
    """
    wordlist_array = [
        # Prepositions
        "about", "to", "IN",
        "accord", "to", "IN",
        "according", "to", "IN",
        "ahead", "of", "IN",
        "as", "to", "IN",
        "aside", "from", "IN",
        "because", "of", "IN",
        "close", "to", "IN",
        "consist", "of", "IN",
        "due", "to", "IN",
        "except", "for", "IN",
        "far", "from", "IN",
        "in", "to", "IN",
        "inside", "of", "IN",
        "instead", "of", "IN",
        "near", "to", "IN",
        "next", "to", "IN",
        "on", "to", "IN",
        "out", "from", "IN",
        "out", "of", "IN",
        "outside", "of", "IN",
        "owing", "to", "IN",
        "prior", "to", "IN",
        "pursuant", "to", "IN",
        "regardless", "of", "IN",
        "subsequent", "to", "IN",
        "similar", "to", "IN",
        "with", "no", "IN",
        #
        "not", "to", "IN",
        "up", "to", "IN",
        "such", "as", "IN",
        "no", "such", "DT",
        "no", "more", "DT",
        "no", "longer", "DT",
        # Others
        "to", "whom", "WP",
        "each", "other", "PP",
        "think", "tank", "NN",
    ]
    
    total_no = len(wordlist_array)
    
    for i in range(0, total_no - 2, 3):
        word_1 = wordlist_array[i]
        word_2 = wordlist_array[i + 1]
        given_tag = wordlist_array[i + 2]
        
        sentence = match_pattern_and_modify_as_directed(
            2, f"\t\t{word_1}", f"\t\t{word_2}",
            "__REMOVE__", f"__CONCAT__\t{given_tag}\t2",
            *sentence
        )
    return sentence


def concatenate_NP_of_NP_and_tag_it_NP(sentence_input: list) -> list:
    """
    Concatenate three successive words if they match NP of NP pattern
    """
    sentence_output = []
    
    word_1_tag_1 = "NP"
    word_1_tag_2 = "NPS"
    word_2 = "of"
    word_3_tag_1 = "NP"
    word_3_tag_2 = "NPS"
    given_tag = "NP"
    
    word_position = 0
    last_word_1_position = 0
    last_word_2_position = 0
    word_1_ind = False
    word_2_ind = False
    
    for sts in sentence_input:
        wds_array = sts.split('\t')
        wds_array.extend([''] * (3 - len(wds_array)))  # Ensure at least 3 elements
        
        if not word_1_ind and (wds_array[1] == word_1_tag_1 or wds_array[1] == word_1_tag_2):
            last_word_1_position = word_position
            sentence_output.append(sts)
            word_1_ind = True
        
        elif word_1_ind and wds_array[0].lower() == word_2:
            last_word_2_position = word_position
            sentence_output.append(sts)
            word_2_ind = True
        
        elif word_1_ind and word_2_ind and (wds_array[1] == word_3_tag_1 or wds_array[1] == word_3_tag_2):
            word_1_ind = False  # reset
            word_2_ind = False  # reset
            
            if (word_position == last_word_1_position + 2 and 
                word_position == last_word_2_position + 1):
                
                ppst = sentence_output[last_word_1_position]
                wds_tmp_array_1 = ppst.split('\t')
                
                ppst = sentence_output[last_word_2_position]
                wds_tmp_array_2 = ppst.split('\t')
                
                ppst = f"{wds_tmp_array_1[0]}.{wds_tmp_array_2[0]}.{wds_array[0]}"
                
                if bn_dict.dictionary_prelim_lookup(f"{ppst.lower()}:{given_tag}", 1):
                    ppst = (
                        f"{wds_tmp_array_1[0]}.{wds_tmp_array_2[0]}.{wds_array[0]}"
                        f"\t{given_tag}\t"
                        f"{wds_tmp_array_1[0].lower()}.{wds_tmp_array_2[0].lower()}.{wds_array[0].lower()}"
                    )
                    
                    # Replace the first word with concatenated version
                    sentence_output[last_word_1_position] = ppst
                    # Remove the "of" word
                    del sentence_output[last_word_2_position]
                    
                    word_position -= 2  # adjust position counter
                else:
                    sentence_output.append(sts)
            else:
                sentence_output.append(sts)
        else:
            word_1_ind = False  # reset
            sentence_output.append(sts)
        
        word_position += 1
    
    return sentence_output


def process_for_adjective_noun_adjustment(sentence_input: list) -> list:
    """
    Check for 'JJ and NN' patterns and concatenate them if present in dictionary
    """
    sentence_output = []
    word_position = 0
    last_adj_position = 0
    word_adj_ind = False

    for sts in sentence_input:
        wds_array = sts.split('\t')
        wds_array.extend([''] * (3 - len(wds_array)))  # Ensure at least 3 elements

        if wds_array[1] == "JJ":
            last_adj_position = word_position
            sentence_output.append(sts)
            word_adj_ind = True
        elif word_adj_ind and wds_array[1] in {"NN", "NNS", "NP", "NPS"}:
            word_adj_ind = False  # reset

            if word_position == last_adj_position + 1:
                ppst = sentence_output[last_adj_position]
                wds_tmp_array = ppst.split('\t')
                
                # Check whether it's in dictionary
                tag = wds_array[1]
                if tag == "NPS":
                    tag = "NP"
                elif tag == "NNS":
                    tag = "NN"
                
                lookup_word = f"{wds_tmp_array[0].lower()}.{wds_array[0].lower()}:{tag}"
                
                if bn_dict.dictionary_prelim_lookup(lookup_word, True):
                    ppst = (
                        f"{wds_tmp_array[0]}.{wds_array[0]}\t"
                        f"{tag}\t"
                        f"{wds_tmp_array[0].lower()}.{wds_array[0].lower()}"
                    )
                    
                    # Replace the adjective with concatenated version
                    sentence_output[last_adj_position] = ppst
                    word_position -= 1  # adjust position counter
                else:
                    sentence_output.append(sts)
            else:
                sentence_output.append(sts)
        else:
            sentence_output.append(sts)
        
        word_position += 1
    
    return sentence_output


def process_for_noun_concatenation(noun_tag_1: str, noun_tag_2: str, sentence_input: list) -> list:
    """
    Concatenate successive proper nouns (e.g., "Golam Mortuza Hossain" => "Golam.Mortuza.Hossain")
    """
    sentence_output = []
    word_position = 0
    last_NP_position = 0
    word_NP_ind = False

    for sts in sentence_input:
        wds_array = sts.split('\t')
        wds_array.extend([''] * (3 - len(wds_array)))  # Ensure at least 3 elements

        if wds_array[1] == noun_tag_1 or wds_array[1] == noun_tag_2:
            if not word_NP_ind:
                last_NP_position = word_position
                sentence_output.append(sts)
                word_NP_ind = True
            else:
                ppst = sentence_output[last_NP_position]
                wds_tmp_array = ppst.split('\t')
                
                ppst = (
                    f"{wds_tmp_array[0]}.{wds_array[0]}\t"
                    f"{noun_tag_1}\t"
                    f"{wds_tmp_array[0].lower()}.{wds_array[0].lower()}"
                )
                
                # Replace the first noun with concatenated version
                sentence_output[last_NP_position] = ppst
                word_position -= 1  # adjust position counter
        else:
            sentence_output.append(sts)
            word_NP_ind = False  # reset
        
        word_position += 1
    
    return sentence_output


def process_for_phrasal_adjustment(sentence_input: list) -> list:
    """
    Check for two successive prepositions followed by a verb and adjust tags
    """
    sentence_output = []
    word_position = 0
    verb_preposition_ind = False

    for sts in sentence_input:
        wds_array = sts.split('\t')
        wds_array.extend([''] * (3 - len(wds_array)))  # Ensure at least 3 elements

        if (wds_array[1] in {"IN", "TO"} and 
            wds_array[0].lower() != "because" and  # Exceptions should be listed here
            ens_parser.check_for_mainverb(sentence_input[word_position-1])):
            verb_preposition_ind = True
            sentence_output.append(sts)
        elif (verb_preposition_ind and 
              wds_array[1] in {"IN", "TO"}):
            ppst = sentence_output[word_position-1]
            wds_tmp_array = ppst.split('\t')
            ppst = f"{wds_tmp_array[0]}\tRP\t{wds_tmp_array[0]}"
            
            # Replace the preposition with RP tag
            sentence_output[word_position-1] = ppst
            verb_preposition_ind = False
            sentence_output.append(sts)
        else:
            sentence_output.append(sts)
            verb_preposition_ind = False
        
        word_position += 1
    
    return sentence_output


def process_for_make_verb_adjustment(sentence_input: list) -> list:
    """
    Check for 'make sure' pattern and concatenate them
    """
    sentence_output = []
    word_position = 0
    last_make_position = 0
    word_make_ind = False

    for sts in sentence_input:
        wds_array = sts.split('\t')
        wds_array.extend([''] * (3 - len(wds_array)))  # Ensure at least 3 elements

        if wds_array[0].lower() == 'make' and wds_array[1] == "VV":
            last_make_position = word_position
            sentence_output.append(sts)
            word_make_ind = True
        elif word_make_ind and wds_array[0].lower() == 'sure':
            word_make_ind = False  # reset

            if word_position == last_make_position + 1:
                ppst = sentence_output[last_make_position]
                wds_tmp_array = ppst.split('\t')
                
                ppst = (
                    f"{wds_tmp_array[0]}.{wds_array[0]}\t"
                    f"{wds_tmp_array[1]}\t"
                    f"{wds_tmp_array[0].lower()}.{wds_array[0].lower()}"
                )
                
                # Replace "make" with "make.sure"
                sentence_output[last_make_position] = ppst
                word_position -= 1  # adjust position counter
            else:
                sentence_output.append(sts)
        else:
            sentence_output.append(sts)
        
        word_position += 1
    
    return sentence_output


def process_for_interrogation_adjustment(sentence_input: list) -> list:
    """
    Check for 'how many' pattern and concatenate them
    """
    sentence_output = []
    word_position = 0
    last_how_position = 0
    word_how_ind = False

    for sts in sentence_input:
        wds_array = sts.split('\t')
        wds_array.extend([''] * (3 - len(wds_array)))  # Ensure at least 3 elements

        if wds_array[1] == "WRB" and wds_array[0].lower() == 'how':
            last_how_position = word_position
            sentence_output.append(sts)
            word_how_ind = True
        elif word_how_ind and wds_array[1] in {"RB", "JJ"}:
            word_how_ind = False  # reset

            if word_position == last_how_position + 1:
                ppst = sentence_output[last_how_position]
                wds_tmp_array = ppst.split('\t')
                
                ppst = (
                    f"{wds_tmp_array[0]}.{wds_array[0]}\t"
                    f"{wds_tmp_array[1]}\t"
                    f"{wds_tmp_array[0].lower()}.{wds_array[0].lower()}"
                )
                
                # Replace "how" with concatenated version
                sentence_output[last_how_position] = ppst
                word_position -= 1  # adjust position counter
            else:
                sentence_output.append(sts)
        else:
            sentence_output.append(sts)
        
        word_position += 1
    
    return sentence_output


def process_for_vvn_tag_adjustment(sentence_input: list) -> list:
    """
    Check for unaccompanied VVN and change their tag to JJ
    """
    sentence_output = []
    word_position = 0

    verb_hhh_ind = False
    verb_aiaw_ind = False
    pp_ind = False
    noun_ind = False

    for sts in sentence_input:
        wds_array = sts.split('\t')
        wds_array.extend([''] * (3 - len(wds_array)))  # Ensure at least 3 elements

        if wds_array[1] in {"VHP", "VH", "VHZ", "VHD"}:
            verb_hhh_ind = True
        elif wds_array[1] in {"PP", "WP"}:
            pp_ind = True
        elif wds_array[1] in {"NN", "NNS", "NP", "NPS"}:
            noun_ind = True
        elif wds_array[1] in {"VBP", "VBZ", "VBD", "VBN", "VB"}:
            verb_aiaw_ind = True
        elif wds_array[1] == "VVN":
            if (check_for_given_tag("IN", sentence_input[word_position-1]) or
                (not verb_hhh_ind and not verb_aiaw_ind and not pp_ind and not noun_ind)):
                sts = f"{wds_array[0]}\tJJ\t{wds_array[2]}"
            elif (not verb_hhh_ind and not verb_aiaw_ind and (pp_ind or noun_ind)):
                sts = f"{wds_array[0]}\tVVD\t{wds_array[2]}"
            
            # Reset indicators
            verb_hhh_ind = verb_aiaw_ind = pp_ind = noun_ind = False
        elif wds_array[1] in {"DT", "VVP", "VVZ", "VVD", "VVG", "VV"}:
            # Reset indicators
            verb_hhh_ind = verb_aiaw_ind = pp_ind = noun_ind = False
        
        word_position += 1
        sentence_output.append(sts)
    
    return sentence_output


def check_for_given_tag(tag: str, word: str) -> bool:
    """
    Check whether the string contains the given tag
    """
    words_array = word.split('\t')
    return len(words_array) > 1 and words_array[1] == tag


def process_for_vvg_tag_adjustment(sentence_input: list) -> list:
    """
    Check for unaccompanied VVG and change their tag to NN
    """
    sentence_output = []
    word_position = 0

    verb_hhh_ind = False
    verb_aiaw_ind = False
    preposition_ind = False

    for sts in sentence_input:
        wds_array = sts.split('\t')
        wds_array.extend([''] * (3 - len(wds_array)))  # Ensure at least 3 elements

        if wds_array[1] == "IN":
            preposition_ind = True
        elif wds_array[1] in {"VHP", "VHZ", "VHD"}:
            verb_hhh_ind = True
        elif wds_array[1] in {"VBP", "VBZ", "VBD", "VBN", "VB"}:
            verb_aiaw_ind = True
        elif wds_array[1] == "VVG" and word_position != 0:
            if not verb_aiaw_ind and not preposition_ind:
                new_tag = new_tag_for_unaccompanied_vvg(wds_array[0])
                
                if new_tag == "IN":
                    sts = f"{wds_array[0]}\t{new_tag}\t{wds_array[0]}"
                else:
                    sts = f"{wds_array[0]}\t{new_tag}\t{wds_array[2]}"
            else:
                verb_aiaw_ind = preposition_ind = False
        elif wds_array[1] in {"SENT", "DT"}:
            verb_hhh_ind = verb_aiaw_ind = preposition_ind = False
            if wds_array[1] == "SENT":
                word_position = 0
        elif wds_array[1] and wds_array[1] not in {"RB", "RBR", "RBS"}:
            preposition_ind = False
        
        if wds_array[1]:
            word_position += 1
        
        sentence_output.append(sts)
    
    return sentence_output


def new_tag_for_unaccompanied_vvg(word: str) -> str:
    """
    Determine new tag for unaccompanied VVG words
    """
    known_list_of_vvg = {
        'including': "IN",
        'using': "IN"
    }
    return known_list_of_vvg.get(word.lower(), "NN")


def process_for_phrasal_verb(sentence_input: list) -> list:
    """
    Check for 'RP' particles and attach them to the last verb
    """
    sentence_output = []
    word_position = 0
    last_SENT_position = 0
    last_verb_position = 0

    for sts in sentence_input:
        wds_array = sts.split('\t')
        wds_array.extend([''] * (3 - len(wds_array)))  # Ensure at least 3 elements

        if wds_array[1] in {"SENT", "CC", ";", ","}:
            last_SENT_position = word_position
            sentence_output.append(sts)
        elif wds_array[1] in {"VV", "VVD", "VVG", "VVN", "VVP", "VVZ"}:
            last_verb_position = word_position
            sentence_output.append(sts)
        elif wds_array[1] == "RP":
            if last_verb_position > last_SENT_position:
                ppst = sentence_output[last_verb_position]
                wds_tmp_array = ppst.split('\t')
                ppst = wds_tmp_array[2].strip()
                
                ppst = (
                    f"{wds_tmp_array[0]}.{wds_array[0].lower()}\t"
                    f"{wds_tmp_array[1]}\t"
                    f"{ppst}.{wds_array[0].lower()}"
                )
                
                # Replace the verb with verb.particle
                sentence_output[last_verb_position] = ppst
                last_verb_position = last_SENT_position  # reset
                word_position -= 1  # adjust position counter
            else:
                sentence_output.append(sts)
        else:
            sentence_output.append(sts)
        
        word_position += 1
    
    return sentence_output
    

