'''
    Old-School Adventure game based on text based interactive use. 

    This file contains the starter code for the game's Rooms, Puzzles and
    Monsters. Left to:do for the student: Build out the Item class.
    The rest of the framework can be extended, but works as-is
'''

'''
    class: Room
    Description:
    This class encapsulates all of the behavior for the "areas" in our
    virtual world. A room is a general idea; rooms might be anywhere
    the player can explore by stepping into them (e.g. closets, boxes)
    Each room has a description and can contain items. Some rooms
    may have a puzzle to solve or a "monster" (our monsters are cute,
    furry animals or toys) that protect the room. If a monster or puzzle
    is present, the user must "deactivate" said puzzle/monster before
    the full room description is presented to them
'''
    
class Room:
    def __init__(self, number = 0, name = 'n/a',
                 description = 'trapped!', adjacent = [], picture = '',
                 items = []):
        self.name = name
        self.number = number
        self.description = description
        self.adjacent_rooms = adjacent
        self.picture = picture
        self.items = items
        self.puzzles = []
        self.monsters = []
    def add_item(self, item): # add an item to the room
        self.items.append(item)
    def remove_item(self, item):
        self.items.remove(item)
    def add_puzzle(self, puzzle): # add a puzzle to the room
        self.puzzles.append(puzzle)
    def add_monster(self, monster): # add a monster to the room
        self.monsters.append(monster)
    def has_items(self):            # answer if the room has items or not
        return not (len(self.items) == 0)
    def has_puzzle(self):           # does the room have puzzles?
        return not (len(self.puzzles) == 0)
    def has_monsters(self):         # answer if monster is in the room
        return not (len(self.monsters) == 0)
    def reverse_effects(self):      # reverse effects of puzzle/monster
        for i in range(len(self.adjacent_rooms)):
            if self.adjacent_rooms[i] < 0: # blocked by a puzzle or monster
                self.adjacent_rooms[i] = 0 - self.adjacent_rooms[i] # make it open
    def contextual_description(self):
        if self.has_puzzle(): # puzzle blocks regular description. 
            for each in self.puzzles:
                if (each.target == self and
                    each.active and
                    each.affects_target):
                    return each.do_effect()
        if self.has_monsters():
            for each in self.monsters:
                if (each.target == self and
                    each.active and
                    each.affects_target):
                    return each.do_effect()
        # if no puzzles/monsters are active, return regular description
        return self.description 
    def __str__(self):
        return (str(self.number) + ':' + self.name + ':' + self.description)

'''
    class: Item
    Description:
    This class encapsulates all of the behavior for the "things" in our
    rooms. Items can be collected by the player by Taking them during
    their quest. Items also have a description that players can see when
    they Look at the item. Players can also Drop or Use items.
'''

class Item:
    def __init__(self, number = 0, name = 'n/a',
                 description = '', weight = 0, value = 0, use = 0):
        self.name = name
        self.number = number
        self.description = description
        self.weight = weight
        self.value = value
        self.use_remaining = use
        self.puzzle = ''
    def has_use_remaining(self):
        # if the item's use_remaining > 0, return True otherwise False
        if self.use_remaining > 0:
            return True
        elif self.use_remaining <= 0:
            return False
    def has_puzzle(self):
        # if self.puzzle == '' return False otherwise return True
        if self.puzzle == '':
            return False
        else:
            return True
    def use(self):
        if self.use_remaining > 0:
            self.use_remaining -= 1
            return(self.name, True)
        else:
            return (self.name, False)

        

'''
    class: Puzzle
    Description:
    This class encapsulates all of the behavior for the challenges in our
    rooms. Puzzle is a general term...right now it's not some hard problem
    to solve, but currently the use of some ITEM to "neutralize" the problem
    or monster the player encounters. E.g. a glass of water might neutralize
    a FIRE puzzle
    If puzzles are active, they occlude the regular description of a room
    Items neutralize puzzles and deactivate them
'''

class Puzzle:
    def __init__(self, name = 'n/a',description = '', target = '',
                 active = True, affects_target = False,
                 solution = '', effect = ''):
        self.name = name
        self.description = description
        self.active = active
        self.affects_target = affects_target
        self.solution = solution
        self.target = target
        self.effect = effect
    def activate(self):
        self.active = True
    def deactivate(self):
        self.active = False
    def is_active(self):
        return self.active
    def do_effect(self):
        return self.effect
    def try_to_solve(self, solution):
        if solution.upper() == self.solution.upper():
            self.deactivate()
            return True
        return False

