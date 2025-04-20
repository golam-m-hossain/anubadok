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


from anubadok.en_tools import match_pattern_and_modify_as_directed


def disambiguate_prepositions(sentence):
    """
    The function tries to disambiguate preposition meanings
    by understanding the context
    """
    
    # Match the pattern and modify them: about CD
    sentence = match_pattern_and_modify_as_directed(
        2, "\tIN\tabout", "\tCD\t", 
        "\tIN\tabout_approx", "__KEEP__", *sentence)

    # Match the pattern and modify them: by DT 
    sentence = match_pattern_and_modify_as_directed(
        2, "by\tIN\tby", "\tDT\t", 
        "by\tIN\tby_NN", "__KEEP__", *sentence)

    # Match the pattern and modify them:  CD TO CD 
    sentence = match_pattern_and_modify_as_directed(
        3, "\tCD\t", "\tTO\t", "\tCD\t", 
        "__KEEP__", "to_from\tIN\tto_from", "__KEEP__", *sentence)

    # Match the pattern and modify them: from NP TO NP
    sentence = match_pattern_and_modify_as_directed(
        4, "\t\tfrom", "\tNP\t", "\tTO\t", "\tNP\t", 
        "\tIGNR\t", "__KEEP__", "\tIN\tto_from", "__KEEP__", *sentence)

    # Match the pattern and modify them: NP TO NP
    sentence = match_pattern_and_modify_as_directed(
        3, "\tNP\t", "\tTO\t", "\tNP\t", 
        "__KEEP__", "\tIN\tto_from", "__KEEP__", *sentence)

    return sentence


