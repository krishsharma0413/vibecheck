import re

msg_pattern = re.compile(r"^\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - .*?:") # helps skip faltu lines

def text_file_parser(file_name:str) -> list[str]:
    texts = []
    with open(file_name, "r", encoding="utf8") as file:
        for x in file.readlines()[1:]:
            newtext = True
            if not msg_pattern.match(x):
                newtext = False
            
            if newtext:
                texts.append(x)
            else:
                texts[-1] += x
    
    return (texts)


def participants(texts: list[str]) -> list[str]:
    participants_found = 0
    parti = []
    i = 0
    while participants_found != 2:
        text = texts[i]
        a = text.split(" - ")[1]
        if len(a.split(":")) > 1:
            username = a.split(":")[0]
            if username not in parti:
                parti.append(username)
                participants_found += 1
        i += 1
    return parti 

if __name__ == "__main__":
    filename = input("enter filename: ")
    print("""
Testing Menu
------------
1. text_file_parser
2. participants       
""")
    filename = f"./personal_dataset/{filename}.txt"
    inp = input("enter: ")
    if inp == "1":
        all_texts = text_file_parser(filename)
        print(len(all_texts))
    elif inp == "2":
        all_texts = text_file_parser(filename)
        print(participants(all_texts))