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

import re
import os
from typing import Dict, List, Optional, Tuple
import user_settings
from anubadok import settings


class BnDict:
    dict_table: Dict[str, str] = {}
    new_words_table: Dict[str, str] = {}


def load_dictionary():
    """
    Load all dictionaries
    """
    BnDict.dict_table = {}
    
    load_main_dictionary()
    load_secondary_dictionary()
    load_user_dictionary()
    load_local_dictionary()
    update_dictionary()
    

def update_dictionary():
    """
    Read translated words from new_words.list and update the secondary_dict_db
    """
    translated_dict_table: Dict[str, str] = {}
    
    new_wordlist = settings.new_words_list
    secondary_dict = settings.secondary_dict_db
    
    # Make hash of new words list
    try:
        with open(new_wordlist, 'r', encoding='utf-8') as f:
            db_content = f.readlines()
    except IOError:
        return -1
    
    if os.path.exists(new_wordlist):
        os.unlink(new_wordlist)
    
    for entry in db_content:
        entry = entry.strip()
        if not entry:
            continue
            
        db_data = entry.split('\t')
        if len(db_data) < 2:
            continue
            
        key = db_data[0]
        value = db_data[1]
        
        if value != "BENGALI_MEANING" and value != key:
            if key.endswith(":VV"):
                nvalue = extract_root_verb(value)
            else:
                nvalue = value
                
            translated_dict_table[key] = nvalue
            BnDict.dict_table[key] = nvalue
            
            # Insert another entry without any tag for default uses
            dictwds_array = key.split(':')
            plain_key = dictwds_array[0]
            
            translated_dict_table[plain_key] = value
            BnDict.dict_table[plain_key] = value
    
    # Add translated new words to secondary dict db
    try:
        with open(secondary_dict, 'a', encoding='utf-8') as f:
            for key in translated_dict_table:
                f.write(f"{key}\t{translated_dict_table[key]}\n")
    except IOError as e:
        print(f"Could not open {secondary_dict} for writing.")
        raise e
    # Reset
    BnDict.new_words_table = {}


def load_main_dictionary():
    """
    Open bdict.db and make a dictionary
    """
    dict_db = settings.primary_dict_db
    
    try:
        with open(dict_db, 'r', encoding='utf-8') as f:
            db_content = f.readlines()
    except IOError as e:
        print(f"\nFATAL ERROR!!!\nCould not open {dict_db}.")
        raise e
    
    for entry in db_content:
        entry = entry.strip()
        if not entry:
            continue
            
        db_data = entry.split('\t')
        if len(db_data) >= 2:
            BnDict.dict_table[db_data[0]] = db_data[1]
    

def load_local_dictionary():
    """
    Open local dir dictionary if any and make a dictionary
    """
    dict_new_db = settings.local_dict_db
    
    try:
        with open(dict_new_db, 'r', encoding='utf-8') as f:
            db_content = f.readlines()
    except IOError:
        return -1
    
    for entry in db_content:
        entry = entry.strip()
        if not entry:
            continue
            
        db_data = entry.split('\t')
        if len(db_data) >= 2:
            BnDict.dict_table[db_data[0]] = db_data[1]
    

def load_user_dictionary():
    """
    Open user's own dictionary and make a dictionary
    """
    dict_new_db = settings.user_dict_db
    
    try:
        with open(dict_new_db, 'r', encoding='utf-8') as f:
            db_content = f.readlines()
    except IOError:
        return -1
    
    for entry in db_content:
        entry = entry.strip()
        if not entry:
            continue
            
        db_data = entry.split('\t')
        if len(db_data) >= 2:
            BnDict.dict_table[db_data[0]] = db_data[1]
    

def load_secondary_dictionary():
    """
    Open bdict.new.db and make a dictionary
    """
    dict_new_db = settings.secondary_dict_db
    count = 0
    
    try:
        with open(dict_new_db, 'r', encoding='utf-8') as f:
            db_content = f.readlines()
    except IOError:
        return -1
    
    for entry in db_content:
        entry = entry.strip()
        if not entry:
            continue
            
        db_data = entry.split('\t')
        if len(db_data) >= 2:
            BnDict.dict_table[db_data[0]] = db_data[1]
            count += 1
    
    if user_settings.verbose and count > 200:
        print("""________________________________________________________

Hey! number of entries in your dictionary that you have
translated during your use of Anubadok is {count}. You may
consider submitting these entries as your contributions
to Anubadok's main dictionary. Your contributions well 
be reviewed and subsequently merged with its main 
dictionary. Thanks!!
The file is: {dict_new_db}
_________________________________________________________""")
    

