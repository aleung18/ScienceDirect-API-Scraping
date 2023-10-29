import requests
import json
import xmltodict
import csv
import os

# num_articles should be factor of 100
# make sure that folder is already created
def generate_list_of_documents(keyword, num_articles, foldername):

    # Variables for the search query (request URL)
    offset = 0

    pii_list = []
    article_background_list = []
    article_title_list = []

    # loop through specified number of articles
    for i in range(int(num_articles / 100)):

        headers = {
            "Accept": "application/xml", 
            "X-ELS-APIKey": "{Your API Key}", 
            "X-ELS-Insttoken": "{Your Institutional Token}",
            'Cookie': '__cf_bm=68HlFrvAa8VWZickduad8eTYRKyqZLqKI.0UNLEEr4Q-1696542666-0-AYrM1Pzt1jwXzBkZTD7BeiJKSLRYOKAyWZtt6KTg+rCCKgr6CpLrCkje+JyY81qXnxnSWo4tS/Lc/mbWYlfeINE='
        }

        # check so that if keyword has spaces, it reformats it with %20 instead of a space (ex. if keyword="gas chromatography")

        search_api = f"https://api.elsevier.com/content/search/sciencedirect?start={offset}&count=100&offset={offset}&query={keyword}"

        payload = {}
        # Call the Search API
        # https://dev.elsevier.com/search.html#/ScienceDirect_Search_V2

        search = requests.request("GET", search_api, headers=headers, data=payload)

        # Converting XML from API (search.text) to JSON
        data_dict = xmltodict.parse(search.text)
        json_data = json.dumps(data_dict, indent=4, sort_keys=True)

        # getting 'pii' key from json
        jsonObject = json.loads(json_data)
        for eachEntry in jsonObject['search-results']['entry']:
            pii_list.append(eachEntry['pii'])

        offset += 100


    for pii in pii_list:
        article_api = f"https://api.elsevier.com/content/article/pii/{pii}"
        article_retrieval = requests.request("GET", article_api, headers=headers)

        dict = xmltodict.parse(article_retrieval.text)
        data = json.dumps(dict, indent=4, sort_keys=True)
        jsonObject = json.loads(data)
        
        # adds description/abstract to list
        article_background_list.append(jsonObject['full-text-retrieval-response']['coredata']['dc:description'])
        article_title_list.append(jsonObject['full-text-retrieval-response']['coredata']['dc:title'])

    # writing description/abstract into text file
    for index, (background, title) in enumerate(zip(article_background_list, article_title_list)):
        with open(f'{foldername}/{index}.txt', 'w') as f:
            f.write(f"Topic: {keyword.title()}\n\n")
            f.write(f"Title: {title}\n\n")
            f.write(f"Abstract: {background}")
        print(f"File saved as: {index}.txt")

    os.system('clear')
    return f"Articles saved to folder {foldername}"

print(generate_list_of_documents("gas chromatography", 500, "gas chromatography articles"))
