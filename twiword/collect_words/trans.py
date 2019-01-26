url = 'http://public.dejizo.jp/NetDicV09.asmx/SearchDicItemLite'
query = {
    'Dic':'EJdict',
    'Word':'infinity',
    'Scope':'HEADWORD',
    'Match':'STARTWITH',
    'Merge':'AND',
    'Prof':'XHTML',
    'PageSize':'1',
    'PageIndex':'0',
}
r = requests.get(url, params=query)
print("response", r.json())