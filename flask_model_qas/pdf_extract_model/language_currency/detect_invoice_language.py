from langdetect import detect
import langid
from babel import Locale
from collections import Counter
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector

def get_lang_detector(nlp, name):
    return LanguageDetector()

def most_repeated_element(x):
    return max(set(x) , key = x.count)

def detect_language(req):
    list_of_string = []
    list_lang = []
    idx_menge = -1
    idx_summe = -1
    idx_dest = -1
    idx_prix = -1
    idx_tvq = -1
    idx_tps = -1
    idx_qunatite = -1
    idx_montant = -1
    idx_tva = -1
    idx_deseripeien = -1
    idx_importe = -1
    idx_cant = -1
    idx_unidades = -1
    idx_unicornio = -1
    idx_liebre = -1
    idx_artikel = -1
    idx_preis = -1
    idx_pos = -1
    idx_mwst = -1
    idx_rabatt = -1
    nlp = spacy.load("en_core_web_sm")
    Language.factory("language_detector", func=get_lang_detector)
    nlp.add_pipe('language_detector', last=True)


    for i in range(len(req)):
        for j in range(len(req[i])):
            for k in range(len(req[i][j])):
                if req[i][j][k] != '':
                    if re.search(r'-?\d+\.?\d*',req[i][j][k]) == None:
                        list_of_string.append(req[i][j][k])  


    # for i in range(len(req[0][0])):
    #     if req[0][0][i] != '':
    #         if re.search(r'-?\d+\.?\d*',req[0][0][i]) == None:
    #             list_of_string.append(req[0][0][i])


        for i in range(len(list_of_string)):
            list_of_string[i] = list_of_string[i].strip()
            # list_of_string[i] = list_of_string[i].encode("ascii" ,"ignore")
            # list_of_string[i] = list_of_string[i].decode()
            list_of_string[i] = list_of_string[i].capitalize()

    print(list_of_string)
    print("Collecting languages please wait......................100%")

    for i in range(len(list_of_string)):

        if list_of_string[i] == 'Menge':
            idx_menge = i

        if list_of_string[i] == 'Summe':
            idx_summe = i

        if list_of_string[i] == 'Artikel':
            idx_artikel = i

        if list_of_string[i] == 'Preis':
            idx_preis = i

        if list_of_string[i] == 'Pos':
            idx_pos = i

        if list_of_string[i] == 'Mwst' or list_of_string[i] == 'Mwst.':
            idx_mwst = i

        if list_of_string[i] == 'Rabatt':
            idx_rabatt = i

        if list_of_string[i] == 'Désignation':
            idx_dest = i

        if list_of_string[i] == 'Prix' or list_of_string[i] == 'Prix unite' or list_of_string[i] == 'Pu ht' or list_of_string[i] == 'Prix chf' or list_of_string[i] == 'Pu ttc'  :
            idx_prix = i

        if list_of_string[i] == 'Tvq':
            idx_tvq = i

        if list_of_string[i] == 'Tps':
            idx_tps = i

        if list_of_string[i] == 'Quantite' or list_of_string[i] == 'Total ht':
            idx_qunatite = i

        if list_of_string[i] == 'Montant' or list_of_string[i] == 'Montant ttc' or list_of_string[i] ==  'Remise(%)':
            idx_montant = i

        if list_of_string[i] == 'Tva':
            idx_tva = i

        if list_of_string[i] == 'Deseripeién':
            idx_deseripeien = i

        if list_of_string[i] == 'Importe':
            idx_importe = i

        if list_of_string[i] == 'Cant.' or list_of_string[i] == 'Cant' or list_of_string[i] == 'Cantidad' or list_of_string[i] == 'Canta. eas':
            idx_cant = i

        if list_of_string[i] == 'Unidades' or list_of_string[i] == 'Valor unitario':
            idx_unidades = i

        if list_of_string[i] == 'Unicornio' or list_of_string[i] == "% i.v.a":
            idx_unicornio  = i

        if list_of_string[i] == 'Liebre':
            idx_liebre = i
        
        lang = langid.classify(list_of_string[i])
        list_lang.append(lang[0])


        # doc = nlp(list_of_string[i])
        # list_lang.append(doc._.language['language'])
        
    
    if idx_menge != -1:
        list_lang[idx_menge] = 'de'  

    if idx_summe != -1:
        list_lang[idx_summe] = 'de'

    if idx_artikel != -1:
        list_lang[idx_artikel] = 'de'

    if idx_preis != -1:
        list_lang[idx_preis] = 'de'

    if idx_pos != -1:
        list_lang[idx_pos] = 'de'

    if idx_mwst != -1:
        list_lang[idx_mwst] = 'de'

    if idx_rabatt != -1:
        list_lang[idx_rabatt] = 'de'
    
    if idx_dest != -1:
        list_lang[idx_dest] = 'fr'   

    if idx_prix != -1:
        list_lang[idx_prix] = 'fr'

    if idx_tvq != -1:
        list_lang[idx_tvq] = 'fr'

    if idx_tps != -1:
        list_lang[idx_tps] = 'fr'

    if idx_qunatite != -1:
        list_lang[idx_qunatite] = 'fr'

    if idx_montant != -1:
        list_lang[idx_montant] = 'fr'

    if idx_tva != -1:
        list_lang[idx_tva] = 'fr'

    if idx_deseripeien != -1:
        list_lang[idx_deseripeien] = 'es'

    if idx_importe != -1:
        list_lang[idx_importe] = 'es'

    if idx_cant != -1:
        list_lang[idx_cant] = 'es'

    if idx_unidades != -1:
        list_lang[idx_unidades] = 'es'

    if idx_unicornio != -1:
        list_lang[idx_unicornio] = 'es'

    if idx_liebre != -1:
        list_lang[idx_liebre] = 'es'

    

    print("Languages Detected please wait......................100%")
    # print(list_of_string)
    # print(list_lang)

    res = {list_of_string[i]: list_lang[i] for i in range(len(list_of_string)) }

    print(res)

    print("--------------------------------------------Language Count----------------------------------------------------------")
    print(Counter(list_lang))

    language = most_repeated_element(list_lang)

    l = Locale.parse(language)
    l = l.get_display_name('en_US')
    print("The Language detected here is" , l)

    


    return language
