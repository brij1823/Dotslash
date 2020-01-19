from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import scholarly
import io
import requests

import requests
from io import StringIO


from collections import Counter
from collections import OrderedDict


import urllib3
import PyPDF2
import textract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from urllib.request import urlopen


import wordninja
from urllib.request import urlopen


from collections import Counter

from nltk.tag import pos_tag


class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
my_list = []
json_list = []
@api_view(['GET'])
def author(request):
    try:
        temp = request.GET["data"]
        result = ((scholarly.search_author(temp)))
        json_content = []
        for i in range(1,10):
            temp = next(result)
            x = {
            "id" : temp.id,
            "name" : temp.name,
            "affiliation" : temp.affiliation,
            "citedby" : temp.citedby,
            "email" : temp.email,
            "interests" : temp.interests,
            "url" : temp.url_picture
            }
            json_content.append(x)
    except:
        print("Something Went Wrong")
    return Response(json_content)

@api_view(['GET'])
def interests(request):
    try:
        temp = request.GET["data"]
        result = scholarly.search_keyword(temp)
        json_content = []
        for i in range(1,20):
            temp = next(result)
            x = {
            "id" : temp.id,
            "name" : temp.name,
            "affiliation" : temp.affiliation,
            "citedby" : temp.citedby,
            "email" : temp.email,
            "interests" : temp.interests,
            "url" : temp.url_picture
            }
            json_content.append(x)
    except:
        print("Something went wrong")
    return Response(json_content)


@api_view(['GET'])
def title(request):
    try:
        temp = request.GET["data"]
        result = scholarly.search_pubs_query(temp)
        json_content = []
        for i in range(1,10):
            temp = next(result)
            x = {
            "title" : temp.bib["title"],
            "author" : temp.bib["author"],
            "abstract" : temp.bib["abstract"],
            "citedby" : temp.citedby,
            "id_scholarcitedby" : temp.id_scholarcitedby,
            "source" : temp.source,
            "url_scholar" : temp.url_scholarbib,
            "E-Print" : temp.bib["eprint"]
            }
            json_content.append(x)
        
    except:
        print("Something Went Wrong")
    return Response(json_content)


@api_view(['GET'])
def recommendation(request):
    try:
        temp = request.GET['data']
        result = scholarly.search_keyword(temp)
        my_list = []
        for i in range(1,20):
            temp= next(result)
            for i in temp.interests:
                my_list.append(i.lower())
        counts = Counter(my_list)
        recommendation = []
        counter = 0
        a1_sorted_keys = sorted(counts, key=counts.get, reverse=True)
        for r in a1_sorted_keys:
            if(counter<6):
                print(r, counts[r])
                recommendation.append(r)
            else:
                break
            counter = counter+1
        x = {"data" : recommendation}
        return Response(x)


    except:
        print("Something went wrong")

def main(temp):
    download_file(temp)

def download_file(download_url):
    print("Download started")
    response =urlopen(download_url)
    file = open("my_dot.pdf", 'wb')
    file.write(response.read())
    file.close()
    print("Completed")

global totalPageNumber
def extractPdfText(filePath=''):
    
    # Open the pdf file in read binary mode.
    fileObject = open(filePath, 'rb')

    # Create a pdf reader .
    pdfFileReader = PyPDF2.PdfFileReader(fileObject)

    # Get total pdf page number.
    totalPageNumber = pdfFileReader.numPages

    # Print pdf total page number.
    print('This pdf file contains totally ' + str(totalPageNumber) + ' pages.')

    currentPageNumber =0 
    text = ''

    # Loop in all the pdf pages.
    while(currentPageNumber < totalPageNumber ):

        # Get the specified pdf page object.
        pdfPage = pdfFileReader.getPage(currentPageNumber)

        # Get pdf page text.
        text = text + pdfPage.extractText()

        # Process next page.
        currentPageNumber += 1

    if(text == ''):
        # If can not extract text then use ocr lib to extract the scanned pdf file.
        text = textract.process(filePath, method='tesseract', encoding='utf-8')
       
    return text

# This function will remove all stop words and punctuations in the text and return a list of keywords.
def extractKeywords(text):
    # Split the text words into tokens
    wordTokens = word_tokenize(text)

    # Remove blow punctuation in the list.
    punctuations = ['(',')',';',':','[',']',',']

    # Get all stop words in english.
    stopWords = stopwords.words('english')

    # Below list comprehension will return only keywords tha are not in stop words and  punctuations
    keywords = [word for word in wordTokens if not word in stopWords and not word in punctuations]
   
    return keywords


@api_view(['GET'])
def keywords(request):
    try:
        temp = request.GET["data"]
        main(temp)
        print("After Main")
        pdfFilePath = 'my_dot.pdf'
        pdfText = extractPdfText(pdfFilePath)
        print('There are ' + str(pdfText.__len__()) + ' word in the pdf file.')
        #print(pdfText)
        keywords = extractKeywords(pdfText)
        print('There are ' + str(keywords.__len__()) + ' keyword in the pdf file.')
        
        final_list = []
        for i in keywords:
            if(len(i) > 5):
                final_list.append(i)
                
        final_str = ' '.join(final_list)
        
        analysis = wordninja.split(final_str)
        print(len(analysis))
        stop_words = set(stopwords.words('english')) 

        for i in analysis:
            if(len(i)<5 or (i in stop_words)):
                analysis.remove(i)
        print(len(analysis))
        tagged_sent = pos_tag(analysis)
        
        propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
        
        for i in propernouns:
            if(len(i)<5):
                propernouns.remove(i)
        
        counts = Counter(propernouns)
        print(counts)
        display = []
        counter = 0
        a1_sorted_keys = sorted(counts, key=counts.get, reverse=True)
        for r in a1_sorted_keys:
            if(counter<6):
                print(r, counts[r])
                display.append(r)
            else:
                break
            counter = counter+1
        x = {
            "data" : display,
            "words" : str(pdfText.__len__())
        }
        return Response(x)

    except:
        print("Something went wrong")

