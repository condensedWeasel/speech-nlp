"""
summary.visualise Contains modules for visualising tokens from documents

Copyright 2020 Peter Dowell <p.g.dowell@gmail.com>
"""

from ._visualise import plot_histogram, plot_wordcloud, count_document_tokens, count_tokens, highlight_entities, count_entities, highlight_str

__all__ = ['plot_histogram', 'plot_wordcloud', 'count_document_tokens', 'count_tokens', 'highlight_entities', 'count_entities', 'highlight_str']