# -*- coding: utf-8 -*-
"""
@author: Junxiao Song
""" 

from __future__ import print_function
import numpy as np
import pdb

class Board(object):
    """
    board for the game
    """

    def __init__(self, **kwargs):
        #self.width = int(kwargs.get('width', 8))
        #self.height = int(kwargs.get('height', 8))
        #self.states = {} # board states, key:move as location on the board, value:player as pieces type
        #self.n_in_row = int(kwargs.get('n_in_row', 5)) # need how many pieces in a row to win
        self.pos=np.zeros([2,3])
        self.width=10
        self.height=10
        
        self.players = [1, 2] # player1 and player2
        self.totaltime=100
        
        self.actiondim=24
        self.angle_direct=[[-1,0],[0,1],[1,0],[0,-1]]
        self.pos_change=[[0,1,0],[0,-1,0],[1,0,0],[-1,0,0],[1,1,0],[1,-1,0],[-1,1,0],[-1,-1,0],
                        [0,1,1],[0,-1,1],[1,0,1],[-1,0,1],[1,1,1],[1,-1,1],[-1,1,1],[-1,-1,1],
                        [0,1,-1],[0,-1,-1],[1,0,-1],[-1,0,-1],[1,1,-1],[1,-1,-1],[-1,1,-1],[-1,-1,-1]]

    def init_board(self, start_player=0):
        self.hp=[1000,1000]
        self.time=0
        #if self.width < self.n_in_row or self.height < self.n_in_row:
        #    raise Exception('board width and height can not less than %d' % self.n_in_row)
        self.current_player = start_player  # start player        
        #self.availables = list(range(self.width * self.height)) # available moves 
        self.statemap=np.zeros([self.width,self.height])
        self.wall=np.zeros([self.width,self.height])
        self.pos[0]=[1,1,1]
        self.pos[1]=[9,9,3]
        self.statemap[1][1]=1
        self.statemap[9][9]=2
        #self.states = {} # board states, key:move as location on the board, value:player as pieces type
        self.last_move = np.array([0,0,0])
        self.availables=self.list_availables()
    # '''
    # def move_to_location(self, move):
    #     """       
    #     3*3 board's moves like:
    #     6 7 8
    #     3 4 5
    #     0 1 2
    #     and move 5's location is (1,2)
    #     """
    #     h = move  // self.width
    #     w = move  %  self.width
    #     return [h, w]

    # def location_to_move(self, location):
    #     if(len(location) != 2):
    #         return -1
    #     h = location[0]
    #     w = location[1]
    #     move = h * self.width + w
    #     if(move not in range(self.width * self.height)):
    #         return -1
    #     return move
    # '''

    def current_state(self): 
        # """return the board state from the perspective of the current player
        # shape: 4*width*height"""
        # '''
        # square_state = np.zeros((4, self.width, self.height))
        # if self.states:
        #     moves, players = np.array(list(zip(*self.states.items())))
        #     move_curr = moves[players == self.current_player]
        #     move_oppo = moves[players != self.current_player]                           
        #     square_state[0][move_curr // self.width, move_curr % self.height] = 1.0
        #     square_state[1][move_oppo // self.width, move_oppo % self.height] = 1.0   
        #     square_state[2][self.last_move //self.width, self.last_move % self.height] = 1.0 # last move indication   
        # if len(self.states)%2 == 0:
        #     square_state[3][:,:] = 1.0
        # return square_state[:,::-1,:]
        # '''
        square_state = np.zeros((3, self.width, self.height))
        
        wall=self.wall
        pos=self.pos[self.current_player].astype(int)
        wall[pos[0],pos[1]]=1
        square_state[0]=wall
        
        wall=self.wall
        pos=self.pos[1-self.current_player].astype(int)
        wall[pos[0],pos[1]]=1
        square_state[1]=wall
        
        wall=self.wall
        pos=self.last_move.astype(int)
        wall[pos[0],pos[1]]=1
        square_state[2]=wall

        time_vec=np.zeros(self.totaltime)
        time_vec[self.time]=1

        return square_state,time_vec


    def check_hit(self,x,y):
        #This is the simplest version, where the robot could only attack four directions
        new_x=self.pos[x].astype(int)

        while(1):
            new_x[0]=new_x[0]+self.angle_direct[new_x[2]][0]
            new_x[1]=new_x[1]+self.angle_direct[new_x[2]][1]
            if not((new_x[0]>-1) and (new_x[0]<self.height) and (new_x[1]>-1) and (new_x[1]<self.height)):
                return False
            t=self.statemap[new_x[0]][new_x[1]]
            if not(t==0):
                if t==self.players[y]:
                    return True
                else:
                    return False



    def update_hp(self):
        for i in range(len(self.players)):
            if not(i==self.current_player):
                if (self.check_hit(self.current_player,i)):
                    self.hp[i]=self.hp[i]-1
                if (self.check_hit(i,self.current_player)):
                    self.hp[self.current_player]=self.hp[self.current_player]-1


    def do_move(self, move):
        pos=self.pos[self.current_player].astype(int)
        self.statemap[pos[0]][pos[1]]=0
        pos[0]=pos[0]+self.pos_change[move][0]
        pos[1]=pos[1]+self.pos_change[move][1]
        pos[2]=(pos[2]+self.pos_change[move][2]) % 4
        self.statemap[pos[0]][pos[1]]=self.players[self.current_player]
        self.pos[self.current_player]=pos
        self.update_hp()
        self.last_move=pos
        self.current_player = 1-self.current_player
        self.availables=self.list_availables()
        self.time=self.time+1

        
    #     '''
    #     self.states[move] = self.current_player
    #     self.availables.remove(move)
    #     self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1] 
    #     self.last_move = move
    #     '''
    #     '''
    # def has_a_winner(self):
        
    #     width = self.width
    #     height = self.height
    #     states = self.states
    #     n = self.n_in_row

    #     moved = list(set(range(width * height)) - set(self.availables))
    #     if(len(moved) < self.n_in_row + 2):
    #         return False, -1

    #     for m in moved:
    #         h = m // width
    #         w = m % width
    #         player = states[m]

    #         if (w in range(width - n + 1) and
    #             len(set(states.get(i, -1) for i in range(m, m + n))) == 1):
    #             return True, player

    #         if (h in range(height - n + 1) and
    #             len(set(states.get(i, -1) for i in range(m, m + n * width, width))) == 1):
    #             return True, player

    #         if (w in range(width - n + 1) and h in range(height - n + 1) and
    #             len(set(states.get(i, -1) for i in range(m, m + n * (width + 1), width + 1))) == 1):
    #             return True, player

    #         if (w in range(n - 1, width) and h in range(height - n + 1) and
    #             len(set(states.get(i, -1) for i in range(m, m + n * (width - 1), width - 1))) == 1):
    #             return True, player

    #     return False, -1
    #     '''

    def has_a_winner(self):
        max_hp=0
        max_i=0
        for i in range(len(self.players)):
            if self.hp[i]>max_hp:
                max_hp=self.hp[i]
                max_i=i
        tie=False
        for i in range(len(self.players)):
            if (not(i==max_i)) and (self.hp[i]==max_hp):
                tie=True
                break
        return tie, max_i

    def game_end(self):
        """Check whether the game is ended or not"""
        # '''
        # win, winner = self.has_a_winner()
        # if win:
        #     return True, winner
        # elif not len(self.availables):#            
        #     return True, -1
        # return False, -1
        # '''
        if self.time==self.totaltime-1:
            win,winner=self.has_a_winner()
            if win:
                return True, winner
            else:
                return True, -1
        else:
            return False, -1

    def get_current_player(self):
        return self.current_player

    def list_availables(self):
        list_avil=[]
        for i in range(self.actiondim):
            new_x=self.pos[self.current_player][0]+self.pos_change[i][0]
            new_y=self.pos[self.current_player][1]+self.pos_change[i][1]
            if (new_x>-1) and (new_x<self.height) and (new_y>-1) and (new_y<self.height):
                if (self.statemap[new_x.astype(int)][new_y.astype(int)]==0):
                    list_avil=list_avil+[i]
        return list_avil

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
        # width = board.width
        # height = board.height

        # print("Player", player1, "with X".rjust(3))
        # print("Player", player2, "with O".rjust(3))
        # print()
        # for x in range(width):
        #     print("{0:8}".format(x), end='')
        # print('\r\n')
        # for i in range(height - 1, -1, -1):
        #     print("{0:4d}".format(i), end='')
        #     for j in range(width):
        #         loc = i * width + j
        #         p = board.states.get(loc, -1)
        #         if p == player1:
        #             print('X'.center(8), end='')
        #         elif p == player2:
        #             print('O'.center(8), end='')
        #         else:
        #             print('_'.center(8), end='')
        #     print('\r\n\r\n')
            
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
        players = {0: player1, 1:player2}
        if is_shown:
            self.graphic(self.board, player1.player, player2.player)
        while(1):
            current_player = self.board.get_current_player()
            player_in_turn = players[current_player]
            move = player_in_turn.get_action(self.board)
            self.board.do_move(move)
            #if is_shown:
            #    self.graphic(self.board, player1.player, player2.player)
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
        states, mcts_probs, current_players, hp_his, times = [], [], [], [], []      
        while(1):
            move, move_probs = player.get_action(self.board, temp=temp, return_prob=1)
            # store the data
            stt,time=self.board.current_state()
            states.append(stt)
            times.append(time)
            hp_his.append(self.board.hp)
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
                    for i in range(len(current_players)):
                        if ((hp_his[i][current_players[i]]-self.board.hp[current_players[i]])>
                             (hp_his[i][1-current_players[i]]-self.board.hp[1-current_players[i]])):
                            winners_z[i]= -1
                        else:
                            winners_z[i] = 1

                    #winners_z[np.array(current_players) == winner] = 1.0
                    #winners_z[np.array(current_players) != winner] = -1.0
                    
                #reset MCTS root node
                player.reset_player() 
                if is_shown:
                    if winner != -1:
                        print("Game end. Winner is player:", winner)
                    else:
                        print("Game end. Tie")
                return winner, list(zip(states, mcts_probs, winners_z, times))
            