"""
Test cases for Assignment 6

You will want to run this script to test out your code. The advantage of this script over
the connectn program is that you can run it on the early classes, before the class Game
is complete.

Author: John H. E. Lasseter (jhl287), Walker M. White (wmw2)
Date:   October 16, 2023
"""

import introcs
import connectn
import a6player
import a6board
import a6game
import a6consts


#### CHANGE THIS TO MATCH YOUR TASK LEVEL (1-5)                 ####
#### OR RUN WITH A COMMAND-LINE ARGUMENT (python a6test.py 5)   ####
TASK_LEVEL = 5


def testPlayer():
    """
    Test function to verify the (human) Player class
    """
    print('Testing the Player class (Task 1)')
    # Test a simple red player
    p = a6player.Player('red','Bob')
    introcs.assert_equals('red',p.getColor())
    introcs.assert_equals('Bob',p.getName())

    # Set the name
    p.setName('Alice')
    introcs.assert_equals('Alice',p.getName())

    # Use an empty name
    p.setName('')
    introcs.assert_equals('Red player',p.getName())

    # Use a web color (orange)
    p = a6player.Player('#ed7014','Bob')
    introcs.assert_equals('#ed7014',p.getColor())
    introcs.assert_equals('Bob',p.getName())

    # Use an empty name
    p.setName('')
    introcs.assert_equals('#ed7014 player',p.getName())

    # Verify that we enforce preconditions
    introcs.assert_error(a6player.Player,1,'Bob')
    introcs.assert_error(a6player.Player,'blurg','Bob')
    introcs.assert_error(a6player.Player,'blue',4)
    introcs.assert_error(p.setName,4)

    p = a6player.Player('red')
    introcs.assert_equals('red',p.getColor())
    introcs.assert_equals('Red player',p.getName())


def testBoardA():
    """
    Test function to verify part A of the Board class.
    """
    print('- Part A: Testing the board initialization')
    # Test the board
    b = a6board.Board(3,4,2)
    introcs.assert_equals(3,b.getHeight())
    introcs.assert_equals(4,b.getWidth())
    introcs.assert_equals(2,b.getStreak())

    # Test the defaults
    b = a6board.Board()
    introcs.assert_equals(6,b.getHeight())
    introcs.assert_equals(7,b.getWidth())
    introcs.assert_equals(4,b.getStreak())

    # Verify that we enforce preconditions
    introcs.assert_error(a6board.Board,-1,2,1)
    introcs.assert_error(a6board.Board,2,-1,1)
    introcs.assert_error(a6board.Board,2,2,3)

    # Verify that clear works
    b._board[0][1] = 'red'
    b._board[1][0] = 'blue'
    b._moves = [(0,1),(1,0)]

    b.clear()
    for r in range(b.getHeight()):
        for c in range(b.getWidth()):
            introcs.assert_equals(a6consts.NOBODY,b.getColor(r,c))
    introcs.assert_equals(0,b.getMoveCount())

    # Let's verify that new board is empty
    b = a6board.Board(10,12,7)
    introcs.assert_equals(10,b.getHeight())
    introcs.assert_equals(12,b.getWidth())
    introcs.assert_equals(7,b.getStreak())

    for r in range(b.getHeight()):
        for c in range(b.getWidth()):
            introcs.assert_equals(a6consts.NOBODY,b.getColor(r,c))
    introcs.assert_equals(0,b.getMoveCount())


def testBoardB():
    """
    Test function to verify part B of the Board class.
    """
    print('- Part B: Testing the board capacity')
    # Fill up the board a bit
    b = a6board.Board(4,6,3)
    tops = [4,3,2,0,1,4]
    for c in range(6):
        for r in range(tops[c]):
            b._board[r][c] = 'red'

    # Let's see what is available
    for c in range(6):
        full = tops[c] == 4
        introcs.assert_equals(tops[c],b.findAvailableRow(c))
        introcs.assert_equals(full,b.isFullColumn(c))
    introcs.assert_equals(False,b.isFullBoard())

    # Fill the entire board
    for r in range(b.getHeight()):
        for c in range(b.getWidth()):
            b._board[r][c] = 'red'
    introcs.assert_equals(True,b.isFullBoard())

    # And clear it
    b.clear()
    for r in range(b.getHeight()):
        for c in range(b.getWidth()):
            introcs.assert_equals(a6consts.NOBODY,b.getColor(r,c))
    introcs.assert_equals(0,b.getMoveCount())


