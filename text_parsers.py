
def scanner_text_parser(command):
    if " " in command:
        split = command.split(" ")

        if len(split) > 2:
            return "INVALID"

        num = 0
        try:
            num = int(split[1])

            if num == 0:
                raise ValueError
        except ValueError:
            return ("INVALID", 0)
            
        
        if command[0:2] == "LO":
            return ("LOCK", num)
        elif command[0:2] == "LI":
            return ("LIFEFORMS", num)
        elif command[0] == "S":
            return ("SCAN", num)
        elif command[0] == "E":
            return ("EXIT", num)
    else:
        if command[0:2] == "LO":
            return ("LOCK", 0)
        elif command[0:2] == "LI":
            return ("LIFEFORMS", 0)
        elif command[0] == "S":
            return ("SCAN", 0)
        elif command[0] == "E":
            return ("EXIT", 0)

    return ("INVALID", 0)