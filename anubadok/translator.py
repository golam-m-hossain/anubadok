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


import sys,re
from typing import List, Tuple, Dict, Any

import user_settings
from anubadok import bn_dict
from anubadok import en_pp
from anubadok import en_ss
from anubadok import bn_sondhi
from anubadok.bn_table import BnTable

version = "Anubadok 0.3.0 : (C) 2005-2025, Golam Mortuza Hossain (gmhossain at gmail.com)"

# Global variables that would be set elsewhere


class Translator:
    """
    All Sentence level indicators
    """
    is_it_first_print = True  # To avoid printing 'space' at the beginning
    object_or_subject_ind = 0
    en_subject = []
    en_object = []
    en_verb = []
    interrogative_sentence_ind = 0
    non_wh_question_ind = 0
    imperative_sentence_ind = 0
    passive_sentence_ind = 0
    tense = ''
    tense_sc = ''
    person = 3  # default: 3rd person
    person_determined = 0  # reset
    formality = 1  # default: Most formal "Aapni"
    formality_determined = 0  # reset
    logical_block_ind = 0
    modal_should_ought_ind = 0
    modal_can_may_ind = 0
    beginning_of_sentence_ind = 1
    end_of_sentence_ind = 1
    verb_mainverb_do_ind = 0
    verb_mainverb_be_ind = 0
    verb_mainverb_ind = 0
    verb_hhh_ind = 0
    bn_negation_word = ""
    bn_word_ki_added_ind = 0
    existential_there_ind = 0
    snd_final_word = ""
    modal_eng_word = ""
    bn_punctuation = ""
    turn_on_debugging = 0
    anubadok_mode = ""
    bn_negation_determiner = ""
    bn_negation_preposition = ""
    bn_determiner_suffix = ""
    bn_pre_determiner = ""
    bn_after_preposition = ""
    bn_verb_sondhi_ind = 0
    bn_sub_obj_hhh_suffix = ""
    bn_mainverb = ""
    bn_adverb = ""
    bn_sub_obj = ""
    bn_sub_obj_verb = ""


def translate_in_bengali(input_text: str) -> str:
    """
    Main translation function
    """
    
    if user_settings.verbose:
        print("Translating...", file=sys.stderr)
    
    # First, load dictionary
    bn_dict.load_dictionary()
    
    # Preprocessing
    input_lines = en_pp.english_sentence_preprocessor(input_text)
    
    if Translator.turn_on_debugging:
        print("\n".join(input_lines), file=sys.stderr)
    
    sentence = []
    bengali_output = ""
    
    # Indicators
    Translator.is_it_first_print = True  # To avoid printing 'space' at the beginning
    reset_sentence_level_indicators()
    
    for sts in input_lines:
        if not re.search(r'\t', sts):
            sts = sts.replace('__ANUBADOK__SPACE__', ' ')
            sts = sts + "\t\t\n"
        
        wds_array = sts.split('\t')
        
        if wds_array[1] == "SENT":  # sentence boundary
            sentence.append(sts)
            bengali_output += bangla_translate(sentence)
            Translator.end_of_sentence_ind = 1
            sentence = []
            sts = ""  # reset
            reset_sentence_level_indicators()
        elif wds_array[1] == "LBLM":  # Logical block marker
            Translator.end_of_sentence_ind = 0
            Translator.logical_block_ind = 1
            bengali_output += bangla_translate(sentence)
            sentence = []
            sts = ""  # reset
            Translator.beginning_of_sentence_ind = 0
        else:
            sentence.append(sts)
    
    # Now saves the new words list
    if user_settings.save_new_words_list:
        bn_dict.save_new_words_list()
    
    # Print to world
    if user_settings.verbose:
        print("Done...", file=sys.stderr)
    
    # Return Bengali output
    return bengali_output

def reset_sentence_level_indicators():
    """
    Reset all sentence level indicators
    """
    Translator.interrogative_sentence_ind = 0  # By default a sentence is not interrogative
    Translator.non_wh_question_ind = 0
    Translator.imperative_sentence_ind = 0  # By default a sentence is not imperative
    Translator.passive_sentence_ind = 0  # By default a sentence is active
    
    Translator.person = 3  # default: 3rd person
    Translator.person_determined = 0  # reset
    Translator.formality = 1  # default: Most formal "Aapni"
    Translator.formality_determined = 0  # reset
    Translator.logical_block_ind = 0
    
    Translator.modal_should_ought_ind = 0
    Translator.modal_can_may_ind = 0
    
    Translator.beginning_of_sentence_ind = 1
    Translator.end_of_sentence_ind = 1
    

def bangla_translate(sentence: List[str]) -> str:
    """Main Bangla translation function"""
    
    Translator.en_subject = []
    Translator.en_object = []
    Translator.en_verb = []
    
    Translator.bn_punctuation = ""
    Translator.bn_word_ki_added_ind = 0
    Translator.object_or_subject_ind = 0  # subject-object indicator
    Translator.verb_hhh_ind = 0  # have, has, had indicator
    verb_should_ought_ind = 0  # 'Should' 'ought'
    Translator.verb_mainverb_ind = 0  # main verb 'VV' indicator
    
    Translator.verb_mainverb_do_ind = 0
    Translator.verb_mainverb_be_ind = 0
    Translator.bn_negation_word = ""
    Translator.existential_there_ind = 0
    Translator.modal_eng_word = ""
    
    # Now determine subject, object and verb
    determine_subject_object_verb_new(sentence)
    
    # Check whether it's an interrogative sentence
    determine_sentence_type(sentence)
    
    # Now determine tense
    determine_tense()
    
    # For most interrogative sentences, subject and object needs to be swapped
    if (Translator.interrogative_sentence_ind and 
        not Translator.non_wh_question_ind):
        swap_subject_object()
    
    bn_subject = translate_subject()
    bn_object = translate_object()
    bn_verb = translate_verb()
    
    # In this case verb comes before object
    if False and not Translator.verb_mainverb_ind and not Translator.end_of_sentence_ind:
        bn_sentence = f"{bn_subject} {bn_verb} {bn_object}"
    else:
        bn_sentence = f"{bn_subject} {bn_object} {bn_verb}"
    
    # Remove unwanted spaces
    bn_sentence = re.sub(r' +', ' ', bn_sentence)
    bn_sentence = re.sub(r' ,', ',', bn_sentence)
    bn_sentence = re.sub(r' $', '', bn_sentence)
    
    if Translator.is_it_first_print:
        bn_sentence = re.sub(r'^ ', '', bn_sentence)
        Translator.is_it_first_print = False
    
    return bn_sentence + Translator.bn_punctuation

