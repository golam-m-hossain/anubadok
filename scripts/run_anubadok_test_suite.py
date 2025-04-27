#!/usr/bin/env python3
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
# Copyright (C) 2008, Golam Mortuza Hossain <gmhossain@gmail.com>
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

import os
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

# Import the necessary
sys.path.insert(0, ".")
from anubadok import initialize
initialize.check_user_anubadok_dir()

from anubadok import settings
from anubadok import xml_pp
from anubadok import pos_tagger
from anubadok import translator
from anubadok.settings import anubadok_tmp_dir

total_no_of_sentences = 0

def translate_test_suite(english_file, bengali_file):
    """Translate a given Test Suites"""
    with open(english_file, 'r', encoding='utf-8') as f:
        input_text = f.read()
    
    processed = xml_pp.xml_pre_processor(input_text)
    tagged = pos_tagger.penn_treebank_tagger(processed)
    translated = translator.translate_in_bengali(tagged)
    output = xml_pp.xml_post_processor(translated)
    
    with open(bengali_file, 'w', encoding='utf-8') as f:
        f.write(output)
    
    return 0

def translate_all_test_suites(test_suites_dir, list_of_files):
    """Translate all test suites at once"""
    combo_file = os.path.join(anubadok_tmp_dir, "__combined_test_suites.xml")
    combo_file_bengali = os.path.join(anubadok_tmp_dir, "__translated_combined_test_suites.xml")
    
    # Parse the list of files
    tree = ET.parse(os.path.join(test_suites_dir, list_of_files))
    root = tree.getroot()
    
    # Make a single file by concatenating all files
    with open(combo_file, 'w', encoding='utf-8') as combo_fl:
        for file_node in root.findall('file'):
            tmp = file_node.text.strip()
            with open(os.path.join(test_suites_dir, tmp), 'r', encoding='utf-8') as xml_fl:
                input_text = xml_fl.read()
            combo_fl.write(f"{input_text}\n<__END__OF__FILE__>\n")
    
    # Create Translated combo Test Suites
    with open(combo_file, 'r', encoding='utf-8') as f:
        input_text = f.read()
    
    processed = xml_pp.xml_pre_processor(input_text)
    tagged = pos_tagger.penn_treebank_tagger(processed)
    translated = translator.translate_in_bengali(tagged)
    output = xml_pp.xml_post_processor(translated)
    
    with open(combo_file_bengali, 'w', encoding='utf-8') as f:
        f.write(output)
    
    # Split translated combo files
    with open(combo_file_bengali, 'r', encoding='utf-8') as combo_fl:
        for file_node in root.findall('file'):
            tmp = file_node.text.strip()
            output_file = os.path.join(anubadok_tmp_dir, f"bengali-{tmp}")
            
            with open(output_file, 'w', encoding='utf-8') as xml_fl:
                while True:
                    line = combo_fl.readline()
                    if not line or "__END__OF__FILE__" in line:
                        break
                    xml_fl.write(line)
    
    # Clean up
    os.unlink(combo_file)
    os.unlink(combo_file_bengali)
    

def check_translated_file(bengali_file):
    """
    Check whether translated sentences differ from expected bengali sentences.
    """
    global total_no_of_sentences
    
    tree = ET.parse(bengali_file)
    root = tree.getroot()
    
    testsuite_type = root.get('type')
    print(f"Description: {testsuite_type}")
    
    success = 0
    failure = 0
    
    for sentence in root.iter('sentence'):
        expected_bn = sentence.attrib['expected_bengali']
        translated_bn = sentence.text
        english = sentence.attrib['english']
        
        # Clean up
        translated_bn = translated_bn.replace('\n', ' ')  # Remove New Line
        translated_bn = translated_bn.replace('\t', ' ')  # Remove Tab
        translated_bn = ' '.join(translated_bn.split())  # Remove extra spaces
        translated_bn = translated_bn.replace(' ,', ',')  # Remove space in front of comma
        
        if expected_bn == translated_bn:
            print(f"{english} => [OK]")
            success += 1
        else:
            print(f"{english} => [FAILED]")
            print(f"       [Expected  : {expected_bn}]")
            print(f"       [Translated: {translated_bn}]")
            failure += 1
        
        total_no_of_sentences += 1
    
    # Print Statistics
    rate = success / (success + failure) * 100 if (success + failure) > 0 else 0
    print(f"Success Rate: {rate:.1f}%")
    
    return failure > 0

def main():
    global total_no_of_sentences
    
    # Configuration
    test_suites_dir = "tests"
    list_of_files = "list_of_test_suites.xml"
    failed_suites = []
    
    given_test_suites = sys.argv[1] if len(sys.argv) > 1 else None
    
    start_time = time.time()
    
    print("Anubadok - Test Suites:")
    
    if given_test_suites and os.path.exists(given_test_suites):
        english_file = given_test_suites
        bengali_file = os.path.join(anubadok_tmp_dir, "bengali-testsuites.xml")
        
        translate_test_suite(english_file, bengali_file)
        if check_translated_file(bengali_file):
            failed_suites.append(english_file)
        
        # Clean up
        os.unlink(bengali_file)
    else:
        print("No specific Test-suite specified. Checking all listed...")
        
        # Translate all Test suites at once
        translate_all_test_suites(test_suites_dir, list_of_files)
        
        # Parse the list of files
        tree = ET.parse(os.path.join(test_suites_dir, list_of_files))
        root = tree.getroot()
        
        for file_node in root.findall('file'):
            tmp = file_node.text.strip()
            english_file = os.path.join(test_suites_dir, tmp)
            bengali_file = os.path.join(anubadok_tmp_dir, f"bengali-{tmp}")
            
            print(f"Checking: {english_file}")
            
            if check_translated_file(bengali_file):
                failed_suites.append(english_file)
            
            # Clean up
            os.unlink(bengali_file)
    
    # Final Statistics
    print("___________________________________________________\n")
    print("Overall Statistics :-- \n")
    print(f"Total no of test sentences: {total_no_of_sentences}")
    
    if failed_suites:
        print("Following test-suites have failed.\n")
        for i, suite in enumerate(failed_suites, 1):
            print(f"({i}) {suite}")
    else:
        print("All test-suites have passed.")
    print()
    
    end_time = time.time()
    time_diff = round(end_time - start_time)
    
    print(f"Time taken to complete the test: {time_diff} Seconds")

if __name__ == "__main__":
    main()
