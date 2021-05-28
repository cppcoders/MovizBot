import pandas as pd
data = pd.read_csv('app/netflix_titles.csv')
data = data.astype('string')


def get_director(entity):
    data1 = data[data['director'].notna()]
    mask = data1['title'] == entity
    if(mask.any()):
        ans = 'The director of ' + entity + \
            ' is : ' + list(data1[mask]['director'])[0]
    else:
        ans = 'Sorry, couldn\'t find anything'
    return ans


def get_directed(entity):
    data1 = data[data['title'].notna()]
    mask = data1['director'] == entity
    if(mask.any()):
        ans = entity + ' directed : ['
        for movie in list(data1[mask]['title']):
            ans += movie
            ans += ', '
        ans += ']'
    else:
        ans = 'Sorry, couldn\'t find anything'
    return ans


def get_actors(entity):
    data1 = data[data['cast'].notna()]
    mask = data1['title'] == entity
    if(mask.any()):
        ans = entity + ' cast were : ['
        for movie in list(data1[mask]['cast']):
            ans += movie
            ans += ', '
        ans += ']'
    else:
        ans = 'Sorry, couldn\'t find anything'
    return ans


def get_acted(entity):
    data1 = data[data['title'].notna()]
    data1 = data1[data1['cast'].notna()]
    ans = entity + ' acted in : ['
    cnt = 0
    cnt2 = 0
    for i in data1['cast']:
        if(entity in i.split(", ")):
            ans += data1.iloc[cnt]['title']
            ans += ', '
            cnt2 += 1
        cnt += 1
    ans += ']'
    if cnt2 == 0:
        return 'Sorry, couldn\'t find anything'
    else:
        return ans


def get_year(entity):
    data1 = data[data['release_year'].notna()]
    mask = data1['title'] == entity
    if(mask.any()):
        ans = entity + ' was release on : ' + \
            list(data1[mask]['release_year'])[0]
    else:
        ans = 'Sorry, couldn\'t find anything'
    return ans


def get_story(entity):
    data1 = data[data['description'].notna()]
    mask = data1['title'] == entity
    if(mask.any()):
        ans = entity + ' story is : ' + list(data1[mask]['description'])[0]
    else:
        ans = 'Sorry, couldn\'t find anything'
    return ans


def get_duration(entity):
    data1 = data[data['duration'].notna()]
    mask = data1['title'] == entity
    if(mask.any()):
        ans = entity + ' duration is : ' + list(data1[mask]['duration'])[0]
    else:
        ans = 'Sorry, couldn\'t find anything'
    return ans


def get_type(entity):
    data1 = data[data['type'].notna()]
    mask = data1['title'] == entity
    if(mask.any()):
        ans = entity + ' is a ' + list(data1[mask]['type'])[0]
    else:
        ans = 'Sorry, couldn\'t find anything'
    return ans


def get_details(entity):
    mask = data['title'] == entity
    if(mask.any()):
        ans = entity + ' is a ' + list(data[mask]['type'])[0]
        ans += '\nwas released on (' + get_year(entity).split(' ')[-1] + ')'
        ans += '\ndirected by ' + get_director(entity).split(' ')[-1]
        ans += '\n' + get_story(entity)
        ans += '\nThe cast consist of ' + ' ' + get_actors(entity)
    else:
        ans = 'Sorry, couldn\'t find anything'
    return ans


def main_function(intent, entity):
    if(intent == 'get_director'):
        return get_director(entity)
    elif(intent == 'get_directed'):
        return get_directed(entity)
    elif(intent == 'get_actors'):
        return get_actors(entity)
    elif(intent == 'get_acted'):
        return get_acted(entity)
    elif(intent == 'get_year'):
        return get_year(entity)
    elif(intent == 'get_story'):
        return get_story(entity)
    elif(intent == 'get_details'):
        return get_details(entity)
    elif(intent == 'get_duration'):
        return get_duration(entity)
    elif(intent == 'get_type'):
        return get_type(entity)
    elif(intent == 'get_details'):
        return get_details(entity)