def determine_subject_object_verb_new(sentence: List[str]) -> None:
    """
    Determine subject, object and verb
    """
    
    Translator.en_subject = []
    Translator.en_object = []
    Translator.en_verb = []
    adverb_array = []
    adv_follow_verb = 0
    word_position = 0
    preposition_ind = 0
    object_ind = 0
    
    for wds in sentence:
        wds_array = wds.split('\t')
        
        if wds_array[1] != "":
            word_position += 1
        
        if wds_array[1] in ["TO", "IN"]:
            if adv_follow_verb:
                Translator.en_verb.extend(adverb_array)
                adverb_array = []
            
            adverb_array.append(wds)
            if not object_ind:
                Translator.en_subject.extend(adverb_array)
            else:
                Translator.en_object.extend(adverb_array)
            
            adv_follow_verb = 0
            adverb_array = []  # reset
            preposition_ind = 1
        
        elif wds_array[1] in ["RB", "RBR", "RBS"]:
            adverb_array.append(wds)
        
        elif wds_array[1] in ["JJ", "JJR", "JJS", "CD"] or wds_array[2] == "@card@":
            adverb_array.append(wds)
            if not object_ind:
                Translator.en_subject.extend(adverb_array)
            else:
                Translator.en_object.extend(adverb_array)
            
            adv_follow_verb = 0
            adverb_array = []  # reset
        
        elif wds_array[1] in ["VB", "VBG", "VBN", "VBP", "VBZ", "VBD"]:
            if wds_array[0].lower() in ["be", "been"]:
                Translator.verb_mainverb_be_ind = 1
            
            adverb_array.append(wds)
            
            if preposition_ind:
                if not object_ind:
                    Translator.en_subject.extend(adverb_array)
                else:
                    Translator.en_object.extend(adverb_array)
                preposition_ind = 0  # reset
            else:
                Translator.en_verb.extend(adverb_array)
            
            adverb_array = []
            if word_position != 1:
                object_ind = 1
            adv_follow_verb = 1
        
        elif wds_array[1] == "MD":
            adverb_array.append(wds)
            
            if preposition_ind:
                if not object_ind:
                    Translator.en_subject.extend(adverb_array)
                else:
                    Translator.en_object.extend(adverb_array)
                preposition_ind = 0  # reset
            else:
                Translator.en_verb.extend(adverb_array)
            
            adverb_array = []
            
            if wds_array[0].lower() in ["should", "ought", "must"]:
                Translator.modal_should_ought_ind = 1
            elif wds_array[0].lower() in ["can", "may", "could", "might"]:
                Translator.modal_can_may_ind = 1
            
            if word_position != 1:
                object_ind = 1
            adv_follow_verb = 1
        
        elif wds_array[1] in ["VV", "VVZ", "VVD", "VVG", "VVP", "VVN"]:
            eng_word = wds_array[2].strip()
            
            if (word_position != 1 or eng_word != 'do') and not preposition_ind:
                object_ind = 1
                adv_follow_verb = 1
                
                if eng_word == 'do':
                    Translator.verb_mainverb_do_ind = 1
                else:
                    Translator.verb_mainverb_ind = 1
            
            adverb_array.append(wds)
            
            if preposition_ind:
                if not object_ind:
                    Translator.en_subject.extend(adverb_array)
                else:
                    Translator.en_object.extend(adverb_array)
                preposition_ind = 0  # reset
            else:
                Translator.en_verb.extend(adverb_array)
                # If 'be' verb has already appeared then treat it as non-mainverb
                if Translator.verb_mainverb_be_ind:
                    Translator.verb_mainverb_be_ind = 0
            
            adverb_array = []
        
        elif wds_array[1] in ["VHZ", "VHP", "VHD", "VHN", "VHG", "VH"]:
            if word_position != 1:
                object_ind = 1
            
            Translator.verb_hhh_ind = 1
            
            # If 'do' verb has already appeared then treat it as non-mainverb
            if Translator.verb_mainverb_do_ind:
                Translator.verb_mainverb_do_ind = 0
            
            adverb_array.append(wds)
            
            if preposition_ind:
                if not object_ind:
                    Translator.en_subject.extend(adverb_array)
                else:
                    Translator.en_object.extend(adverb_array)
                preposition_ind = 0  # reset
            else:
                Translator.en_verb.extend(adverb_array)
            
            adverb_array = []
        
        elif wds_array[1] == "":  # without any Penn tag but can have contents
            if not object_ind:
                Translator.en_subject.append(wds)
            else:
                Translator.en_object.append(wds)
        else:
            if adv_follow_verb == 1:
                Translator.en_verb.extend(adverb_array)
                adverb_array = []
            
            adverb_array.append(wds)
            adv_follow_verb = 0
            
            if preposition_ind:
                preposition_ind = 0  # reset
            
            if not object_ind:
                Translator.en_subject.extend(adverb_array)
            else:
                Translator.en_object.extend(adverb_array)
            adverb_array = []
    
    if preposition_ind:
        if not object_ind:
            Translator.en_subject.extend(adverb_array)
        else:
            Translator.en_object.extend(adverb_array)
        preposition_ind = 0  # reset
    else:
        Translator.en_verb.extend(adverb_array)
    
    adverb_array = []
   
    # Print details for debugging
    if Translator.turn_on_debugging >= 3:
        print("\n==Sentence==\n" + "\n".join(sentence) + 
              "\n==Subject==\n" + "\n".join(Translator.en_subject) +
              "\n==Object==\n" + "\n".join(Translator.en_object) +
              "\n==Verb==\n" + "\n".join(Translator.en_verb), file=sys.stderr)

