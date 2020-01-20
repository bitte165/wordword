import os, re, requests, json
from datetime import datetime

def cls():
    import subprocess, platform

    if platform.system() == "Windows":
        subprocess.Popen("cls",
                         shell=True).communicate()
    else:  # Linux and Mac
        print("\033c", end="")

class create_menu:
    def __init__(self, text, menu):
        self.text = text
        self.menu = menu
        print(text)
        for i, option in enumerate(menu):

            menunum = i + 1
            # Check to see if this line has the 'return to main menu' code
            match = re.search("0D", option)
            # If it's not the return to menu line:
            if not match:
                if menunum < 10:
                    print(('   %s) %s' % (menunum, option)))
                else:
                    print(('  %s) %s' % (menunum, option)))
            else:
                print('\n  99) Return to Main Menu\n')
        return

main_text = " Select from the menu:\n"

main_menu = ['Social-Engineering Attacks',
             'Penetration Testing (Fast-Track)',
             'Third Party Modules',
             'Update the Social-Engineer Toolkit',
             'Update SET configuration',
             'Help, Credits, and About']

def title(extended=False):
    print(r"""\
    
                 _    _               _        _    _               _ 
                | |  | |             | |      | |  | |             | |
                | |  | | ___  _ __ __| |______| |  | | ___  _ __ __| |
                | |/\| |/ _ \| '__/ _` |______| |/\| |/ _ \| '__/ _` |
                \  /\  / (_) | | | (_| |      \  /\  / (_) | | | (_| |
                 \/  \/ \___/|_|  \__,_|       \/  \/ \___/|_|  \__,_|
    
    
            """)

    if extended:
        print("Welcome to Word-Word!\n")

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
        definitions[word] = defs
        definitions.sort()

        pos = set([i['partOfSpeech'] for i in defs])

        return pos

    elif resp_stat == 404:
        return "notaword"

    else:
        print(resp_stat)
        raise Warning

def sortWords(contents):
    for k, v in enumerate(contents):
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




def main():
    title(True)

    number_of_dbs = len(os.listdir(path="dbs")) - 1   # checks if there are any existing databasescd ..
    isEmpty = True
    for i in range(number_of_dbs):
        name = "db_" + i + ".json"
        with open(name) as openfile:
            openfile = openfile.read()
            if openfile == "":
                continue
            else:
                break
                isEmpty = False

    if isEmpty:
        print("Apparently, there are no any word databases saved.")
        filename = str(input("Please, enter the name of the file with words (either .txt or .json): "))

        filename_pattern = re.compile(r"([a-zA-Z0-9\s_\\.\-\(\):])+(.txt|.json)$")
        match = filename_pattern.match(filename)
        extension = match.group(2)

        if extension == ".txt":
            with open(filename, "r+") as f:
                contents = f.readlines()
        elif extension == ".json":
            with open(filename, "r+") as json_file:
                contents = json.load(json_file)

        print("\n Successfully loaded the file.\n")

        



if __name__ == "__main__":
    main()