
# Telium - The game

import random

# Global variables
num_modules = 0                                          # The number of modules in the space station
module = 1                                               # The module of the space station we are in
last_module = 0                                          # The last module we were in
possible_moves = []                                      # List of the possible moves we can make
alive = True                                             # Whether the player is alive or dead
won = False                                              # Whether the player has won
power = 100                                              # The amount of power the space station has
fuel = 500                                               # The amount of fuel the player has in the flamethrower
locked = 0                                               # The module that has been locked by the player
queen = 0                                                # Location of the queen alien
vent_shafts = []                                         # Location of the ventilation shaft entrances
info_panels = []                                         # Location of the information panels
workers = []                                             # Location of the worker aliens


# Procedure declarations

def load_module():
    global module, possible_moves
    possible_moves = get_modules_from(module)
    output_module()
    
def get_modules_from(module):
    moves = []
    text_file = open("Charles_Darwin/module" + str(module) + ".txt", "r")
    for counter in range(0,4):
        move_read = text_file.readline()
        move_read = int(move_read.strip())
        if move_read != 0:
            moves.append(move_read)
    text_file.close()
    return moves

def output_module():
    global module
    print("\n----------------------------------------------------------------------------------")
    print("\nYou are in module", module, "\n")

def output_moves():
    global possible_moves
    print("\nFrom here you can move to modules: | ",end="") 
    for move in possible_moves:
        print(move,"| ", end="")

def get_action():
    global module, last_module, possible_moves
    valid_action = False
    while valid_action == False:
        print("What do you want to do next? (MOVE, SCANNER)") 
        action = input("> ").upper()
        if action == "MOVE":
            move = int(input("Enter the module to move to: "))
            if move in possible_moves:
                valid_action = True
                last_module = module
                module = move
            else:
                print("The module must be connected to the current module.")

def spawn_npcs():
    global num_modules, queen, vent_shafts, info_panels, workers
    
    module_set = []
    
    for counter in range(2, num_modules + 1):
        module_set.append(counter)

    random.shuffle(module_set)
    i = 0
    
    queen = module_set[i]
    
    for counter in range(0,3):
        i=i+1
        vent_shafts.append(module_set[i])

    for counter in range(0,2):
        i=i+1
        info_panels.append(module_set[i])

    for counter in range(0,3):
        i=i+1
        workers.append(module_set[i])

# Main program starts here

try:
    while True:
        num_modules += 1
        open("Charles_Darwin/module" + str(num_modules) + ".txt", "r")
except FileNotFoundError:
    num_modules -= 1


spawn_npcs()
print("Queen alien is located in module:", queen)
print("Ventilation shafts are located in modules:", vent_shafts)
print("Information panels are located in modules:",info_panels)
print("Worker aliens are located in modules:", workers)

while alive and not won:
    load_module()
    if won == False and alive == True:
        output_moves()
        get_action()

if won == True:
    print("The queen is trapped and you burn it to death with your flamethrower.\n\n")
    print("     *** You have survived ***")
if alive == False:
    print("The station has run out of power. Unable to sustain life support, you fall unconscious.")
    print("     *** You have died ***")