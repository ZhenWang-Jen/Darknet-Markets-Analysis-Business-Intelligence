################ start process web files ################## http://python.jobbole.com/87811/
import re, csv

listingNumberArray     = []
listingArray 	 = []

# to get each listsing 
listings = '24459 42171 56750 80539 82702'.split()

for listing in listings:
    listingNumberArray.append(listing)

    file = "E:/hansa/HansaMarketFullFiles/http _hansamkt2rr6nfg3.onion_listing_" + listing + "_.htm"
    f = open(file, "r+")
    text = f.read().replace("\n", "")
    f.close()

    thisListing = []

    title = re.match( r'(.*)<title>(.*?) ::.*', text, re.M|re.I).group(2)
    categoryNumber = re.match( r'(.*)<a href="/category/(.*?)/">.*', text, re.M|re.I).group(2)
    category = re.match( r'(.*)' + categoryNumber + '(.*?)</a>.*', text, re.M|re.I).group(2).replace("""/">""", "")
    vendor = re.match( r'(.*)/vendor/(.*?)/">.*', text, re.M|re.I).group(2)
    price = re.match( r'(.*)<strong>(.*?)</small>.*', text, re.M|re.I).group(2).replace("</strong>","").replace("""<small class="text-muted">""","") 
    vendorLevel = re.match( r'(.*)">Level (.*?)</span>.*', text, re.M|re.I).group(2) 
    #ifTrusted = re.match( r'(.*)<i class="fa fa-star  "></i>(.*?)</span>.*', text, re.M|re.I).group(2) 
    classStatus = re.match( r'(.*)Class</td>(.*?)</td>.*', text, re.M|re.I).group(2).replace("                            <td>", "")
    if classStatus == "Physical": 
        shipFrom = re.match( r'(.*)Ships From</td>    (.*?)</td>.*', text, re.M|re.I).group(2).replace("                            <td>", "")
        shipTo = re.match( r'(.*)Ships To</td>    (.*?)</td>.*', text, re.M|re.I).group(2).replace("                            <td>", "")
    else:
        shipFrom = "Instant Delivery"
        shipTo = "Instant Delivery"
    detail = re.match( r'(.*)<p>(.*?)</p>.*', text, re.M|re.I).group(2).replace("<br />", " ")
    date = re.match( r'(.*)<td>Date: (.*?)</td>.*', text, re.M|re.I).group(2).replace("--------------------------------", " ") #this replace not work 

    thisListing.append(title)
    thisListing.append(categoryNumber)
    thisListing.append(category)
    thisListing.append(vendor)
    thisListing.append(price)
    thisListing.append(vendorLevel)
    thisListing.append(classStatus)
    thisListing.append(detail)
    thisListing.append(date)

    listingArray.append(thisListing)

# classifying listings by vendors
tramapro 	  = listingArray[0]  # level 5
kingodua	  = listingArray[3]  # level 9
terrysukstock = listingArray[2] + listingArray[4] # level 9
pornsel       = listingArray[1]  # level 8

# make all text a string for each vendor
tramapro 	  = ' '.join(tramapro)
kingodua      = ' '.join(kingodua)
terrysukstock = ' '.join(terrysukstock)
pornsel       = ' '.join(pornsel)

# remove stopwords
with open ("E:/hansa/stopWordList.txt", "r") as stopWordsFile:
	stopWordsList = stopWordsFile.read().splitlines()

tramaproWords = tramapro.split()
resultwords   = [word.lower() for word in tramaproWords if word.lower() not in stopWordsList]
tramapro      = ' '.join(resultwords)

kingoduaWords = kingodua.split()
resultwords   = [word.lower() for word in kingoduaWords if word.lower() not in stopWordsList]
kingodua      = ' '.join(resultwords)

terrysukstockWords = terrysukstock.split()
resultwords   = [word.lower() for word in terrysukstockWords if word.lower() not in stopWordsList]
terrysukstock = ' '.join(resultwords)

