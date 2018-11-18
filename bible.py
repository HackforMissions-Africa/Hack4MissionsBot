import json
import requests
import sys
sys.path.insert(0, '/home/bots/')
import simi
import random
import configparser



def read_bible(  ):
    with open("/home/bots/hack4missions/en_kjv.json", 'rb') as e:
        bible = json.loads(e.read())
    return bible

    # for book in bible:
    #     print( book['abbrev'], 'has', len(book['chapters']), 'chapters' )
    #     # for chapter in book['chapters']:
    #     #     # print first verse
    #     #     print(chapter[0])


def read_users():
    users = simi.xload("/home/bots/test_users.bot")
    return users


def post_to_graph(user_id, bible_verse):
    reply_data = {
        "recipient": {"id": user_id},
        "message": {"text": bible_verse}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=reply_data)

    return resp


def get_verse():
    try:
        bible = read_bible()
        print(len(bible))
        random_book = bible[ random.choice( range(1, len(bible)) ) ]
        print(random_book['name'], 'random_book')
        random_chapter = random.choice( range(1,  len(random_book['chapters']) ) )
        print(random_chapter, 'random_chapter')
        random_verse = random.choice( range(1, random_chapter ) )
        print(random_verse, 'random_verse')
        verse = random_book['chapters'][random_chapter][random_verse]
        result_list = ['*DAILY DEVOTION*:\n\n', random_book['name'], 'chapter', random_chapter, 'verse', random_verse, ':: ', verse]
        msg = " ".join([str(s) for s in result_list])
        print('MESSAGE:', msg)
        return msg

    except Exception as e:
        # raise e
        print(e)
        main()


def main():
    bible_verse = get_verse()
    users = read_users()
    for user_id in users:
        resp = post_to_graph(user_id, bible_verse)
        print(json.loads(resp.content))

    try:
        json.loads(resp.content)['error']
        main()
    except Exception as e:
        print(e)



if __name__ == '__main__':
    # credentials have been moved to a config file to remove them from public github visibility
    config = configparser.ConfigParser()
    config.read("/home/bots/config.ini")
    ACCESS_TOKEN = config.get('Creds', 'ACCESS_TOKEN')
    VERIFY_TOKEN = config.get('Creds', 'VERIFY_TOKEN')
