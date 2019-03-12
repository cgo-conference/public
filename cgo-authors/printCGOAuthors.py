import requests


def cgo_url(y):
    return "https://dblp.uni-trier.de/search/publ/api?q=toc%3Adb/conf/cgo/cgo" + str(y) + ".bht%3A&format=json"


all_authors = []

start_year = 2003
end_year = 2019

for year in range(start_year, end_year+1):
    with requests.get(cgo_url(year)) as r:
        data = r.json()

        papers = data['result']['hits']['hit']
        for paper in papers:
            try:
                authors = paper['info']['authors']
                if isinstance(authors['author'], str):
                    all_authors.append(authors['author'])
                elif isinstance(authors['author'], list):
                    all_authors = all_authors + authors['author']
            except KeyError:
                pass

unique_authors = list(set(all_authors))
unique_authors.sort()

with open("cgo_author_list_" + str(start_year) + "-" + str(end_year) + ".txt", "w", encoding='utf-8') as f:
    for author in unique_authors:
        f.write("%s\n" % author)
