# this program abstract web pages of real darknet markets to analyze the relation between similarities of seller profiles and their seller levels
#!/usr/bin/env python
# coding: utf8

# extract all files from the converted .zip file  
import zipfile

zip_ref = zipfile.ZipFile("E:/rsClub/rsclubvvwcoovivi.onion.link.zip", 'r')
print("Please be patient, the zip file is in extraction.")
zip_ref.extractall("E:/rsClub/")
zip_ref.close()
print("The .zip file extraction is complete.")

# change all abstracted files into proper html files
import os

def makepath(pathname):
	if not os.path.exists(pathname):
		os.makedirs(pathname)	

makepath("E:/rsClub/listingsWEB/")

for subfolder in os.listdir("E:/rsClub/rsclubvvwcoovivi.onion.link"):
	furtherpath = "E:/rsClub/rsclubvvwcoovivi.onion.link/" + subfolder
	print("Folder", subfolder, "is opened @", furtherpath)
	for targetfile in os.listdir(furtherpath):	
		# get all listings web pages
		if os.path.isfile(os.path.join(furtherpath, targetfile)) == True and "listing.php@ls_id=" in targetfile:
			os.rename(furtherpath +"/"+ targetfile, "E:/rsClub/listingsWEB/"+ targetfile + '.html')
print("--------------All listings web pages are ready to be parsed--------------")

print("--------------Start to parse original web data--------------")
import re, xlsxwriter
import pandas as pd

workbook   = xlsxwriter.Workbook('resultsALL.xlsx')
formatnormal = workbook.add_format()
formatnormal.set_pattern(1)  			# This is optional when using a solid fill.
formatnormal.set_bg_color('yellow')
formatnormal.set_text_wrap()

formatrotation = workbook.add_format()
formatrotation.set_bg_color('yellow')
formatrotation.set_rotation(30)

formatwarn = workbook.add_format()
formatwarn.set_bg_color('red')

worksheetSellers = workbook.add_worksheet('Max Seller Levels')
worksheetSellers.write('A1', 'Seller', formatnormal)
worksheetSellers.write('B1', 'Seller Level', formatnormal)
worksheetSellers.insert_textbox('D2', 'Please go to the end sheet for summary.', {'width': 192, 'height': 80})

def adddescription(text, file):
	# Product Tags
	if "tab=3" in file:
		description = ' '.join(re.findall(r'<div class="panel-body">\s*(.*?)\s*</div>', text))
	# Feedback
	elif "tab=4" in file:
		description = "Total Feedback List Total Feedback Feedback Buyer Price Date Time "
		newdescription = ' '.join(re.findall(r'<td><small>\s*(.*?)\s*</small><br/><sub style="color', text))
		description = description + newdescription.replace('<i>','').replace('</i>','')		
	elif re.findall(r'<pre>\s*(.*?)\s*</pre>', text, re.DOTALL):
		description = ' '.join(re.findall(r'<pre>\s*(.*?)\s*</pre>', text, re.DOTALL))
	else: 
		description = ''
	return description	

def addlisting(ID, text):
	newListing = ["empty listing data point"]*10		# create an array to store the new listing info 

	title = re.findall(r'<title>\s*(.*?)\s*</title>', text)[0].replace(" - RsClub Market", "")
	seller = re.findall(r'<small><a href="user.php@u_id=\s*(.*?)\s*">', text)[0]
	sellerlevel = re.findall(r'er Level\s*(.*?)\s*</span></small>', text)[0].replace(" (",".").replace(")", "")
	origincountry = re.findall(r'Origin Country : </b></label>\s*(.*?)\s*</small>', text)[0]	
	shipto = re.findall(r'Ship To : </b></label></small>\s*(.*?)\s*</small>', text)[0].replace("<small> ","")
	payment = re.findall(r'Payment :</b></label> <font color="green">\s*(.*?)\s*</font>', text)[0]
	productclass = re.findall(r'Product class :</b></label>\s*(.*?)\s*</small>', text)[0]
	quantity = re.findall(r'Quantity :</b></label>\s*(.*?)\s*</small><br/>', text)[0]
	description = adddescription(text, listingfile)
	# index     no.0  no.1   no.2		no.3 		  	  no.4		    no.5	  no.6		no.7		  no.8	  	 no.9	
	newListing= [ID, title, seller, sellerlevel, origincountry, shipto, payment, productclass, quantity, description]
	return newListing

