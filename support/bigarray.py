import os, sys, zlib, itertools, tempfile

try:
    import _pickle as picle
except:
    import pickle
    

from core.exceptions import AnkabSystemException
from .enums import MKStempPrefix
from .settings import BIGARRAY_CHUNK_SIZE, BIGARRAY_COMPRESS_LEVEL