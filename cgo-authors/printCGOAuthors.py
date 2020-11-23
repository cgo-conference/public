import requests
from collections import Counter


def cgo_url(y):
    return "https://dblp.uni-trier.de/search/publ/api?q=toc%3Adb/conf/cgo/cgo" + str(y) + ".bht%3A&format=json"


all_authors = []

start_year = 2003
end_year = 2020

for year in range(start_year, end_year+1):
    with requests.get(cgo_url(year)) as r:
        data = r.json()

        papers = data['result']['hits']['hit']
        for paper in papers:
            try:
                authors = paper['info']['authors']
                if isinstance(authors['author'], list):
                    all_authors = all_authors + [a['text'] for a in authors['author']]
                elif isinstance(authors['author'], dict):
                    all_authors.append(authors['author']['text'])
            except KeyError:
                pass

all_authors.sort()
authors_and_count = Counter(all_authors)

with open("cgo_author_list_" + str(start_year) + "-" + str(end_year) + ".txt", "w", encoding='utf-8') as f:
    for author, count in authors_and_count.most_common():
        f.write("%s, %s\n" % (author, count))