pornselWords  = pornsel.split()
resultwords   = [word.lower() for word in pornselWords if word.lower() not in stopWordsList]
pornsel       = ' '.join(resultwords)

# remove punctuations
tramapro      = "".join(c for c in tramapro if c not in ("'",',','|','?','!','.',':',';','-','—','=','/','%','(',')','+','&','*')).replace('iam', '').replace('ill','').replace('quot','').replace('http','').replace('dont', '').replace('arent', '').replace('wont','').replace('didnt','').replace('cuz','')
kingodua      = "".join(c for c in kingodua if c not in ("'",',','|','?','!','.',':',';','-','—','=','/','%','(',')','+','&','*')).replace('iam', '').replace('ill','').replace('quot','').replace('http','').replace('dont', '').replace('arent', '').replace('wont','').replace('didnt','').replace('cuz','')
terrysukstock = "".join(c for c in terrysukstock if c not in ("'",',','|','?','!','.',':',';','-','—','=','/','%','(',')','+','&','*')).replace('iam', '').replace('ill','').replace('quot','').replace('http','').replace('dont', '').replace('arent', '').replace('wont','').replace('it','').replace('yourself', '').replace('thorugh', '').replace('didnt','').replace('cuz','')
pornsel       = "".join(c for c in pornsel if c not in ("'",',','|','?','!','.',':',';','-','—','=','/','%','(',')','+','&','*')).replace('iam', '').replace('ill','').replace('quot','').replace('http','').replace('dont', '').replace('arent', '').replace('wont','').replace('didnt','').replace('cuz','').replace('hbo鈥攖he', 'hbo the').replace('titles鈥攖o','titles to')

# store data in proper files
tramapro_txt = open("E:/hansa/author/tramapro.txt", "w")
tramapro_txt.write(tramapro)
tramapro_txt.close()
print("\n---------------processed data for vendor tramapro saved-------\n")	

kingodua_txt = open("E:/hansa/author/kingodua.txt", "w")
kingodua_txt.write(kingodua)
kingodua_txt.close()
print("\n---------------processed data for vendor kingodua saved-------\n")	

terrysukstock_txt = open("E:/hansa/author/terrysukstock.txt", "w")
terrysukstock_txt.write(terrysukstock)
terrysukstock_txt.close()
print("\n---------------processed data for vendor terrysukstock saved--\n")	

pornsel_txt = open("E:/hansa/author/pornsel.txt", "w")
pornsel_txt.write(pornsel)
pornsel_txt.close()
print("\n---------------processed data for vendor pornsel saved--------\n")	

######################### start doc2vec ##############################
#Loading data and file names into memory
#create a list that contains the name of all the text file in author folder
from os import listdir

labels = []
labels = [f for f in listdir('E:/hansa/author') if 
 f.endswith('.txt')]
#create a list data that stores the content of all text files in order of their names in labels
data = []
for doc in labels:
  data.append(open('E:/hansa/author/' + doc).read())

print("\n---------------doc2vec   program   starts---------------------\n")
# Gensim's Doc2Vec implementation requires each document/paragraph to have a label associated with it.
# doing it by using the LabeledSentence method. 
import gensim
LabeledSentence = gensim.models.doc2vec.LabeledSentence

#Creating an class to return iterator object
class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):
        self.labels_list = labels_list
        self.doc_list = doc_list
    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
              yield gensim.models.doc2vec.LabeledSentence(doc,[self.labels_list[idx]])

#iterator returned over all documents
sentences = LabeledLineSentence(data, labels)
model = gensim.models.Doc2Vec(
	size=500, 	# the dimensionality of the feature vector
	min_count=2, # ignore words with freq less than min_count
	alpha=0.025, # initial learning rate
	min_alpha=0.025)

