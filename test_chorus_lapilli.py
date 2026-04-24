#!/usr/bin/env python3
import unittest
import os
import sys
import argparse
import subprocess
import unittest
import urllib.request


class TestChorusLapilli(unittest.TestCase):
    '''Integration testing for Chorus Lapilli

    This class handles the entire react start up, testing, and take down
    process. Feel free to modify it to suit your needs.
    '''

    # ========================== [USEFUL CONSTANTS] ===========================

    # Vite default startup address
    VITE_HOST_ADDR = 'http://localhost:5173'

    # XPATH query used to find Chorus Lapilli board tiles
    BOARD_TILE_XPATH = '//button[contains(@class, \'square\')]'

    # Sets of symbol classes - each string contains all valid characters
    # for that particular symbol
    SYMBOL_BLANK = ''
    SYMBOL_X = 'Xx'
    SYMBOL_O = '0Oo'

    # ======================== [SETUP/TEARDOWN HOOKS] =========================

    @classmethod
    def setUpClass(cls):
        '''This function runs before testing occurs.

        Bring up the web app and configure Selenium
        '''

        env = dict(os.environ)
        env.update({
            # Prevent React from starting its own browser window
            'BROWSER': 'none',
        })

        subprocess.run(['npm', 'install'],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           env=env,
                           check=True)

        # Await Webserver Start
        cls.vite = subprocess.Popen(
            ['npm', 'run', 'dev'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=env)

        if cls.vite.stdout is None:
            raise OSError("Vite failed to start")
        for _ in cls.vite.stdout:
            try:
                with urllib.request.urlopen(cls.VITE_HOST_ADDR):
                    break

            except IOError:
                pass

            # Ensure Vite does not terminate early
            if cls.vite.poll() is not None:
                raise OSError('Vite terminated before test')
        if cls.vite.poll() is not None:
            raise OSError('Vite terminated before test')

        cls.driver = Browser()
        cls.driver.get(cls.VITE_HOST_ADDR)
        cls.driver.implicitly_wait(0.5)

    @classmethod
    def tearDownClass(cls):
        '''This function runs after all testing have run.

        Terminate Vite and take down the Selenium webdriver.
        '''
        cls.vite.terminate()
        cls.vite.wait()
        cls.driver.quit()

    def setUp(self):
        '''This function runs before every test.

        Refresh the browser so we get a new board.
        '''
        self.driver.refresh()

    def tearDown(self):
        '''This function runs after every test.

        Not needed, but feel free to add stuff here.
        '''

    # ========================== [HELPER FUNCTIONS] ===========================

    def assertBoardEmpty(self, tiles):
        '''Checks if all board tiles are empty.

        Arguments:
          tiles: List[WebElement] - a board consisting of 9 buttons elements
        '''
        if len(tiles) != 9:
            raise AssertionError('tiles is not a 3x3 grid')
        for i, tile in enumerate(tiles):
            if tile.text.strip():
                raise AssertionError(f'tile {i} is not empty: '
                                     f'\'{tile.text}\'')

    def assertTileIs(self, tile, symbol_set):
        '''Checks if a certain tile has a certain symbol.

        Arguments:
          tile: WebElement - the button element to check
          symbol_set: str - a string containing all the valid symbols
        Raises:
          AssertionError - if tile is not in the symbol set
        '''
        if symbol_set is None:
            return
        if symbol_set == self.SYMBOL_BLANK:
            name = 'BLANK'
        elif symbol_set == self.SYMBOL_X:
            name = 'X'
        elif symbol_set == self.SYMBOL_O:
            name = 'O'
        else:
            name = 'in symbol_set'
        text = tile.text.strip()
        if ((symbol_set == self.SYMBOL_BLANK and text)
                or (symbol_set != self.SYMBOL_BLANK and not text)
                or text not in symbol_set):
            raise AssertionError(f'tile is not {name}: \'{tile.text}\'')


# =========================== [ADD YOUR TESTS HERE] ===========================

    def test_new_board_empty(self):
        '''Check if a new game always starts with an empty board.'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        self.assertBoardEmpty(tiles)

    def test_button_click(self):
        '''Check if clicking the top-left button adds an X.'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        self.assertTileIs(tiles[0], self.SYMBOL_BLANK)
        tiles[0].click()
        self.assertTileIs(tiles[0], self.SYMBOL_X)

    # [GenAI Use] Prompt: "write a test for my chorus lapilli game that checks X and O take turns correctly during the placement phase — click 4 different squares and check that the first and third are X and the second and fourth are O"
    # [GenAI Use] LLM Response Start
    def test_alternating_turns(self):
        '''Check that X and O alternate correctly during placement.'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        tiles[0].click()  # X
        tiles[1].click()  # O
        tiles[2].click()  # X
        tiles[3].click()  # O
        self.assertTileIs(tiles[0], self.SYMBOL_X)
        self.assertTileIs(tiles[1], self.SYMBOL_O)
        self.assertTileIs(tiles[2], self.SYMBOL_X)
        self.assertTileIs(tiles[3], self.SYMBOL_O)
    # [GenAI Use] LLM Response End
    # [GenAI Use] Reflection: The test clicks 4 distinct squares and checks that they alternate X, O, X, O, it's exactly what I asked for. It uses assertTileIs with the right constants. I ran it and it passed, confirming the alternation logic in handleClick works as expected.

    # [GenAI Use] Prompt: "write a test that clicks the same square twice, first click should place X, second click is O's turn but the square is already taken so nothing should change, assert the square still shows X"
    # [GenAI Use] LLM Response Start
    def test_filled_square_not_overwritten(self):
        '''Check that clicking an occupied square does not overwrite it.'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        tiles[0].click()       # X places at 0
        tiles[0].click()       # O tries to click same square — should have no effect
        self.assertTileIs(tiles[0], self.SYMBOL_X)
    # [GenAI Use] LLM Response End
    # [GenAI Use] Reflection: Clean and minimal. The second click on an occupied square maps to the `if (squares[i]) return;` guard in my placement-phase code, so the square should stay as X. Test passed and confirmed that guard works.

    # [GenAI Use] Prompt: "write a test where X wins by filling the top row (with O filling row 2), then try clicking an empty square after the win and assert that square stays blank, the game should be frozen after a win"
    # [GenAI Use] LLM Response Start
    def test_winner_stops_game(self):
        '''Check that no moves are accepted after a player wins.'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        # X wins top row: X at 0,1,2; O at 3,4
        tiles[0].click()  # X
        tiles[3].click()  # O
        tiles[1].click()  # X
        tiles[4].click()  # O
        tiles[2].click()  # X wins
        # Clicking an empty square after win should have no effect
        tiles[5].click()
        self.assertTileIs(tiles[5], self.SYMBOL_BLANK)
    # [GenAI Use] LLM Response End
    # [GenAI Use] Reflection: I verified the click sequence manually where X gets 0, 1, 2 (top row) and O gets 3, 4, so X wins on the 5th click with no accidental win before that. The post-win click tests the `if (calculateWinner(squares)) return;` early exit at the top of handleClick. Test passed.

    # [GenAI Use] Prompt: "write a test that places 3 X pieces and 3 O pieces without triggering a win to enter full board, then selects one of X's pieces and moves it to an empty adjacent square, and asserts the old square is now blank and the new square shows X"
    # [GenAI Use] LLM Response Start
    def test_movement_phase(self):
        '''Check that after 6 placements pieces can be moved to adjacent squares.'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        # Place without winning: X at 0,7,1 — O at 3,4,8
        tiles[0].click()  # X
        tiles[3].click()  # O
        tiles[7].click()  # X
        tiles[4].click()  # O
        tiles[1].click()  # X
        tiles[8].click()  # O — full board condition begins
        # X's turn: select X at 1 (row 0, col 1), move to 2 (row 0, col 2) — adjacent
        tiles[1].click()  # select
        tiles[2].click()  # move
        self.assertTileIs(tiles[1], self.SYMBOL_BLANK)
        self.assertTileIs(tiles[2], self.SYMBOL_X)
    # [GenAI Use] LLM Response End
    # [GenAI Use] Reflection: I double-checked that the placement sequence (X at 0,7,1 and O at 3,4,8) produces no winner, and that indices 1 and 2 are adjacent (same row, adjacent columns). The test exercises the full board else branch in handleClick. It passed and confirmed pieces move correctly.

    # [GenAI Use] Prompt: "write a test for the center constraint rule: place pieces so X ends up with a piece at center (index 4) after the full board starts, then have X try to move a different piece to a square that doesn't win the game, and assert both squares are unchanged since the move should be blocked"
    # [GenAI Use] LLM Response Start
    def test_center_constraint(self):
        '''Check that a player with a piece at center must move it or win.'''
        tiles = self.driver.find_elements(By.XPATH, self.BOARD_TILE_XPATH)
        # X at 0,4,6 — O at 1,5,8 (no winner yet)
        tiles[0].click()  # X
        tiles[1].click()  # O
        tiles[4].click()  # X (center)
        tiles[5].click()  # O
        tiles[6].click()  # X
        tiles[8].click()  # O — full board condition begins
        # X has center (4). X tries to move piece at 0 to 3:
        # that doesn't win and doesn't vacate center, should be blocked.
        tiles[0].click()  # select X at 0
        tiles[3].click()  # attempt move to 3 (invalid)
        self.assertTileIs(tiles[0], self.SYMBOL_X)   # X still at 0
        self.assertTileIs(tiles[3], self.SYMBOL_BLANK)  # 3 still empty
    # [GenAI Use] LLM Response End
    # [GenAI Use] Reflection: I traced through the placement to confirm X has pieces at 0, 4, 6 and O at 1, 5, 8 with no winner. Moving X from 0 to 3 is geometrically adjacent (row 0 col 0 → row 1 col 0), so it would normally be valid — but the center constraint blocks it since it neither vacates index 4 nor produces a win. The test correctly isolates that specific guard in the code, and it passed.


# ================= [DO NOT MAKE ANY CHANGES BELOW THIS LINE] =================

if __name__ != '__main__':
    from selenium.webdriver import Firefox as Browser
    from selenium.webdriver.common.by import By
else:
    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description='Chorus Lapilli Tester')
    parser.add_argument('-b',
                        '--browser',
                        action='store',
                        metavar='name',
                        choices=['firefox', 'chrome', 'safari'],
                        default='firefox',
                        help='the browser to run tests with')
    parser.add_argument('-c',
                        '--change-dir',
                        action='store',
                        metavar='dir',
                        default=None,
                        help=('change the working directory before running '
                              'tests'))

    # Change the working directory
    options = parser.parse_args(sys.argv[1:])
    # Import different browser drivers based on user selection
    try:
        if options.browser == 'firefox':
            from selenium.webdriver import Firefox as Browser
        elif options.browser == 'chrome':
            from selenium.webdriver import Chrome as Browser
        else:
            from selenium.webdriver import Safari as Browser
        from selenium.webdriver.common.by import By
    except ImportError as err:
        print('[Error]',
              err, '\n\n'
              'Please refer to the Selenium documentation on installing the '
              'webdriver:\n'
              'https://www.selenium.dev/documentation/webdriver/'
              'getting_started/',
              file=sys.stderr)
        sys.exit(1)

    if options.change_dir:
        try:
            os.chdir(options.change_dir)
        except OSError as err:
            print(err, file=sys.stderr)
            sys.exit(1)

    if not os.path.isfile('package.json'):
        print('Invalid directory: cannot find \'package.json\'',
              file=sys.stderr)
        sys.exit(1)

    tests = unittest.defaultTestLoader.loadTestsFromTestCase(TestChorusLapilli)
    unittest.TextTestRunner().run(tests)
