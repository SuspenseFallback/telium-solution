
# Telium - The game

import random
from text_parsers import scanner_text_parser, movement_text_parser
from custom_print import custom_print
from better import main

# Global variables

num_modules = 0  # The number of modules in the space station
module = 1 # The module of the space station we are in
last_module = 0  # The last module we were in
possible_moves = []  # List of the possible moves we can make
alive = True # Whether the player is alive or dead
won = False # Whether the player has won
power = 100 # The amount of power the space station has
fuel = 500  # The amount of fuel the player has in the flamethrower
locked = 0  # The module that has been locked by the player
queen = 0  # Location of the queen alien
vent_shafts = [] # Location of the ventilation shaft entrances
info_panels = [] # Location of the information panels
workers = [] # Location of the worker aliens
scan_cost = 5 # cost of scanning
lifeforms_cost = 8 # cost of scanning for lifeforms


# Procedure declarations

def load_module():
    global module, possible_moves
    possible_moves = get_modules_from(module)
    output_module()
    
def get_modules_from(module):
    moves = []
    text_file = open("Charles_Darwin/module" + str(module) + ".txt", "r")
    for counter in range(0,4):
        move_read = int(text_file.readline().strip())
        if move_read != 0:
            moves.append(move_read)
    
    text_file.close()
    return moves

def output_module():
    global module
    custom_print("\n" + ("-"*50))
    custom_print("\nYou are in module", module, "\n")

def output_moves():
    global possible_moves
    custom_print("\nFrom here you can move to modules ",end="") 
    custom_print(", ".join([str(move) for move in possible_moves]), end=". ")

def scan():
    global power, scan_cost

    confirm = ""
    while confirm == "":
        confirm = input(f"This command will take {scan_cost} power. Are you sure? (y/n) ").lower()

        if confirm != "y" and confirm != "n":
            custom_print("Please enter a valid operation.\n")
            confirm = ""

    if confirm == "y":
        power -= scan_cost
        custom_print("Scanning...")
        custom_print("The queen is in module", queen, end=".\n")
        custom_print("Current power is", power, end=".\n")

def lifeforms():
    global power, lifeforms_cost
    
    confirm = ""
    while confirm == "":
        confirm = input(f"This command will take {lifeforms_cost} power. Are you sure? (y/n) ").lower()

        if confirm != "y" and confirm != "n":
            custom_print("Please enter a valid operation.\n")
            confirm = ""
            
    if confirm == "y":
        power -= lifeforms_cost
        custom_print("Scanning...")
        custom_print("The queen is in module", queen, end=".\n")
        custom_print("The worker aliens are in modules", workers, end=".\n")

def scanner():
    global power, scan_cost
    
    custom_print("Scanner ready.\n")
    command = ""
    while command == "":
        command = input("Enter command (LOCK, SCAN, LIFEFORMS, EXIT): ").upper()

        res = scanner_text_parser(command)
        command = res[0]
        num = res[1]

        if command == "LOCK":
            lock(num)
        elif command == "SCAN":
            scan()
        elif command == "LIFEFORMS":
            lifeforms()
        elif command == "EXIT":
            custom_print("Cancelling...")
        else:
            custom_print("Invalid operation. Please try again.\n")
            command = ""

def get_action():
    global module, last_module, possible_moves

    options = ["MOVE"]
    if module in info_panels:
        options.append("SCANNER")

    valid_action = False
    while valid_action == False:
        custom_print(f"What do you want to do next? ({', '.join(options)})") 
        action = input("> ").upper()
        command, num = movement_text_parser(action)
        tried = False
        
        if command == "MOVE":
            move = num if (num > 0 and (not tried)) else int(input("Enter the module to move to: "))
            if move in possible_moves:
                valid_action = True
                last_module = module
                module = move
            else:
                custom_print("The module must be connected to the current module.")
        elif command == "SCANNER":
            scanner()

def spawn_npcs():
    global num_modules, queen, vent_shafts, info_panels, workers
    module_set = []
    
    for counter in range(2, num_modules + 1):
        module_set.append(counter)

    random.shuffle(module_set)
    i = 0
    queen = module_set[i]
    
    for counter in range(3):
        i += 1
        vent_shafts.append(module_set[i])

    for counter in range(2):
        i += 1
        info_panels.append(module_set[i])

    for counter in range(3):
        i += 1
        workers.append(module_set[i])

def check_info_panel():
    if module in info_panels:
        custom_print("You see an information panel.")

def check_vent_shafts():
    global num_modules, module, vent_shafts, fuel
    if module in vent_shafts:
        custom_print("There is a bank of fuel cells here.", "You load one into your flamethrower.", sep="\n")
        fuel_gained = random.choice([20, 30, 40, 50])
        custom_print("Fuel was",fuel,"now reading:",fuel+fuel_gained)
        fuel = fuel + fuel_gained
        custom_print("The doors suddenly lock shut.", "What is happening to the station?", "Our only escape is to climb into the ventilation shaft.", "We have no idea where we are going.", "We follow the passages and find ourselves sliding down.", sep="\n")
        last_module = module
        module = random.choice([i for i in range(1, num_modules) if i not in vent_shafts])
        load_module()

def lock(num):
    global num_modules, power, locked
    new_lock = ""
    tried = False
    while new_lock == "":
        try:            
            new_lock = num if not tried else int(input("Enter module to lock: "))

            # If module number is invalid
            if new_lock < 0 or new_lock > num_modules or new_lock == queen or new_lock == lock:
                raise ValueError
        except ValueError:
            # Invalid operation
            custom_print("Operation failed. Unable to lock module. Try again.")
            new_lock = ""

    locked = new_lock
    custom_print("Aliens cannot get into module", locked)
    power_used = 25 + 5 * random.randint(0,5)
    power -= power_used

