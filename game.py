# -*- coding: utf-8 -*-
"""
@author: Junxiao Song
""" 

from __future__ import print_function
import numpy as np

class Board(object):
    """
    board for the game
    """

    def __init__(self, **kwargs):

        self.width = 80
        self.height =50
        self.states ={}
        self.players =[1,2]
        self.actiondim=12 #The number of possibile actions for each group of robots
        '''
        self.width = int(kwargs.get('width', 8))
        self.height = int(kwargs.get('height', 8))
        self.states = {} # board states, key:move as location on the board, value:player as pieces type
        self.n_in_row = int(kwargs.get('n_in_row', 5)) # need how many pieces in a row to win
        self.players = [1, 2] # player1 and player2
        '''

    def checkavilables(states):
        {
            
        }

    def init_board(self, start_player=0):
        
        self.current_player = self.players[start_player]  # start player
        self.availables = checkavilables()
        self.states={}
        self.last_move=-1
        '''
        if self.width < self.n_in_row or self.height < self.n_in_row:
            raise Exception('board width and height can not less than %d' % self.n_in_row)
        self.current_player = self.players[start_player]  # start player        
        self.availables = list(range(self.width * self.height)) # available moves 
        self.states = {} # board states, key:move as location on the board, value:player as pieces type
        self.last_move = -1
        '''
    def move_to_location(self, move):
        """       
        3*3 board's moves like:
        6 7 8
        3 4 5
        0 1 2
        and move 5's location is (1,2)
        """
        h = move  // self.width
        w = move  %  self.width
        return [h, w]

    def location_to_move(self, location):
        if(len(location) != 2):
            return -1
        h = location[0]
        w = location[1]
        move = h * self.width + w
        if(move not in range(self.width * self.height)):
            return -1
        return move

    def current_state(self): 
        """return the board state from the perspective of the current player
        shape: 4*width*height"""
        
        square_state = np.zeros((4, self.width, self.height))
        if self.states:
            moves, players = np.array(list(zip(*self.states.items())))
            move_curr = moves[players == self.current_player]
            move_oppo = moves[players != self.current_player]                           
            square_state[0][move_curr // self.width, move_curr % self.height] = 1.0
            square_state[1][move_oppo // self.width, move_oppo % self.height] = 1.0   
            square_state[2][self.last_move //self.width, self.last_move % self.height] = 1.0 # last move indication   
        if len(self.states)%2 == 0:
            square_state[3][:,:] = 1.0
        return square_state[:,::-1,:]

    def checkavilables():
        def clearrow(l,x):
            for i in range(self.actiondim):
                l[x][i]=0
            return l

        def clearcolom(l,y):
            for i in range(self.actiondom):
                l[i][y]=0
            return l

        l=np.array([[1 for _ in range(self.actiondim)] for _ in range(self.actiondim)])
        # The possible move is in form of actiondim^2 matrix, where the row represents the action of the first 
        # robot, the colom represents the action of the second robot. The first nine actions are moving in eight directions
        # the ninth action is no action. 
        # and the last three action is 3 ways of changing the angle of turret: stay the same, turn left 45 degree, turn right 45 degree
        # at this point, we assume that moving and turning turret could not be in the same time.

        # statemap is the map of obstacle and position of the robots         
        x=self.pos_x[self.current_player][0]       #The coordicnate for the first robot
        y=self.pos_y[self.current_player][0]
        x2=self.pos_x[self.current_player][1]      #The coordinate for the second robot
        y2=self.pos_y[self.current_player][1]
        
        if self.statemap[x+1,y]==1: l=clearrow(l,0)     #clear the possibility of crashing into the wall or opponent
        if self.statemap[x+1,y+1]==1: l=clearrow(l,1)
        if self.statemap[x,y+1]==1: l=clearrow(l,2)
        if self.statemap[x-1,y+1]==1: l=clearrow(l,3)
        if self.statemap[x-1,y]==1: l=clearrow(l,4)
        if self.statemap[x-1,y-1]==1: l=clearrow(l,5)
        if self.statemap[x,y-1]==1: l=clearrow(l,6)
        if self.statemap[x+1,y-1]==1: l=clearrow(l,7)

        if self.statemap[x2+1,y2]==1: l=clearcolom(l,0)
        if self.statemap[x2+1,y2+1]==1: l=clearcolom(l,1)
        if self.statemap[x2,y2+1]==1: l=clearcolom(l,2)
        if self.statemap[x2-1,y2+1]==1: l=clearcolom(l,3)
        if self.statemap[x2-1,y2]==1: l=clearcolom(l,4)
        if self.statemap[x2-1,y2-1]==1: l=clearcolom(l,5)
        if self.statemap[x2,y2-1]==1: l=clearcolom(l,6)
        if self.statemap[x2+1,y2-1]==1: l=clearcolom(l,7)

        return np.reshape(l,-1)

    def do_move(self, move):

        row=move // 12
        col=move % 12
        change=calpos(row,col)
        self.pos_x[self.current_player][0]+=change[0][0]       #The coordicnate for the first robot
        self.pos_y[self.current_player][0]+=change[0][1]
        self.pos_x[self.current_player][1]+=change[1][0]      #The coordinate for the second robot
        self.pos_y[self.current_player][1]+=change[1][1]

        self.hp=calhit(self.pos_x,self.pos_y)        #change the hp of both sides after this round of action
        self.time=self.time-1                        #change the remaining time

        #self.states[move] = self.current_player
        self.availables=self.checkavilables()   #update new available move for the robots

        self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1] 
        self.last_move = move

    def has_a_winner(self):
        width = self.width
        height = self.height
        states = self.states
        n = self.n_in_row

        moved = list(set(range(width * height)) - set(self.availables))
        if(len(moved) < self.n_in_row + 2):
            return False, -1

        for m in moved:
            h = m // width
            w = m % width
            player = states[m]

            if (w in range(width - n + 1) and
                len(set(states.get(i, -1) for i in range(m, m + n))) == 1):
                return True, player

            if (h in range(height - n + 1) and
                len(set(states.get(i, -1) for i in range(m, m + n * width, width))) == 1):
                return True, player

            if (w in range(width - n + 1) and h in range(height - n + 1) and
                len(set(states.get(i, -1) for i in range(m, m + n * (width + 1), width + 1))) == 1):
                return True, player

            if (w in range(n - 1, width) and h in range(height - n + 1) and
                len(set(states.get(i, -1) for i in range(m, m + n * (width - 1), width - 1))) == 1):
                return True, player

        return False, -1

    def game_end(self):
        """Check whether the game is ended or not"""
        win, winner = self.has_a_winner()
        if win:
            return True, winner
        elif not len(self.availables):#            
            return True, -1
        return False, -1

    def get_current_player(self):
        return self.current_player


class Game(object):
    """
    game server
    """

    def __init__(self, board, **kwargs):
        self.board = board

    def graphic(self, board, player1, player2):
        """
        Draw the board and show game info
        """
        width = board.width
        height = board.height

        print("Player", player1, "with X".rjust(3))
        print("Player", player2, "with O".rjust(3))
        print()
        for x in range(width):
            print("{0:8}".format(x), end='')
        print('\r\n')
        for i in range(height - 1, -1, -1):
            print("{0:4d}".format(i), end='')
            for j in range(width):
                loc = i * width + j
                p = board.states.get(loc, -1)
                if p == player1:
                    print('X'.center(8), end='')
                elif p == player2:
                    print('O'.center(8), end='')
                else:
                    print('_'.center(8), end='')
            print('\r\n\r\n')
            
    def start_play(self, player1, player2, start_player=0, is_shown=1):
        """
        start a game between two players
        """
        if start_player not in (0,1):
            raise Exception('start_player should be 0 (player1 first) or 1 (player2 first)')
        self.board.init_board(start_player)
        p1, p2 = self.board.players
        player1.set_player_ind(p1)
        player2.set_player_ind(p2)
        players = {p1: player1, p2:player2}
        if is_shown:
            self.graphic(self.board, player1.player, player2.player)
        while(1):
            current_player = self.board.get_current_player()
            player_in_turn = players[current_player]
            move = player_in_turn.get_action(self.board)
            self.board.do_move(move)
            if is_shown:
                self.graphic(self.board, player1.player, player2.player)
            end, winner = self.board.game_end()
            if end:
                if is_shown:
                    if winner != -1:
                        print("Game end. Winner is", players[winner])
                    else:
                        print("Game end. Tie")
                return winner   
            
            
    def start_self_play(self, player, is_shown=0, temp=1e-3):
        """ start a self-play game using a MCTS player, reuse the search tree
        store the self-play data: (state, mcts_probs, z)
        """
        self.board.init_board()        
        p1, p2 = self.board.players
        states, mcts_probs, current_players = [], [], []        
        while(1):
            move, move_probs = player.get_action(self.board, temp=temp, return_prob=1)
            # store the data
            states.append(self.board.current_state())
            mcts_probs.append(move_probs)
            current_players.append(self.board.current_player)
            # perform a move
            self.board.do_move(move)
            if is_shown:
                self.graphic(self.board, p1, p2)
            end, winner = self.board.game_end()
            if end:
                # winner from the perspective of the current player of each state
                winners_z = np.zeros(len(current_players))  
                if winner != -1:
                    winners_z[np.array(current_players) == winner] = 1.0
                    winners_z[np.array(current_players) != winner] = -1.0
                #reset MCTS root node
                player.reset_player() 
                if is_shown:
                    if winner != -1:
                        print("Game end. Winner is player:", winner)
                    else:
                        print("Game end. Tie")
                return winner, list(zip(states, mcts_probs, winners_z))
            