def testBoardC():
    """
    Test function to verify part C of the Board class.
    """
    print('- Part C: Testing board placement')
    b = a6board.Board(4,6,3)

    # Time to place a piece
    b.place(0,'red')
    introcs.assert_equals('red',b.getColor(0,0))
    introcs.assert_equals(1,b.getMoveCount())
    introcs.assert_equals((0,0),b.getLastMove())

    b.place(1,'blue')
    introcs.assert_equals('blue',b.getColor(0,1))
    introcs.assert_equals(2,b.getMoveCount())
    introcs.assert_equals((0,1),b.getLastMove())

    b.place(0,'yellow')
    introcs.assert_equals('yellow',b.getColor(1,0))
    introcs.assert_equals(3,b.getMoveCount())
    introcs.assert_equals((1,0),b.getLastMove())

    # Check move undo:

    b.undoPlace()
    introcs.assert_equals(a6consts.NOBODY,b.getColor(1,0))
    introcs.assert_equals(2,b.getMoveCount())
    introcs.assert_equals((0,1),b.getLastMove())

    # And clear it
    b.clear()
    for r in range(b.getHeight()):
        for c in range(b.getWidth()):
            introcs.assert_equals(a6consts.NOBODY,b.getColor(r,c))
    introcs.assert_equals(0,b.getMoveCount())


def testBoardD():
    """
    Test function to verify part D of the Board class.
    """
    print('- Part D: Testing streak functions')
    b = play_game1()

    # [[    '',    '',    '',    '',    '',    '', 'red'],
    #  [    '',    '',    '',    '',    '',    '', 'red'],
    #  [    '',    '', 'red','blue',    '','blue', 'red'],
    #  [    '',    '','blue', 'red','blue','blue', 'red'],
    #  ['blue','blue','blue','blue', 'red', 'red','blue'],
    #  [ 'red', 'red','blue', 'red','blue', 'red', 'red']]

    # test findAcross
    introcs.assert_equals((2, 2, 2, 2),b.findAcross(2,2,1))
    introcs.assert_equals(None,b.findAcross(2,2,2))
    introcs.assert_equals((1, 0, 1, 3),b.findAcross(1,1,2))
    introcs.assert_equals((1, 0, 1, 3),b.findAcross(1,0,2))
    introcs.assert_equals((3, 5, 3, 5),b.findAcross(3,5,1))

    #test findSWNE
    introcs.assert_equals((3, 2, 3, 2),b.findSWNE(3,2,1))

    introcs.assert_equals(None,b.findSWNE(3,2,2))
    introcs.assert_equals(None,b.findSWNE(3,5,5))
    introcs.assert_equals((0, 2, 3, 5),b.findSWNE(3,5,4))
    introcs.assert_equals((0, 2, 3, 5),b.findSWNE(2,4,4))
    introcs.assert_equals((0, 2, 3, 5),b.findSWNE(0,2,4))

    # test findNWSE
    introcs.assert_equals((3, 5, 3, 5),b.findNWSE(3,5,1))
    introcs.assert_equals(None,b.findNWSE(3,5,2))

    introcs.assert_equals(None,b.findNWSE(3,2,5))
    introcs.assert_equals((3, 2, 0, 5),b.findNWSE(3,2,4))
    introcs.assert_equals((3, 2, 0, 5),b.findNWSE(2,3,4))
    introcs.assert_equals((3, 2, 0, 5),b.findNWSE(0,5,4))


