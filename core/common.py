from __future__ import division

import binascii, codecs, contextlib, copy, functools, getpass, hashlib, inspect, io, json, keyword, locale, logging, ntpath, os, platform, posixpath, random, re, socket, string, subprocess, sys, tempfile, threading, time, types, unicodedata, zlib


from .data import cmdLineOptions, conf, kb, logger, paths
from .datatype import OrderedDict
from .dicts import DBMS_DICT, DEFAULT_DOC_ROOTS, DEPRECATED_OPTIONS, OBSOLETE_OPTIONS, SQL_STATEMENTS
from .enums import AdjustTimeDelay, CharsetType, ContentStatus, DBMS, Expected, HASHDBKeys, HeuristicTest, HTTPHeader, HTTPMethod, LoggingLevel, MKStempPrefix, OptionType, OS, Payload, Place, PostHint, ReflectiveCounter, SortOrder
from .exceptions import AnkabutBaseException, AnkabDataException, AnkabGenericException, AnkabInstallationException, AnkabMissingDependence, AnkabNoneDataException, AnkabSilentQuitException, AnkabSyntaxException, AnkabSystemException, AnkabUserQuitException, AnkabValueException

from .settings import (
    BANNER,
    BOLD_PATTERNS,
    BOUNDARY_BACKSLASH_MARKER,
    BOUNDED_INJECTION_MARKER,
    BRUTE_DOC_ROOT_PREFIXES,
    BRUTE_DOC_ROOT_SUFFIXES,
    BRUTE_DOC_ROOT_TARGET_MARK,
    BURP_REQUEST_REGEX,
    BURP_XML_HISTORY_REGEX,
    CRAWL_EXCLUDE_EXTENSIONS,
    CUSTOM_INJECTION_MARK_CHAR,
    DBMS_DIRECTORY_DICT,
    DEFAULT_COOKIE_DELIMITER,
    DEFAULT_GET_POST_DELIMITER,
    DEFAULT_MSSQL_SCHEMA,
    DEV_EMAIL_ADDRESS,
    DOLLAR_MARKER,
    DUMMY_USER_INJECTION,
    DYNAMICITY_BOUNDARY_LENGTH,
    ERROR_PARSING_REGEXES,
    EVALCODE_ENCODED_PREFIX,
    FILE_PATH_REGEXES,
    FORCE_COOKIE_EXPIRATION_TIME,
    FORM_SEARCH_REGEX,
    GENERIC_DOC_ROOT_DIRECTORY_NAMES,
    GIT_PAGE,
    GITHUB_REPORT_OAUTH_TOKEN,
    GOOGLE_ANALYTICS_COOKIE_REGEX,
    HASHDB_MILESTONE_VALUE,
    HOST_ALIASES,
    HTTP_CHUNKED_SPLIT_KEYWORDS,
    IGNORE_PARAMETERS,
    IGNORE_SAVE_OPTIONS,
    INFERENCE_UNKNOWN_CHAR,
    INJECT_HERE_REGEX,
    IP_ADDRESS_REGEX,
    ISSUES_PAGE,
    IS_TTY,
    IS_WIN,
    LARGE_OUTPUT_THRESHOLD,
    LOCALHOST,
    MAX_INT,
    MIN_ENCODED_LEN_CHECK,
    MIN_ERROR_PARSING_NON_WRITING_RATIO,
    MIN_TIME_RESPONSES,
    MIN_VALID_DELAYED_RESPONSE,
    NETSCAPE_FORMAT_HEADER_COOKIES,
    NULL,
    PARAMETER_AMP_MARKER,
    PARAMETER_SEMICOLON_MARKER,
    PARAMETER_PERCENTAGE_MARKER,
    PARTIAL_HEX_VALUE_MARKER,
    PARTIAL_VALUE_MARKER,
    PAYLOAD_DELIMITER,
    PLATFORM,
    PRINTABLE_CHAR_REGEX,
    PROBLEMATIC_CUSTOM_INJECTION_PATTERNS,
    PUSH_VALUE_EXCEPTION_RETRY_COUNT,
    PYVERSION,
    RANDOMIZATION_TLDS,
    REFERER_ALIASES,
    REFLECTED_BORDER_REGEX,
    REFLECTED_MAX_REGEX_PARTS,
    REFLECTED_REPLACEMENT_REGEX,
    REFLECTED_REPLACEMENT_TIMEOUT,
    REFLECTED_VALUE_MARKER,
    REFLECTIVE_MISS_THRESHOLD,
    SENSITIVE_DATA_REGEX,
    SENSITIVE_OPTIONS,
    STDIN_PIPE_DASH,
    SUPPORTED_DBMS,
    TEXT_TAG_REGEX,
    TIME_STDEV_COEFF,
    UNICODE_ENCODING,
    UNKNOWN_DBMS_VERSION,
    URI_QUESTION_MARKER,
    URLENCODE_CHAR_LIMIT,
    URLENCODE_FAILSAFE_CHARS,
    USER_AGENT_ALIASES,
    VERSION_COMPARISON_CORRECTION,
    VERSION_STRING,
    ZIP_HEADER,
    WEBSCARAB_SPLITTER,
)
from .bigarr import BigArray

from pkg import six
from pkg.clientform.clientform import ParseResponse, ParseError
from pkg.colorama.initialise import init as coloramainit
from pkg.magic import magic
from pkg.odict import OrderedDict
from pkg.six import unichr as _unichr
from pkg.termcolor.termcolor import colored
from pkg.six.moves import ( 
            collections_abc as _collections, 
            configparser as _configparser, 
            http_client as _http_client, 
            input as _input, 
            reload_module as _reload_module, 
            urllib as _urllib, 
            zip as _zip 
)
from difflib import SequenceMatcher
from math import sqrt
from optparse import OptionValueError
from xml.sax import parse, SAXParseException














