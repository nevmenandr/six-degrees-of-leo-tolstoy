import os


def manual_marking():
    marked = eval(open('marked.json', 'r', encoding='utf-8').read(), {})
    files = os.listdir('more')
    for file in files:
        if file.split('.')[0] not in marked:
            js = eval(open('more/' + file, 'r', encoding='utf-8').read(), {})
            print(js['name'])
            st = input('Input wikidata url: ')
            if st == 'stop':
                x = open('marked.json', 'w', encoding='utf-8')
                x.write(str(marked))
                x.close()
                print('Done')
            else:
                js['urls'] = [st]
                marked[file.split('.')[0]] = js
