from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import scholarly

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
my_list = []
json_list = []
@api_view(['GET'])
def index(request):
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
        return Response(json_content)
