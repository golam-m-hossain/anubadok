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

#____________________________________________________________________
#
#                 Settings: System dependent
#____________________________________________________________________

primary_dict_db = "__PREFIX__/share/anubadok/bdict.db"
primary_dict_db = "./data/bdict.db"   # REMOVE THIS LINE during installation 
user_anubadok_dir = os.path.expanduser("~/.anubadok")
anubadok_tmp_dir = "."
penn_treebank_tagger = "gposttl"

#____________________________________________________________________
#
#            Settings: System independent
#____________________________________________________________________

# Add user directory to Python path
if user_anubadok_dir not in sys.path:
    sys.path.insert(0, user_anubadok_dir)

secondary_dict_db = os.path.join(user_anubadok_dir, "bdict.new.db")
user_dict_db = os.path.join(user_anubadok_dir, "bdict.user.db")
user_settings_py = os.path.join(user_anubadok_dir, "user_settings.py")
user_info_py = os.path.join(user_anubadok_dir, "user_info.py")

local_dict_db = os.path.join(anubadok_tmp_dir, "bdict.local.db")
new_words_list = os.path.join(anubadok_tmp_dir, "new_words.list")