def determine_sentence_type(sentence: List[str]) -> int:
    """Determine the sentence type"""
    
    if Translator.beginning_of_sentence_ind:
        (Translator.interrogative_sentence_ind, 
         Translator.non_wh_question_ind) = en_ss.check_for_interrogative_sentence(sentence)
    else:
        Translator.interrogative_sentence_ind = 0
        Translator.non_wh_question_ind = 0
    
    if not Translator.interrogative_sentence_ind:
        Translator.imperative_sentence_ind = en_ss.check_for_imperative_sentence(sentence)
    
    if Translator.turn_on_debugging >= 2:
        print("\n -: Sentence Type :-", file=sys.stderr)
        print(f"Question Mark={Translator.interrogative_sentence_ind}", file=sys.stderr)
        print(f"Non-Wh question={Translator.non_wh_question_ind}", file=sys.stderr)
        print(f"Imperative Sentence={Translator.imperative_sentence_ind}", file=sys.stderr)
    
    return 0

def determine_tense() -> int:
    """Determine tense"""
    Translator.tense, Translator.tense_sc, Translator.passive_sentence_ind = en_ss.find_out_tense_details(Translator.en_verb)
    
    if Translator.turn_on_debugging >= 2:
        print("\n -: Tense Details :-", file=sys.stderr)
        print(f"Tense=({Translator.tense}, {Translator.tense_sc})", file=sys.stderr)
        print(f"Passive sentence={Translator.passive_sentence_ind}", file=sys.stderr)
    
    return 0

def swap_subject_object():
    """
    Swap subject and object
    """
    new_sub = Translator.en_object
    Translator.en_object = Translator.en_subject
    Translator.en_subject = new_sub

def translate_subject() -> str:
    """Translates the subject and finds out the 'person'"""
    Translator.object_or_subject_ind = 0  # set it to 'subject' and call general sub_obj
    return construct_sub_obj(Translator.en_subject)

def translate_object() -> str:
    """Translate the object"""
    Translator.object_or_subject_ind = 1  # set it to 'object' and call general sub_obj
    return construct_sub_obj(Translator.en_object)