i = s = 0
listingArray      = []
sellerNamesLevels = []					# to store all names of sellers' listings files

for listingfile in os.listdir("E:/rsClub/listingsWEB"):
	# store all web content into the text variable
	webcontent = open("E:/rsClub/listingsWEB/"+listingfile, "r+", encoding="utf-8").read()
	
	# start to collect all needed data points
	listingID = listingfile.replace("listing.php@ls_id=", "").replace(".html","")
	actuallistingID = listingID.split('&')[0]
	
	if len(listingArray) > 0 and actuallistingID == listingArray[i-1][0]:# new description for the same listing			
		description = adddescription(webcontent, listingfile)
		if description and description not in listingArray[i-1][9]:		# avoid repeated description f
			listingArray[i-1][9] = ' '.join([listingArray[i-1][9], description]) # append new description
	else:
		newlisting = addlisting(actuallistingID, webcontent)			# new listing
		listingArray.append(newlisting)								# add new listing to array	
		i = i+1
		# check if the seller's info has existed
		if any(newlisting[2] in sublist for sublist in sellerNamesLevels) == True:
			x = [x for x in sellerNamesLevels if newlisting[2] in x][0]
			if sellerNamesLevels[sellerNamesLevels.index(x)][1] < newlisting[3]:
				print(sellerNamesLevels[sellerNamesLevels.index(x)][1])
				sellerNamesLevels[sellerNamesLevels.index(x)][1] = newlisting[3]
				print(newlisting[3])
				#print('The index is (%d,%d)'%(sellerNamesLevels.index(x),x.index("vendor")))
		else: # add new seller to array
			sellerNamesLevels.append([newlisting[2], newlisting[3]])
		#print('The index is (%d,%d)'%(sellerNamesLevels.index(x),x.index(newlisting[2])))										# increase index of the next listing
		'''
		for seller in sellerNamesLevels:
			print(seller)
			if newlisting[2] != seller[0]:
				print(newlisting[2], newlisting[3])
				#print(seller[0])
				sellerNamesLevels.append([newlisting[2], newlisting[3]])
				print(sellerNamesLevels)
				print("endddd")
			elif newlisting[2] == seller[0] and newlisting[3] > seller[1]: # means this seller has existed so needs to check if max level exists
				seller[1] = newlisting[3]
		'''
print(sellerNamesLevels)
sellerNamesLevels = sorted(sellerNamesLevels, key=lambda x: x[0])
print(sellerNamesLevels)
'''
b = sorted(sellerNamesLevels, key=lambda x: x[0])
c = { x[0] : x[1:len(x)] for x in b}
duplicatedLevelsRemoved = [[n]+c[n] for n in c]
duplicatedLevelsRemoved = sorted(duplicatedLevelsRemoved, key=lambda x: x[0].lower())
'''
i = 0
for each in sellerNamesLevels:
	worksheetSellers.write(i+1, 0, each[0])					# add seller's name 
	worksheetSellers.write(i+1, 1, float(each[1]))			# add seller's seller level
	i = i +1
print("--------------Original web data is parsed successfully--------------")

print("--------------Start to clean parsed data-----------------")
# prepara to remove stopwords
stopWordsList = open ("E:/rsClub/stopWordList.txt", "r").read().splitlines()

makepath("E:/rsClub/listingsTEXT/")	
makepath("E:/rsClub/sellersTEXT/")		

