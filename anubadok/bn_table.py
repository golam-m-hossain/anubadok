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


class BnTable:
    """
    Class containing all Bengali language tables and constants
    """
    
    # Misc. Table
    bn_word_te = 'তে'
    bn_word_ache = "আছে"
    bn_word_chilo = "ছিল"
    bn_word_thakbe = 'থাকবে'
    bn_word_na = 'না'
    bn_word_nei = 'নেই'
    bn_word_ni = 'নি'
    bn_word_ti = "টি"
    bn_word_gulo = "গুলি"
    bn_word_er = "ের"
    bn_word_ki = " কি"
    bn_word_a_jai_ni = "া যায় নি"
    bn_object_suffix = "কে"
    bn_subject_hhh_suffix = "ের"

    # Bengali conjunction Table
    bn_conjunction_table = {
        'neither': 'না',
        'nor': 'না',
        'either': 'হয়',
        'or': 'অথবা',
        'and': 'এবং'
    }

    # Adverb Negation Table
    bn_adverb_negation_table = {
        'no': 'না',
        'not': 'না'
    }

    bn_adverb_negation_person_table = {
        1: 'নই',
        2: 'নন',
        3: 'নয়'
    }

    # Have had, will have Table
    bn_hhh_word_table = {
        'present': {
            'have': "রয়েছে",
            'have.to': "হবে"
        },
        'past': {
            'have': "ছিল",
            'have.to': "হয়েছিল"
        },
        'future': {
            'have': 'থাকবে',
            'have.to': 'হবে'
        }
    }

    bn_hhh_word_negation_table = {
        'present': {'have': 'নেই'},
        'past': {'have': 'ছিলনা'},
        'future': {'have': 'থাকবেনা'}
    }

    # Modal hhh verb Table: Active Sentences
    modal_hhh_table_active = {
        'present': {
            'should': 'থাকা উচিত',
            'can': 'থাকতে পারে',
            'may': 'থাকতে পারে',
            'might': 'থাকতে পারে',
            'could': 'থাকতে পারে'
        },
        'past': {
            'should': 'থাকা উচিত ছিল',
            'can': 'থাকতে পারে',
            'may': 'থাকতে পারে',
            'might': 'থাকতে পারে',
            'could': 'থাকতে পারে'
        },
        'future': {
            'should': 'থাকা উচিত'
        }
    }

    modal_hhh_table_active_negation = {
        'present': {
            'should': 'থাকা উচিত নয়',
            'may': 'থাকতে নাও পারে'
        },
        'past': {
            'should': 'থাকা উচিত হয়নি',
            'may': 'থাকতে নাও পারে'
        },
        'future': {
            'should': 'থাকা উচিত নয়'
        }
    }

    # Modal verb Table: Active Sentences
    modal_verb_table_1_active = {
        'can': 'তে পার',
        'may': 'তে পার',
        'could': 'তে পার',
        'might': 'তে পার'
    }

    modal_verb_table_1_active_negation = {
        'may': 'তে নাও পার',
        'might': 'তে নাও পার'
    }

    modal_verb_table_2_active = {
        's': {
            'should': 'া উচিত',
            'ought': 'া উচিত',
            'must': 'া উচিত'
        },
        'c': {
            'should': 'া উচিত',
            'ought': 'া উচিত',
            'must': 'া উচিত'
        },
        'p': {
            'should': 'া উচিত ছিল',
            'ought': 'া উচিত ছিল',
            'must': 'া উচিত ছিল'
        },
        'pc': {
            'should': 'া উচিত ছিল',
            'ought': 'া উচিত ছিল',
            'must': 'া উচিত ছিল'
        }
    }

    modal_verb_table_2_active_negation = {
        's': {
            'should': 'া উচিত নয়',
            'ought': 'া উচিত নয়',
            'must': 'া উচিত নয়'
        },
        'c': {
            'should': 'া উচিত নয়',
            'ought': 'া উচিত নয়',
            'must': 'া উচিত নয়'
        },
        'p': {
            'should': 'া উচিত হয়নি',
            'ought': 'া উচিত হয়নি',
            'must': 'া উচিত হয়নি'
        },
        'pc': {
            'should': 'া উচিত হয়নি',
            'ought': 'া উচিত হয়নি',
            'must': 'া উচিত হয়নি'
        }
    }

    # Modal verb: Passive Table
    modal_verb_table_passive = {
        's': {
            'can': 'া যাবে',
            'may': 'া হয়ত যাবে',
            'could': 'া যাবে',
            'might': 'া যাবে',
            'should': 'া উচিত',
            'ought': 'া উচিত',
            'must': 'া উচিত'
        },
        'c': {
            'can': 'া যাবে',
            'may': 'া হয়ত যাবে',
            'could': 'া যাবে',
            'might': 'া যাবে',
            'should': 'া উচিত',
            'ought': 'া উচিত',
            'must': 'া উচিত'
        },
        'p': {
            'can': 'া যেত',
            'may': 'া যেত',
            'could': 'া যেত',
            'might': 'া যেত',
            'should': 'া উচিত ছিল',
            'ought': 'া উচিত ছিল',
            'must': 'া উচিত ছিল'
        },
        'pc': {
            'can': 'া যেত',
            'may': 'া যেত',
            'could': 'া যেত',
            'might': 'া যেত',
            'should': 'া উচিত ছিল',
            'ought': 'া উচিত ছিল',
            'must': 'া উচিত ছিল'
        }
    }

    modal_verb_table_passive_negation = {
        's': {
            'should': 'া উচিত নয়',
            'ought': 'া উচিত নয়',
            'must': 'া উচিত নয়'
        },
        'c': {
            'should': 'া উচিত নয়',
            'ought': 'া উচিত নয়',
            'must': 'া উচিত নয়'
        },
        'p': {
            'should': 'া উচিত হয়নি',
            'ought': 'া উচিত হয়নি',
            'must': 'া উচিত হয়নি'
        },
        'pc': {
            'should': 'া উচিত হয়নি',
            'ought': 'া উচিত হয়নি',
            'must': 'া উচিত হয়নি'
        }
    }

    # Preposition Tables
    bn_preposition_table_1 = {
        'of': 'ের',
        'on': 'ে',
        'into': 'ের দিকে',
        'in.to': 'ের দিকে',
        'with': 'ের সঙ্গে',
        'than': 'ের চেয়ে',
        'from': ' থেকে',
        'towards': 'ার প্রতি',
        'at': 'তে',
        'against': 'ের বিরুদ্ধে',
        'about': 'ের সম্বন্ধে',
        'like': 'ের মত',
        'similar.to': 'ের মত',
        'unlike': 'ের মত নয়',
        'despite': ' সত্ত্বেও',
        'in.spite.of': ' সত্ত্বেও',
        'in': 'তে',
        'as': ' হিসেবে',
        'not.to': 'তে',
        'to': 'তে',
        'for': 'ের জন্য',
        'by': 'ের মধ্যে',
        'by_nn': 'ের দ্বারা',
        'consist.of': 'ের দ্বারা গঠিত',
        'between': 'ের মধ্যে',
        'under': 'ের অধীনে',
        'below': 'ের নিচে',
        'since': ' থেকে',
        'while': 'ার সময়',
        'whilst': 'ার সময়',
        'in.case.of': 'ার সময়',
        'before': 'ার পূর্বে',
        'inside': 'ের ভেতরে',
        'outside': 'ের বাইরে',
        'near': 'ের কাছে',
        'during': 'ের সময়',
        'amid': 'ের মধ্যে',
        'within': 'ের মধ্যে',
        'among': 'ের মধ্যে',
        'amongst': 'ের মধ্যে',
        'onto': 'ের ওপর',
        'on.to': 'ের ওপর',
        'on.top.of': 'ের ওপর',
        'over': 'ের ওপর',
        'upon': 'ের ওপর',
        'above': 'ের ওপর',
        'alongside': 'ের পাশাপাশি',
        'around': 'ের ধারেকাছে',
        'through': 'ের মধ্য দিয়ে',
        'beyond': 'ের পরেও',
        'till': ' পর্যন্ত',
        'until': ' পর্যন্ত',
        'up.to': ' পর্যন্ত',
        'after': 'ের পরে',
        'behind': 'ের পেছনে',
        'across': ' জুড়ে',
        'via': ' হয়ে',
        'throughout': ' জুড়ে',
        'without': ' ব্যতীত',
        'with.no': ' ব্যতীত',
        'along': ' বরাবর',
        'due.to': 'ের দরুন',
        'according.to': ' অনুসারে',
        'accord.to': ' অনুসারে',
        'in.accordance.with': ' অনুযায়ী',
        'besides': ' ছাড়াও',
        'in.addition.to': 'ের সাথে',
        'about.to': 'তে চলেছে',
        'including': ' সহ',
        'using': ' ব্যবহার করে',
        'by.means.of': ' ব্যবহার করে',
        'by.mean.of': ' ব্যবহার করে',
        'because.of': 'ের কারণে',
        'with.respect.to': 'ের সাপেক্ষে',
        'in.front.of': 'ের সামনে',
        'instead.of': 'ের পরিবর্তে',
        'in.lieu.of': 'ের পরিবর্তে',
        'in.place.of': 'ের পরিবর্তে',
        'on.behalf.of': 'ের পক্ষ থেকে',
        'on.account.of': 'ের পরিপ্রেক্ষিতে',
        'ahead.of': 'ের আগে',
        'aside.from': ' ছাড়া'
    }

    bn_preposition_table_2 = {
        'so': 'সুতরাং',
        'to_from': 'থেকে',
        'that': 'যে',
        'if': 'যদি',
        'then': 'যখন',
        'although': 'যদিও',
        'though': 'যদিও',
        'whereas': 'কিন্তু অন্যদিকে',
        'albeit': 'যদিও',
        'because': 'কারণ',
        'per': 'প্রতি',
        'unless': 'যদি না',
        'once': 'একবার',
        'ago': 'আগে',
        'such.as': 'যেমন',
        'about_approx': 'প্রায়',
        'as.well.as': 'ও',
        'as.far.as': 'যতদূর',
        'the': ' '
    }

    bn_preposition_table_3 = {
        'whether': ' কিনা'
    }

    bn_preposition_negation_table = {
        'not.to': 'না'
    }

    # Determiner tables
    bn_determiner_table_1 = {
        'a': 'একটি',
        'an': 'একটি',
        'the': ' ',
        'this': 'এই',
        'that': 'সেই',
        'these': 'এই',
        'those': 'সেই',
        'some': 'কিছু',
        'every': 'প্রতি'
    }

    bn_determiner_suffix_table_1 = {
        'a': '',
        'an': '',
        'the': ' ',
        'this': 'টি',
        'that': 'টি',
        'these': 'গুলি',
        'those': 'গুলি',
        'some': '',
        'every': ''
    }

    bn_determiner_table_2 = {
        'no': 'কোনও',
        'no.such': 'তেমন কোনও',
        'neither': 'কোনও',
        'no.longer': 'আর',
        'no.more': 'আর'
    }

    bn_determiner_suffix_table_2 = {
        'no': 'না',
        'no.such': 'নেই',
        'neither': 'না',
        'no.longer': 'না',
        'no.more': 'না'
    }

    bn_determiner_table_3 = {}

    # Person table
    person_table = {
        'i': 1,
        'me': 1,
        'my': 3,
        'mine': 1,
        'we': 1,
        'us': 1,
        'you': 2,
        'he': 3,
        'she': 3,
        'him': 3,
        'his': 3,
        'her': 3,
        'they': 3,
        'them': 3,
        'it': 3,
        'our': 3,
        'your': 3,
        'their': 3,
        "let's": 1,
        'lets': 1
    }

    # Punctuation table
    bn_punctuation_table = {
        '.': '।',
        '?': '?',
        '!': '!'
    }

    # Auxiliary verb tables
    bn_aux_verb_table = {
        1: {
            'am': ' ',
            'is': ' ',
            'are': 'আছি',
            'was': 'ছিলাম',
            'were': 'ছিলাম',
            'will': 'থাকব',
            'shall': 'থাকব'
        },
        2: {
            'are': ' ',
            'is': ' ',
            'were': 'ছিলেন',
            'will': 'থাকবেন',
            'shall': 'থাকবেন'
        },
        3: {
            'is': ' ',
            'are': 'আছে',
            'was': 'ছিল',
            'were': 'ছিল',
            'will': 'থাকবে',
            'shall': 'থাকবে'
        }
    }

    bn_aux_verb_negation_table = {
        1: {
            'am': 'নই',
            'are': 'নই',
            'was': 'ছিলাম না',
            'were': 'ছিলাম না',
            'will': 'থাকব না',
            'shall': 'থাকব না'
        },
        2: {
            'are': 'নন',
            'were': 'ছিলেন না',
            'will': 'থাকবেন না',
            'shall': 'থাকবেন না'
        },
        3: {
            'is': 'নয়',
            'are': 'নয়',
            'was': 'ছিলনা',
            'were': 'ছিলনা',
            'will': 'থাকবে না',
            'shall': 'থাকবে না'
        }
    }

    # Existential there tables
    bn_ex_aux_verb_table = {
        'present': {
            'is': 'আছে',
            'are': 'আছে'
        }
    }

    bn_ex_aux_verb_negation_table = {
        'present': {
            'is': 'নেই',
            'are': 'নেই'
        }
    }

    # Be as main verb tables
    be_as_mainverb_table = {
        1: {
            'present': ' ',
            'past': 'ছিলাম',
            'future': 'হব'
        },
        2: {
            'present': ' ',
            'past': 'ছিলেন',
            'future': 'হবেন'
        },
        3: {
            'present': ' ',
            'past': 'ছিল',
            'future': 'হবে'
        }
    }

    be_as_mainverb_negation_table = {}

    # Verb suffix tables for passive sentences
    verb_suffix_table_passive = {
        'present': {
            's': 'া হয়',
            'c': 'া হচ্ছে',
            'p': 'া হয়েছে',
            'pc': 'া হচ্ছে'
        },
        'past': {
            's': 'া হয়েছিল',
            'c': 'া হচ্ছিল',
            'p': 'া হয়েছিল',
            'pc': 'া হচ্ছিল'
        },
        'future': {
            's': 'া হবে',
            'c': 'া হবে',
            'p': 'া হবে',
            'pc': 'া হবে'
        }
    }

    verb_suffix_table_passive_negation = {
        'present': {'p': 'া হয়নি'},
        'past': {
            's': 'া হয়নি',
            'p': 'া হয়নি'
        }
    }

    # Verb modifier tables for active sentences
    verb_mod_table_active = {
        1: {
            'present': {
                's': 'ি',
                'c': 'ছি',
                'p': 'েছি',
                'pc': 'ছি'
            },
            'past': {
                's': 'েছিলাম',
                'c': 'ছিলাম',
                'p': 'েছিলাম',
                'pc': 'ছিলাম'
            },
            'future': {
                's': 'ব',
                'c': 'ব',
                'p': 'ব',
                'pc': 'ব'
            }
        },
        2: {
            'present': {
                's': 'েন',
                'c': 'ছেন',
                'p': 'েছেন',
                'pc': 'ছেন'
            },
            'past': {
                's': 'েছিলেন',
                'c': 'ছিলেন',
                'p': 'েছিলেন',
                'pc': 'ছিলেন'
            },
            'future': {
                's': 'বেন',
                'c': 'বেন',
                'p': 'বেন',
                'pc': 'বেন'
            }
        },
        3: {
            'present': {
                's': 'ে',
                'c': 'ছে',
                'p': 'েছে',
                'pc': 'ছে'
            },
            'past': {
                's': 'েছিল',
                'c': 'ছিল',
                'p': 'েছিল',
                'pc': 'ছিল'
            },
            'future': {
                's': 'বে',
                'c': 'বে',
                'p': 'বে',
                'pc': 'বে'
            }
        }
    }

    verb_mod_table_active_formality_2 = 'ো'

    verb_mod_table_active_negation = {
        1: {
            'present': {'p': 'িনি'},
            'past': {
                's': 'িনি',
                'p': 'িনি'
            }
        },
        2: {
            'present': {
                's': 'েন না',
                'p': 'েননি'
            },
            'past': {
                's': 'েননি',
                'p': 'েননি'
            }
        },
        3: {
            'present': {'p': 'েনি'},
            'past': {
                's': 'েনি',
                'p': 'েনি'
            }
        }
    }

    # Pronoun tables
    pronoun_table = {
        'i': 'আমি',
        'me': 'আমাকে',
        'my': 'আমার',
        'mine': 'আমার',
        'we': 'আমরা',
        'our': 'আমাদের',
        'ours': 'আমাদের',
        'us': 'আমাদেরকে',
        'you': 'আপনি',
        'you_obj': 'আপনাকে',
        'your': 'আপনার',
        'he': 'সে',
        'she': 'সে',
        'him': 'তাকে',
        'his': 'তার',
        'her': 'তার',
        'they': 'তারা',
        'their': 'তাদের',
        'them': 'তাদেরকে',
        'myself': 'নিজে',
        'ourselves': 'নিজেরা',
        'yourself': 'নিজে',
        'yourselves': 'নিজেরা',
        'himself': 'নিজে',
        'herself': 'নিজে',
        'themselves': 'নিজেরা',
        'it': 'এইটি',
        'its': 'এর',
        'itself': 'নিজেরা',
        "let's": 'আসুন',
        'lets': 'আসুন',
        'each.other': 'একে অপরকে'
    }

    pronoun_active_to_modal_table = {
        'i': 'my',
        'we': 'our',
        'you': 'your',
        'he': 'his',
        'she': 'her',
        'they': 'their'
    }

    pronoun_active_to_passive_table = {
        'i': 'me',
        'we': 'us',
        'you': 'you_obj',
        'he': 'him',
        'she': 'him',
        'they': 'them',
        'me': 'my',
        'us': 'our',
        'you_obj': 'your',
        'him': 'his',
        'her': 'his',
        'them': 'their'
    }

    # WH-word tables
    wh_table_question = {
        'what': 'কি',
        'who': 'কে',
        'whom': 'কাকে',
        'whose': 'কার',
        'when': 'কখন',
        'which': 'কোন',
        'why': 'কেন',
        'where': 'কোথায়',
        'to.whom': 'কাকে',
        'that': 'যে',
        'whatever': 'সব কিছু',
        'how': 'কিভাবে',
        'how.to': 'হয় কিভাবে',
        'how.do': 'কিভাবে',
        'how.be': 'কেমন'
    }

    wh_table_relation = {
        'what': 'যার',
        'who': 'যে',
        'whom': 'যাকে',
        'whose': 'যার',
        'when': 'যখন',
        'which': 'যেটি',
        'why': 'জন্য',
        'where': 'যেখানে',
        'that': 'যে',
        'to.whom': 'যাকে',
        'whatever': 'সব কিছু',
        'how': 'যেমন',
        'how.much': 'কত',
        'how.long': 'কতক্ষন',
        'how.many': 'কতগুলি'
    }
    

