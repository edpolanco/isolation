"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import numpy as np
from operator import itemgetter

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass
                       
#helper variable for our custom score functions to 
#count the legal moves from a board location
directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                    (1, -2), (1, 2), (2, -1), (2, 1)]

def custom_score(game, player):
    """Counts the possible moves from the available legal moves from 
    current game state from the point of view of the given player and
    then subtract the same count from the opposing player.

    For example if the given player has possible legals of (2,2) & (1,0) then
    we count the legal moves from (2,2) & (1,0) to get *NEW LEGAL MOVES (one move ahead)*.
    We then perform the same count but for the opposing player and 
    subtract from the given player amount (current player - opposing player).

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # count the available moves from the available legal moves 
    # for current player
    move_count = 0.0
    for move in game.get_legal_moves(player):
        r, c = move
        for dr, dc in directions:
            if game.move_is_legal((r + dr, c + dc)):
                move_count += 1

    # count the available moves from the available legal moves 
    # for opposing player   
    for opp_move in game.get_legal_moves(game.get_opponent(player)):
        r2, c2 = opp_move
        for dr2, dc2 in directions:
            if game.move_is_legal((r2 + dr2, c2 + dc2)):
                move_count -= 1

    return move_count

def custom_score_2(game, player):
    """Counts the possible moves from the available legal moves from 
    current game state from the point of view of the given player two moves ahead.

    For example if the given player has possible legals of (2,2) & (1,0) then
    we count the legal moves from (2,2) & (1,0) to get *NEW LEGAL MOVES (one move ahead)*.
    We further then count the possible legal from the *NEW LEGAL MOVES (one move ahead)* 
    to get **NEW LEGAL MOVES (two moves ahead)**

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    #The below code counts the possible moves for the given player
    # from each legal move location
    moves = []
    for move in game.get_legal_moves(player):
        r, c = move
        for dr, dc in directions:
            current_move = (r + dr , c + dc)
            if game.move_is_legal(current_move):
                if (current_move) not in moves:
                    moves.append(current_move) 

                    #go a second level and count available move from new location without   
                    for dr2, dc2 in directions:
                        current_move2 = (r + dr + dr2, c + dc + dc2)
                        if game.move_is_legal(current_move2):
                            if (current_move2) not in moves:
                                moves.append(current_move2)
                        
    return float(len(moves))

def custom_score_3(game, player):
    """Counts the possible moves from the available legal moves from 
    current game state from the point of view of the given player one move ahead.

    For example if the given player has possible legals of (2,2) & (1,0) then
    we count the legal moves from (2,2) & (1,0) to get *NEW LEGAL MOVES (one move ahead)*.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    move_count = 0.0
    for move in game.get_legal_moves(player):
        r, c = move
        for dr, dc in directions:
            if game.move_is_legal((r + dr, c + dc)):
                move_count += 1
    
    return move_count 

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move
    
    def __min_value(self,game,depth):
        """ Return the value for a win if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0 or not game.get_legal_moves():
            return self.score(game, self)
        else:
            v = float("inf")
            for move in game.get_legal_moves():
                v = min(v,self.__max_value(game.forecast_move(move), depth - 1))
            return v

    def __max_value(self,game, depth):
        """ Return the value for a loss if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        if depth == 0 or not game.get_legal_moves():
            return self.score(game, self)
        else:
            v =  float("-inf")
            for move in game.get_legal_moves():
                v = max(v,self.__min_value(game.forecast_move(move), depth - 1))
            return v


    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

       #get the available legal moves and check that we have at least one move
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        
        #saved the first available move in case we run out of time
        best_move_default = legal_moves[0]

        moves = []
        for move in game.get_legal_moves():
            result = self.__min_value(game.forecast_move(move),depth-1)
            moves.append((move,result))

        #now find the hightest score along with its corresponding move coordinates
        best_score_found = max(moves,key=itemgetter(1)) 
        if best_score_found[1] > float("-inf"):
            return best_score_found[0]
        else:
            return  best_move_default

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

       # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            depth_count = 1
            while True:   
                 new_move = self.alphabeta(game,depth_count)
                 if new_move != (-1, -1):
                     best_move = new_move

                 depth_count +=1

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def __min_value(self,game,depth, alpha, beta):
        """ Return the value for a win if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0 or not game.get_legal_moves():
            return self.score(game, self)
        else:
            v = float("inf")
            for move in game.get_legal_moves():
                v = min(v,self.__max_value(game.forecast_move(move), depth - 1, alpha, beta))
                if v <= alpha:
                    return v

                beta = min(beta, v)
            
            return v

    def __max_value(self,game, depth, alpha,beta):
        """ Return the value for a loss if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        if depth == 0 or not game.get_legal_moves():
            return self.score(game, self)
        else:
            v =  float("-inf")
            for move in game.get_legal_moves():
                v = max(v,self.__min_value(game.forecast_move(move), depth - 1, alpha,beta))
                if v >= beta:
                    return v
                
                alpha = max(alpha, v)
            return v

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #get the available legal moves and check that we have at least one move
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        
        #saved the first available move in case we run out of time
        best_score = float("-inf")
        best_move= legal_moves[0]

        #lets loop through all the available moves and then find the 
        # one with the highest score
        for move in game.get_legal_moves():
            v = self.__min_value(game.forecast_move(move),depth-1,alpha, beta)
            if v > best_score:
                best_score = v
                best_move = move

            alpha = max(alpha,best_score)
        
        return best_move        