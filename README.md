# Anubadok: The Bengali Machine Translator  

[![License: GPL](https://img.shields.io/badge/License-GPL-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Anubadok is an open-source English to Bengali machine translator that uses Penn Treebank annotation system for natural language processing.

**This GitHub version is a python port of the original Perl version of Anubadok written during 2005-2008**

## Motivations  
The project began with the idea of making manual translation of PO files (Portable Object files) 
faster—essential for local language computation. 

While initially focused on PO files, its scope expanded to broader applications, such as 
translating Wikipedia content. As a Sanskrit-derived language, Bengali has structural advantages 
for machine sentence synthesis. In its feature-complete state, Anubadok can handle preliminary 
translations reasonably well, allowing volunteers to focus on manual editing.

## Architecture  
This GitHub version is Python (it was originally written in Perl). The Anubadok system uses the Penn Treebank 
annotation system for natural language processing. It supports multiple input types:  
- Plain text files  
- XML documents  
- HTML files with inline JavaScript/CSS  

Translated outputs are written as Unicode-encoded Bengali texts.

## Documentation  
- **[A Brief Introduction to Anubadok (PDF)](docs/anubadok-in-brief.pdf)**  
  Explains the internal workings and algorithms with example sentences.  
- **[Implementation Status]()**  
  Details current feature progress.  

## Running Anubadok  
Run locally without installation:  
1. Download the source code.  
2. Navigate to the package directory:  
   ```bash
   cd anubadok
   echo "I love you." | ./scripts/anubadok.py
   ```
Output will appear in Unicode Bengali.   
   
## License
This project is licensed under the GNU General Public License v2+ - see the **[LICENSE](LICENSE)** file for details.
