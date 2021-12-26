import csv 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize,pos_tag



nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

output = {'budget': '1', 'desc': 'fashion'}


budget = output["budget"]
budget = output["desc"]

def findCity(budget,userDesc):

  #Functions
  def preprocess(words):
    # Finds the root/stem of the word
    # Ex. connecting - > connect
    wordNet = WordNetLemmatizer()
    # Puts everything back together, back into a string
    lemWords = ""
    for token,tag in pos_tag(word_tokenize(words)):
        pos=tag[0].lower()
        
        if pos not in ['a', 'r', 'n', 'v']:
            pos='n'
        lemWords += " " + wordNet.lemmatize(token,pos)
    
    return lemWords
  

  vect = TfidfVectorizer(stop_words="english")
  toler = 0.1

  areaDict = {}

  userDesc = vect.fit_transform([preprocess(userDesc)])

  with open("costs.csv", 'rb') as dummy: 
    dataReader = csv.reader(dummy)

    # avoids labels
    next(dataReader)

    for data in dataReader: 
    
      desc = vect.transform([preprocess(data[2])])
    
      sim = cosine_similarity(userDesc,desc)

      if sim >= toler:
        areaDict[data[0]] = data[1]
      
       # key: name
        # value: average price
      #next loop through dictionary values and find the price thats closest to budget

    minAbs = 999999999
    curCity = None
    for i,j in areaDict.items():
      if abs(budget-int(j))<minAbs:
        curCity = i
        minAbs = abs(budget-int(j))
    return(curCity)

findCity()


