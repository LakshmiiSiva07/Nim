import random
import math

"This program simulates NIM GAME with the help of Alpa Beta pruning algorithm"
infinity = 10000 


#NIM Game is structured as a class 
class NimGame:

  def __init__(self,player): #The initial configuration is initialized
    self.pile1 = 1           #The game 4 piles each initialized to 1,3,5,7
    self.pile2 = 3
    self.pile3 = 5
    self.pile4 = 7
    self.player = player    #The first player to play,"Can be "You" or "Computer"
    self.utility = 0
    

  def _generate_legal_moves(self):  # Given a state of the game it generates all posiblle legal moves
     
    m = []
    legalmoves = []
    for i in range(4):
     pileno = i + 1
     temppile = 0                   # The pile is chosen
     if pileno == 1:
       temppile = self.pile1
     elif pileno == 2:
       temppile = self.pile2
     elif pileno == 3:
       temppile = self.pile3
     elif pileno == 4:
       temppile = self.pile4

     for j in range(temppile):      #One or total number of piles can be removed
       m  = temppile - j,pileno
       legalmoves.append(m)
    return legalmoves

  def _clone(self):                 #The state of an object is cloned and actions
                                    #take place on it.The purpose of this is to obtain result
      p = NimGame(self.player)      #modifying parent
      p.pile1 = self.pile1
      p.pile2 = self.pile2
      p.pile3 = self.pile3
      p.pile4 = self.pile4

      self.utility = 0
      return p
  
  def actions(self):
      x = self._generate_legal_moves()  #Returns legal actions
      return x
  
  def result(self,a):                   #Given a state and an action it generates the result of an action
        sticks,pileno = a  
        p = self._clone()
        if pileno == 1:
         if (sticks <= p.pile1):         #If chosen sticks are greater than the available sticks a warning appears
          p.pile1 = p.pile1 - sticks
         else:
          print "Invalid Entry"         
        elif pileno == 2:
         if (sticks <= self.pile2):
          p.pile2 = p.pile2 - sticks
         else:
          print "Invalid Entry"
        elif pileno == 3:
         if (sticks <= self.pile3):
          p.pile3 = p.pile3 - sticks
         else:
          print "Invalid Entry"
        elif pileno == 4:
         if (sticks <= self.pile4):
          p.pile4 = p.pile4 - sticks
         else:
          print "Invalid Entry"

         if p.player == "Computer":   #At the end of an action players are swapped
           p.player = "User"
         else:
           p.player = "Computer"
        return p


  def display(self):                 #Displays pile no and corresponding sticks in a pile
     
     print "PILE 1 - ",
     print self.pile1
     print "\n"
     print "PILE 2  - ",
     print self.pile2
     print "\n"
     print "PILE 3  - ",
     print self.pile3
     print "\n"
     print "PILE 4  - ",
     print self.pile4

     return "_________________________________________________________________________" 

   
 
  def making_move(self,pileno,sticks): #Removes the given no of sticks in a given pile altering the state of
      if pileno == 1:                  #the game
        if (sticks <= self.pile1):
      	  self.pile1 = self.pile1 - sticks
        else:
          return "Invalid Entry"
      elif pileno == 2:
         if (sticks <= self.pile2):
          self.pile2 = self.pile2 - sticks
         else: 
          return "Invalid Entry"      #Returns an error message if move is not valid
      elif pileno == 3:
         if (sticks <= self.pile3):
          self.pile3 = self.pile3 - sticks
         else:
          return "Invalid Entry"
      elif pileno == 4:
         if (sticks <= self.pile4):
          self.pile4 = self.pile4 - sticks
         else:
          return "Invalid Entry"
      return "VALID"

  def terminal_test(self):            #If the action removes all the sticks then it means the last stick is removed
  	if self.pile1 + self.pile2 + self.pile3 + self.pile4  == 0:
          return True
        else:
          return False

  def utility_func(self,player):     #Returns the utility value 1 is Win for Computer 0 is Loss for computer
        if player == "Computer":
          return 1
        else:
          return 0
 
  def declare_win(self,player):     #Returns the utility value 1 is Win for Computer 0 is Loss for computer
        if player == "Computer":
          print "COMPUTER HAS WON"
        else:
          print "USER HAS WON"

  

def best_action(game_state):        #Given a state of the game it generates the best action to win

  Tree = Node(game_state)
  Tree = makeTreeAplhaBeta(Tree,game_state)  #Generates a tree
  if len(Tree.children) > 0:
   for i in Tree.children:
      if  i.state.utility == 1:              #Returns the best utility state
	if(game_state.pile1 != i.state.pile1):
          action_pile_no = 1
	  action_sticks = game_state.pile1 - i.state.pile1
	elif(game_state.pile2 != i.state.pile2):
	  action_pile_no = 2
	  action_sticks = game_state.pile2 - i.state.pile2
        elif(game_state.pile3 != i.state.pile3):
          action_pile_no = 3
          action_sticks = game_state.pile3 - i.state.pile3
        elif(game_state.pile4 != i.state.pile4):
          action_pile_no = 4
          action_sticks = game_state.pile4 - i.state.pile4
        print "ACTION: ",action_sticks, " sticks has been taken from pile",action_pile_no
        return action_pile_no, action_sticks
   print "No best move so a random action taken"
  for a in game_state.actions():   #If no action is best it generates the random action
     action_sticks,action_pile_no = a
     print "ACTION:" ,action_sticks,"sticks has been taken from pile",action_pile_no
     return action_pile_no, action_sticks

class Node:  #Node structure to store all the generated nodes

   def __init__(self,state):
       self.state = state
       self.children = [] 



def makeTreeAplhaBeta(root,game):
#make tree using alphabeta pruning
    player = game.player
    
    def max_value(node, state, alpha, beta):
	if state.terminal_test():
             return state.utility_func(state.player)
        v = -infinity
        for a in state.actions():
            node.children.append(Node(state.result(a)))
            v = max(v, min_value(node.children[len(node.children)-1], state.result(a), alpha, beta))
            if v >= beta:
                node.state.utility = v
                return v
            alpha = max(alpha, v)
        node.state.utility = v
        return v

    def min_value(node, state, alpha, beta):
        if state.terminal_test():
            return state.utility_func(state.player)
        v = infinity
        for a in state.actions():
            node.children.append(Node(state.result(a)))
            v = min(v, max_value(node.children[len(node.children)-1], state.result(a), alpha, beta))
            if v <= alpha:
                node.state.utility = v
                return v
            beta = min(beta, v)
        node.state.utility = v
        return v
    if game.player == "Computer":

        max_value(root, root.state, -infinity, infinity)
    else:
        min_value(root, root.state, -infinity, infinity)
    return root

def main ():
 
  pile_no = 0
  no_of_sticks = 0
  PLAYER = raw_input("Enter who should play first Computer or You \n")
  game = NimGame(PLAYER)
  #Visual representaation of the game
  game.display()
  while (game.terminal_test() == 0): #Play till terminal state is reached
    print game.player
    if game.player == "Computer":
       pile_no, sticks = best_action(game) #Computer generates an action using the alpha beta pruning tree
       game.making_move(pile_no, sticks)
       game.player = "User"                 #Alternate the player
    else:
       print "Legal moves Available"
       print game.actions()                #Returns legal moves the user can make
       print "(3,2) means you can remove 2 sticks from pile 3"
       pile_no = input("Enter the pile")
       no_of_sticks = input("Enter the no of sticks")
       VALID = game.making_move(pile_no,no_of_sticks)
       if VALID == "Invalid Entry":        # If illegal move play again
        print "INVALID ENTRY PLAY AGAIN"
        game.player = "User"
       else:
        game.player = "Computer"
    game.display()
  game.declare_win(game.player)
  
 
if __name__ == "__main__":
  main()
