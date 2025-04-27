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


import os
import sys
from pathlib import Path
from anubadok import settings


class UserSettings:
    verbose = False
    save_new_words_list = False


def check_user_anubadok_dir():
    """
    Check whether .anubadok dir exists if not create it.
    Also checks/creates user settings file.
    
    Args:
        user_anubadok_dir: Path to user's .anubadok directory
        user_settings_py: Path to user's settings file
    """
    user_anubadok_dir = settings.user_anubadok_dir
    user_settings_py = settings.user_settings_py

    # Create Path objects for easier path handling
    user_dir = Path(user_anubadok_dir)
    settings_file = Path(user_settings_py)
    
    if user_dir.exists():
        if not settings_file.exists():
            create_user_settings_py(user_anubadok_dir, user_settings_py)
    else:
        user_dir.mkdir(parents=True, exist_ok=True)
        create_user_settings_py(user_anubadok_dir, user_settings_py)

def create_user_settings_py(user_anubadok_dir: str, user_settings_py: str):
    """
    Create User Settings Python file
    
    Args:
        user_anubadok_dir: Path to user's .anubadok directory
        user_settings_py: Path to user's settings file
    """
    print("\n" + "_"*60 + "\n", file=sys.stderr)
    print(f'User specific configuration file "{user_settings_py}"', file=sys.stderr)
    print("is created. You can edit these settings later.", file=sys.stderr)
    print("_"*60 + "\n", file=sys.stderr)

    # Ensure directory exists
    Path(user_anubadok_dir).mkdir(parents=True, exist_ok=True)

    # Create settings file
    settings_content = '''# -*- coding: utf-8 -*-
#___________________________________________________________________
#
# This module specifies user specific configurations for "Anubadok"
#___________________________________________________________________

verbose = True
save_new_words_list = True

# To use TreeTagger as PoS tagger for Anubadok uncomment the following
# penn_treebank_tagger = "tree-tagger-english"

#___________________________________________________________________
# 
# Don't change anything below
#___________________________________________________________________
'''

    try:
        with open(user_settings_py, 'w', encoding='utf-8') as f:
            f.write(settings_content)
    except IOError as e:
        raise IOError(f"Error!! Couldn't open {user_settings_py} for writing!!") from e

