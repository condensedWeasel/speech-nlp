# Ideas
A place for documenting ideas

## Design Brief
- Produce a short presentation using the last three publically available speeches on AI, ML and Fintech
- Summarise the speeches using Data Science techniques
- 5 minutes to present back on your analysis and findings
- You are free to use any additional resources

## Notes
- Small data set (3 documents)
- .pdf format - requires pre-processing to extract raw text
- Brief mentions 3 topics - could be relavent for topic modelling?
- Use regular expressions to extract references, headings, etc?

## Summarisation Techniques

| Technology | Description | Time  | Notes |
| ---------- | ----------- | :---: | ----- | 
| Bag of words / TF-IDF | Token frequency analysis | Low | Pre-requisite for other techniques |
| Word cloud | Visualisation | Low | Useful for exploratory analysis of small data sets |
| Named entity recognition | Text pre-processing for identifying names / organisations / locations | Low | Useful for mining subject of text |
| Parts of speech tagging | Identifies the grammatical group of a given word (e.g. noun, verb) | Low | |
| Lemmatization | Find root words (lemma / dictionary form) from inflected form | Low | May be useful for presentation / visualisation, "nicer looking" compared to stemming techniques |
| Topic modelling | Unsupervised ML technique for extracting topics from documents | Medium | May not be applicable for small data sets |
| Sentiment Analysis | Derive sentiment score / label for given text | Medium | Relevancy? |
| Extractive  Summarisation | Identfy key phrases & extract from document | High | TextRank? |
| Abstractive  Summarisation | Generates new sentences based on original document using deep learning | High | Requires pre-trained model (RNN, LSTM, Transformers) |


## Tools
| Description | URL |
| ----------- | --- | 
| PDF extraction library | https://github.com/euske/pdfminer/ |
| Natural language toolkit | https://www.nltk.org/ |
| SpaCy | https://spacy.io/ |

## References

| Description | URL |
| ----------- | --- |
| PDF extraction example | https://towardsdatascience.com/pdf-preprocessing-with-python-19829752af9f |
| Text rank summarisation | https://www.analyticsvidhya.com/blog/2018/11/introduction-text-summarization-textrank-python/ |
| Transformer summarisation | https://towardsdatascience.com/summarization-has-gotten-commoditized-thanks-to-bert-9bb73f2d6922 |


