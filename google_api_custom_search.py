#!/usr/bin/env python3

from apiclient.discovery import build
import os

class GoogleCustomSearch:

    def __init__(self):
        self.api_key = os.environ['API_KEY']
        self.cx = os.environ['CX']

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

    def parsedTop5(self, query):
        top5 = self.search(query=query)
        string = ''
        for item in top5:
            string += item['title'] + '\n' + item['link'] + '\n'

        return string.strip()

if __name__=='__main__':
    gcs = GoogleCustomSearch()
    top5 = gcs.parsedTop5(query='nodejs')
    print(top5)
