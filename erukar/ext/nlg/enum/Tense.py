from enum import Enum

class Tense(Enum):
    SimplePresent           = 0 # I _read_ every day
    SimplePast              = 1 # Last night, I _read_ a book
    SimpleFuture            = 2 # I _will read_ as much as I can
    PresentContinuous       = 3 # I _am reading_ at the moment
    PastContinuous          = 4 # I _was reading_ a book last night
    FutureContinuous        = 5 # I _will be reading_ another tonight
    PresentPerfect          = 6 # I _have read_ a lot of books
    PastPerfect             = 7 # I _had read_ at least 30 when I was a kid
    FuturePerfect           = 8 # I _will have read_ blah
    PresentPerfectContinous = 9 # I _have been reading_ since ... 
    PastPerfectContinous    = 10# I _had been reading_ for at least a year when
    FuturePerfectContinous  = 11# I _will have been reading_ 
