from wikidata import *
import re
import json
import os

def find_philosophers():
    result = ''
    items = open('leo-tolstoy-entities-master\manually-categorized\philosophers.csv', 'r', encoding='utf-8').read().split('\n')
    for item in items:
        realname = item
        query = find_human(item, profession='Q4964182')       
        if query == []:
            item = item.split(' ')
            item.reverse()
            new_item = ''
            for i in item:
                new_item += i + ' '
            query = find_human(new_item[:-1], profession='Q4964182')
            if query == []:
                result += realname + '	Not Found\n'
            else:
                ids = [i['id'] for i in query]
                result += realname + '	' + str(ids) + '\n'
        else:
            ids = [i['id'] for i in query]
            result += realname + '	' + str(ids) + '\n'
    return result

def search_all_items():
    items = [i.split('	') for i in open('leo-tolstoy-entities-master/nodes_id.tsv', 'r', encoding='utf-8').read().split('\n')]
    print(len(items))
    for item in items:
        result = {"id" : item[1], "name" : item[0], "urls" : classic_search(re.sub(', .*$', '', re.sub(' \(.*?\)', '', item[0])))}
        if len(result['urls']) == 0:
            path = '0\\'
        elif len(result['urls']) == 1:
            path = '1\\'
        else:
            path = 'more\\'
        x = open(path + result['id'] + '.json', 'w', encoding='utf-8')
        json.dump(result, x)
        x.close()


def alt_search():
    marked = eval(open('marked.json', 'r', encoding='utf-8').read(), {})
    for file in os.listdir('0'):
        if file.split('.')[0] not in marked:
            item = eval(open('0/' + file, 'r', encoding='utf-8').read(), {})
            result = {"id" : item["id"], "name" : item["name"], "urls" : altlabel_search(re.sub(', .*$', '', re.sub(' \(.*?\)', '', item["name"])))}
            if len(result['urls']) == 1:
                marked[result['id']] = result
            elif len(result['urls']) > 1:
                x = open('more\\' + result['id'] + '.json', 'w', encoding='utf-8')
                x.write(str(result))
                x.close()
    return marked
