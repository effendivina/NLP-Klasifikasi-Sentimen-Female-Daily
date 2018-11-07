import csv

def openarticle(doc_name):
    with open(doc_name, encoding="utf-8") as csvfile: 
        next(csvfile)
        rawArticles = csv.reader(csvfile, delimiter=',') 
        articles = [] 
        labels = []
        for row in rawArticles:
            articles.append(row[3].lower()) 
            labels.append(row[5].lower())
    return articles, labels 


