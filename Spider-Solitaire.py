#  , Carson Mead
#
#Spider - Solotaire
#solving for "stacks" of cards from king to ace.  All cards are the same suit.
#104 cards in play, with 54 cards in ten stacks, then a draw pile of the other 50.
#
import random

class Board():
  def __init__(self):
    # "[]" is a face down card    "--" is an empty slot
    #cards are letters or numbers otherwise

    #cards array holds all cards required for the game, 104 cards all of the same suit
    self.cards = [
      "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
      "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
      "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
      "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
      "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
      "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
      "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
      "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
    ]
    #the board will be a 2d array, two boards will be stored, one with the cards to keep track of them, and the other to display for the player
    self.map_board = [[], [], [], [], [], [], [], [], [], []]
    self.display_board = [[], [], [], [], [], [], [], [], [], []]
    #this is the way we keep track of what cards the player has flipped over
    self.visible_ind = [5, 5, 5, 5, 4, 4, 4, 4, 4, 4]
    #the stack of draw cars will be an array as well
    self.draw = []

    #now we begin the actions to set up the board, including shuffling and dispersing
    #shuffling
    random.shuffle(self.cards)
    #this is creating the draw pile
    for x in range(0, 50):
      self.draw.insert(0, self.cards.pop(0))

    #then, we distribute the rest onto the board
    for x in range(0, 10):
      for y in range(0, 5):
        self.map_board[x].insert(0, self.cards.pop(0))

    for x in range(0, 4):
      self.map_board[x].insert(0, self.cards.pop(0))

    #now to encode the display board
    self.display_board_update()

  #this encodes the display_board from the map_board, it iterates through the map board and deciphers
  #  the position of the cards, or absence of cards.  It also changes face card numbers into letters
  def display_board_update(self):
    self.display_board = [[], [], [], [], [], [], [], [], [], []]
    #find largest coloumn
    tall_ind = 0
    for x in range(1, 10):
      if (len(self.map_board[x]) > len(self.map_board[tall_ind])):
        tall_ind = x
    for x in range(0, 10):
        for y in range(0, len(self.map_board[tall_ind])):
          if (len(self.map_board[x]) <= y):
            self.display_board[x].append("--")
          elif (y < self.visible_ind[x]):
            self.display_board[x].append("[]")
          else:
            self.display_board[x].append(self.map_board[x][y])
            temp = self.display_board[x][y]
            if (temp == "1"):
              self.display_board[x][y] = "A"
            elif (temp == "11"):
              self.display_board[x][y] = "J"
            elif (temp == "12"):
              self.display_board[x][y] = "Q"
            elif (temp == "13"):
              self.display_board[x][y] = "K"

              
  #draw_cards -- adds turned over cards to board in each coloumn
  def draw_cards(self):
    for x in range(0, 10):
      temp = self.draw.pop(0)
      self.map_board[x].append(temp)
    self.update_board()

  
  #these next methods are in order for gameplay, move_stack, update board, print board
    
  #move_stack -- returns false if move can't be carried out, otherwise makes move and reutrn true
  def move_stack(self, c1, c2):
    col1 = int(c1) - 1
    col2 = int(c2) - 1
    
    #keeps track of the stack we're moving
    stack = [self.map_board[col1][len(self.map_board[col1]) - 1]]
    #first, we find how large the stack is that the user is trying to move
    #  this is done by taking the visible cards, and traveling up them counting the stack 
    if (int(stack[0]) + 1 == int(self.map_board[col1][len(self.map_board[col1]) - 2])):
      for y in range(1, (int((len(self.map_board[col1]) + 1) - (int(self.visible_ind[col1]))))):
        #this tests if the next card in the stack is 1 greather than the current card in stack
        if ((int(self.map_board[col1][len(self.map_board[col1]) - y]) + 1) == int(self.map_board[col1][len(self.map_board[col1]) - y - 1])):
          print(stack)
          #if that card qualifies as another in the stack it's added to the stack array
          stack.append(self.map_board[col1][len(self.map_board[col1]) - y - 1])
        else:
          break

    if (((int(stack[len(stack) - 1])) == 13) and (len(self.map_board[col2]) == 0)):
      for y in range(0, len(stack)):
        self.map_board[col2].append(stack.pop())
        self.map_board[col1].pop()
      #Now, we're finding if the visible cards needs to be changed after that move
      if (self.visible_ind[col1] == len(self.map_board[col1])):
        self.visible_ind[col1] -= 1
      self.update_board()
      return True

    for i in range(0, len(stack) - 1):
      if (int(stack[i]) >= int(self.map_board[col2][len(self.map_board[col2]) - 1])):
        stack.pop()
    #then we test if we can actually move it, if so the move is carried out
    if (len(stack) >= 1):
      if ((int(stack[len(stack) - 1]) + 1) == int(self.map_board[col2][len(self.map_board[col2]) - 1])):
        #then, for each card in the stack we just cut and paste them on the destination column
        for y in range(0, len(stack)):
          self.map_board[col2].append(stack.pop())
          self.map_board[col1].pop()
        #Now, we're finding if the visible cards needs to be changed after that move
        if (self.visible_ind[col1] == len(self.map_board[col1])):
          self.visible_ind[col1] -= 1
        self.update_board()
        return True
    else:
      return False
    
  #update_board -- at the end of an input round, run this after, it willcheck for stacks and cards to reveal
  def update_board(self):
    #this loop iterates through each column and tries to find completed stacks A - K
    for x in range(0, 10):
      if (len(self.map_board[x]) >= 13):
        count = 1
        for y in range(0, 13):
          if (int(self.map_board[x][y]) == count):
            count += 1
        if (count == 13):
          for r in range(0, 13):
            self.map_board.pop(len(self.map_board[x] - r))
    #then, it sets the changes made to the map_board to the display_board
    self.display_board_update()


    
  #print_board -- prints baord to console when called
  def print_board(self):
    print("1\t2\t3\t4\t5\t6\t7\t8\t9\t10")
    
    #print based off largest column
    for y in range(0, len(self.display_board[0])):
      line = ""
      for x in range(0, 10):
        line += self.display_board[x][y] + "\t"
      print(line)

    print("Draw pile: " + str(len(self.draw)))


#setting up the game
board = Board()
pile_total = 0
for x in range(0, 10):
  for y in range(0, len(board.map_board[x])):
    pile_total += 1

pile_total += len(board.draw)

#turns and round system
while pile_total > 0:
    board.print_board()
    print('\nEnter d:draw, q:quit, or the column number of a stack you\'d like to move')
    enter = input('>>>>>\t')
    if enter == 'd':
        if len(board.draw) > 0:
            board.draw_cards()
        else:
            print('The deck is empty')
            
    elif enter == 'q':
        pile_total -= 104

    elif enter == "":
         pass
    elif ((int(enter) <= 10) and (int(enter) >= 1)):
      col2 = input("Where is this going?\t")
      if (col2 != ""):
        if ((int(col2) <= 10) and (int(col2) >= 1)):
          if (board.move_stack(enter, col2)):
            print("Move made!")
          else:
            print("Move cannot be made.")
        else:
          print("Not a valid placement.")
      else:
        print("Please try again, first number.")
    else:
        print('Invalid Option')

print("Make sure to play again!")