def testBoardE():
    """
    Test function to verify part E of the Board class.
    """
    print('- Part E: Testing win detection')

    b = play_game2()
    # [[    '',    ,    ,    ,    ,    ,    ],
    #  [    '',    ,    ,    ,    ,    ,    ],
    #  [    '',red ,red ,    ,red ,    ,    ],
    #  ['blue',blue,red ,red ,red ,blue,blue],
    #  ['blue,red ,blue,red ,blue,red ,blue],
    #  [red ,blue,blue,red ,blue,blue,red ]]

    introcs.assert_equals(None,b.findWins(2,3))

    b.place(3,b.getColor(2,3))

    endpts = [(3, 3, 0, 3),(3, 1, 3, 4),(0, 0, 3, 3),(3, 3, 0, 6),
              (0, 3, 3, 3),(3, 4, 3, 1),(3, 3, 0, 0),(0, 6, 3, 3)]
    win = b.findWins(3,3)
    introcs.assert_true(win in endpts)

    introcs.assert_true(b.findWins(3,1) in [(3, 1, 3, 4),(3, 4, 3, 1)])
    introcs.assert_true(b.findWins(1,1) in [(0, 0, 3, 3),(3, 3, 0, 0)])
    introcs.assert_true(b.findWins(2,4) in [(3, 3, 0, 6),(0, 6, 3, 3)])


def testBoard():
    """
    Test function to verify the Board class.

    This only tests the Board methods implemented in Tasks 2 and 4.
    """
    if TASK_LEVEL < 2:
        return

    if TASK_LEVEL < 4:
        task = 2
    else:
        task = 4

    print('Testing the Board class (Task '+str(task)+')')
    testBoardA()
    testBoardB()
    testBoardC()

    if TASK_LEVEL >= 4:
        testBoardD()
        testBoardE()


def testGameA():
    """
    Test function to verify the Game class.

    This tests everything but the run() method in Game:

    getBoard, getPlayers, getWinner, __init__, advance, takeTurn
    """
    print('- Part A: Testing the game initialization')

    # Verify that we enforce preconditions
    introcs.assert_error(a6game.Game,-1,2,1)
    introcs.assert_error(a6game.Game,2,-1,1)
    introcs.assert_error(a6game.Game,2,2,3)

    # Valid setup:
    g = a6game.Game(8,5,3)

    # dimensions used correctly?
    b = g.getBoard()
    introcs.assert_equals(5,b.getHeight())
    introcs.assert_equals(8,b.getWidth())
    introcs.assert_equals(3,b.getStreak())

    # _winner attribute defined, but currently None?

    introcs.assert_equals(None,g.getWinner())

    # make sure we start with no players
    players = g.getPlayers()
    introcs.assert_equals(list,type(players))
    introcs.assert_equals(0,len(players))

    # Every player distinct, and advance reaches each one?
    g.addPlayer(a6player.Player('red',''))
    g.addPlayer(a6player.Player('blue',''))
    p0 = g.getCurrent()

    # Make sure the first player is the red player
    introcs.assert_equals(a6player.Player,type(p0))
    introcs.assert_equals('red',p0.getColor())

    # Make sure all colors not equal
    plast = p0
    for _ in range(len(players[1:])):
        g.advance()
        p1 = plast
        p2 = g.getCurrent()
        introcs.assert_not_equals(p1.getColor(),p2.getColor())
        plast = p2

    # Make sure we loop around to beginning
    g.advance()
    introcs.assert_equals(p0,g.getCurrent())


def testGameB():
    """
    Test function to verify the Game class.

    This tests version of the Game class completed in Task 3,
    """
    print('- Part B: Testing human players with no win condition')
    # control for testing takeTurn and run:
    g = a6game.Game(4,3,3)
    p1 = a6player.Player('red','')
    g.addPlayer(p1)
    p2 = a6player.Player('blue','')
    g.addPlayer(p2)

    # testing takeTurn and advance
    # inject automatic moves play into p1, p2
    setAutoMoves(p1,[2,2,1,0,1,3,3])

    # This is one move too many for the board.  If run stops correctly on a
    # full board, we'll never reach the last move.
    setAutoMoves(p2,[3,2,1,0,0,3])

    # play these five moves:

    c1 = g.takeTurn(p1); g.advance()
    c2 = g.takeTurn(p2)

    introcs.assert_equals(2,c1)
    introcs.assert_equals(3,c2)

    introcs.assert_equals('red',g.getBoard().getColor(0,2))
    introcs.assert_equals('blue',g.getBoard().getColor(0,3))

    # The board so far:
    # [[    ,    ,    ,    ],
    #  [    ,    ,    ,    ],
    #  [    ,    ,red ,blue]]

    # test run():  should stop when the rest board has filled
    try:
        g.run()
        # print('DEBUG (testGameB):  full board?\n' + str(g.getBoard()))
    except StopIteration:
        # This means that the game loop ran at least one extra move
        introcs.assert_false(True,
                             message='run() did not quit on full game board.')

    introcs.assert_true(g.getBoard().isFullBoard())