def construct_sub_obj(en_sub_obj: List[str]) -> str:
    """
    Translates and constructs the subject/object and finds out the 'person' of subject
    """
    Translator.bn_sub_obj = ""
    Translator.bn_determiner_suffix = ""
    number_of_nouns_in_object = 0

    Translator.bn_after_preposition = ""
    Translator.bn_pre_determiner = ""

    Translator.bn_adverb = ""
    Translator.bn_sub_obj_verb = ""

    Translator.bn_verb_sondhi_ind = 0
    Translator.snd_final_word = ""

    Translator.bn_sub_obj_hhh_suffix = ""

    # This tests whether has/have/had is the only verb
    if (Translator.object_or_subject_ind == 0 and ((Translator.verb_hhh_ind and not Translator.verb_mainverb_ind 
                        and not Translator.verb_mainverb_do_ind
                        and not Translator.verb_mainverb_be_ind)
                       or Translator.modal_should_ought_ind)):
        Translator.bn_sub_obj_hhh_suffix = BnTable.bn_subject_hhh_suffix

    for wds in en_sub_obj:
        wds_array = wds.split('\t')

        if wds_array[1] == "IGNR":  # Just ignore it
            pass

        elif wds_array[1] in [',', ';', ':']:
            Translator.bn_sub_obj += wds_array[0]

        elif (':' in wds_array[0] or '|' in wds_array[0] or 
              ('%' in wds_array[0] and wds_array[1] != "CD") or 
              '&' in wds_array[0] or '(' in wds_array[0] or ')' in wds_array[0]):
            Translator.bn_sub_obj += " " + wds_array[0]

        elif wds_array[1] == "UH":
            en_word = wds_array[0]
            bn_wd = bn_dict.dictionary_lookup(en_word)
            Translator.bn_sub_obj += " " + bn_wd

        elif wds_array[1] == "FW":
            en_word = wds_array[0] + ":NP"
            bn_wd = bn_dict.dictionary_lookup(en_word)
            Translator.bn_sub_obj += " " + bn_wd

        elif wds_array[1] in ["LS", "SYM"]:
            en_word = wds_array[0]
            bn_wd = bn_dict.dictionary_lookup(en_word)
            Translator.bn_sub_obj += " " + bn_wd

        elif wds_array[1] == 'SENT':
            en_word = wds_array[0]
            Translator.bn_punctuation = BnTable.bn_punctuation_table.get(en_word, "")

        elif wds_array[1] == 'CD' or wds_array[2] == "@card@":
            en_word = wds_array[0] + ":CD"  # ask for Number
            bn_wd = bn_dict.dictionary_lookup(en_word)
            bn_wd = Translator.bn_adverb + " " + bn_wd
            Translator.bn_adverb = ""  # reset
            Translator.bn_sub_obj += " " + bn_wd

        elif wds_array[1] == 'POS':
            Translator.bn_sub_obj = bn_sondhi.bn_sondhi_possessive(Translator.bn_sub_obj, BnTable.bn_word_er)

        elif wds_array[1] == 'EX':
            Translator.existential_there_ind = 1
            bn_wd = ""

        elif wds_array[1] == 'PDT':
            en_word = wds_array[0].lower()
            Translator.bn_pre_determiner = bn_dict.dictionary_lookup(en_word)
            Translator.bn_pre_determiner = Translator.bn_adverb + " " + Translator.bn_pre_determiner
            Translator.bn_adverb = ""  # Reset

        elif wds_array[1] == 'DT':
            en_word = wds_array[0].lower()
            if not process_and_translate_determiner(en_word):
                en_word = wds_array[0]
                bn_wd = bn_dict.dictionary_lookup(en_word)
                Translator.bn_sub_obj += " " + bn_wd

            if (en_word != "the" and Translator.object_or_subject_ind == 0 
                and not Translator.person_determined):
                Translator.person = 3
                Translator.person_determined = 1

        elif wds_array[1] in ['IN', 'TO']:  # check prepositions and TO
            en_word = wds_array[2].lower()
            if not process_and_translate_preposition(en_word):
                en_word = en_word + ":IN"
                bn_wd = bn_dict.dictionary_lookup(en_word)
                Translator.bn_sub_obj += " " + bn_wd

        elif wds_array[1] in ['RB', 'RBR', 'RBS']:
            en_word = wds_array[2].strip().lower()
            
            if en_word in BnTable.bn_adverb_negation_table:
                Translator.bn_negation_word = BnTable.bn_adverb_negation_table[en_word]
                bn_wd = ""
            else:
                en_word = wds_array[0] + ":RB"
                bn_wd = bn_dict.dictionary_lookup(en_word)

            Translator.bn_adverb += " " + bn_wd

        elif wds_array[1] in ['JJ', 'JJR', 'JJS']:
            en_word = wds_array[0] + ":JJ"  # ask for adjective
            bn_wd = bn_dict.dictionary_lookup(en_word)
            bn_wd = Translator.bn_adverb + " " + bn_wd
            Translator.bn_adverb = ""  # reset
            Translator.bn_sub_obj += " " + bn_wd

        elif wds_array[1] == 'NNS':
            en_word = wds_array[0]
            bn_wd = bn_dict.dictionary_lookup(en_word)
            
            if Translator.object_or_subject_ind == 0 and not Translator.person_determined:
                Translator.person = 3

            if bn_wd != en_word:
                Translator.bn_determiner_suffix = ""  # no need of suffix
            else:
                if wds_array[2] != "<unknown>":
                    en_word = wds_array[2]
                    bn_wd = bn_dict.dictionary_lookup(en_word)
                    if bn_wd == en_word:
                        bn_wd = wds_array[0]
            
            bn_wd += Translator.bn_determiner_suffix
            Translator.bn_determiner_suffix = ""  # reset
            Translator.bn_sub_obj += " " + bn_wd

        elif wds_array[1] in ['WDT', 'WRB', 'WP$', 'WP']:
            en_word = wds_array[2]
            bn_wd = bengali_wh_words(en_word)
            Translator.bn_sub_obj += " " + bn_wd

        elif wds_array[1] in ['PP', 'PP$']:
            en_word = wds_array[0]
            bn_wd = find_out_pronoun(en_word)

            # From subject
            if Translator.object_or_subject_ind == 0 and not Translator.person_determined:
                Translator.person = find_out_person(en_word)
                Translator.person_determined = 1
            
            # From object
            if Translator.object_or_subject_ind == 1 and not Translator.person_determined:
                Translator.person = guess_person_from_object(en_word)
                
                if Translator.anubadok_mode == "PO_MODE":
                    Translator.formality_determined = 1  # TBC

            if (Translator.non_wh_question_ind 
                and not Translator.bn_word_ki_added_ind):  # add 'ki'
                bn_wd += BnTable.bn_word_ki
                Translator.bn_word_ki_added_ind = 1
            
            Translator.bn_sub_obj += " " + bn_wd

        elif wds_array[1] == 'NN':
            en_word = wds_array[0] + ":NN"
            bn_wd = bn_dict.dictionary_lookup(en_word)
            
            if Translator.object_or_subject_ind == 0 and not Translator.person_determined:
                Translator.person = 3

            if Translator.object_or_subject_ind == 1:
                bn_wd += Translator.bn_determiner_suffix
                Translator.bn_determiner_suffix = ""  # reset

            if (Translator.non_wh_question_ind == 1 
                and Translator.bn_word_ki_added_ind == 0):  # add 'ki'
                bn_wd += BnTable.bn_word_ki
                Translator.bn_word_ki_added_ind = 1
            
            Translator.bn_sub_obj += " " + bn_wd

        elif wds_array[1] in ['NP', 'NPS']:
            en_word = wds_array[0] + ":NP"
            bn_wd = bn_dict.dictionary_lookup(en_word)
            
            if (Translator.object_or_subject_ind == 0 and Translator.person_determined == 0):
                Translator.person = 3
                Translator.person_determined = 1

            if Translator.object_or_subject_ind == 1 and number_of_nouns_in_object == 0:
                number_of_nouns_in_object += 1

            if (Translator.non_wh_question_ind == 1 
                and Translator.bn_word_ki_added_ind == 0):  # add 'ki'
                bn_wd += BnTable.bn_word_ki
                Translator.bn_word_ki_added_ind = 1
            
            Translator.bn_sub_obj += " " + bn_wd

        elif wds_array[1] == "CC":
            en_word = wds_array[0].lower()
            bn_wd = BnTable.bn_conjunction_table.get(en_word, "")
            if not bn_wd:
                bn_wd = bn_dict.dictionary_lookup(en_word)
            Translator.bn_sub_obj += " " + bn_wd

        elif wds_array[1] == "":
            bn_wd = wds_array[0]
            Translator.bn_sub_obj += bn_wd

        elif check_for_verb_tag(wds_array[1]):
            en_word = wds_array[2].strip()
            
            if en_word == "<unknown>":
                en_word = wds_array[0]
            
            en_word = en_word + ":VV"
            bn_wd = bn_final_rootverb_after_preposition(en_word)

            Translator.bn_sub_obj_verb += " " + Translator.bn_adverb + " " + bn_wd
            Translator.bn_adverb = ""
            Translator.bn_verb_sondhi_ind = 1

        else:
            bn_wd = wds_array[0]
            Translator.bn_sub_obj += " " + bn_wd

    Translator.bn_sub_obj += " " + Translator.bn_adverb + " " + Translator.bn_sub_obj_verb

    if Translator.bn_verb_sondhi_ind:
        Translator.snd_final_word = bn_sondhi.bn_verb_sondhi_preposition(
            Translator.bn_sub_obj, Translator.bn_after_preposition) + Translator.bn_determiner_suffix
        Translator.bn_verb_sondhi_ind = 0
    else:
        Translator.snd_final_word = bn_sondhi.bn_sondhi_preposition(
            bn_sondhi.bn_sondhi_preposition(
                Translator.bn_sub_obj, Translator.bn_after_preposition), Translator.bn_determiner_suffix)

    # Check whether hhh suffix is non-empty
    if Translator.bn_sub_obj_hhh_suffix:
        return bn_sondhi.bn_sondhi_preposition(Translator.snd_final_word, Translator.bn_sub_obj_hhh_suffix)
    else:
        return Translator.snd_final_word

