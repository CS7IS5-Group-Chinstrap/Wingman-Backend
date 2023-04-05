import pandas as pd
import spacy
import gensim
from gensim import corpora
from textblob import TextBlob
import nltk
from nltk.stem import WordNetLemmatizer
import re
import string

nltk.download('stopwords')
# Load stop words
stop_words = set(nltk.corpus.stopwords.words('english'))

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load punctuations
exclude_punctuations = string.punctuation

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

def local_testing():
    # Read CSV file into dataframe
    df = pd.read_csv("okcupid_profiles.csv")
    # Print dataframe
    print(df.head())

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

def clean_corpus(docs):
    lemmatizer = WordNetLemmatizer()
    # Clean the documents
    # Remove numericals
    docs = re.sub('[0-9]', '', docs)
    # Convert to lowercase and remove stop words
    docs = " ".join([ch for ch in docs.lower().split() if ch not in stop_words])
    # Remove special characters
    docs = "".join(ch for ch in docs if ch not in exclude_punctuations)
    # Lemmatize words
    docs = " ".join(lemmatizer.lemmatize(word) for word in docs.split())
    return docs
   
def extract_topics(tokenized_docs):
    num_topics = 3

    # Create dictionary from tokenized documents
    dictionary = corpora.Dictionary(tokenized_docs)

    # Create corpus from dictionary and tokenized documents
    corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

    # Create LDA model from corpus and dictionary
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=dictionary,
                                                num_topics=num_topics,
                                                passes=10,chunksize=100,
                                                random_state=100,
                                                eval_every=None,
                                                alpha='auto')

    # Extract topics from LDA model
    topics = lda_model.print_topics(num_words=5)

    # Print topic and words associated with each topic - can be commented out
    for index, topic in lda_model.show_topics(formatted=False, num_words= 5):
        print('Topic: {} \nWords: {}'.format(index, '|'.join([w[0] for w in topic])))

    # Extract dominant topic
    topics = []
    for i, row in enumerate(lda_model[corpus]):
        new_row = sorted(row, key=lambda x: x[1], reverse=True)
        for j, (topic_num, prop_topic) in enumerate(new_row):
            if j == 0:
                wp = lda_model.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                topics.append(topic_keywords)
            else:
                    break
    return topics

# Function that cleans the corpus and extracts dominant topics from easy - customized to user
def extract_topics_per_user(user_data):
    # Combine all the bio into one document
    essay = user_data['essay0'] + user_data['essay1'] + user_data['essay2'] + user_data['essay3'] + user_data['essay4'] + user_data['essay5'] + user_data['essay6'] + user_data['essay7'] + user_data['essay8'] + user_data['essay9']

    docs = clean_corpus(docs=essay)
    tokenized_docs = [[word for word in docs.split()]]
    topics = extract_topics(tokenized_docs=tokenized_docs)
    return topics