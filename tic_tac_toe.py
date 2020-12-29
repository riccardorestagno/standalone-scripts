import tkinter
import random
from itertools import permutations
from time import sleep


class Player:
    """
    Player class to be used in the Game obj

    Attributes:
    name: text to distinguish name of player ie player1, player2, computer
    color: hex code to color each player square on click event
    selected_sq: set data structure to keep track of player squares

    """
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.selected_sq = set()


class Board:
    """
    Board class to be used in the Game obj

    Attributes:
    sq_size: integer to set size of each squares
    color: hex code to color the board size
    """

    def __init__(self, parent, sq_size, color):
        self.parent = parent   # parent is root
        self.sq_size = sq_size
        self.color = color

        # use as a pseudo private attribute, read only
        self._winning_combos = [{1, 2, 3}, {4, 5, 6}, {7, 8, 9},
                      {1, 4, 7}, {2, 5, 8}, {3, 6, 9},
                      {1, 5, 9}, {3, 5, 7}]

        # design to fit tkinter grid(row, col)two params
        self.unused_squares_dict = { '00': 1, '10': 2, '20': 3,
                                     '01': 4, '11': 5, '21': 6,
                                     '02': 7, '12': 8, '22': 9  }

        # create a main container for board
        self.container = tkinter.Frame(self.parent)
        self.container.pack()

        # create canvas for container
        self.canvas = tkinter.Canvas(self.container,
                                     width= self.sq_size * 3,
                                     height= self.sq_size * 3)
        # register main canvas
        self.canvas.grid()

    def get_unused_squares_dict(self):
        return self.unused_squares_dict

    def reset_unused_squares_dict(self):
        self.unused_squares_dict = { '00': 1, '10': 2, '20': 3,
                                     '01': 4, '11': 5, '21': 6,
                                     '02': 7, '12': 8, '22': 9  }

    def draw_board(self):
        for row in range(3):
            for column in range(3):
                self.canvas.create_rectangle(self.sq_size  * column,
                                        self.sq_size  * row,
                                        self.sq_size  * (column + 1),
                                        self.sq_size  * (row + 1),
                                        fill = self.color)

    def get_row_col(self, evt):
        # get the row and col from event's x and y coords
        return evt.x, evt.y

    def floor_of_row_col(self, col, rw):
        """
        normalize col and row number for all board size by taking
        the floor of event's x and y coords as col and row, respectively
        """
        col_flr = col // self.sq_size
        rw_flr = rw // self.sq_size
        return col_flr, rw_flr

    def convert_to_key(self, col_floor, row_floor):
        # turn col and row's quotient into a string for the key
        return str(col_floor) + str(row_floor)

    def find_coords_of_selected_sq(self, evt):
        """
        finding coords in a 9-sq grid

        params: event triggered by user's click
        return: tuple of two values for second corner's col, row
        """
        # saves row and col tuple into two variables
        column, row = self.get_row_col(evt)
        # normalize for all square size by keeping the floor
        column_floor, row_floor = self.floor_of_row_col(column, row)

        # convert to key, use key to locate position in 3x3 grid
        rowcol_key_str = self.convert_to_key(column_floor, row_floor)

        corner_column = (column_floor * self.sq_size) + self.sq_size
        corner_row =  (row_floor  * self.sq_size) + self.sq_size
        #print("rowcol_key_str: " + str(rowcol_key_str))
        return corner_column, corner_row

    def draw_cross(self, evt, second_corner_col, second_corner_row):
        #print(" ---- inside color_selected_sq method ----")
        self.canvas.create_line(
            (evt.x // self.sq_size) * self.sq_size+10,
            (evt.y // self.sq_size) * self.sq_size+10,
            second_corner_col-10,
            second_corner_row-10,
            width = 5)
        self.canvas.create_line(
            (evt.x // self.sq_size) * self.sq_size+10,
            second_corner_row-10,
            second_corner_col-10,
            (evt.y // self.sq_size) * self.sq_size+10,
            width = 5)
            
    def draw_circle(self, evt, second_corner_col,
                      second_corner_row):
        #print(" ---- inside color_selected_sq method ----")
        self.canvas.create_oval(
            (evt.x // self.sq_size) * self.sq_size+10,
            (evt.y // self.sq_size) * self.sq_size+10,
            second_corner_col-10,
            second_corner_row-10,
            width = 5)
        
    def draw_circle_AI(self, square):
        x_coord = {1:100,2:200,3:300,4:100,\
              5:200,6:300,7:100,8:200,9:300}
        y_coord = {1:100,2:100,3:100,4:200,\
                5:200,6:200,7:300,8:300,9:300}
        self.canvas.create_oval(x_coord[square]-90, y_coord[square]-90, 
            x_coord[square]-10, y_coord[square]-10, width = 5)

    @property
    def winning_combos(self):
        return self._winning_combos

class GameApp(object):
    """
    GameApp class as controller for board and player objects

    Attributes:
    parent: (tkinter.Tk) the root window, parent of the frame
    board: instance of the board class
    unused_squares_dict: keep track of squares left on the board
    player1: instance of player class
    player2: ibid
    computer: ibid
    """
    global AI_moves
    AI_moves = []
    
    global player_moves
    player_moves = []
    
    def __init__(self, parent):
        self.parent = parent  # parent is root

        # create a board
        self.board = Board(self.parent, 100, "#ECECEC")  # hex color gray
        self.board.draw_board()

        self.unused_squares_dict = self.board.get_unused_squares_dict()

        # create all players instances
        self.player1 = Player("Player 1", "#446CB3") # hex blue
        self.player2 = Player("Player 2", "#F4D03F") # hex yellow
        self.computer = Player("Computer", "#E67E22") # hex orange

        self.initialize_buttons()
        # create a menu for game option
        self.show_menu()
        
    def AI_move(self):
        """ When selecting to play against the computer, 
        this is the code that runs."""
        
        player_win_combo = 0
        AI_win_combo = 0
        move_to_save = 0
        total_iterations = 0
        row_col_combo_move_chosen = 0
        corners = [1,3,7,9]
        corner_move_comeback = {1:9,3:7,7:3,9:1}
        adjacent_corner_move = [{1,9},{3,7}]
        adjacent_corner_move_comeback = [2,4,6,8]
        row_col_combo_move = [{2,6},{6,8},{4,8},{2,4}]
        row_col_combo_move_comeback ={1:9,2:7,3:1,4:3} 
        keys, number = zip(*self.board.unused_squares_dict.items()) #needed to read dictionary like a list
        corner_moves_left = [move for move in number if move in corners]
        if 5 in number:
            AI_moves.append(5)
            self.delete_values_dict(5)
            self.board.draw_circle_AI(5)
            return
        if len(self.board.unused_squares_dict) == 6:
            for values in adjacent_corner_move:
                for i in values:
                    if i in player_moves:
                        player_win_combo += 1
                if player_win_combo == 2:
                    move = random.choice(adjacent_corner_move_comeback)
                    AI_moves.append(move)
                    self.delete_values_dict(move)
                    self.board.draw_circle_AI(move)
                    return
                player_win_combo = 0
        if len(self.board.unused_squares_dict) == 6:
            for values in row_col_combo_move:
                row_col_combo_move_chosen += 1
                for i in values:        
                    if i in player_moves:
                        player_win_combo +=1
                if player_win_combo == 2:
                    AI_moves.append(row_col_combo_move_comeback[row_col_combo_move_chosen])
                    self.delete_values_dict(row_col_combo_move_comeback[row_col_combo_move_chosen])
                    self.board.draw_circle_AI(row_col_combo_move_comeback[row_col_combo_move_chosen])
                    return
                player_win_combo = 0
            row_col_combo_move_chosen = 0
                    
        for values in self.board.winning_combos:
            for i in values:
                total_iterations +=1
                if i in AI_moves and total_iterations < 3 :
                    AI_win_combo +=1
                    continue
                elif i in AI_moves and total_iterations == 3 :
                    AI_win_combo +=1
                else:
                    move_to_save = i
                if AI_win_combo == 2 and move_to_save in number:
                    AI_moves.append(move_to_save)
                    self.delete_values_dict(move_to_save)
                    self.board.draw_circle_AI(move_to_save)
                    return				
            AI_win_combo = 0
            total_iterations = 0
        for values in self.board.winning_combos:
            for i in values:
                total_iterations +=1
                if i in player_moves and total_iterations < 3 :
                    player_win_combo +=1
                    continue
                elif i in player_moves and total_iterations == 3 :
                    player_win_combo +=1
                else:
                    move_to_save = i
                if player_win_combo == 2 and move_to_save in number:
                    AI_moves.append(move_to_save)
                    self.delete_values_dict(move_to_save)
                    self.board.draw_circle_AI(move_to_save)
                    return
            player_win_combo = 0
            total_iterations = 0
        available_corners = [slot for slot in number if slot in corners]
        if available_corners:
            rand_turn = random.choice(available_corners)
        else:
            rand_turn = random.choice(number)
        AI_moves.append(rand_turn)
        self.delete_values_dict(rand_turn)
        self.board.draw_circle_AI(rand_turn)
        
    def initialize_buttons(self):
        #  --- create buttons for menu ---
        self.two_players_button = tkinter.Button(self.board.container,
                                text = "PLAY WITH A FRIEND",
                                width = 25,
                                command = self.init_two_players_game)

        # bind button to self.play_computer method
        self.computer_button = tkinter.Button(self.board.container,
                                            text = "PLAY WITH THE COMPUTER\n (IMPOSSIBLE TO WIN)",
                                            width = 25,
                                            command = self.init_computer_game)

        self.reset_button = tkinter.Button(self.board.container,
                                           text = "RESET",
                                           width = 25,
                                           command = self.restart)

    def show_menu(self):
         # register buttons to board's container
        self.two_players_button.grid()
        self.computer_button.grid()

    def init_computer_game(self):
    
        #initializing game also resets the current game
        AI_moves[:] = [] 
        player_moves[:] = []
        self.board.container.destroy()
        # create a new board object and draw board + buttons again
        self.board = Board(self.parent, 100, "#ECECEC")
        self.board.draw_board()
        self.initialize_buttons()
        self.show_menu()

        print("Single Player Game")
        
        # reset unused squares on the board
        self.board.reset_unused_squares_dict()

        # reset players' squares
        self.player1.selected_sq = set()
        self.computer.selected_sq = set()
        
        # User starts first
        self.player1_turn = True
        self.computer_turn = True

        # show reset button
        self.reset_button.grid()
        
        #bind play() to the leftmost button click, for macs
        #windows or other pcs might be "<Button-2>"
        self.board.canvas.bind("<Button-1>", self.play)

    def init_two_players_game(self):
    
        #initializing game also resets the current game
        AI_moves[:] = [] 
        player_moves[:] = []
        self.board.container.destroy()
        # create a new board object and draw board + buttons again
        self.board = Board(self.parent, 100, "#ECECEC")
        self.board.draw_board()
        self.initialize_buttons()
        self.show_menu()

        print("Two Player Game")
        #reset current game
        
        # reset board's unused squares
        self.board.reset_unused_squares_dict()

        # reset players' squares to empty set
        self.player1.selected_sq = set()
        self.player2.selected_sq = set()

        # keep track of turns
        self.player1_turn = True
        self.computer_turn = False

        # show reset button
        self.reset_button.grid()

        #bind play() to the leftmost button click, for macs
        #windows or other pcs might be "<Button-2>"
        self.board.canvas.bind("<Button-1>", self.play)

    def restart(self):
        """ Reinitialize the game and board after restart button is pressed """

        AI_moves[:] = [] 
        player_moves[:] = []
        self.board.container.destroy()
        # create a new board object and draw board + buttons again
        self.board = Board(self.parent, 100, "#ECECEC")
        self.board.draw_board()
        self.initialize_buttons()
        self.show_menu()
        print("Game Over")


    def add_to_player_sq(self, key, player_sq):
        """
        use key of col and row to locate position of square
        and add square to player's selected_sq set
        :param key: str concat of col and row key str
        """
        global current_selected_sq
        current_selected_sq = self.board.unused_squares_dict[key]
        # print("current selected sq  ---->", current_selected_sq)
        # print("BEFORE player selected_sq: ", player_sq)
        player_sq.add(current_selected_sq)   # player 1 = {1}
        if self.computer_turn == True:
            player_moves.append(int(current_selected_sq))
        # print("AFTER player selected_sq: ", player_sq)
            


    def delete_used_sq(self, key):
        # delete selected sq in self.board.unused_squares_dict
        # print(" ---- square to delete ---: ", self.board.unused_squares_dict[key])
        # print("unused squares dictionary before: ", self.board.unused_squares_dict)
        del self.board.unused_squares_dict[key]
        # print("unused squares dictionary after: ", self.board.unused_squares_dict)
        
    def delete_values_dict(self, value):
        for values in list(self.board.unused_squares_dict.keys()):
            if self.board.unused_squares_dict[values] == value:
                del self.board.unused_squares_dict[values]
    
    def play(self, event):
        """  method is invoked when the user clicks on a square
        handles click event on UI for player
        Params: event (as mouse click, with x/y coords)
        """
        try:
            # locate second column and row when player click on a square
            colrow_tuple = self.board.find_coords_of_selected_sq(event)

            # save the col and row as variable
            corner_two_col, corner_two_row = colrow_tuple[0], colrow_tuple[1]

            # calculations to get the key to help locate specific square on
            # the unused dictionary of squares left to play
            col_fl, row_fl = self.board.floor_of_row_col(event.x, event.y)
            rowcol_key = self.board.convert_to_key(col_fl, row_fl)
            if self.computer_turn == False:
                try:
                    self.unused_squares_dict[rowcol_key]
                except KeyError:
                    return

            if self.player1_turn == True:
                self.add_to_player_sq(rowcol_key, self.player1.selected_sq)

                # delete from game unused dictionary of set
                self.delete_used_sq(rowcol_key)

                self.board.draw_cross(event,
                                       corner_two_col,
                                       corner_two_row)

                # check game for 3 conditions: a tie, player1 win, or player2 win

                # switch turn with either player 2 or computer
                self.check_for_winner(self.player1.selected_sq, self.player1.name)
                
                if self.computer_turn == True and len(self.board.unused_squares_dict) != 0: 
                    root.update()
                    sleep(1)
                    try:
                        self.AI_move()
                        self.check_for_winner_AI()
                    except ValueError:
                        pass
                else:
                    self.check_for_winner(self.player1.selected_sq, self.player1.name)            
                    self.player1_turn = False

            elif self.player1_turn == False and self.computer_turn == False:  # player 2's turn
                self.add_to_player_sq(rowcol_key, self.player2.selected_sq)
                self.delete_used_sq(rowcol_key)
                self.board.draw_circle(event, corner_two_col, corner_two_row)

                self.check_for_winner(self.player2.selected_sq, self.player2.name)
                self.player1_turn = True
        except KeyError:
                print("A move has already been made on that square. Please make a play on a blank square.")
    
    def check_for_winner(self, player_sq, player_name):
        #removed [if len(self.board.unused_squares_dict) == 0]
        #from original since it wont work if someone wins at the end
        
        if len(player_sq) > 2:
            # start permutation of selected squares
            for combo in permutations(player_sq, 3):
                # loop through all possible combination of 3 from player_sq set
                # return as tuples ex: (1,2,4), (1,2,9), (2,1,9)...
                # change tuple to set and match against winning condition
                # by another inner loop to get through all winning condition list
                for wc in self.board.winning_combos:
                    if set(combo) == wc :
                        player_moves[:] = []
                        AI_moves[:] = []
                        self.show_game_result(player_name + " Wins!")
                        self.restart

        if len(self.board.unused_squares_dict) == 0:
            player_moves[:] = []
            AI_moves[:] = []
            self.show_game_result("Tie Game! Nobody Wins")
            self.restart
            
    def check_for_winner_AI(self):
        player_wins = 0
        AI_wins = 0
        global player_moves
        global AI_moves
        if len(self.board.unused_squares_dict) == 0:
            self.show_game_result("Tie Game. Nobody Wins")
            player_moves[:] = []
            AI_moves[:] = []
            self.restart   
        for values in self.board.winning_combos:
            for i in values:
                if i in player_moves:
                    player_wins +=1
            if player_wins == 3:
                self.show_game_result("Congratz! You win!! \n Which means I fked up somewhere")
                player_moves[:] = []
                AI_moves[:] = []
                self.restart
            else:
                player_wins = 0
        for values in self.board.winning_combos:
            for i in values:
                if i in AI_moves:
                    AI_wins +=1
            if AI_wins == 3:             
                self.show_game_result("Game over. I win!")
                AI_moves[:] = [] 
                player_moves[:] = []
                self.restart
            else:
                AI_wins = 0
    def show_game_result(self, txt):
        """
        make a label to display three possible winning conditions
        params: txt to display the winner
                player_color to display matching color as player's sq
        """
        result_label = tkinter.Label(self.board.container,
                                            text= txt,
                                            width = 32,
                                            height = 10,
                                            foreground = "red",
                                            background = "gray",
                                            borderwidth = 3)

        result_label.grid(row = 0, column = 0)
        # unbind button so player cannot click on square
        self.board.canvas.unbind("<Button-1>")

def main():
    global root
    root = tkinter.Tk()
    root.title("Tic Tac Toe")
    tictac_game = GameApp(root)  # root is parent
    root.mainloop()

if __name__ == '__main__':
    main()