def USBdecode(data):
    flag = ''

    table = {
        "04":"a",
        "05":"b",
        "06":"c",
        "07":"d",
        "08":"e",
        "09":"f",
        "0a":"g",
        "0b":"h",
        "0c":"i",
        "0d":"j",
        "0e":"k",
        "0f":"l",
        "10":"m",
        "11":"n",
        "12":"o",
        "13":"p",
        "14":"q",
        "15":"r",
        "16":"s",
        "17":"t",
        "18":"u",
        "19":"v",
        "1a":"w",
        "1b":"x",
        "1c":"y",
        "1d":"z",
        "1e":"1",
        "1f":"2",
        "20":"3",
        "21":"4",
        "22":"5",
        "23":"6",
        "24":"7",
        "25":"8",
        "26":"9",
        "27":"0",
        "2d":"_",
        "2f":"{",
        "30":"}",
        }

    for line in data:
        if line[4:6] in table.keys():
            if line[0:2] == "20":
                flag = flag + table[line[4:6]].upper()
            else:
                flag = flag + table[line[4:6]]

    return flag


if __name__ == "__main__":
    with open("data") as f:
        lines = f.read()
        lines = lines.split("\n")
        lines = lines[:-1]

    flag = USBdecode(lines)
    print(flag)