for eachlisting in listingArray:
	thisListingWords = ' '.join(eachlisting).split() # separate each array of listing into words

	firstArray = []
	for eachword in thisListingWords:
		if eachword.lower() not in stopWordsList:
			firstArray.append(eachword)
			firstArray = ' '.join(firstArray).split()

	digitsremoved = []
	for eachword in firstArray:
		eachword = ''.join([i for i in eachword if not i.isdigit()])
		digitsremoved.append(eachword)
		digitsremoved = ' '.join(digitsremoved).split()
	punctuationsremoved = []
	for eachword in digitsremoved:
		eachword = re.sub(r'[^\w]', ' ', eachword).replace("_", "")
		punctuationsremoved.append(eachword)
		punctuationsremoved = ' '.join(punctuationsremoved).split()
	#stopwordsremoved  = [eachword.lower() for eachword in punctuationsremoved if eachword.lower() not in stopWordsList]
	stopwordsremoved  = []
	for eachword in punctuationsremoved:
		if eachword.lower() not in stopWordsList:
			stopwordsremoved.append(eachword.lower())
			stopwordsremoved = ' '.join(stopwordsremoved).split()
	resultwords   = ' '.join(stopwordsremoved)
	print(resultwords+"\n")

	l = open("E:/rsClub/listingsTEXT/"+eachlisting[0]+".txt", "w+", encoding="utf-8")
	l.write(resultwords)
	l.close()
	# classify listings info by sellers
	v = open("E:/rsClub/sellersTEXT/"+eachlisting[2]+".txt", "a+", encoding='utf-8') 
	v.write(resultwords)
	v.close()
print("--------------Parsed data cleaned successfully--------------")

print("--------------Start to implement doc2vec--------------------")
# Gensim's Doc2Vec implementation requires each document/paragraph to have a label associated with it.
# doing it by using the LabeledSentence method. 
import gensim
from os import listdir
import pandas as pd

LabeledSentence = gensim.models.doc2vec.LabeledSentence
#Creating an class to return iterator object
class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):
        self.labels_list = labels_list
        self.doc_list = doc_list
    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
              yield gensim.models.doc2vec.LabeledSentence(doc,[self.labels_list[idx]])

#create a list that contains the name of all the text file in author folder
labels = []
labels = [f for f in listdir('E:/rsClub/sellersTEXT') if f.endswith('.txt')]
#create a list data of all content of all processed text files in order of their names in labels
data = []
for doc in labels:
	data.append(open('E:/rsClub/sellersTEXT/' + doc, encoding="utf-8").read())
#to get the similarity scores between vendors (based on all their listings pages content) 

# creat alphebet index
import itertools, string
list(itertools.product(string.ascii_uppercase, repeat=2))
alphbets = list(itertools.chain(string.ascii_uppercase, (''.join(pair) for pair in itertools.product(string.ascii_uppercase, repeat=2))))
del alphbets[0]		# remove "A" since similarities start to print at "B"
formatnumber = workbook.add_format()
formatnumber.set_num_format('0.00000')
# create a dictionary for worksheets
d={}		
# get 10 sets of similarities by running the program 10 times
for i in range(0,10):						# loop through the program multiple times for improved accuracy
	print("\nNo."+str(i+1)+ " doc2vec program starts")
	#iterator returned over all documents
	sentences = LabeledLineSentence(data, labels)
	model = gensim.models.Doc2Vec(
		size=500, 							# the dimensionality of the feature vector
		min_count=1, 						# ignore words with freq less than min_count
		alpha=0.025, 						# initial learning rate
		min_alpha=0.025)
	#Loading data and file names into memory
	print ("begin to build vocab")	
	model.build_vocab(sentences)			#build vocab
	#training of mode by passing through the data set multiple times, shuffling the training text each time to improve accuracy
	for epoch in range(10):  #manually control the learning rate over the course of 10 epochs
	    print ('iteration '+ str(epoch+1))
	    model.train(sentences,total_examples=model.corpus_count,epochs=model.iter)
	    model.alpha -= 0.002    			# decrease the learning rate
	    model.min_alpha = model.min_alpha   # fix the learning rate, no decay	
	model.save('doc2vec.model')				#saving the created model
	print ('model is saved')
	#loading the model
	model_loaded = gensim.models.doc2vec.Doc2Vec.load('doc2vec.model')

	# set up sheet with row & column headers
	d["worksheetSimilarity{0}".format(i+1)] = workbook.add_worksheet('Similarities Set '+ str(i+1))
	d["worksheetSimilarity{0}".format(i+1)].write('A1', 'SELLER', formatrotation)	

	for h in range(len(sellerNamesLevels)):
		d["worksheetSimilarity{0}".format(i+1)].write(h+1, 0, sellerNamesLevels[h][0], formatnormal)
		d["worksheetSimilarity{0}".format(i+1)].write(0, h+1, sellerNamesLevels[h][0], formatnormal)
		for j in range(len(sellerNamesLevels)):		# numbers of vendors plus one for the row title
			sims = model_loaded.docvecs.similarity(sellerNamesLevels[h][0]+".txt", sellerNamesLevels[j][0]+".txt")
			d["worksheetSimilarity{0}".format(i+1)].write(h+1, j+1, sims, formatnumber)

