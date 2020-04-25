from room import *

MAX_WEIGHT = 10


def menu(message, options='N, S, E, W, I, T, D, U, L, Q'):
    '''
    This function creates a menu and checks for valid input

    Input: A message to be printed for the user.

    Output: The user input and a boolean value verifying if the
    input was valid or not.
    '''
    answer = input(message)
    answer = answer.upper()  # convert to uppercase for comparison
    if answer in options.upper():
        return answer, True
    else:
        return answer, False


def is_valid(answer, options='N, S, E, W, I, T, D, U, L, Q'):
    answer = answer.upper()
    if answer in options.upper():
        return True
    else:
        return False

def direction_check(direction, adjacent_rooms):
    '''
    This function evaluates whether the direction the player
    chooses is a valid option as per the rules of the game.

    Input: A string, containing the direction in which the
    player wishes to move. A list extracted from the MetaData
    that contains rules about entry into adjacent rooms.

    Output: Returns a boolean value that verifies if moving in
    a certain direction is allowed. An integer that indicates
    the number of the room.
    '''
    direction_lst = ['N', 'S', 'E', 'W']  # using a standard list as a measure to evaluate the input.
    # Indexing the input of the user against the direction_lst
    direction_index = direction_lst.index(direction)
    # Checking if the direction is accessible as per the game (i.e. has value > 0)
    if int(adjacent_rooms[direction_index]) > 0:
        return True, int(adjacent_rooms[direction_index])
    else:
        print('You cannot move in that direction')
        return False, 0


def walk_around(room_number, rooms):
    '''
    This function allows the user to walk around in the virtual
    space.

    Input: An integer representing the current room the user
    is in. Also takes a dictionary containing data of all rooms.

    Output: None! Prints important information that allows
    the user to move between rooms.
    '''
    room = rooms[room_number]  # Identifying the room
    print('You are now in room: ' + room.name)
    # Using the method of class Room to print information representing the room
    # and the situation of that room.
    print(room.contextual_description())
    # If statement that validates the presence of items in the room.
    if room.has_items():
        for each in room.items:
            print('A ' + each + ' is here in the room')


def pickup_items(player, rooms, items, room_no):
    '''
    This function allows the user to pick up items in a room.

    Input: An object of the class Player, Room and Item, and
    an integer value representing the number of the room.

    Output: Updated list of items belonging to the Class Player
    as well as updated items list for the Class Room
    '''
    user_take = input('Take which item?\n')  # gathering input.
    user_take = user_take.upper()  # Uppercase for compliance with data.
    total_weight = 0  # forming a counter for weight calculation.

    # Converting room items to uppercase for data compliance.
    for i in range(len(rooms[room_no].items)):
        rooms[room_no].items[i] = rooms[room_no].items[i].upper()
    # Try and except block to account for bad user_input.
    try:
        if user_take in rooms[room_no].items:
            player.items.append(user_take)
            for each in player.items:
                total_weight += int(items[each].weight)
            # Prevents carrying more weight that permissible.
            if total_weight <= MAX_WEIGHT:
                rooms[room_no].items.remove(user_take)
                print(user_take, ' has been added to the inventory\n')
            else:
                print('Sorry',
                      'you are carrying too much weight in your inventory')
                player.items.remove(user_take)

        return player.items, rooms[room_no].items
    except:
        print('Please enter a valid item')
        return player.items, rooms[room_no].items


def game_management_system(rooms, items, monsters, puzzles, player):
    '''
   This function manages the business end of the game.
   Ensures compliance with the rules and prints out all
   the important information the user needs to know.

   Input: 4 dictionaries containing class objects from
   rooms, items, monsters and puzzles. A class object
   from the class player.

   Output: None. Prints out all the required information
   and allows the user to play the game in it's entirety
    '''
    global name
    room_number = 1  # Starting the game in room 1.

    message = ('=======\n''Enter N, S, E or W to move in those directions.\n'
               'I for Inventory, L to look at something, U to use <an item>\n'
               'T to take <an item> or Q to Quit and exit the game\n')
    # Calling function to print description.
    walk_around(room_number, rooms)
    # Gathering user input and assessing validity.
    selection, validity = menu(message)

    while validity == False:  # If false
        selection, validity = menu(message)

    while selection != 'Q':  # Quit condition
        if selection == 'N':  # If user chooses North.
            # Checking for validity of input.
            check, facing = direction_check(selection,
                                            rooms[room_number].adjacent_rooms)
            if check:
                room_number = facing
            if not check:
                room_number = room_number
            # Printing updated room information.
            walk_around(room_number, rooms)
            selection, validity = menu(message)

        if selection == 'S':
            # Checking for validity of input.
            check, facing = direction_check(selection,
                                            rooms[room_number].adjacent_rooms)
            if check == True:
                room_number = facing
            elif check == False:
                room_number = room_number
            # Printing updated room information.
            walk_around(room_number, rooms)
            selection, validity = menu(message)

        if selection == 'E':
            # Checking for validity of input.
            check, facing = direction_check(selection,
                                            rooms[room_number].adjacent_rooms)
            if check == True:
                room_number = facing
            elif check == False:
                room_number = room_number
            # Printing updated room information.
            walk_around(room_number, rooms)
            selection, validity = menu(message)

        if selection == 'W':
            # Checking for validity of input.
            check, facing = direction_check(selection,
                                            rooms[room_number].adjacent_rooms)
            if check == True:
                room_number = facing
            elif check == False:
                room_number = room_number
            # Printing updated room information.
            walk_around(room_number, rooms)
            selection, validity = menu(message)

        if selection == 'T':
            # Using the function to pick up items.
            x, y = pickup_items(player, rooms, items, room_number)
            player.items = x  # Updating the Player Class attribute.
            rooms[room_number].items = y  # Updating the dictionary of rooms.
            # Printing updated room information.
            walk_around(room_number, rooms)
            selection, validity = menu(message)

        if selection == 'I':
            for each in player.items:  # Using Class Player method on the object.
                print('You have', each)
                print('-----------------------------------------')
            # Printing updated room information.
            walk_around(room_number, rooms)
            selection, validity = menu(message)

        if selection == 'L':
            looking = input('What would you like to look at?\n')
            looking = looking.upper()
            if looking in rooms[room_number].items:
                print('------------------------------------')
                print(items[looking].description, '\n')
            # Printing updated room information.
            walk_around(room_number, rooms)
            selection, validity = menu(message)

        if selection == 'D':
            drop_item = input('Which item do you want to drop?\n')
            drop_item = drop_item.upper()
            if drop_item in player.items:
                player.remove_items(drop_item)  # Removing from player's items.
                # Adding to the room's items.
                rooms[room_number].add_item(drop_item)
                print('You have dropped ', drop_item)
                print('-------------------------------------------')
            # Printing updated room information.
            walk_around(room_number, rooms)
            selection, validity = menu(message)

        if selection == 'U':
            use_item = input('Which item do you want to use?\n')
            use_item = use_item.upper()
            if len(player.items) > 0:  # User has items to use.
                # DEALING WITH PUZZLES.
                # If Room has a puzzle to solve.
                if rooms[room_number].has_puzzle():
                    try:
                        if use_item in player.items:
                            # Evaluating if the item can be used.
                            if items[use_item].has_use_remaining():
                                # Using the item. (Reduces use count)
                                name, validity = items[use_item].use()
                                if validity == True:
                                    for each in puzzles:
                                        if puzzles[each].solution == name:
                                            print('Success! You have used ',
                                                  name, 'on ', each)
                                            # Deactivating puzzle.
                                            puzzles[each].deactivate()
                                            # Removing effect from the room.
                                            rooms[room_number].reverse_effects()
                    # If there is a KeyError, that means the user
                    # entered an invalid item.
                    except KeyError:
                        print('Please enter a valid item')
                # DEALING WITH MONSTERS.
                elif rooms[room_number].has_monsters():
                    try:
                        if use_item in player.items:  # Validating item.
                            # If item can be used.
                            if items[use_item].has_use_remaining():
                                # Using the item. (Reduces use count)
                                name, validity = items[use_item].use()
                            if validity == True:
                                for each in monsters:
                                    if monsters[each].solution == name:
                                        # Monster is defeated
                                        defeat = monsters[each].defeated()
                                        print('Success! You have used ',
                                              name, 'on ',
                                              each)
                                        print(defeat)
                                        # Reversing the effects from the room.
                                        rooms[room_number].reverse_effects()
                                        # Deactivating the monster.
                                        monsters[each].deactivate()
                    # KeyError where there is bad input.
                    except KeyError:
                        print('Please enter a valid item')
            # Printing updated room information.
            walk_around(room_number, rooms)
            selection, validity = menu(message)
    # If the option is Quit, classifying the player.
    # Classification is based on the weight of items that the player has.
    classification_counter = 0
    for each in player.items:
        value = items[each].value  # weight for each item.
        classification_counter += int(value)
    if classification_counter >= 10000:
        print('Your classification: Seasoned Navigator!')
    elif classification_counter >= 1200:
        print('Your classification: Proficient Navigator!')
    elif classification_counter >= 5:
        print('Your classification: Novice Navigator')
    elif classification_counter == 0:
        print('Try harder, you can do this. We believe in you!')
    print('Your score is:', classification_counter)
    print('You have exited the game. Farewell, brave traveller!')


def main():
    # Initializing required data.
    rooms = initialize_room()
    items = initialize_items()
    monsters = initialize_monsters()
    puzzles = initialize_puzzles()
    player = initialize_player()

    # House keeping on the data, ensuring it complies with the requirements.
    for each in puzzles:
        if 'Room' in puzzles[each].target:
            element = puzzles[each].target.split()
            puzzles[each].target = rooms[int(element[1])]
            rooms[int(element[1])].add_puzzle(puzzles[each])
    for each in monsters:
        if 'Room' in monsters[each].target:
            element = monsters[each].target.split()
            monsters[each].target = rooms[int(element[1])]
            rooms[int(element[1])].add_monster(monsters[each])
    for each in rooms:
        if 'None' in rooms[each].items:
            rooms[each].items = []
    for each in rooms:
        for i in range(len(rooms[each].adjacent_rooms)):
            rooms[each].adjacent_rooms[i] = int(rooms[each].adjacent_rooms[i])
    for each in rooms:
        for i in range(len(rooms[each].items)):
            rooms[each].items[i] = rooms[each].items[i].upper()

    # Playing the game from the data.
    game_management_system(rooms, items, monsters, puzzles, player)


main()
