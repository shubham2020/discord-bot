#!/usr/bin/env python3

################################################################
#         MODULE TO DEAL WITH GOOGLE CUSTOM SEARCH API
################################################################

from apiclient.discovery import build
import os

class GoogleCustomSearch:

    # initialize the keys required for api calls
    def __init__(self):
        self.api_key = os.environ['API_KEY']
        self.cx = os.environ['CX']

    # function to call the custom search API with exception handling
    def search(self, query):
        try:
            resource = build("customsearch", 'v1', developerKey=self.api_key).cse()
            result = resource.list(q=query, cx=self.cx).execute()
        except Exception as e:
            print(e)
            return None

        if len(result['items']) >= 5:
            return result['items'][0:5]
        else:
            return result['items']

    # function to send the search query result parsed in the form of top 5 results
    def parsedTop5(self, query):
        top5 = self.search(query=query)

        if top5 is None:
            return "Search Not possible: Error communicating with Google engine"
            
        string = ''
        for item in top5:
            string += item['title'] + '\n' + item['link'] + '\n'

        return string.strip()

if __name__=='__main__':
    gcs = GoogleCustomSearch()
    top5 = gcs.parsedTop5(query='nodejs')
    print(top5)