def process_and_translate_determiner(eng_word: str) -> bool:
    """Process determiner: a, an, the, these, those..."""
    bn_word_determiner = BnTable.bn_determiner_table_1.get(eng_word)
    
    if bn_word_determiner:
        Translator.bn_sub_obj += " " + bn_word_determiner + " " + Translator.bn_pre_determiner
        Translator.bn_determiner_suffix = BnTable.bn_determiner_suffix_table_1.get(eng_word, "")
        Translator.bn_pre_determiner = ""  # reset
        return True

    # Preposition with negation suffix
    bn_word_determiner = BnTable.bn_determiner_table_2.get(eng_word)
    
    if bn_word_determiner:
        Translator.bn_sub_obj += " " + bn_word_determiner + " " + Translator.bn_pre_determiner
        Translator.bn_negation_determiner = BnTable.bn_determiner_suffix_table_2.get(eng_word, "")
        Translator.bn_pre_determiner = ""  # reset
        return True

    return False

def bengali_wh_words(eng_word: str) -> str:
    """Find out the appropriate translation for wh.. words"""
    eng_word = eng_word.lower()
    
    if Translator.interrogative_sentence_ind:
        bng_word = BnTable.wh_table_question.get(eng_word)
        if not bng_word:
            bng_word = bn_dict.dictionary_lookup(eng_word)
        return bng_word
    else:
        bng_word = BnTable.wh_table_relation.get(eng_word)
        if not bng_word:
            bng_word = bn_dict.dictionary_lookup(eng_word)
        return bng_word

# process preposition and subordinating conjunction
def process_and_translate_preposition(eng_word):
    bn_word_preposition = BnTable.bn_preposition_table_1.get(eng_word, "")
    Translator.snd_final_word = ""

    if not Translator.bn_negation_preposition:
        Translator.bn_negation_preposition = BnTable.bn_preposition_negation_table.get(eng_word, "")

    if bn_word_preposition:
        Translator.snd_final_word = f"{Translator.bn_adverb} {Translator.bn_sub_obj_verb}"
        Translator.bn_sub_obj = bn_sondhi.bn_verb_sondhi_preposition(Translator.bn_sub_obj, Translator.bn_determiner_suffix) + " " + Translator.snd_final_word

        Translator.bn_sub_obj_verb = ""
        Translator.bn_determiner_suffix = ""
        Translator.bn_adverb = ""

        if Translator.bn_verb_sondhi_ind == 1:
            Translator.snd_final_word = bn_sondhi.bn_verb_sondhi_preposition(Translator.bn_sub_obj, Translator.bn_after_preposition)
            Translator.bn_verb_sondhi_ind = 0
        else:
            Translator.snd_final_word = bn_sondhi.bn_sondhi_preposition(Translator.bn_sub_obj, Translator.bn_after_preposition)

        Translator.bn_after_preposition = f"{bn_word_preposition} {Translator.snd_final_word}"
        Translator.bn_sub_obj = ""
        return 1

    # preposition of 2nd kind
    bn_word_preposition = BnTable.bn_preposition_table_2.get(eng_word, "")
    if bn_word_preposition:
        Translator.bn_sub_obj = bn_sondhi.bn_verb_sondhi_preposition(Translator.bn_sub_obj, Translator.bn_determiner_suffix)
        Translator.bn_determiner_suffix = ""
        Translator.bn_sub_obj = f"{Translator.bn_sub_obj} {bn_word_preposition}"
        return 1

    # preposition of 3rd kind
    bn_word_preposition = BnTable.bn_preposition_table_3.get(eng_word, "")
    if bn_word_preposition:
        Translator.bn_negation_determiner = bn_word_preposition
        return 1

    return 0

# Find out appropriate pronoun
def find_out_pronoun(eng_word):
    # When in object
    if Translator.object_or_subject_ind == 1:
        if eng_word.lower() == 'you':
            eng_word = 'you_obj'
        if eng_word.lower() == 'her':
            eng_word = 'him'

    if Translator.passive_sentence_ind:
        return find_out_pronoun_passive(eng_word)
    else:
        return find_out_pronoun_active(eng_word)

# Find out appropriate translation for personal pronoun in passive sentences
def find_out_pronoun_passive(eng_word):
    if BnTable.pronoun_active_to_passive_table.get(eng_word.lower()):
        eng_word = BnTable.pronoun_active_to_passive_table[eng_word.lower()]
    
    # Now reset as for Pronouns as it is taken care of.
    Translator.bn_sub_obj_hhh_suffix = ""
    return get_basic_pronoun_translation(eng_word)

# Find out appropriate translation for personal pronoun, PP
def find_out_pronoun_active(eng_word):
    
    eng_word = eng_word.lower()
    
    # This tests, whether has/have/had is the only verb
    if (Translator.object_or_subject_ind == 0 and 
        ((Translator.verb_hhh_ind and not Translator.verb_mainverb_ind 
          and not Translator.verb_mainverb_do_ind
          and not Translator.verb_mainverb_be_ind) 
         or Translator.modal_should_ought_ind)
        and BnTable.pronoun_active_to_modal_table.get(eng_word)):
        eng_word = BnTable.pronoun_active_to_modal_table[eng_word]
        Translator.bn_sub_obj_hhh_suffix = ""

    # In bengali, gender does not matter.
    if (Translator.non_wh_question_ind and eng_word == 'her' and Translator.object_or_subject_ind == 0):
        eng_word = 'him'

    return get_basic_pronoun_translation(eng_word)

# Get basic pronoun translation
def get_basic_pronoun_translation(eng_word):
    bng_word = BnTable.pronoun_table.get(eng_word.lower(), "")
    return bng_word if bng_word else eng_word

# Try to guess 'person' from the object when the subject is not specified.
def guess_person_from_object(eng_word):
    object_person = find_out_person(eng_word)
    if object_person == 1:
        return 2
    elif object_person == 2:
        return 1
    elif object_person == 3:
        return 3

# find out 'person' of the subject 
def find_out_person(eng_word):
    eng_word = eng_word.lower()
    person = BnTable.person_table.get(eng_word, "")
    return Translator.person if not person else person

# Translate and construct the verb
def translate_verb():
    Translator.bn_adverb = ""
    Translator.bn_mainverb = ""
    Translator.bn_mainverb_suffix = ""

    if not Translator.bn_negation_word:
        Translator.bn_negation_word = Translator.bn_negation_determiner
        Translator.bn_negation_determiner = ""

    # We need to know whether 'not' is present 
    if not Translator.bn_negation_word:
        for wds in Translator.en_verb:
            wds_array = wds.split('\t')
            en_word = wds_array[2].lower().strip()
            
            if (BnTable.bn_adverb_negation_table.get(en_word) and wds_array[1] == "RB"):
                Translator.bn_negation_word = BnTable.bn_adverb_negation_table[en_word]

    # Imperative sentence implies second person.
    if Translator.imperative_sentence_ind:
        Translator.person = 2

    for wds in Translator.en_verb:
        wds_array = wds.split('\t')
        bn_wd = ""

        # Translate start constructing
        if wds_array[1] == "IGNR":    # Just ignore it
            pass
        elif wds_array[1] in ["RB", "RBR", "RBS"]:  # adverb
            en_word = wds_array[2].lower().strip()
            
            if BnTable.bn_adverb_negation_table.get(en_word):
                bn_wd = ""
            else:
                en_word = f"{wds_array[0]}:RB"
                bn_wd = bn_dict.dictionary_lookup(en_word)

            Translator.bn_adverb = f"{Translator.bn_adverb} {bn_wd}"
        elif wds_array[1] == 'MD':
            process_modal_verb(wds_array[0])
        elif wds_array[1] in ["VV", "VVD", "VVG", "VVN", "VVP", "VVZ"]:
            en_word = wds_array[2].strip()
            
            if (en_word.lower() == 'do' and 
                (Translator.verb_mainverb_ind or 
                 (not Translator.verb_mainverb_do_ind and not Translator.imperative_sentence_ind) 
                 or Translator.non_wh_question_ind)):
                en_word = ""
            elif en_word == "<unknown>":
                en_word = wds_array[0]
            
            if en_word:
                en_word = f"{en_word}:VV"
                bn_wd = bn_final_rootverb(en_word)
                Translator.bn_mainverb = f"{Translator.bn_mainverb} {bn_wd}"
        elif wds_array[1] in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]:
            en_word = wds_array[0].lower()
            
            if Translator.verb_mainverb_ind or Translator.verb_mainverb_do_ind:
                bn_wd = ""
            elif (Translator.verb_mainverb_be_ind and 
                  (en_word in ['be', 'been'])):
                bn_wd = process_be_as_mainverb(en_word)
            elif en_word in ['be', 'been']:
                bn_wd = ""
            else:
                bn_wd = bn_non_mainverb(en_word)
            
            Translator.bn_mainverb = f"{Translator.bn_mainverb} {bn_wd}"
        elif wds_array[1] in ["VH", "VHD", "VHG", "VHN", "VHP", "VHZ"]:
            if (not Translator.verb_mainverb_ind and not Translator.verb_mainverb_do_ind 
                and not Translator.verb_mainverb_be_ind):
                en_word = wds_array[2].strip()
                bn_wd = process_hhh_as_main_verb(en_word)
            else:
                bn_wd = ""
            
            Translator.bn_mainverb = f"{Translator.bn_mainverb} {bn_wd}"
        else:
            if wds_array[1]:
                bn_wd = bn_dict.dictionary_lookup(wds_array[0])
            else:
                bn_wd = wds_array[0]
            
            Translator.bn_mainverb = f"{Translator.bn_mainverb} {bn_wd}"

    if Translator.bn_negation_word:
        Translator.bn_mainverb = f"{Translator.bn_adverb} {Translator.bn_mainverb} {Translator.bn_negation_word}"
    else:
        Translator.bn_mainverb = f"{Translator.bn_adverb} {Translator.bn_mainverb}"

    Translator.bn_negation_word = ""
    Translator.bn_mainverb_suffix = f"{Translator.bn_mainverb_suffix} {Translator.bn_negation_determiner}"
    Translator.bn_negation_determiner = ""
    
    return bn_sondhi.bn_verb_sondhi_preposition(Translator.bn_mainverb, Translator.bn_mainverb_suffix)

# Process for have,has,had as main verb 
def process_hhh_as_main_verb(eng_word):
    bng_word = ""
    
    if Translator.modal_should_ought_ind:
        Translator.modal_should_ought_ind = 0  # reset
        
        if (Translator.bn_negation_word and 
            BnTable.modal_hhh_table_active_negation.get(Translator.tense, {}).get(Translator.modal_eng_word)):
            Translator.bn_negation_word = ""
            bng_word = BnTable.modal_hhh_table_active_negation[Translator.tense][Translator.modal_eng_word]
        else:
            bng_word = BnTable.modal_hhh_table_active[Translator.tense][Translator.modal_eng_word]
        return bng_word
    elif Translator.modal_can_may_ind:
        Translator.modal_can_may_ind = 0  # reset
        
        if (Translator.bn_negation_word and 
            BnTable.modal_hhh_table_active_negation.get(Translator.tense, {}).get(Translator.modal_eng_word)):
            Translator.bn_negation_word = ""
            bng_word = BnTable.modal_hhh_table_active_negation[Translator.tense][Translator.modal_eng_word]
        else:
            bng_word = BnTable.modal_hhh_table_active[Translator.tense][Translator.modal_eng_word]
        return bng_word
    else:
        if Translator.bn_negation_word:
            Translator.bn_negation_word = BnTable.bn_hhh_word_negation_table.get(Translator.tense, {}).get(eng_word, "")
        else:
            bng_word = BnTable.bn_hhh_word_table.get(Translator.tense, {}).get(eng_word, "")
        return bng_word

# This process for negation when verb is followed by preposition
def bn_final_rootverb_after_preposition(eng_word):
    bng_word = bn_dict.dictionary_lookup(eng_word)
    
    if not Translator.bn_negation_preposition:
        return bng_word
    elif " " in bng_word:
        bng_word = bng_word.replace(" ", f" {Translator.bn_negation_preposition} ")
        Translator.bn_negation_preposition = ""
        return bng_word
    else:
        bng_word = f"{Translator.bn_negation_preposition} {bng_word}"
        Translator.bn_negation_preposition = ""
        return bng_word

# process modal verb
def process_modal_verb(eng_word):
    eng_word = eng_word.lower()
    
    if eng_word in ["should", "ought", "must"]:
        Translator.modal_eng_word = eng_word
        bn_wd = ""
    elif eng_word in ['can', 'may', 'could', 'might']:
        Translator.bn_mainverb_suffix = Translator.bn_mainverb + Translator.bn_mainverb_suffix
        Translator.bn_mainverb = ""
        bn_wd = ""
        Translator.modal_eng_word = eng_word
    else:
        bn_wd = BnTable.modal_verb_table_1_active.get(eng_word, "")
        Translator.bn_mainverb = f"{Translator.bn_mainverb} {bn_wd}"
    
    return 0

# Translate "be" as main verb 
def process_be_as_mainverb(eng_word):
    eng_word = eng_word.lower()
    
    if (Translator.bn_negation_word and 
        BnTable.be_as_mainverb_negation_table.get(Translator.person, {}).get(Translator.tense)):
        bng_word = BnTable.be_as_mainverb_negation_table[Translator.person][Translator.tense]
        Translator.bn_negation_word = ""
    else:
        bng_word = BnTable.be_as_mainverb_table.get(Translator.person, {}).get(Translator.tense, "")
    
    return bng_word

# Translate non-main verb: am, is, are, was, were, will, shall
def bn_non_mainverb(eng_word):
    eng_word = eng_word.lower()
    bng_word = ""
    
    if Translator.bn_negation_word:
        if Translator.existential_there_ind:
            bng_word = BnTable.bn_ex_aux_verb_negation_table.get(Translator.tense, {}).get(eng_word, "")
        
        if not bng_word:
            bng_word = BnTable.bn_aux_verb_negation_table.get(Translator.person, {}).get(eng_word, "")
        
        if not bng_word:
            bng_word = BnTable.bn_aux_verb_table.get(Translator.person, {}).get(eng_word, "")
            if not bng_word:
                bng_word = bn_dict.dictionary_lookup(eng_word)
            bng_word = f"{bng_word} {Translator.bn_negation_word}"
        Translator.bn_negation_word = ""
    else:
        if Translator.existential_there_ind:
            bng_word = BnTable.bn_ex_aux_verb_table.get(Translator.tense, {}).get(eng_word, "")
        
        if not bng_word:
            bng_word = BnTable.bn_aux_verb_table.get(Translator.person, {}).get(eng_word, "")
        
        if not bng_word:
            bng_word = bn_dict.dictionary_lookup(eng_word)
    
    return bng_word