def testGameC():
    """
    Test function to verify the Game class.

    This tests version of the Game class completed in Task 4.
    """
    print('- Part C: Testing human players with a win condition')
    # control for testing takeTurn and run:
    g = a6game.Game(4,3,3)
    p1 = a6player.Player('red','')
    g.addPlayer(p1)
    p2 = a6player.Player('blue','')
    g.addPlayer(p2)

    # testing takeTurn and advance
    # inject automatic moves play into p1, p2
    setAutoMoves(p1,[2,2,1,0,1,3,3])
    setAutoMoves(p2,[3,2,1,0,0,3])

    # Same move set as in testGameB.  Red wins on its 4th move (column 0), so
    # the game should stop there.

    # test run():  should stop after p1's 4th move, which wins the game
    g.run()
    # print('DEBUG (testGameB):  did Red win?\n' + str(g.getBoard()))

    introcs.assert_equals((0,0),g.getBoard().getLastMove())
    introcs.assert_equals(p1.getColor(),g.getWinner())
    introcs.assert_equals(7, g.getBoard().getMoveCount())
    introcs.assert_false(g.getBoard().isFullBoard())

    ### Test win detection on a full board:
    g = a6game.Game(4,3,3)
    p1 = a6player.Player('red','')
    g.addPlayer(p1)
    p2 = a6player.Player('blue','')
    g.addPlayer(p2)

    introcs.assert_true(g.getWinner() == None)
    # This time, the board should fill, with blue winning on the final move
    setAutoMoves(p1,[1, 3, 1, 0, 3, 0])
    setAutoMoves(p2,[2, 1, 0, 2, 3, 2])

    g.run()
    # print('DEBUG (testGameB):  did Blue win?\n' + str(g.getBoard()))

    introcs.assert_equals((2,2),g.getBoard().getLastMove())
    introcs.assert_true(g.getBoard().isFullBoard())
    introcs.assert_equals(p2.getColor(),g.getWinner())


def testGameD():
    """
    Test function to verify the Game class.

    This tests version of the Game class completed in Part E.
    """
    print('- Part D: Testing a human vs an AI opponent')

    #print('(DEBUG) red human vs blue AI:  blue wins')
    g1human = [1, 0,3,3]
    g1ai = [[0,1,2,3], [1], [2,1,0], [0]]
    winner, move = human_vs_ai('red','blue',g1human,g1ai,False)
    introcs.assert_equals('blue',winner)
    introcs.assert_equals((2,0),move)

    #print('(DEBUG) blue lucks out when red misses a winning move, twice')
    g2human = [1, 2, 0,2]
    g2ai =  [[0,1,2,3], [1,0], [0,1,2], [2]]
    winner, move = human_vs_ai('red','blue',g2human,g2ai,False)
    introcs.assert_equals('blue',winner)
    introcs.assert_equals((2,2),move)

    #print('(DEBUG) blue loses, despite two chances to avoid it')
    g3human = [1, 2, 0,0,3]
    g3ai = [[0,1,2,3], [1,0], [1,0,2], [2]]
    winner, move = human_vs_ai('red','blue',g3human,g3ai,False)
    introcs.assert_equals('red',winner)
    introcs.assert_equals((0,3),move)

    #print('(DEBUG) red AI vs blue human: red wins')
    g4human = [1,1,2,0]
    g4ai = [[2,1,0,3], [1,2,3], [2,0,3], [0,3], [0]]
    winner, move = human_vs_ai('red','blue',g4human,g4ai,True)
    introcs.assert_equals('red',winner)
    introcs.assert_equals((2,0),move)

    #print('(DEBUG) red AI loses')
    g5human = [2,1,0,0,3,3]
    g5ai = [[2,1,0,3], [3,1], [1,3], [0,1,2,3], [1,2,3], [2]]
    winner, move = human_vs_ai('red','blue',g5human,g5ai,True)
    introcs.assert_equals('blue',winner)
    introcs.assert_equals((2,3),move)


