from enum import Enum

class QueryType(Enum):
    thing=1
    time=2
    location=3
    reason=4

class WordType(Enum):
    thing=1
    time=2
    location=3
    reason=4
    noun=5
    verb=6
    noise=7