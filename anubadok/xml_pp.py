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

###########################################
#
#  XML Preprocessing :: pre and post
#
###########################################

def xml_pre_processor(*args):
    input_string = "".join(args)
    input_string = input_string.rstrip('\n')

    if len(input_string) == 0:
        return input_string  # no processing

    output_array = []
    counter = 0

    # Define mark-up indicators
    mark_up_ind = 0
    comments_ind = 0
    outchar = ""
    xml_doc_ind = 0

    # Empty sent mimics end of sentence without punctuation marks
    empty_sent = " <__ANUBADOK__EMPTY__SENT__> "

    # The middle " . " forces PoS Tagger to treat it as end of sentence.
    # However, it needs to be removed as it is not present in original 
    # texts.
    anu_remove = " <__ANUBADOK__REMOVE__START__>" + " . " + "<__ANUBADOK__REMOVE__END__> "

    # First sanitise
    input_string = sanitise(input_string)

    # Check whether its XML
    if re.search(r'<\?xml', input_string, re.IGNORECASE):
        xml_doc_ind = 1
    elif re.search(r'<html', input_string, re.IGNORECASE):
        input_string = re.sub(r'charset=.*"', 'charset=UTF-8"', input_string, flags=re.IGNORECASE)
        if not re.search(r'charset=', input_string, re.IGNORECASE):
            input_string = re.sub(r'</head', '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head', input_string, flags=re.IGNORECASE)

    input_array = list(input_string)  # character splitting

    while counter < len(input_array):
        char = input_array[counter]
        outchar = char
        
        # XML/XML Comment begins
        if (counter + 3 < len(input_array) and 
            char == "<" and 
            input_array[counter+1] == "!" and 
            input_array[counter+2] == "-" and 
            input_array[counter+3] == "-"):
            comments_ind += 1
            outchar = char
        # Treat java script as comments so that they are kept untouched
        elif (not xml_doc_ind and 
              counter + 6 < len(input_array) and 
              char == "<" and 
              input_array[counter+1].lower() == "s" and 
              input_array[counter+2].lower() == "c" and 
              input_array[counter+3].lower() == "r" and 
              input_array[counter+4].lower() == "i" and 
              input_array[counter+5].lower() == "p" and 
              input_array[counter+6].lower() == "t"):
            comments_ind += 1
            outchar = char

        elif not mark_up_ind and not comments_ind:
            if char == "\n":
                outchar = " <__ANUBADOK__LINE__BREAK__> "
            elif char == "\t":
                outchar = " <__ANUBADOK__TAB__> "
            elif char == "<":
                mark_up_ind = 1
                outchar = empty_sent + " " + anu_remove + " " + char
        else:
            if comments_ind:
                if (counter >= 2 and 
                    char == ">" and 
                    input_array[counter-1] == "-" and 
                    input_array[counter-2] == "-"):
                    comments_ind -= 1
                elif (counter >= 7 and 
                      input_array[counter-7] == "/" and 
                      input_array[counter-6].lower() == "s" and 
                      input_array[counter-5].lower() == "c" and 
                      input_array[counter-4].lower() == "r" and 
                      input_array[counter-3].lower() == "i" and 
                      input_array[counter-2].lower() == "p" and 
                      input_array[counter-1].lower() == "t" and 
                      char == ">"):
                    comments_ind -= 1
                elif char == ">":
                    outchar = "__ANUBADOK__GT__"
                elif char == "<":
                    outchar = "__ANUBADOK__LT__"

            if char == " ":
                outchar = "__ANUBADOK__SPACE__"
            elif char == "\t":
                outchar = "__ANUBADOK__TAB__"
            elif char == "\n":
                outchar = "__ANUBADOK__LINE__BREAK__"

            if char == ">" and mark_up_ind and not comments_ind:
                mark_up_ind = 0
                outchar = char + " " + anu_remove + " " + empty_sent

        output_array.append(outchar)
        counter += 1

    return "".join(output_array)

def sanitise(string):
    # Original Perl code had commented-out sanitization steps
    # Here's the Python equivalent of what was commented out:
    
    # string = string.translate(str.maketrans('\x91\x92\x93\x94\x96\x97', "''\"\"--"))
    # string = re.sub(r'\x85', '...', string)
    # string = string.translate({i: None for i in range(0x80, 0xA0)})
    
    # These are my hack
    # string = string.replace('\xA3', 'yo')
    # string = string.replace('\xB2', '')
    # string = string.replace('\xF4', 'o')
    # string = string.replace('\xF6', 'o')
    # string = string.replace('\xFC', 'u')
    
    return string

def xml_post_processor(*args):
    input_string = "".join(args)
    input_string = input_string.rstrip('\n')

    input_string = input_string.replace('<__ANUBADOK__LINE__BREAK__>', '\n')
    input_string = input_string.replace('<__ANUBADOK__TAB__>', '\t')

    input_string = input_string.replace('__ANUBADOK__LINE__BREAK__', '\n')
    input_string = input_string.replace('__ANUBADOK__SPACE__', ' ')
    input_string = input_string.replace('__ANUBADOK__TAB__', '\t')
    input_string = input_string.replace('__ANUBADOK__GT__', '>')
    input_string = input_string.replace('__ANUBADOK__LT__', '<')
    
    input_string = re.sub(r' :', ':', input_string)
    
    # input_string = re.sub(r'" ', '"', input_string)
    # input_string = re.sub(r' "', '"', input_string)
    
    input_string = re.sub(r'\( ', '(', input_string)
    input_string = re.sub(r' \)', ')', input_string)
    
    input_string = re.sub(r'\[ ', '[', input_string)
    input_string = re.sub(r' \]', ']', input_string)
    
    # input_string = re.sub(r'> >', '>>', input_string)
    # input_string = re.sub(r' <', '<', input_string)
    
    return input_string

