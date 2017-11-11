
# coding: utf-8

# In[1]:




# In[ ]:

import requests
from bs4 import BeautifulSoup
import csv
import nltk, string
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet
from nltk.corpus import stopwords     

score=[]
title=[]
date=[]
reviews=[]
le_words=[]
tok=[]
sentiment=[]
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
# url_review="https://www.amazon.com/Samsung-Galaxy-S8-Unlocked-64GB/product-reviews/B06Y14T5YW/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
url_review="https://www.amazon.com/Samsung-Galaxy-S8-Unlocked-64GB/product-reviews/B06Y14T5YW/ref=cm_cr_getr_d_show_all?ie=UTF8&reviewerType=all_reviews&pageNumber=1"
url_home="https://www.amazon.com/Samsung-Galaxy-S8-Unlocked-64GB/dp/B06Y14T5YW"

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




def getReviewsAmazon(url_review):
#     page_url="https://www.amazon.com/Samsung-Galaxy-S8-Unlocked-64GB/product-reviews/B06Y14T5YW/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"    
    c=0;
    c1=0;
    while (url_review!=None):
#         c+=1
#         c1=0
#         print "while entering while",url_review
        soup=setSoup(url_review)
        divs=soup.select("div#cm_cr-review_list")
#         divs=soup.select("div.a-section.celwidget")
#         print len(divs)

        for idx, div in enumerate(divs):
            #print div
#             c1+=1
#             print (div.select("span.a-size-base.a-color-secondary.review-date"))
            #.encode('ascii','ignore')a-size-base a-color-secondary review-date
            date.append(div.select("span.a-size-base.a-color-secondary.review-date")[0].get_text().encode('ascii','ignore'))
            score.append(div.select("span.a-icon-alt")[0].get_text().encode('ascii','ignore'))
            title.append(div.select("a.a-size-base.a-link-normal.review-title.a-color-base.a-text-bold")[0].get_text().encode('ascii','ignore'))
            reviews.append(div.select("span.a-size-base.review-text")[0].get_text().encode('ascii','ignore'))
#             print len(date),len(score),len(title),len(reviews)
#             print c1
        divTag=(((soup.find("li",class_="a-selected page-button")).find_next_sibling("li", class_="page-button")))
#         print "divTAg",divTag
        if(divTag!=None):
            t=0;
            for tag in divTag:
                t+=1
                if "Next" not in tag.getText():
                    url_review="https://www.amazon.com"+tag.get('href')
#                     print "inside if",url_review
                else:
                    url_review=None
#                 print "t",t
        else:
            url_review=None
#         print "outside if & fr",url_review
#         print "c",c
    
    rows=zip(date, score, title, reviews)
    with open ("amazon.csv",'wb') as az:
        writer=csv.writer(az)
        writer.writerows(rows)
          
def mainPageContent():
    soup=setSoup(url_home)
    average_score=None
    ratings_count=None
    price=None
    
    average_score=(((soup.select("span#acrPopover i.a-icon-star.a-star-4-5 span.a-icon-alt"))[0].getText()).split())[0]
    ratings_count=(((soup.select("a#acrCustomerReviewLink span#acrCustomerReviewText"))[0].getText()).split())[0]
    price=soup.select("span.a-offscreen")[2].getText()
    print average_score
    print ratings_count
    print price
        
        
if __name__ == "__main__":  
    
    mainPageContent()
    getReviewsAmazon(url_review)
    for rev in reviews:
        tok.append(getTokens(rev))
        sentiment.append(sentiment_analysis(rev))
#         print "Tok here is ",tok
#     print tok
#     print sentiment
    
    


# In[ ]:



