"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def GetOpenSpaces(game):
    summ = 0
    for row in game.__board_state__:
        summ += row.count(0)
    return summ

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

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

    # TODO: finish this function!
    
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    
    if not opp_moves and game.inactive_player == player:
        return float("inf")
    
    elif not own_moves and game.active_player == player:
        return float("-inf")
    
    elif GetOpenSpaces(game) > 43:
        return float(len(own_moves) - 4 * len(opp_moves))
    
    else:
        temps = []
        score = 0
        for move in game.get_legal_moves():
            game2 = game.forecast_move(move)
            temp = len(game2.get_legal_moves())
            if game2.active_player == player:
                temps.append(temp)
            else:
                temps.append(-temp)
        if temps:
            score = sum(temps) / float(len(temps))

        return float(len(own_moves) - 0.2 * len(opp_moves) + .5 * score)
    

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

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

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        
        if not legal_moves:
            return (-1,-1)
        best_move = None
        
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            depth = 0
            if self.method == 'minimax' and not self.iterative:
                if game.active_player == game.__player_1__:
                    return self.minimax(game, self.search_depth, maximizing_player=True)[1]
                else:
                    return self.minimax(game, self.search_depth, maximizing_player=False)[1]
            
            elif self.method == 'alphabeta' and not self.iterative:
                if game.active_player == game.__player_1__:
                    return self.alphabeta(game, self.search_depth, maximizing_player=True)[1]
                else:
                    return self.alphabeta(game, self.search_depth, maximizing_player=False)[1]
            
            elif self.method == 'minimax' and self.iterative:
                best_move = legal_moves[0]
                while True:
                    depth += 1
                    if game.active_player == game.__player_1__:
                        best_move = self.minimax(game, depth, maximizing_player=True)[1]
                    else:
                        best_move = self.minimax(game, depth, maximizing_player=False)[1]
                return best_move
            
            elif self.method == 'alphabeta' and self.iterative:
                best_move = legal_moves[0]
                while True:
                    depth += 1
                    if game.active_player == game.__player_1__:
                        out = self.alphabeta(game, depth, maximizing_player=True)
                        best_move = out[1]
                        if abs(out[0]) >= 200:
                            return best_move
                    else:
                        out = self.alphabeta(game, depth, maximizing_player=False)
                        best_move = out[1]
                        if abs(out[0]) >= 200:
                            return best_move
                return best_move
        
        except Timeout:
            # Handle any actions required at timeout, if necessary
            return best_move

        # Return the best move from the last completed search iteration
        #raise NotImplementedError

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        
        depth_tracker = depth

        def Max_Value(game, depth_tracker):
            
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()

            depth_tracker -=1
            if depth_tracker == 0 or not game.get_legal_moves():
                return self.score(game, game.__player_1__)
            v = float('-inf')
            for move_max in game.get_legal_moves():
                v = max(v, Min_Value(game.forecast_move(move_max), depth_tracker))
            return v
        
        def Min_Value(game, depth_tracker):
            
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()

            depth_tracker -=1
            if depth_tracker == 0 or not game.get_legal_moves():
                return self.score(game, game.__player_1__)
            
            v = float('inf')
            for move_min in game.get_legal_moves():
                v = min(v, Max_Value(game.forecast_move(move_min), depth_tracker))
            return v    
        
        if maximizing_player:
            return max([(Min_Value(game.forecast_move(move), depth_tracker), move) for move in game.get_legal_moves()], key = lambda x: x[0])  
        
        else:
            return min([(Max_Value(game.forecast_move(move), depth_tracker), move) for move in game.get_legal_moves()], key = lambda x: x[0])

            
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

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

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        
        depth_tracker = depth

        def Max_Value(game, alpha, beta, depth_tracker):
            
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()
            
            depth_tracker -=1
            if depth_tracker == 0 or not game.get_legal_moves():
                return self.score(game, game.__player_1__)
            v = float('-inf')
            for move_max in game.get_legal_moves():
                if self.time_left() < self.TIMER_THRESHOLD:
                    break
                v = max(v, Min_Value(game.forecast_move(move_max), alpha, beta, depth_tracker))
                if v >= beta:
                    return v
                alpha = max(alpha,v)
            return v
        
        def Min_Value(game, alpha, beta, depth_tracker):
            
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()
            
            depth_tracker -=1
            if depth_tracker == 0 or not game.get_legal_moves():
                return self.score(game, game.__player_1__)
            v = float('inf')
            for move_min in game.get_legal_moves():
                v = min(v, Max_Value(game.forecast_move(move_min), alpha, beta, depth_tracker))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v
        
        if maximizing_player:
            best_action = game.get_legal_moves()[0]
            for move in game.get_legal_moves():
                v = Min_Value(game.forecast_move(move), alpha, beta, depth_tracker)
                if v > alpha:
                    alpha = v
                    best_action = move
            return alpha, best_action
        else:
            best_action = game.get_legal_moves()[0]
            for move in game.get_legal_moves():
                v = Max_Value(game.forecast_move(move), alpha, beta, depth_tracker)
                if v < beta:
                    beta = v
                    best_action = move
            return beta, best_action 
    