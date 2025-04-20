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

import sys
import argparse
from pathlib import Path

# Import the necessary
sys.path.insert(0, ".")
from anubadok import settings
from anubadok import initialize
from anubadok import xml_pp
from anubadok import pos_tagger
from anubadok import translator
import user_settings

def main():
    parser = argparse.ArgumentParser(description="Anubadok - The Bengali Machine Translator")
    parser.add_argument('-v', '--version', action='store_true', help='Print version information')
    parser.add_argument('-s', '--silent', '--quiet', action='store_true', 
                        help='Suppress non-essential console output')
    parser.add_argument('-d', '--debug', action='count', default=0,
                        help='Enable debugging (use multiple times for more detail)')
    parser.add_argument('input_file', nargs='?', help='Input file (default: STDIN)')
    
    args = parser.parse_args()

    if args.version:
        print(f"{translator.version}")
        sys.exit(0)
    
    if args.debug:
        translator.Translator.turn_on_debugging = args.debug

    input_source = sys.stdin
    input_type = "STDIN"

    if args.input_file:
        input_path = Path(args.input_file)
        if input_path.exists():
            try:
                input_source = open(input_path, 'r', encoding='utf-8')
                input_type = "FILE"
            except IOError as e:
                print(f"Error! Couldn't open \"{args.input_file}\"! Exiting.", file=sys.stderr)
                sys.exit(1)
        else:
            print(f"Error! Couldn't find \"{args.input_file}\"! Exiting.", file=sys.stderr)
            sys.exit(1)
    elif not args.silent:
        print("Reading from STDIN; (try: anubadok --help for usage or", file=sys.stderr)
        print("see manpage for details.)", file=sys.stderr)

    # Initialize
    initialize.check_user_anubadok_dir()
    
    # Read input
    input_content = input_source.read()
    if input_type == "FILE":
        input_source.close()
    
    # Process the content
    processed = xml_pp.xml_pre_processor(input_content)
    tagged = pos_tagger.penn_treebank_tagger(processed)
    translated = translator.translate_in_bengali(tagged)
    output = xml_pp.xml_post_processor(translated)
    
    print(output)

if __name__ == "__main__":
    main()

