# Anubadok: The Bengali Machine Translator  

[![License: GPL](https://img.shields.io/badge/License-GPL-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Anubadok is an open-source English to Bengali machine translator that uses Penn Treebank annotation system for natural language processing.

**This GitHub version is a python port of Anubadok's original Perl version written during 2005-2008**

## Motivations  
The project began with the idea of making manual translation of PO files (Portable Object files) 
faster—essential for local language computation. 

While initially focused on PO files, its scope expanded to broader applications, such as 
translating Wikipedia content. As a Sanskrit-derived language, Bengali has structural advantages 
for machine synthesis of sentences. In its current state, Anubadok can handle preliminary 
translations reasonably well, allowing volunteers to focus on manual editing.

## Architecture  
This GitHub version is written Python (and ported from the original Perl codes). The Anubadok system uses the Penn Treebank 
annotation system for natural language processing. It supports multiple input types:  
- Plain text files  
- XML documents  
- HTML files with inline JavaScript/CSS  

Translated outputs are written as Unicode-encoded Bengali texts.

## Documentation  
- **[A Brief Introduction to Anubadok (PDF)](docs/anubadok-in-brief.pdf)**  
  Explains the internal workings and algorithms with example sentences.  

## Dependencies
To run Anubadok, you must have the following PoS tagger installed and available in your system's PATH
- **[GPoSTTL Parts-of-Speech tagger](https://github.com/golam-m-hossain/gposttl)** 


## Running Anubadok  
Run locally without installation:  
1. Download the source code.  
2. Navigate to the package directory:
   
   ```bash
   echo "I love you." | ./scripts/anubadok.py
   ```
Output will appear in Unicode Bengali.   

## Running Test Suites of Anubadok

To run all available test suites, use the following command:

  ```bash
  ./scripts/run_anubadok_test_suite.py
  ```
To run a particular test suite, specify it as a command-line argument. For example:

  ```bash
  ./scripts/run_anubadok_test_suite.py tests/first_person_tenses_active.xml
  ```


## License
This project is licensed under the GNU General Public License v2+ - see the **[LICENSE](LICENSE)** file for details.


## Author & Contact

**Golam Mortuza Hossain**   (gmhossain at gmail dot com)  [Personal Webpage](https://www.iiserkol.ac.in/~ghossain/)