'''
    class: Monster
    Description:
    This class is a subtype of Puzzle that can "attack" the user.
    All of our monsters are soft and furry creatures so they can't
    really hurt the user (no need for inducing PTSD in a computer game)
    Like their superclass, they occlude the regular room description
    until they are neutralized
'''

class Monster(Puzzle):
    def __init__(self, name = 'n/a',description = '', target = '',
                 active = True, affects_target = False,
                 solution = '', effect = '',
                 can_attack = True, attack = 'Cotton Balls'):
        super().__init__(name, description, target,
                         active, affects_target, solution, effect)
        self.can_attack = can_attack
        self.attack = attack
    def do_effect(self):
        return self.effect + '\n' + self.do_attack()
    def do_attack(self):
        return self.name + ' ' + self.attack
    def deactivate(self):
        self.active = False
    def defeated(self):
        return 'The ' + self.name + ' has been defeated. It is not moving.'

class Player:
    def __init__(self, items = []):
        self.items = items
    def add_items(self, item):
        self.items.append(item)
    def remove_items(self, item):
        self.items.remove(item)



def initialize_room():
    '''
    Does: Forms a dictionary of room objects for use in the game

    Returns: A dictionary containing each room in the game as
    an object.
    '''
    openfile = open('aquest_rooms.txt','r')
    lines = openfile.readlines()
    openfile.close()
    room = []
    rooms = {}
    for i in range(len(lines)):
        if i != 0:
            x = lines[i].strip('\n')
            y = x.split('|')
            room.append(y)

    for i in range(len(room)):
        room[i][3] = room[i][3].split()

    for i in range(len(room)):
        rooms[int(room[i][0])] = Room(int(room[i][0]),room[i][1],room[i][2],
                                      room[i][3],room[i][7],
                                      room[i][6].split(','))

    return rooms

def initialize_items():
    '''
    Does: Forms a dictionary of item objects for use in the game

    Returns: A dictionary containing each item in the game as
    an object.
    '''
    openfile = open('aquest_items.txt', 'r')
    lines = openfile.readlines()
    openfile.close()
    item = []
    items = {}
    for i in range(len(lines)):
        if i != 0:
            x = lines[i].strip('\n')
            y = x.split('|')
            item.append(y)

    for i in range(len(item)):
        items[item[i][1].upper()] = Item(int(item[i][0]), item[i][1].upper(),
                                         item[i][2],item[i][3], item[i][4],
                                         int(item[i][5]))
    return items

def initialize_monsters():
    '''
    Does: Forms a dictionary of monster objects for use in the game

    Returns: A dictionary containing each monster in the game as
    an object.
    '''
    openfile = open('puzzles_n_monsters.txt', 'r')
    lines = openfile.readlines()
    openfile.close()
    monster = []
    monsters = {}
    for i in range(len(lines)):
        if i != 0:
            if i < 3:
                x = lines[i].strip('\n')
                y = x.split('|')
                monster.append(y)

    for i in range(len(monster)):
        monsters[monster[i][0].upper()] = Monster(monster[i][0].upper(),monster[i][1],
                                                  monster[i][5],monster[i][2],
                                                  monster[i][3],
                                                  monster[i][4].upper(),monster[i][6],
                                                  monster[i][7],monster[i][8])
    
    return monsters
   
def initialize_puzzles():
    '''
    Does: Forms a dictionary of puzzle objects for use in the game

    Returns: A dictionary containing each puzzle in the game as
    an object.
    '''
    openfile = open('puzzles_n_monsters.txt', 'r')
    lines = openfile.readlines()
    openfile.close()
    puzzle = []
    puzzles = {}
    for i in range(len(lines)):
        if i != 0:
            if i >= 3:
                x = lines[i].strip('\n')
                y = x.split('|')
                puzzle.append(y)

    for i in range(len(puzzle)):
        puzzles[puzzle[i][0].upper()] = Puzzle(puzzle[i][0].upper(),puzzle[i][1],
                                               puzzle[i][5],puzzle[i][2],
                                               puzzle[i][3],puzzle[i][4].upper(),
                                               puzzle[i][6])
    return puzzles

def initialize_player():
    '''
    Does: Creates a player object for the game to keep track
    of items and progress.

    Returns: An object of Class Player.
    '''
    player = Player([])
    return player