# create a sheet for average of calculated 10 similarities
worksheetAverage = workbook.add_worksheet('Averages of 10 Similarities')
worksheetAverage.write('A1', 'SELLER', formatrotation)
# create a sheet for standard deviation of calculated 10 similarities
worksheetStandardDV = workbook.add_worksheet('Standard DV of 10 Similarities')
worksheetStandardDV.write('A1', 'SELLER', formatrotation)

for h in range(len(sellerNamesLevels)):
	worksheetAverage.write(h+1, 0, sellerNamesLevels[h][0], formatnormal)
	worksheetAverage.write(0, h+1, sellerNamesLevels[h][0], formatnormal)

	worksheetStandardDV.write(h+1, 0, sellerNamesLevels[h][0], formatnormal)
	worksheetStandardDV.write(0, h+1, sellerNamesLevels[h][0], formatnormal)

	for j in range(len(sellerNamesLevels)):		# numbers of vendors plus one for the row title
		alphbet = alphbets[j]
		worksheetAverage.write(h+1, j+1,"=AVERAGE('Similarities Set 1'!"+alphbet+str(h+2)+",'Similarities Set 2'!"+alphbet+str(h+2)+",'Similarities Set 3'!"+alphbet+str(h+2)+",'Similarities Set 4'!"+alphbet+str(h+2)+",'Similarities Set 5'!"+alphbet+str(h+2)+",'Similarities Set 6'!"+alphbet+str(h+2)+",'Similarities Set 7'!"+alphbet+str(h+2)+",'Similarities Set 8'!"+alphbet+str(h+2)+",'Similarities Set 9'!"+alphbet+str(h+2)+",'Similarities Set 10'!"+alphbet+str(h+2)+")*1", formatnumber)
		worksheetStandardDV.write(h+1, j+1,"=STDEV('Similarities Set 1'!"+alphbet+str(h+2)+",'Similarities Set 2'!"+alphbet+str(h+2)+",'Similarities Set 3'!"+alphbet+str(h+2)+",'Similarities Set 4'!"+alphbet+str(h+2)+",'Similarities Set 5'!"+alphbet+str(h+2)+",'Similarities Set 6'!"+alphbet+str(h+2)+",'Similarities Set 7'!"+alphbet+str(h+2)+",'Similarities Set 8'!"+alphbet+str(h+2)+",'Similarities Set 9'!"+alphbet+str(h+2)+",'Similarities Set 10'!"+alphbet+str(h+2)+")*1", formatnumber)

worksheetAverage.conditional_format('B2:KQ303', {'type': 'cell', 'criteria': '<', 'value': 0, 'format': formatwarn})					  # highlight negative similarities
worksheetStandardDV.conditional_format('B2:KQ303', {'type': 'cell', 'criteria': '=', 'value': 0.00000, 'format': formatwarn})					  # highlight negative similarities