def testGame():
    """
    Test function to verify the Game class.

    This game varies its tests to match the appropriate Task
    """
    if TASK_LEVEL < 3:
        return

    print('Testing the Game class (Task '+str(TASK_LEVEL)+')')
    testGameA()
    testGameB()
    if TASK_LEVEL >= 4:
        testGameC()
    if TASK_LEVEL == 5:
        testGameD()


def testAIPlayerA():
    """
    Test function to verify part A of the AIPlayer class.
    """
    print('- Part A: Testing AI player rating and evaluation')

    ai = a6player.AIPlayer('blue','')
    bd = play_game0()
    bd.place(2,'red'); bd.place(2,'blue')
    bd.place(6,'red'); bd.place(6,'blue')
    # [[    ,    ,    ,    ,    ,    ,    ],
    #  [    ,    ,    ,    ,    ,    ,blue],
    #  [    ,    ,    ,    ,    ,blue,red ],
    #  [    ,    ,blue,    ,    ,blue,red ],
    #  [    ,    ,red ,blue,red ,red ,blue],
    #  [    ,    ,blue,red ,blue,red ,red ]]

    runs = [None,(0,2,0,2),(0,2,3,5),(5,1,1,5),
            (1,3,1,6),(3,3,1,3),(3,2,0,2)]
    scores = []
    for rn in runs:
        scores.append(ai._scoreRun(bd,rn))

    introcs.assert_equals([0, 1, 4, 5, 4, 3, 4],scores)

    # Now check actual piece scores:
    topPieces = [(2,2),(1,3),(1,3),(1,4),(3,5),(4,6)]
    scores = []
    for r,c in topPieces:
        scores.append(ai._evaluate(bd,r,c))

    introcs.assert_equals([3, 3, 3, 2, 2, 2], scores)


def testAIPlayerB():
    """
    Test function to verify part B of the AIPlayer class.
    """
    print('- Part B: Testing AI player move evaluation')

    # test _gatherMoves
    testGatherGame = ([1,3,1],[2,3,1])
    bd = make_game_moves('red','blue',(3,4,3),testGatherGame)
    # [[    ,blue,    ,    ],
    #  [    ,red ,    ,blue],
    #  [    ,red ,blue,red ]]

    ai = a6player.AIPlayer('blue','')
    moves = ai._gatherMoves(bd)

    introcs.assert_equals([0,2,3], sorted(moves.keys()))
    for k in moves:
        introcs.assert_equals(a6consts.SCORE_BAD,moves[k])

    # test _evaluateMoves
    bd = play_game0(); bd.place(6,'red')
    # [[    ,    ,    ,    ,    ,    ,    ],
    #  [    ,    ,    ,    ,    ,    ,    ],
    #  [    ,    ,    ,    ,    ,blue,red ],
    #  [    ,    ,    ,    ,    ,blue,red ],
    #  [    ,    ,    ,blue,red ,red ,blue],
    #  [    ,    ,blue,red ,blue,red ,red ]]

    x = a6consts.SCORE_BAD
    moves = {0:x,1:x,2:x,3:x,5:x}
    ai._evaluateMoves(bd,moves)

    scores1 = []
    for c in sorted(moves.keys()):
        scores1.append(moves[c])

    introcs.assert_equals([1, 2, 2, 2, 3], scores1)
    # now add other two columns
    moves[4] = moves[6] = x
    ai._evaluateMoves(bd,moves)

    scores2 = []
    for c in sorted(moves.keys()):
        scores2.append(moves[c])
    introcs.assert_equals([1, 2, 2, 2, a6consts.SCORE_WIN, 3, 2], scores2)

    # test _findBestMoves.
    # First prize:
    introcs.assert_equals([4],ai._findBestMoves(bd,moves))
    #Second prize:
    del(moves[4])
    introcs.assert_equals([5],ai._findBestMoves(bd,moves))
    # Third prize
    del(moves[5])
    introcs.assert_equals([1,2,3,6],sorted(ai._findBestMoves(bd,moves)))


