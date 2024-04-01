import regex as re
def search_currency(x,language):
    for i in x:
        for j in i:
            for k in j:
                match = re.search(r'\p{Sc}' , k)
                if match != None:
                    x = match.group()
                    # print(x)
                    break

    dictionary_currency = {
        '₹' : "INR",
        '€' : "EUR",
        '$' : "USD"
    }

    dictionary_currency_language = {
        'de': 'EUR',
        'en': 'INR',
        'fr': 'EUR',
        'es': 'EUR',
        'pt':'EUR',
        'it':'EUR',
        'nl':'EUR',
        'pl':'EUR',
        'dk':'DKK'
    }


    if x == None:
        currency = dictionary_currency_language[language]
    else:
        for key,value in dictionary_currency.items():
            
            
            if key == x:
              currency =   dictionary_currency[key]
              break
            else:
                currency = dictionary_currency_language[language]
    
    return currency
