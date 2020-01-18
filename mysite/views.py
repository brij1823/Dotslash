from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import scholarly
import io

import requests
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