def testAIPlayerC():
    """
    Test function to verify part C of the AIPlayer class.
    """
    print('- Part C: Testing AI player move selection')

    testChooseGame = ([3,5,5,6],[2,3,4,4])
    bd = make_game_moves('red','blue',(6,7,4),testChooseGame)
    # [[    ,    ,    ,    ,    ,    ,    ],
    #  [    ,    ,    ,    ,    ,    ,    ],
    #  [    ,    ,    ,    ,    ,    ,    ],
    #  [    ,    ,    ,    ,    ,    ,    ],
    #  [    ,    ,    ,blue,blue,red ,    ],
    #  [    ,    ,blue,red ,blue,red ,red ]]

    humanMoves = [1,4,1,2,1]
    aiBests = [[4,2],[2],[2],[3],[1,5]]

    ai = a6player.AIPlayer('blue','')

    # We don't need the behavior of set_choice, so turn it off
    oldSetChoice = connectn.set_choice
    setattr(connectn,'set_choice',(lambda i,v:None))

    try:
        for i in range(5):
            bd.place(humanMoves[i],'red')
            m = ai.chooseMove(bd)

            introcs.assert_true(m in aiBests[i])
            m = aiBests[i][0]
            bd.place(m,'blue')

        introcs.assert_true(bd.findWins(3,1) != None)
    finally:
        setattr(connectn,'set_choice',oldSetChoice)


def testAIPlayer():
    """
    Test function to verify the AIPlayer class
    """
    if TASK_LEVEL < 5:
        return

    print('Testing the AIPlayer class (Task 5)')
    testAIPlayerA()
    testAIPlayerB()
    testAIPlayerC()


#### Test Utility Functions ####
# You should not need to undersand anything below this line

def setAutoMoves(player,moves,restore=False):
    """
    Injects moves into an object of the Player class.

    This function temporarily overrides the chooseMove method in player. It
    causes that player to run through an iteration of moves until the last
    one is played.

    If restore is true, it restores the original chooseMove method once the
    moves are exhausted.  Otherwise, calls to chooseMove beyond the injected
    moves will result in an error.

    Parameter player: The player to override
    Precondition: player is an instance of Player

    Parameter moves: The moves (columns) to inject
    Precondition: moves is a list of ints

    Parameter restore: Whether to restore chooseMove when done
    Precondition: restore is a bool
    """
    oldChooseFn = player.chooseMove
    moves_id = '_automoves_' + str(id(player))
    moves = iter(moves)
    setattr(player,moves_id,moves)

    def autoChoose(board):
        """
        Local closure to replace chooseMove

        Parameter board: The board to choose from
        Precondition: board is a Board object that is not full
        """
        assert type(board) == a6board.Board
        try:
            m = next(getattr(player,moves_id))
            return m
        except StopIteration as e:
            if restore:
                delattr(player,moves_id)
                delattr(player,'chooseMove')
                setattr(player,'chooseMove',oldChooseFn)

                assert not hasattr(player,moves_id)
                return player.chooseMove(board)
            else:
                raise e

    setattr(player,'chooseMove',autoChoose)

    return oldChooseFn