print ("\n---------------begin   to   build   vocab-------------------\n")
#build vocab
model.build_vocab(sentences)
#training of model
#pass through the data set multiple times, shuffling the training text each time to improve accuracy
for epoch in range(10):  #manually control the learning rate over the course of 10 epochs
    print ('iteration '+ str(epoch+1))
    model.train(sentences,total_examples=model.corpus_count,epochs=model.iter)
    model.alpha -= 0.002    # decrease the learning rate
    model.min_alpha = model.min_alpha    # fix the learning rate, no decay
#saving the created model
model.save('doc2vec.model')
print ('\n----------------model-----------saved-----------------------\n')
#loading the model
model_loaded = gensim.models.doc2vec.Doc2Vec.load('doc2vec.model')

##################start testing#########################
#printing the vector of document at index 1 in labels
#docvec = model_loaded.docvecs[0]

#printing the vector of the file using its name
docvecTramapro 		= model_loaded.docvecs['tramapro.txt'] #if string tag used in training
docvecKingodua 		= model_loaded.docvecs['kingodua.txt'] 
docvecTerrysukstock = model_loaded.docvecs['terrysukstock.txt'] 
docvecPornsel 		= model_loaded.docvecs['pornsel.txt'] 

print(docvecTramapro)

#to get most similar document with similarity scores using document-index
#similar_doc = model_loaded.docvecs.most_similar(1) 

#to get most similar document with similarity scores using document- name
simsTramapro 	  = model_loaded.docvecs.most_similar('tramapro.txt')
simsKingodua 	  = model_loaded.docvecs.most_similar('kingodua.txt')
simsTerrysukstock = model_loaded.docvecs.most_similar('terrysukstock.txt')
simsPornsel 	  = model_loaded.docvecs.most_similar('pornsel.txt')

print("\n----------similarity between vendor tramapro with others------------\n")
print(simsTramapro[0][0].replace('.txt', ' :'), simsTramapro[0][1], "\n", simsTramapro[1][0].replace('.txt', ' :'), simsTramapro[1][1], "\n", simsTramapro[2][0].replace('.txt', ' :'), simsTramapro[2][1])
print("\n----------similarity between vendor kingodua with others------------\n")

print(simsTramapro)
print(simsKingodua)

print("\n----------similarity between vendor terrysukstock with others-------\n")
print(simsTerrysukstock)

print("\n----------similarity between vendor pornsel with others-------------\n")
print(simsPornsel)

# create tables for visulization

from tabulate import tabulate

similarities = [("tramapro", "N/A", simsTramapro[1][1], simsTramapro[0][1], simsTramapro[2][1]),
                ("kingodua", simsKingodua[2][1], "N/A", simsKingodua[1][1], simsKingodua[0][1]),
                ("terrysukstock", simsTerrysukstock[0][1], simsTerrysukstock[1][1], "N/A", simsTerrysukstock[2][1]),
                ("pornsel", simsPornsel[2][1], simsPornsel[0][1], simsPornsel[1][1], "N/A")]

reputations  = [("reputation", 5.06, 9.9, 9.3, 8.9)]

headers = ["VENDOR", "tramapro", "kingodua", "terrysukstock", "pornsel"]

print(tabulate(similarities, headers=headers), "\n")

# compare similarities 
from statistics import mean, median

numbers      = [simsPornsel[2][1], simsPornsel[1][1], simsPornsel[0][1], simsKingodua[2][1], simsKingodua[0][1], simsTerrysukstock[2][1]]

minimum      = min(numbers)
maximum      = max(numbers)
average      = mean(numbers)

results      = [(minimum, maximum, average)]

headersResult= ["Minimum", "Maximum", "Mean"]

print(tabulate(results, headers=headersResult), "\n")
print ('----------------reputation levels are below-------------------\n')
print(tabulate(reputations, headers=headers), "\n")

import matplotlib.pyplot as plt 

x = [2,4,6,8,10]
y = [6,7,8,2,4]

plt.bar(x,y, label='Bar 1')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Interesting')
plt.legend()
plt.show()