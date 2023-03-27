import pandas as pd
import spacy
import gensim
from gensim import corpora
from textblob import TextBlob
import nltk

nltk.download('stopwords')
# Load stop words
stop_words = set(nltk.corpus.stopwords.words('english'))

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Read CSV file into dataframe
df = pd.read_csv("okcupid_profiles.csv")

# Print dataframe
print(df.head())

def extract_polarity(text):
    # Create TextBlob object from input text
    blob = TextBlob(text)
    
    # Extract sentiment polarity from TextBlob object
    polarity = blob.sentiment.polarity

    return polarity

def extract_subjectivity(text):
    # Create TextBlob object from input text
    blob = TextBlob(text)
    
    # Extract sentiment subjectivity from TextBlob object
    subjectivity = blob.sentiment.subjectivity
    
    return subjectivity

def get_entities(text):
    if isinstance(text, str):
        doc = nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append(ent.text)
        return entities
    else:
        return None

# def extract_topics(docs):
#     num_topics = 2
#     # Tokenize documents
#     tokenized_docs = [doc.split() for doc in docs]
#     # Create dictionary from tokenized documents
#     dictionary = corpora.Dictionary(tokenized_docs)
#     # Create corpus from dictionary and tokenized documents
#     corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]
#     # Create LDA model from corpus and dictionary
#     lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, passes=10)
#     # Extract topics from LDA model
#     topics = lda_model.print_topics(num_words=5)
#     return topics

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

df2 = df.head(5)

df2["essay"] = df2["essay0"].astype(str) + df2["essay1"].astype(str) + df2["essay2"].astype(str)+df2["essay3"].astype(str) + df2["essay4"].astype(str) + df2["essay5"].astype(str)+df2["essay6"].astype(str) + df2["essay7"].astype(str) + df2["essay8"].astype(str)+df2["essay9"].astype(str)

# Drop original columns
df2.drop(columns=["essay0", "essay1", "essay2","essay3", "essay4", "essay5",
                    "essay6", "essay7", "essay8","essay9"], inplace=True)

df2['text'] = df2['essay'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

df2["essay_entities"] = df2["text"].apply(get_entities)
# df2["essay_topics"] = df2["text"].apply(extract_topics)
df2["essay_subjectivity"] = df2["text"].apply(extract_subjectivity)
df2["essay_polarity"] = df2["text"].apply(extract_polarity)

print(df2["essay_entities"])
# print(df2["essay_topics"])
print(df2["essay_subjectivity"])
print(df2["essay_polarity"])