def setAIChoiceValidation(ai,move_sets,ui_in_use=False):
    """
    Injects moves into an object of the AIPlayer class.

    This method disables set_choice for the AIPlayer (so that we can ignore
    the UI). It also adds an iteration of "best move sets" to the AI. It
    verifies that these values are returned by the _findBestMoves methods.
    Finally, it replaces the actual value replaced with the one specified.

    This function returns both the original connectn_set_choice method and
    the newly created move_sets_id attribute, so the caller can restore them,
    if necessary.

    NOTE:  For automatic Player vs AIPlayer testing, this method should only be
    used in conjunction with an automatic moves set injected into the Player
    class, using setAutoMoves().

    Parameter ai: The ai player
    Precondition: ai is an instance of AIPlayer

    Parameter move_sets: The move sets to inject
    Precondition: move_sets is a list of of list of ints

    Parameter ui_in_use: Whether the UI is currently being used
    Precondition: ui_in_use is a bool
    """
    oldSetChoice = connectn.set_choice
    if not ui_in_use:
        # We don't need the behavior of set_choice, so turn it off
        setattr(connectn,'set_choice',(lambda i,v:None))

    move_sets_id = '_movesets_' + str(id(ai))
    setattr(ai, move_sets_id, iter(move_sets))

    _fbmOriginal = getattr(ai,'_findBestMoves')

    def validateChoose(board,moves):
        """
        A closure to validate a collection of moves

        Parameter board: The board to choose from
        Precondition: board is a Board object that is not full

        Parameter moves: A set of possible moves
        Precondition: moves is a list of ints
        """
        try:
            bestMoves = next(getattr(ai,move_sets_id))

            aiChoices = _fbmOriginal(board,moves)
            # print("DEBUG (AIValidation):  AI chose {m}".format(m=aiChoices))
            # print("      (AIValidation):  bestMoves is {m}".format(m=bestMoves))

            assert sorted(bestMoves) == sorted(aiChoices)

            # Even if we do have a "best" move, we need to ensure that the AI
            # plays a predictable choice out of the set, since the effect of
            # the opponent's response will vary, depending on the AI choice
            # made here.
            value = bestMoves[0]
            # print('      (AIValidation): playing {v} instead'.format(v=value))
            return [value]
        except StopIteration as si:
            print("Ran out of known best move sets")
            raise si

    setattr(ai,'_findBestMoves',validateChoose)
    return (oldSetChoice, move_sets_id)


def zzip(z):
    """
    Returns a flattened zip of the list z.

    Zip is used to combine lists of the same length into a single list of
    tuples. This function performs zip on a nested list of lists all of the
    same length.

    The result of this function can be undone with unzip.

    Parameter z: The nested list to zip
    Precondition: z is a list of lists all of the same length
    """
    return list(zip(*z))


def unzzip(u):
    """
    Returns a nested list of lists from a zip flattened list.

    This function undoes the result of zzip.

    Parameter u: The list to unzip
    Precondition: u is a list of tuples, all of the same length
    """
    if len(u) == 0:
        return []

    result = []
    for item in u:
        for p in range(len(item)):
            while p >= len(result):
                result.append([])
            result[p].append(item[p])
    return result


def place_game(board,p1,p2,moves):
    """
    Plays the list of p1/p2 moves in the board.

    This function assumes that it is has to be possible to play every move.
    There is no check for a win, but preconditions prevent playing past a
    full board

    Parameter board: The board to fill
    Precondition: board is a Board object

    Parameter p1: The color of the first player
    Precondition: p1 is a color string

    Parameter p2: The color of the first player
    Precondition: p2 is a color string

    Parameter moves: The moves for each player
    Precondition: moves is a two-element tuple of lists of ints
    """
    for i,j in zzip(moves):
        assert board.place(i,p1) >= 0
        assert board.place(j,p2) >= 0

    if len(moves[0]) > len(moves[1]):  # one more p1 move to make
        assert board.place(moves[0][-1],p1)

    return board


def make_game_moves(p1,p2,state,moves):
    """
    Uses state to create a game between p1 and p2, which it plays with moves

    Parameter p1: The color of the first player
    Precondition: p1 is a color string

    Parameter p2: The color of the first player
    Precondition: p2 is a color string

    Parameter state: The state necessary to initialize the game board
    Precondition: state is a tuple (width,height,streak)

    Parameter moves: The moves for each player
    Precondition: moves is a two-element tuple of lists of ints
    """
    b = a6board.Board(*state)

    return place_game(b,p1,p2,moves)


