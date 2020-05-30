"""
summary.model Contains modules for modelling data from documents

Copyright 2020 Peter Dowell <p.g.dowell@gmail.com>
"""

from ._textrank import KeywordTextRank, SentenceTextRank

__all__ = ['KeywordTextRank', 'SentenceTextRank']