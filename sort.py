import requests, json
from datetime import datetime
word_db = []

def getPOS(word):
    url = "https://wordsapiv1.p.rapidapi.com/words/" + word + "/definitions"

    headers = {
        'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
        'x-rapidapi-key': "0c2910eee0mshd939f61fc8d5ab1p1532cfjsna210d387f491"
    }

    response = requests.request("GET", url, headers=headers)

    resp_stat = response.status_code

    if resp_stat == 200:
        json_data = response.text
        data = json.loads(json_data)

        defs = data['definitions']
        pos = [i['partOfSpeech'] for i in defs]
        pos = set(pos)

        return pos
    elif resp_stat == 404:
        return "notaword"
    else:
        print(resp_stat)
        raise Warning

def main():
    with open('db.json') as json_file:
        word_db = json.load(json_file)

    file_name = str(input("Enter the word list file name: "))

    with open(file_name, "r+") as f:
        contents = f.readlines()

    for k,v in enumerate(contents):
        x = v.lower()
        x = x.replace("\n", "")
        x = x.strip()
        contents[k] = x

    contents.sort()

    for word in contents:
        poses = getPOS(word)
        if type(poses) is set:
            first_letter = word[0].upper()
            for pos in poses:
                try:
                    word_db[first_letter][pos].append(word)
                except KeyError:
                    word_db["errors and exceptions"].append(word)
                    print(word.title() + " is added to the exceptions list.")
                    word_db["errors and exceptions"].sort()
                else:
                    print(word.title() + " added successfully.")
                    word_db[first_letter][pos].sort()
        elif type(poses) is str:
            word_db["not words"].append(word)
            print(word.title() + " is not a word!")
            word_db["not words"].sort()

    print("Writing to a dump JSON file...")
    name = 'JSON_output_database_' + datetime.strftime(datetime.now(), "%Y-%m-%d_%H.%M.%S" + ".json")
    with open(name, 'w+') as outfile:
        json.dump(word_db, outfile)
    print("Done! The name of your database is " + name)


if __name__ == "__main__":
    main()