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
import random
import subprocess

from anubadok import settings

###########################################
#
#  Parts of Speech Tagger handling
#
###########################################

POSTAGGER_VERSION = "GPoSTTL 0.9.6git"

def penn_treebank_tagger(text):
    """
    Calls the Penn Treebank tagger on the input text.
    
    Args:
        text: The text to be tagged
        anubadok_tmp_dir: Directory for temporary files (from Settings)
        penn_treebank_tagger_path: Path to the tagger executable (from Settings)
        
    Returns:
        The tagged output as a string
        
    Raises:
        IOError: If temp file cannot be created or tagger cannot be executed
    """
    anubadok_tmp_dir = settings.anubadok_tmp_dir
    penn_treebank_tagger_path = settings.penn_treebank_tagger

    # Create a temporary file with random name
    tmp_file = os.path.join(
        anubadok_tmp_dir,
        f"_{random.randint(0, 100000)}_tmp_tagger_input_file"
    )
    
    try:
        # Write the input text to the temp file
        with open(tmp_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        # Call the tagger and capture its output
        result = subprocess.run(
            [penn_treebank_tagger_path, tmp_file],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Clean up the temp file
        try:
            os.unlink(tmp_file)
        except:
            pass
        
        return result.stdout
        
    except subprocess.CalledProcessError as e:
        # Clean up temp file if it exists
        try:
            os.unlink(tmp_file)
        except:
            pass
        raise IOError(
            f"Error! Penn Treebank tagger failed ({penn_treebank_tagger_path}). "
            f"Error: {e.stderr}"
        )
    except IOError as e:
        # Clean up temp file if it exists
        try:
            os.unlink(tmp_file)
        except:
            pass
        raise IOError(f"Error! Could not open temp file: {str(e)}")


