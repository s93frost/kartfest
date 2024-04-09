def fastest(dict):
    smallest = 20000
    fastest_person = []
    for x in dict:
        if float(dict[x][4]) < smallest:
            smallest = float(dict[x][4])
            fastest_person.clear()
            fastest_person.append(dict[x][1])
            fastest_person.append(dict[x][4])

    return fastest_person


def dict_creator(dataframe):
    dict = {}
    for ind in dataframe.index:
        my_list = []
        for x in dataframe.iloc[ind]:
            my_list.append(x)
        dict[ind] = my_list

    return dict
