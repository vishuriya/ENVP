from pymongo import MongoClient


def get_language_list():
    language_list = [
        { 'name' : 'English',
            'code' : 'en'
         },
        { 'name' : 'German',
            'code' : 'de'
         },
         { 'name' : 'French',
            'code' : 'fr'
         },
         { 'name' : 'Spanish',
            'code' : 'es'
         },
         { 'name' : 'Portuguese',
            'code' : 'pt'
         },
         { 'name' : 'Italian',
            'code' : 'it'
         },
         {
             'name' : 'Dutch',
             'code' : 'nl'
         },
         {
             'name' : 'Polish',
             'code' : 'pl'
         },
        {
            'name':'Danish',
            'code':'dk'
         }
         
         
        ]

    return language_list


def language_seperator(req,db):
    dict_of_val = {}
    collections = db.list_collection_names()
    print("Collections : ",collections)
    for t in req:
        for i in t:
            for col in collections:
                li = []
                for r in db[col].find({}, {"_id":0, "name": 1}):
                    li.append(r['name'])
                dict_of_val[col] = li

    template_header = list(dict_of_val.keys())

    return template_header,dict_of_val

def get_database(req,language):
    dict_of_val = {}
    try:
        client = MongoClient()
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    db = client.myproject
    db_german = client.myproject_german
    db_french = client.myproject_french
    db_spanish = client.myproject_spanish
    db_portugese = client.myproject_portugese
    db_italy = client.myproject_italy
    db_dutch = client.myproject_dutch
    db_polish = client.myproject_polish
    db_danish = client.myproject_danish

    if language == 'de':
        template_header,dict_of_val = language_seperator(req,db_german)

    if language == 'en':
        template_header,dict_of_val = language_seperator(req,db)

    if language == 'fr':
        template_header,dict_of_val = language_seperator(req,db_french)

    if language == 'es':
        template_header,dict_of_val = language_seperator(req,db_spanish)

    if language == 'pt':
        template_header,dict_of_val = language_seperator(req,db_portugese)

    if language == 'it':
        template_header,dict_of_val = language_seperator(req,db_italy)

    if language == 'nl':
        template_header,dict_of_val = language_seperator(req,db_dutch)

    if language == 'pl':
        template_header,dict_of_val = language_seperator(req,db_polish)

    if language == 'dk':
        template_header,dict_of_val = language_seperator(req,db_danish)

    return template_header,dict_of_val

    

    