# create a summary sheet
worksheetSummary = workbook.add_worksheet('Results Summary')
worksheetSummary.write('A1', 'Seller', formatnormal)
worksheetSummary.write('B1', 'Max Seller Level', formatnormal)
worksheetSummary.write('C1', 'Comparing with Seller...', formatnormal)
worksheetSummary.write('D1', 'Max Seller Level', formatnormal)
worksheetSummary.write('E1', 'Difference of Seller Levels', formatnormal)
worksheetSummary.write('F1', 'Similarity of Listings', formatnormal)

row = j = h = 0
import math

for eachseller in sellerNamesLevels:
	for eachComparedWithSeller in sellerNamesLevels:
		alphbet = alphbets[j]
		worksheetSummary.write(row+1, 0, eachseller[0])
		worksheetSummary.write(row+1, 1, float(eachseller[1]))
		worksheetSummary.write(row+1, 2, eachComparedWithSeller[0])
		worksheetSummary.write(row+1, 3, float(eachComparedWithSeller[1]))
		worksheetSummary.write(row+1, 4, math.sqrt(pow(float(eachseller[1])-float(eachComparedWithSeller[1]),2)))
		worksheetSummary.write(row+1, 5, "='Averages of 10 Similarities'!"+alphbet+str(h+2))
		row = row + 1 
		h = h + 1
	j = j + 1
	h = 0

worksheetSummary.write(0, 6, "Standard Deviation of Levels' Difference", formatnormal)
worksheetSummary.write(1, 6, "=STDEV(E2:E"+str(row+1)+")")
worksheetSummary.write(0, 7, "Standard Deviation of Similarities", formatnormal)
worksheetSummary.write(1, 7, "=STDEV(F2:F"+str(row+1)+")")
worksheetSummary.write(0, 8, "Correlation", formatnormal)
worksheetSummary.write(1, 8, "=CORREL(E2:E"+str(row+1)+",F2:F"+str(row+1)+")")
worksheetSummary.write(0, 9, "Pearson Correlation", formatnormal)
worksheetSummary.write(1, 9, "=PEARSON(E2:E"+str(row+1)+",F2:F"+str(row+1)+")")
worksheetSummary.write(0, 10, "Interpretation", formatnormal)
# worksheetSummary.write(1, 8, '=IF(AND(-1<=H2,H2<-0.5),"Strong negative relation",IF(AND(-0.5<=H2,H2<-0.3),"Mid negative relation",IF(AND(-0.3<=H2,H2<-0.09),"Slight negative relation",IF(AND(-0.09<=H2,H2<=0.09),"No relation",IF(AND(0.09<H2,H2<=0.3),"Slight positive relation",IF(AND(0.3<H2,H2<=0.5),"Mid positive relation",IF(AND(0.5<H2,H2<=1),"Strong positive relation","Wrong input")))))))')
worksheetSummary.write(1, 10, '=IF(AND(-1<=J2,J2<-0.5),"Large negative association",IF(AND(-0.5<=J2,J2<-0.3),"Medium negative association",IF(AND(-0.3<=J2,J2<-0.1),"Small negative association",IF(AND(-0.1<=J2,J2<=0.1),"No association",IF(AND(0.1<J2,J2<=0.3),"Small positive association",IF(AND(0.3<J2,J2<=0.5),"Medium positive association",IF(AND(0.5<J2,J2<=1),"Large positive association","Wrong input")))))))')
worksheetSummary.write(0, 11, 'Source', formatnormal)
worksheetSummary.write(1, 11, 'https://statistics.laerd.com/statistical-guides/pearson-correlation-coefficient-statistical-guide.php')
# source: https://statistics.laerd.com/statistical-guides/pearson-correlation-coefficient-statistical-guide.php
worksheetSummary.write_comment('I2', '"The interpretation of a correlation coefficient depends on the context and purposes. A correlation of 0.8 may be very low if one is verifying a physical law using high-quality instruments, but may be regarded as very high in the social sciences where there may be a greater contribution from complicating factors."')

workbook.close()
print("Excel sheets are complete.")
print("Program ends.\nPlease refer to the resultsALL.xlsx in the rsClub folder for detailed results.")
os.system("start "+'resultsALL.xlsx')
# program ends.