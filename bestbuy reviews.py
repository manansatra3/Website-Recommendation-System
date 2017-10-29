url_home="https://www.bestbuy.com/site/samsung-galaxy-s8-64gb-unlocked-midnight-black/5803741.p?skuId=5803741"
url_review="https://www.bestbuy.com/site/reviews/samsung-galaxy-s8-64gb-unlocked-midnight-black/5803741"
score=[]
title=[]
date=[]
reviews=[]
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

def setSoup(url):
    page = requests.get(url,headers=headers)
    if page.status_code==200:
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup
    else:
        print "Error"
        
def getReviewsBestBuy():
    soup=setSoup(url_review)
    divs=soup.select("div.review-item-feedback")
#     print type(divs)
    for idx,div in enumerate(divs):
        score.append(div.select("span.reviewer-score")[0].get_text().encode('utf8'))
        title.append(div.select("h4.col-md-9.col-sm-9.col-xs-12.title")[0].get_text().encode('utf8'))
        date.append(div.select("div.review-date")[0].get_text().encode('utf8'))
        reviews.append(div.select("p.pre-white-space")[0].get_text().encode('utf8'))
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
    print "done"
    
        
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
        print price
    if discount_div!=[]:

        discount=((discount_div[0].get_text()).split())[1]
        print discount

    if avg_div!=[]:
        average_score=avg_div[0].get_text()
        print average_score
    if rating_div!=[]:
        ratings_count=rating_div[0].get_text()
        print ratings_count
#     all_reviews_div=soup.select("div.write-a-review a")[0]['href']
#     print all_reviews_div
#     reviews_page=requests.get(all_reviews_div,headers=headers)
#     if reviews_page.status_code==200:
#         print "Extract reviews"

if __name__=="__main__":
    mainPageContent();
    getReviewsBestBuy();
        