def extract_root_verb(root_verb):
    """
    Extract root verb from Bengali verb form
    """
    # Remove trailing spaces
    root_verb = root_verb.rstrip()
    
    patterns = [
        (r'ওয়া$', ''),
        (r'করা$', 'কর'),
        (r'বলা$', 'বল'),
        (r'ফেলা$', 'ফেল'),
        (r'মারা$', 'মার'),
        (r'পড়া$', 'পড়'),
        (r'পাঠান$', 'পাঠা'),
        (r'থাকা$', 'থাক'),
        (r'দেয়া$', 'দে'),
        (r'চলা$', 'চল'),
        (r'ধরা$', 'ধর'),
        (r'দৌড়ান$', 'দৌড়া'),
        (r'দৌড়ানো$', 'দৌড়া'),
        (r'বেড়ান$', 'বেড়া'),
        (r'বেড়ানো$', 'বেড়া'),
        (r'গোছান$', 'গোছা'),
        (r'গোছানো$', 'গোছা'),
        (r'ভালবাসা$', 'ভালবাস'),
        (r'তোলা$', 'তোল'),
        (r'মানান$', 'মানা'),
        (r'মানানো$', 'মানা'),
        (r'বোনা$', 'বুন'),
        (r'জ্বালানো$', 'জ্বালা'),
        (r'জ্বালান$', 'জ্বালা'),
        (r'হাসা$', 'হাস'),
        (r'কাঁদা$', 'কাঁদ')
    ]
    
    for pattern, replacement in patterns:
        if re.search(pattern, root_verb):
            root_verb = re.sub(pattern, replacement, root_verb)
            break
    # Return 
    return root_verb


def dictionary_prelim_lookup(en_word, new_log=False):
    """
    Check whether given word is present (tagged or untagged)
    """
    if not en_word or en_word == '<unknown>':
        return False
    
    # Get the word, tag
    dictwds_array = en_word.split(':')
    word = dictwds_array[0].strip().lower()
    tag = dictwds_array[1] if len(dictwds_array) > 1 else None
    
    if not word:
        return False
    
    # Exact lookup
    lookup_key = f"{word}:{tag}" if tag else word
    
    if lookup_key in BnDict.dict_table:
        return True
    elif new_log:
        BnDict.new_words_table[lookup_key] = lookup_key
    
    # Now try default entry, if available
    if word in BnDict.dict_table:
        return True
    # Return    
    return False


def dictionary_lookup(en_word):
    """
    Lookup word in dictionary and return translation
    """
    if not en_word or en_word == '<unknown>':
        return en_word
    
    en_word = en_word.strip()
    dictwds_array = en_word.split(':')
    words = dictwds_array[0].strip()
    tag = dictwds_array[1] if len(dictwds_array) > 1 else ""
    
    if not words:
        return ""
    
    # Exact lookup
    lookup_key = f"{words.lower()}:{tag}" if tag else words.lower()
    bn_word = BnDict.dict_table.get(lookup_key, "")
    
    if bn_word:
        return bn_word
    
    # Update new words if not found
    if tag:  # Original condition was more complex, simplified here
        BnDict.new_words_table[lookup_key] = lookup_key
    
    # Try default entry
    lookup_key = words.lower()
    bn_word = BnDict.dict_table.get(lookup_key, "")
    
    if bn_word:
        return bn_word
    elif tag == "CD" or words[0].isdigit():
        return bn_cardinal_number(words)
    
    # Check for 'dotted' words
    if '.' in words:
        tmpwd = words + "."
        tmpwd = tmpwd.replace('.', ':').replace('::', '.:')
        dictwds_array2 = tmpwd.split(':')
        bng_word = ""
        
        for wd in dictwds_array2:
            lookup_key = f"{wd.lower()}:{tag}" if tag else wd.lower()
            bn_word = BnDict.dict_table.get(lookup_key, "")
            
            if not bn_word:
                lookup_key = wd.lower()
                bn_word = BnDict.dict_table.get(lookup_key, "")
                if not bn_word:
                    BnDict.new_words_table[lookup_key] = lookup_key
                    bn_word = wd
            
            bng_word = f"{bng_word} {bn_word}"
        
        return bng_word.strip()
    else:
        return words


def bn_cardinal_number(eng_word):
    """
    Translates any cardinal number to Bengali digits
    """
    bn_number_table = {
        '0': '০',
        '1': '১',
        '2': '২',
        '3': '৩',
        '4': '৪',
        '5': '৫',
        '6': '৬',
        '7': '৭',
        '8': '৮',
        '9': '৯',
        '.': '.',
        ',': ',',
        '-': '-',
        '+': '+'
    }
    
    bng_word = []
    for number in eng_word:
        bng_letter = bn_number_table.get(number, number)
        bng_word.append(bng_letter)
    
    bng_word_str = ''.join(bng_word)
    
    # Translate ordinal suffixes
    bng_word_str = re.sub(r'th$', 'তম', bng_word_str, flags=re.IGNORECASE)
    bng_word_str = re.sub(r'st$', 'তম', bng_word_str, flags=re.IGNORECASE)
    bng_word_str = re.sub(r'nd$', 'তম', bng_word_str, flags=re.IGNORECASE)
    bng_word_str = re.sub(r'rd$', 'তম', bng_word_str, flags=re.IGNORECASE)
    
    return bng_word_str


def save_new_words_list():
    """
    Make new words db
    """
    new_db = settings.new_words_list
    
    if BnDict.new_words_table:
        if user_settings.verbose:
            print(f"""________________________________________________________

Anubadok has encountered some new English words for which 
it does not know the Bengali meaning. These are written
in the file "{new_db}". 
You may want to translate some of these new words (simply
by substituting BENGALI_MEANING in the file). Anubadok will 
use these translated words in your subsequent translations.
_________________________________________________________
""")
        
        try:
            with open(new_db, 'w', encoding='utf-8') as f:
                for key in sorted(BnDict.new_words_table.keys()):
                    f.write(f"{key}\tBENGALI_MEANING\n")
        except IOError:
            pass
