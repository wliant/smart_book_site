import spacy
import pandas as pd
import numpy as np


#Instructions
#1. Pre-Trained Spacy Model is loaded
#2. Aspect mining based on 3 categories
#3. Sentiment Classification for Review
#4. Integration: function to use: evaluate_review, need to doc = nlp(review) first. For some strange reason, cannot put into the evaluate_review function 

#Load Pre-Trained SPacy model
output_dir = "Output\my_nlp_sm"
my_nlp = spacy.load(output_dir)

nlp = spacy.load('en')

# entity & aspect categories
aspect = {"book": ["book"],
        "author" : ["author", "writer" ],
        "characters" : ["character","characters"]   }

def aspectCat(sentence):
    category=[]
    for tok in sentence:
        tok = tok.text.lower()
        for key, val in aspect.items():
            if tok in val: category.append(key)
    if len(category) == 0 : category.append("overall")
    return category

sent_map = {"positive":1, "neutral":0, "negative":-1}

def getSentiment(span):
    res = my_nlp(span.text)
    
    # map score from positive -> +1; negative -> -1; neutral -> 0
    senti = np.round(sum([sent_map[items[0]]*items[1] for items in res.cats.items()]),2)
    
    #print(res, senti)
    #print("-------------")
    return (res,senti)

def evaluate_review(review):
    cat_list=[]
    for idx, sentence in enumerate(review.sents):
            try:
                cat = aspectCat(sentence)      
                cat_list.append(cat)
            except IndexError:
                cat_list.append('overall')
    flat_cat_list = [item for sublist in cat_list for item in sublist]
    sentence, predicted_sentiment = getSentiment(review)
    categorized_sentiment  = 'netural'
    if predicted_sentiment>0:
        categorized_sentiment  = 'positive'
    elif predicted_sentiment<0:
        categorized_sentiment  = 'negative'
    return sentence,predicted_sentiment,categorized_sentiment,flat_cat_list

def evaluate_review_text(review_text):
    doc = nlp(review_text)
    evaluate_review(doc)