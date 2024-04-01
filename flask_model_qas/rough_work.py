import re



def return_without_quotes(x):
    y = []
    x = x[0]
    x  =  x.strip(']['' ').split(', ')
    for i in range(len(x)):
        match = re.search('[0-9]+',x[i])
        if match != None:
            y.append(match.group())

    x = [y]
    return x
        

x = ["['95', '66', '137', '70', '20']"]

print(return_without_quotes(x))