''' This file is any and all helper functions used by app.py '''

def fastest(dictionary):
    ''' function for iterating and working out fastest driver '''
    smallest = 20000
    fastest_person = []
    for x in dictionary:
        if float(dictionary[x][4]) < smallest:
            smallest = float(dictionary[x][4])
            fastest_person.clear()
            fastest_person.append(dictionary[x][1])
            fastest_person.append(dictionary[x][4])

    return fastest_person


def dict_creator(dataframe):
    ''' function for creating a dictionary from a pandas dataframe '''
    dictionary = {}
    for ind in dataframe.index:
        my_list = []
        for x in dataframe.iloc[ind]:
            my_list.append(x)
        dictionary[ind] = my_list

    return dictionary
