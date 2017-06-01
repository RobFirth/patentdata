# -*- coding: utf-8 -*-
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
import string

# Extend these stopwords to include patent stopwords
ENG_STOPWORDS = stopwords.words('english')

REGEX_US_APPLICATION = r"\d{2}\/\d{3}(,|\s)\d{3}"
REGEX_US_GRANT = r"\d(,|\s)\d{3}(,|\s)\d{3}"
REGEX_PCT_APPLICATION = r"PCT\/[A-Z]{2}\d{2,4}\/\d{5,6}"

PRINTABLE_CHAR_MAP = {c: i for i, c in enumerate(string.printable[:-2])}
REVERSE_PRINT_CHAR_MAP = {i: c for i, c in enumerate(string.printable[:-2])}


def check_list(listvar):
    """Turns single items into a list of 1."""
    if not isinstance(listvar, list):
        listvar = [listvar]
    return listvar


def safeget(dct, *keys):
    """ Recursive function to safely access nested dicts or return None.
    param dict dct: dictionary to process
    param string keys: one or more keys"""
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
    return dct


def remove_non_words(tokens):
    """ Remove digits and punctuation from text. """
    # Alternative for complete text is re.sub('\W+', '', text)
    return [w for w in tokens if w.isalpha()]


def remove_stopwords(tokens):
    """ Remove stopwords from tokens. """
    return [w for w in tokens if w not in ENG_STOPWORDS]


def stem(tokens):
    """ Stem passed text tokens. """
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in tokens]


def lemmatise(tokens_with_pos):
    """ Lemmatise tokens using pos data. """
    pass


def stem_split(tokens):
    """ Takes a list of tokens and splits stemmed tokens into
    stem, ending - inserting ending as extra token.

    returns: revised (possibly longer) list of tokens. """
    stemmer = PorterStemmer()
    token_list = list()
    for token in tokens:
        stem = stemmer.stem(token)
        split_list = token.split(stem)
        if token == stem:
            token_list.append(token)
        elif len(split_list) > 1:
            token_list.append(stem)
            token_list.append(split_list[1])
        else:
            token_list.append(split_list[0])
    return token_list


def capitals_process(tokens):
    """ Process a list of tokens and lower case.

    Adds a new <CAPITAL> token before a capitalised word to
    retain capital information."""
    token_list = list()
    for token in tokens:
        if token:
            if token[0].isupper():
                capital_token = "_CAPITAL_"
                if len(token) > 1:
                    if token[1].isupper():
                        capital_token = "_ALL_CAPITAL_"
                token_list.append(capital_token)
            if token[0] is not "_" and token[-1] is not "_":
                token_list.append(token.lower())
            else:
                token_list.append(token)
    return token_list


def punctuation_split(tokens):
    """ Split hyphenated and slashed tokens into words. """
    token_list = list()
    for token in tokens:
        # Keep and/or as special high frequency token
        if "/" in token and token is not "and/or":
            parts = token.split("/")
            for i, part in enumerate(parts):
                token_list.append(part)
                if i < (len(parts) - 1):
                    token_list.append("or")
        # Replace other non-alpha characters with space then split
        elif "-" in token:
            for part in token.split("-"):
                token_list.append(part)
        elif "—" in token:
            for part in token.split("—"):
                token_list.append(part)
        else:
            token_list.append(token)
            # token = "".join(
            # [c if c.isalnum() else " " for c in token]
            # )
            # for substrings in token.split(" "):
            # token_list.append(substrings)
    return token_list


def replace_patent_numbers(text):
    """ Replace patent number with _PATENT_NO_. """
    regex = r"({0}|{1}|{2})".format(
        REGEX_US_APPLICATION,
        REGEX_US_GRANT,
        REGEX_PCT_APPLICATION
        )
    m = re.sub(regex, "_PATENT_NO_", text)
    return m


def string2int(text, filter_printable=True):
    """ Convert text of document into a list of integers representing
    its characters.

    If filter_printable is true limit to 98 printable characters."""
    if filter_printable:
        ints = [
            ord(c) if c in string.printable[:-2] else ord(" ")
            for c in text
            ]
    else:
        ints = [ord(c) for c in text]
    return ints


def string2printint(text):
    """ Convert a string into a list of integers representing
    its printable characters."""
    return [
        PRINTABLE_CHAR_MAP[c]
        if c in PRINTABLE_CHAR_MAP.keys()
        else PRINTABLE_CHAR_MAP[" "]
        for c in text
    ]


def printint2string(doc_as_ints):
    """ Reconstruct document string from list of integers."""
    return "".join([REVERSE_PRINT_CHAR_MAP[i] for i in doc_as_ints])