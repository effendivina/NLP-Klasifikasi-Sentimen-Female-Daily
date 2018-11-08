import csv

def openarticle(doc_name):
    with open(doc_name, encoding="utf-8") as csvfile: 
        next(csvfile)
        rawArticles = csv.reader(csvfile, delimiter=',') 
        perkata = [] #array perkata akan menyimpan semua kalimat menjadi perkata
        perkalimat = [] #array perkalimat menyimpan semua kalimat menjadi perkalimat
        kelas = []
        for row in rawArticles:
            perkalimat=row[3].lower()
            perkata.append(perkalimat.split())
            kelas.append(row[5].lower())
    return perkata, kelas 