def human_vs_ai(p1,p2,automoves,aimoves,ai_goes_first):
    """
    Returns the winner and last move in human player vs an AI player

    Parameter p1: The color of the first player
    Precondition: p1 is a color string

    Parameter p2: The color of the first player
    Precondition: p2 is a color string

    Parameter automoves: The human player moves
    Precondition: automoves is a list of ints

    Parameter aimoves: The AI player moves
    Precondition: aimoves is a list of ints

    Parameter ai_goes_first: Whether the AI goes first
    Precondition: ai_goes_first is a bool
    """
    g = a6game.Game(4,3,3)

    if ai_goes_first:
        ai = a6player.AIPlayer(p1,'')
        g.addPlayer(ai)
        human = a6player.Player(p2,'')
        g.addPlayer(human)
    else:
        human = a6player.Player(p1,'')
        g.addPlayer(human)
        ai = a6player.AIPlayer(p2,'')
        g.addPlayer(ai)

    setAutoMoves(human,automoves)
    scFn,_ = setAIChoiceValidation(ai,aimoves)

    winner = None
    lastmv = None
    try:
        g.run()
        # print("DEBUG (testGameD):  finished g with board:\n{b}".format(
        #                                                         b=g.getBoard()))
        # print('       final move was ' + str(g.getBoard().getLastMove()))
        winner = g.getWinner()
        lastmv = g.getBoard().getLastMove()
    finally:
        setattr(connectn,'set_choice',scFn)

    return (winner, lastmv)


#### Some sample, Board-only "games" ####
GAME_SIZE = (6,7,4)
GAME_1_MOVES = ([3, 6, 5, 4, 5, 6], [2, 6, 4, 3, 5, 5])
GAME_2_MOVES = ([3, 3, 3, 4, 1, 2, 0, 1, 2, 6, 5, 4],
                [2, 4, 4, 1, 2, 1, 0, 0, 5, 6, 6, 5])


def play_game0():
    """
    Creates the following game:

    [[    ,    ,    ,    ,    ,    ,    ],
     [    ,    ,    ,    ,    ,    ,    ],
     [    ,    ,    ,    ,    ,blue,    ],
     [    ,    ,    ,    ,    ,blue,red ],
     [    ,    ,    ,blue,red ,red ,blue],
     [    ,    ,blue,red ,blue,red ,red ]]
    """
    return make_game_moves('red','blue',GAME_SIZE,GAME_1_MOVES)


def play_game1():
    """
    Creates the following game:

    [[    ,    ,    ,    ,    ,    , red],
     [    ,    ,    ,    ,    ,    , red],
     [    ,    , red,blue,    ,blue, red],
     [    ,    ,blue, red,blue,blue, red],
     [blue,blue,blue,blue, red, red,blue],
     [ red, red,blue, red,blue, red, red]]
    """
    p1,p2 = 'red', 'blue'
    bd = play_game0()

    nextMoves = ([3,1,0,2,6,6,6],[2,1,2,4,0,3])
    return place_game(bd,p1,p2,nextMoves)


def play_game2():
    """
    Creates the following game:

    [[    ,    ,    ,    ,    ,    ,    ],
     [    ,    ,    ,    ,    ,    ,    ],
     [    ,red ,red ,    ,red ,    ,    ],
     [blue,blue,red ,red ,red ,blue,blue],
     [blue,red ,blue,red ,blue,red ,blue],
     [red ,blue,blue,red ,blue,blue,red ]]

    This one will have four wins after red plays (3,3)
    """

    return make_game_moves('red','blue',GAME_SIZE,GAME_2_MOVES)


def set_task_level():
    """
    Sets the active TASK_LEVEL
    """
    global TASK_LEVEL
    import sys
    if len(sys.argv) > 1:
        try:
            level = int(sys.argv[1])
            if 1 <= level <= 5:
                TASK_LEVEL = level
            else:
                raise ValueError("TASK_LEVEL must be 1-5:", level)
        except ValueError:
            pass
        print('TASK_LEVEL is currently',TASK_LEVEL)


if __name__ == '__main__':
    set_task_level()
    testPlayer()
    testBoard()
    testAIPlayer()
    testGame()
    print('Assignment 6 passed all tests up to Task',TASK_LEVEL)
