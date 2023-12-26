"""
The controller class to run the game

This module provides tha class that handles the basic game loop. Once this class is
completed, you can start to play with the connectn program.

Izabela L.
11/11/23
"""
import a6board
import a6player


#### TASK 3 ####
class Game:
    """
    A class representing a game of Connect-N

    Instances of this class contain both a board and a list of players. They play the
    game by calling chooseMove() for each player, and making the corresponding play in
    the game board. They also check for wins or ties.

    The game also has a takeback feature supported by the method take_back().  This is
    used in AI play to undo speculative moves,
    """
    # HIDDEN ATTRIBUTES
    # Attribute _board: The game board
    # Invariant: _board is a Board object
    #
    # Attribute _players: The game players
    # Attribute _players: The game players
    # Invariant: _players is a (possibly empty) list of Player objects, each
    #            with distinct colors
    #
    # Attribute _current: The index of the current player
    # Invariant: _current is an int >= 0 and < len(_players), or -1 if _players
    #            is empty
    #
    # Attribute _winner: The (color of) the winner of the game
    # Invariant: _winner is either None (no winner) or a color of one of the
    #            Players in _players

    #### PART A ####
    def getBoard(self):
        """
        Returns the game board
        """
        return self._board

    def getPlayers(self):
        """
        Returns a list of players in the game
        """
        return self._players

    def addPlayer(self, player):
        """
        Adds the given player to the game.

        If the list of players was currently empty, this makes this player the
        current player.

        Parameter player: the Player to add
        Precondition: player is a Player object with a different color than any
        of the current players.
        """
        assert isinstance(player, a6player.Player)
        assert is_new_player(self._players, player) == True
        if self._players == []:
            self._current = 0
        self._players.append(player)

    def clearPlayers(self):
        """
        Removes all the players from the game
        """
        self._players = []

    def getCurrent(self):
        """
        Returns the current player object in the game. If there are no players, it
        returns None.
        """
        if self._players == []:
            return None
        else:
            return self._players[self._current]

    def getWinner(self):
        """
        Returns the (color of) the winner of the game (or None if there is no winner)
        """
        return self._winner

    def __init__(self,width,height,streak):
        """
        Initializes a new game with the given width, height, and streak.

        This method should start out with no players. Read the invariant closely
        to see how to do this.

        Parameter width: The board width
        Precondition: width is an int > 0

        Parameter height: The board height
        Precondition: height is an int > 0

        Parameter streak: The number of pieces in a line necessary to win
        Precondition: streak is an int > 0 and <= min(width,height)
        """
        assert isinstance(width, int)
        assert (width > 0)
        assert isinstance(height, int)
        assert (height > 0)
        assert isinstance(streak, int)
        assert (streak > 0) and (streak <= min(height, width))
        self._board = a6board.Board(height, width, streak)
        self._players = []
        self._winner = None
        self._current = -1

    #### PART B ####
    def advance(self):
        """
        Advances the game to the next player.

        This increments the current player index by 1 (or resets it to 0 when
        all players have had a chance.
        """
        self._current = self._current + 1
        if self._current == len(self._players):
            self._current = 0

    def takeTurn(self,player):
        """
        Returns the column chosen by the given player.

        This method processes a turn for the current player. That means choosing a
        column AND placing the player's color in that column.

        If the player is unable to make a move, this method returns -1.

        Parameter player: The current player
        Precondition: player is a Player object
        """
        assert isinstance(player, a6player.Player)
        col = player.chooseMove(self._board)
        if self._board.isFullBoard() == True:
            return -1
        else:
            self._board.place(col, player.getColor())
            return col

    def run(self):
        """
        Runs the game until completion.

        This method contains a while loop that runs until either there is a
        winner or the game board fills up.
        """
        while self._winner == None:
            self.takeTurn(self._players[self._current])
            self.advance()
            #This is the win condition. If it's None, there's no winner or it's a tie.
            condition = self._board.findWins(self._board.getLastMove()[0], \
            self._board.getLastMove()[1])
            if condition != None:
                self._winner = self._players[self._current - 1].getColor()
                return self._winner
            elif (self._board.getHeight() * self._board.getWidth()) == \
            self._board.getMoveCount():
                return None

#### HELPER FUNCTION ####
# DO NOT MODIFY
def is_new_player(players,p):
    """
    Returns True if p is a different color than the objects in players

    Parameter players: The existing players
    Precondition: players is a list of Player objects

    Parameter p: The player to test
    Precondition: p is a Player object
    """
    result = True
    for opponent in players:
        if opponent.getColor() == p.getColor():
            return False
    return True
