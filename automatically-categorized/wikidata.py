import requests

def search_by_classes(classes, lang='ru'):
    out = {}
    query1 = 'Select ?id ?label where {?id wdt:P31 wd:'
    query2 = '. ?id ?rdfs_label ?label filter (lang(?label) = "' + lang + '")}'
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    for class_type in classes:
        query = query1 + class_type + query2
        print('query: ' + query)
        data = requests.get(url, params={'query': query, 'format': 'json'}).json()
        out[class_type] = data['results']['bindings']
    return out

def find_human(label, profession=''):
    if profession != '':
        profession = '?id wdt:P106 wd:' + profession + '.'
    query1 = '''PREFIX wikibase: <http://wikiba.se/ontology#>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?id WHERE {
          ?id ?label "''' + label + '''"@ru.
          ''' + profession + '''
          ?id wdt:P31 wd:Q5.
        }'''
    query2 = '''PREFIX wikibase: <http://wikiba.se/ontology#>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?id WHERE {
          ?id ?label "''' + label + '''"@ru.
          ?id wdt:P31 wd:Q5.
        }'''
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    data1 = requests.get(url, params={'query': query1, 'format': 'json'}).json()
    data2 = requests.get(url, params={'query': query2, 'format': 'json'}).json()
    humans = []
    if data1['results']['bindings'] == []:
        data = data2
    else:
        data = data1
    for item in data['results']['bindings']:
        my_item = dict()
        my_item['label'] = label
        my_item['id'] = item['id']['value']
        humans.append(my_item)
    return humans

def classic_search(item):
    query = 'Select ?id where { ?id rdfs:label "' + item + '"@ru.}'
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    data = requests.get(url, params={'query': query, 'format': 'json'}).json()
    return [i['id']['value'] for i in data['results']['bindings']]

def altlabel_search(item):
    query = 'Select ?id where { ?id skos:altLabel "' + item + '"@ru.}'
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    data = requests.get(url, params={'query': query, 'format': 'json'}).json()
    return [i['id']['value'] for i in data['results']['bindings']]
