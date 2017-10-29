
# coding: utf-8

# In[73]:

import requests
from bs4 import BeautifulSoup
import csv
import nltk, string
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet
from nltk.corpus import stopwords

url_home="https://www.bestbuy.com/site/samsung-galaxy-s8-64gb-unlocked-midnight-black/5803741.p?skuId=5803741"
url_review="https://www.bestbuy.com/site/reviews/samsung-galaxy-s8-64gb-unlocked-midnight-black/5803741"
score=[]
title=[]
date=[]
reviews=[]
le_words=[]
tok=[]
sentiment=[]
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


def sentiment_analysis(str):
    list1=getTokens(str)
    from nltk.corpus import stopwords
    stop_words = stopwords.words('english')
    #stop_words+=["film", "films"] #Application specific stop words
    #print (stop_words)
    filtered_list=[]
    for word in list1:
        if word not in stop_words:
            filtered_list.append(word)
    #filtered_dictionary={word: dictionary[word] for word in dictionary if word not in stop_words}
    #print("\nsort dictionary without stop words by frequency")
    #print(sorted(filtered_dictionary.items(), key=lambda item:-item[1]))
    #print(filtered_list)
    filtered_list=[x.lower() for x in filtered_list]
    #print(filtered_list)
    with open("positive-words.txt",'r') as f:
        positive_words=[line.strip() for line in f]
        positive_tokens=[token for token in filtered_list if token in positive_words]
    #print(positive_tokens)
    with open("negative-words.txt",'r') as f:
        negative_words=[line.strip() for line in f]
        negative_tokens=[token for token in filtered_list if token in negative_words]
    #print(negative_tokens)
    a=len(positive_tokens)
    b=len(negative_tokens)
    sentiment=""
    if(a>b):
        sentiment="positive"
    elif(b>a):
        sentiment="negative"
    else:
        sentiment="neutral"
    return sentiment


def getTokens(docs):
        stop_words = stopwords.words('english')
        tokens=[token.strip()             for token in nltk.word_tokenize(docs.lower())             if token.strip() not in stop_words and               token.strip() not in string.punctuation]
#         print "Tokens formed:", tokens
        tagged_tokens= nltk.pos_tag(tokens)
        wordnet_lemmatizer = WordNetLemmatizer()
        le_words=[wordnet_lemmatizer.lemmatize(word, get_wordnet_pos(tag)) for (word, tag) in tagged_tokens]
#         print "Le words is:", le_words
        return le_words
    
def get_wordnet_pos(pos_tag):    
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    
    elif pos_tag.startswith('V'):
        return wordnet.VERB

    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def setSoup(url):
    page = requests.get(url,headers=headers)
    if page.status_code==200:
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup
    else:
        print "Error"
        
def getReviewsBestBuy(url_review):
    while(url_review!=None):
        soup=setSoup(url_review)
        divs=soup.select("div.review-item-feedback")
    #     print type(divs)
        for idx,div in enumerate(divs):
            #.encode('utf8','ignore')
            score.append(div.select("span.reviewer-score")[0].get_text())
            title.append(div.select("h4.col-md-9.col-sm-9.col-xs-12.title")[0].get_text())
            date.append(div.select("div.review-date")[0].get_text())
            reviews.append(div.select("p.pre-white-space")[0].get_text())
#         divTag=(((soup.find("li",class_="page active")).find_next_sibling("li", class_="page")))
#         for tag in divTag:
#             link=tag.get('href')
#             if(link=='javascript:void(0);'):
#                 url_review=None
#             else:
#                 url_review=link
        url_review=None
#         print page_url
#     for i in range(len(score)):
#         print "\nPrinting the ",i+1," review"
#         print "Score:\n",score[i]
#         print "Title:\n",title[i]
#         print "Date:\n",date[i]
#         print "Review:\n",reviews[i]
    rows=zip(date, score, title, reviews)
    with open ("bestbuy.csv",'wb') as bb:
        writer=csv.writer(bb)
        writer.writerows(rows)
#     print "done"
    
        
def mainPageContent():
    soup=setSoup(url_home)
    average_score=None
    ratings_count=None
    price=None
    discount=None
    avg_div=soup.select("span.average-score")

    rating_div=soup.select("a#ratings-count-link")

    price_div=soup.select("div.pb-hero-price.pb-purchase-price span")
    discount_div=soup.select("div.pb-savings")
    if price_div!=[]:
        price=price_div[0].get_text()
#         print price
    if discount_div!=[]:

        discount=((discount_div[0].get_text()).split())[1]
#         print discount

    if avg_div!=[]:
        average_score=avg_div[0].get_text()
#         print average_score
    if rating_div!=[]:
        ratings_count=rating_div[0].get_text()
#         print ratings_count
#     all_reviews_div=soup.select("div.write-a-review a")[0]['href']
#     print all_reviews_div
#     reviews_page=requests.get(all_reviews_div,headers=headers)
#     if reviews_page.status_code==200:
#         print "Extract reviews"

if __name__=="__main__":
    mainPageContent();
    getReviewsBestBuy(url_review);
    for rev in reviews:
        tok.append(getTokens(rev))
        sentiment.append(sentiment_analysis(rev))
#         print "Tok here is ",tok
    print tok
    print sentiment


# In[ ]:



