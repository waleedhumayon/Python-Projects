import unittest
from room import*

class TestRoom(unittest.TestCase):


    def test_room(self):
        room = initialize_room()

        self.assertEqual(room[3].monsters, [])
        self.assertEqual(room[1].items, ['Hair Clippers'])

    def test_items(self):
        items = initialize_items()

        self.assertEqual(items['MOD_2'].weight, '0')
        self.assertTrue(items['HAIR CLIPPERS'].use_remaining, True)
        self.assertNotEqual(items['THUMB DRIVE'].value, 100) # 100 is a string.

    def test_monsters(self):
        monster = initialize_monsters()

        self.assertTrue(monster['RABBIT'].can_attack, 'T')
        self.assertNotEqual(monster['TEDDY BEAR'].affects_target, 'F')

    def test_puzzles(self):
        puzzle = initialize_puzzles()

        self.assertTrue(puzzle['RECURSION'].active, 'T') # checking status
        self.assertTrue(puzzle['USB'].deactivate,True) # checking deactivation
        self.assertEqual(puzzle['DARKNESS'].active, 'T')

    def test_player(self):
        player = initialize_player()

        self.assertEqual(player.items, [])

def main():
    unittest.main(verbosity = 3)
main()