# Check whether tag is a verb form
def check_for_verb_tag(given_tag):
    verb_tags = ["VV", "VVZ", "VVD", "VVG", "VVP", "VVN", 
                 "VB", "VBZ", "VBD", "VBG", "VBP", "VBN",
                 "VH", "VHZ", "VHD", "VHG", "VHP", "VHN"]
    return given_tag in verb_tags

## final form of the main verb
def bn_final_rootverb(en_root_verb):
    if Translator.passive_sentence_ind:
        return bn_final_rootverb_passive(en_root_verb)
    else:
        return bn_final_rootverb_active(en_root_verb)

## final form of the main verb
def bn_final_rootverb_active(en_root_verb):
    bn_root_verb = bn_dict.dictionary_lookup(en_root_verb)
    
    # Return if not found in dictionary
    if bn_root_verb == en_root_verb:
        return en_root_verb
    
    verb_suffix = ""
    
    if Translator.modal_should_ought_ind:
        Translator.modal_should_ought_ind = 0  # reset
        
        if (Translator.bn_negation_word and 
            BnTable.modal_verb_table_2_active_negation.get(Translator.tense_sc, {}).get(Translator.modal_eng_word)):
            Translator.bn_negation_word = ""
            verb_suffix = BnTable.modal_verb_table_2_active_negation[Translator.tense_sc][Translator.modal_eng_word]
        else:
            verb_suffix = BnTable.modal_verb_table_2_active[Translator.tense_sc][Translator.modal_eng_word]
        
        return bn_sondhi.bn_verb_sondhi_passive(bn_root_verb, verb_suffix)
    elif Translator.modal_can_may_ind:
        Translator.modal_can_may_ind = 0
        
        if (Translator.bn_negation_word and 
            BnTable.modal_verb_table_1_active_negation.get(Translator.modal_eng_word)):
            verb_suffix = BnTable.modal_verb_table_1_active_negation[Translator.modal_eng_word]
            Translator.bn_negation_word = ""
        else:
            verb_suffix = BnTable.modal_verb_table_1_active[Translator.modal_eng_word]
        
        verb_suffix = bn_sondhi.bn_verb_sondhi_active(
            verb_suffix, 
            BnTable.verb_mod_table_active.get(Translator.person, {}).get(Translator.tense, {}).get('s', "")
        )
        verb_suffix = verb_suffix.lstrip()
        return bn_sondhi.bn_verb_sondhi_preposition(bn_root_verb, verb_suffix)
    elif (Translator.bn_negation_word and 
          BnTable.verb_mod_table_active_negation.get(Translator.person, {}).get(Translator.tense, {}).get(Translator.tense_sc)):
        Translator.bn_negation_word = ""
        verb_suffix = BnTable.verb_mod_table_active_negation[Translator.person][Translator.tense][Translator.tense_sc]
        print("P,T,TSC",Translator.person,Translator.tense,Translator.tense_sc,'S',verb_suffix)
        return bn_sondhi.bn_verb_sondhi_active(bn_root_verb, verb_suffix)
    else:
        if (Translator.formality == 2 and Translator.tense == 'present' and
            Translator.tense_sc == 's'):
            verb_suffix = BnTable.verb_mod_table_active_formality_2
        else:
            verb_suffix = BnTable.verb_mod_table_active.get(Translator.person, {}).get(Translator.tense, {}).get(Translator.tense_sc, "")
        
        return bn_sondhi.bn_verb_sondhi_active(
            bn_root_verb, 
            verb_suffix, 
            Translator.imperative_sentence_ind
        )

## final form of the main verb
def bn_final_rootverb_passive(en_root_verb):
    bn_root_verb = bn_dict.dictionary_lookup(en_root_verb)
    
    # Return if not found in dictionary
    if bn_root_verb == en_root_verb:
        return en_root_verb
    
    if Translator.modal_should_ought_ind:
        Translator.modal_should_ought_ind = 0  # reset
        
        if (Translator.bn_negation_word and 
            BnTable.modal_verb_table_passive_negation.get(Translator.tense_sc, {}).get(Translator.modal_eng_word)):
            Translator.bn_negation_word = ""
            verb_suffix = BnTable.modal_verb_table_passive_negation[Translator.tense_sc][Translator.modal_eng_word]
        else:
            verb_suffix = BnTable.modal_verb_table_passive[Translator.tense_sc][Translator.modal_eng_word]
        
        return bn_sondhi.bn_verb_sondhi_passive(bn_root_verb, verb_suffix)
    elif Translator.modal_can_may_ind:
        Translator.modal_can_may_ind = 0
        
        if (Translator.bn_negation_word and 
            BnTable.modal_verb_table_passive_negation.get(Translator.tense_sc, {}).get(Translator.modal_eng_word)):
            verb_suffix = BnTable.modal_verb_table_passive_negation[Translator.tense_sc][Translator.modal_eng_word]
            Translator.bn_negation_word = ""
        else:
            verb_suffix = BnTable.modal_verb_table_passive[Translator.tense_sc][Translator.modal_eng_word]
        
        return bn_sondhi.bn_verb_sondhi_preposition(bn_root_verb, verb_suffix)
    elif Translator.bn_negation_word:
        verbmod = BnTable.verb_suffix_table_passive_negation.get(Translator.tense, {}).get(Translator.tense_sc, "")
        if not verbmod:
            verbmod = BnTable.verb_suffix_table_passive.get(Translator.tense, {}).get(Translator.tense_sc, "")
        else:
            Translator.bn_negation_word = ""
        return bn_sondhi.bn_verb_sondhi_passive(bn_root_verb, verbmod)
    else:
        return bn_sondhi.bn_verb_sondhi_passive(
            bn_root_verb, 
            BnTable.verb_suffix_table_passive.get(Translator.tense, {}).get(Translator.tense_sc, "")
        )
        