def move_queen():
    global num_modules, module, last_module, locked, queen, won, vent_shafts
    # If we are in the same module as the queen...
    if module == queen:
        custom_print("There it is! The queen alien is in this module...")

        # Decide how many moves the queen should take
        moves_to_make = random.randint(1,3)
        can_move_to_last_module = False
        while moves_to_make > 0:
            # Get the escapes the queen can make
            escapes = get_modules_from(queen)

            # Remove the current module as an escape
            if module in escapes:
                escapes.remove(module)

            # Allow queen to double back behind us from another module
            if last_module in escapes and can_move_to_last_module == False:
                escapes.remove(last_module)

            # Remove a module that is locked as an escape
            if locked in escapes:
                escapes.remove(locked)

            # If there is no escape then player has won...
            if len(escapes) == 0:
                won = True
                moves_to_make = 0
                custom_print("...and the door is locked. It's trapped.")
            # Otherwise move the queen to an adjacent module
            else:
                if moves_to_make == 1:
                    custom_print("...and has escaped.")
                queen = random.choice(escapes)
                moves_to_make = moves_to_make - 1
                can_move_to_last_module = True
                # Handle the queen being in a module with a ventilation shaft
                while queen in vent_shafts:
                    if moves_to_make > 1:
                        custom_print("...and has escaped.")
                    custom_print("We can hear scuttling in the ventilation shafts.")

                    valid_moves = [i for i in range(1, num_modules) if i not in vent_shafts and i != locked]
                    queen = random.choice(valid_moves)

                    # Queen always stops moving after travelling through shaft
                    moves_to_make = 0

def intuition():
    global possible_moves, workers, vent_shafts, info_panels
    workers_seen, vent_seen, info_seen = 0, 0, 0
    # Check what is in each of the possible moves
    for connected_module in possible_moves:
        # Workers are nearby
        if connected_module in workers:
            workers_seen += 1
            
            custom_print("I can hear something small moving around near me.") if workers_seen == 1 else custom_print("That sounds like another worker!")

        # Vent shaft is nearby
        if connected_module in vent_shafts:
            vent_seen += 1
            custom_print("I can feel cold air!") if vent_seen == 1 else custom_print("Brr. It's really really cold. Whirring sounds come from nearby.")

        # Queen is nearby
        if connected_module == queen:
            custom_print("Listen... did you hear that? It sounded big...")

        # Info panel is nearby
        if connected_module in info_panels:
            if not info_seen:
                custom_print("There is a panel in a nearby room. We could use it to find lifeforms.")
                info_seen = 1

def worker_aliens():
    global module, workers, fuel, alive, vent_shafts
    # Output alien encountered
    if module in workers:
        custom_print("Startled, a young alien scuttles across the floor.")
        custom_print("It turns and leaps towards us.")
        # Get the player's action
        successful_attack = False
        while successful_attack == False:
            custom_print("You can:")
            custom_print()
            custom_print("- Short blast your flamethrower to frighten it away.")
            custom_print("- Long blast your flamethrower to try to kill it.")
            custom_print("- RUN!")
            custom_print()
            custom_print("How will you react? (S, L, R)")
            action = 0
            while action not in ("S", "L", "R"):
                action = input("Press the trigger: ").upper()
            if action == "R":
                custom_print("You burst out of the module...")
                if last_module in vent_shafts:
                    last_module = module
                    module = random.choice(possible_moves)
                else:
                    module, last_module = last_module, module
            while fuel_used == 0 or fuel_used > fuel:
                fuel_used = int(input("How much fuel will you use? ...")).upper()
                if fuel_used > fuel:
                    custom_print("There isn't enough charge!")
                elif fuel_used <= 0:
                    custom_print("Har har.")
                else:
                    break

            fuel = fuel - fuel_used        
            # Check if player has run out of fuel
            if fuel <= 0:
                alive = False
                return

            # Work out how much fuel is needed
            if action == "S":
                fuel_needed = 30 + 10*random.randint(0,5)
            if action == "L":
                fuel_needed = 90 + 10*random.randint(0,5)

            # Try again if not enough fuel was used
            if fuel_used >= fuel_needed:
                successful_attack = True
            else:
                custom_print("The alien squeals but is not dead. It's angry.")

        # Successful action
        if action == "S":
            custom_print("The alien scuttles away into the corner of the room.")

        if action == "L":
            custom_print("The alien has been destroyed.")
            # Remove the worker from the module
            workers.remove(module)
        custom_print()

# Main program starts here

try:
    while True:
        num_modules += 1
        open("Charles_Darwin/module" + str(num_modules) + ".txt", "r")
except FileNotFoundError:
    num_modules -= 1

main()

spawn_npcs()
custom_print("Queen alien is located in module", queen)
custom_print("Ventilation shafts are located in modules", vent_shafts)
custom_print("Information panels are located in modules",info_panels)
custom_print("Worker aliens are located in modules", workers)

while alive and not won:
    load_module()
    check_vent_shafts()
    move_queen()
    worker_aliens()
    check_info_panel()
    intuition()
    if won == False and alive == True:
        output_moves()
        get_action()

if won == True:
    custom_print("The queen is trapped and you burn it to death with your flamethrower.\n\n")
    custom_print("     *** You have survived ***")

if alive == False:
    custom_print("The station has run out of power. Unable to sustain life support, you fall unconscious.\n\n")
    custom_print("     *** You have died ***")