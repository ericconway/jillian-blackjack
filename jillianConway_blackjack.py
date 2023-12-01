##blackjack

import random
import re

""""
initializing a scoreBoard and a full deck of cards as dictionaries 
"""
full_deck = {
    "2 of Hearts": 2, "3 of Hearts": 3, "4 of Hearts": 4, "5 of Hearts": 5, "6 of Hearts": 6, "7 of Hearts": 7, "8 of Hearts": 8, "9 of Hearts": 9, "10 of Hearts": 10,
    "Jack of Hearts": 10, "Queen of Hearts": 10, "King of Hearts": 10, "Ace of Hearts": 11, 
    "2 of Diamonds": 2, "3 of Diamonds": 3, "4 of Diamonds": 4, "5 of Diamonds": 5, "6 of Diamonds": 6, "7 of Diamonds": 7, "8 of Diamonds": 8, "9 of Diamonds": 9, "10 of Diamonds": 10,
    "Jack of Diamonds": 10, "Queen of Diamonds": 10, "King of Diamonds": 10, "Ace of Diamonds": 11, 
    "2 of Spades": 2, "3 of Spades": 3, "4 of Spades": 4, "5 of Spades": 5, "6 of Spades": 6, "7 of Spades": 7, "8 of Spades": 8, "9 of Spades": 9, "10 of Spades": 10,
    "Jack of Spades": 10, "Queen of Spades": 10, "King of Spades": 10, "Ace of Spades": 11,
    "2 of Clubs": 2, "3 of Clubs": 3, "4 of Clubs": 4, "5 of Clubs": 5, "6 of Clubs": 6, "7 of Clubs": 7, "8 of Clubs": 8, "9 of Clubs": 9, "10 of Clubs": 10,
    "Jack of Clubs": 10, "Queen of Clubs": 10, "King of Clubs": 10, "Ace of Clubs": 11
                }
scoreBoard = {}
cards = {}
         

"""
This function starts the program. It asks the user if they know how to play or if they want to know the rules. After the user's choice,
it starts the game and calls the game() function.
"""
def intro():
    global scoreBoard #creates a global scoreBoard to be accessed in other functions
    global cards #creates a global cards to be accessed in other functions
    cards = full_deck.copy() #creates a copy of the deck
    scoreBoard = {}
    test = True
    print("Welcome to blackjack!")
    while test == True:
        rules = input("Do you want to know the rules of blackjack? y/n: \t")
        if rules == "y":
            print("""
                In blackjack, the goal is to have a hand value as close to 21 as possible without exceeding it. 
                Players are dealt two cards and can choose to "hit" (take additional cards) to improve their hand or "stand" (keep their current total).
                Number cards are worth their face value, face cards (Jack, Queen, King) are worth 10 points each, and Aces can be worth 1 or 11 points.
                The value of aces depends on if the player"s hand exceeds 21 when the value is worth 11. If it does, it is worth 1.
                If a player"s hand exceeds 21, they bust and lose the game. 
                The player wins if their hand is closer to 21 without going over. 
                """)
            print("Alright, now that you know the rules, lets get ready to play")
            test = False
        elif rules == "n":
            print("Alright lets get ready to play!")
            test = False
        else:
            print("enter either y or n") #if the user enters anything other than y or n, asks the user again
    game() # calls the function "game" after running through "intro"
    end_game()  # calls the function "end game" after "game" and all of the smaller functions called within "game"



"""
This function asks the user how many players are playing blackjack. Then, it deals the first two cards for each player and removes the cards that
were draw from the card dictionary. It calls the calculate_score() function to determine if the user's hand is over 21 or not.
If the score is under 21, it will continue to ask the user to hit or stand until the user enters stand, or the score is over 21. 
Once the first player is done with his/hers turn it adds the player and score to the scoreBoard dictionary, and moves on to the next player. 
If the player busts, they are not added to the scoreBoard.
"""
def game():
    while True:
        num_of_players_str = input("how many players are playing blackjack?\t") 
        num_of_players = 0 #initializes number of players to zero
        try: 
            num_of_players = int(num_of_players_str) #turns user input of number of players into an integer and sets it equal to the variable num of players
            if num_of_players >= 2: #this version of blackjack must have more than one player
                break
            else:
                print("Please enter at least 2 players.")
        except ValueError:
            print("Please enter a valid integer.") #error catch if the user enters anything other than an integer
    print("Okay! There will be: " , num_of_players, " players") #displays how many players are playing
    for player in range(num_of_players): #for each player that the user entered
        score = 0 #initialize the player's score
        player_hand = {} #initialize the player's hand
        #draw one card
        player_hand = draw_card(player_hand)
        #draw two card
        player_hand = draw_card(player_hand)
        score = calculate_score(player_hand) #calculates the players score
        # prints out the players hand and their current score
        print("player " + str(player + 1) + " s hand is: " , player_hand )
        print("Total: " , score)

        while score < 21: #if score is less than 21, the program asks the user to hit or stand
            hit_or_stand = input("enter hit or stand for player: " + str(player + 1)+ "\t")
            if hit_or_stand == "hit":
                # draw another card
                player_hand = draw_card(player_hand)
                score = calculate_score(player_hand) 
                #prints the player's hand and new score
                print("player " + str(player + 1) + " s hand is: " , player_hand )
                print("Total: " , score)
            elif hit_or_stand == "stand":
                break #moves on to the next player
        if score > 21: #if score is more than 21 the player busts
            print("bust!")
        if score <= 21: #if score is less than or equal to 21 the player's score is added to scoreboard
            scoreBoard["player" + str(player + 1)] = score 



"""
draws a card from the deck, adds it to the player's hand, and then removes that card from the deck so it can't be drawn again
"""
def draw_card(player_hand):
    #draw one card
    random_card1 = random.choice(list(cards.keys()))
    player_hand[random_card1] = cards[random_card1] 
    cards.pop(random_card1) #removes the card from the deck
    return player_hand



"""
This function calculates the score of a players hand when it is called in the game() function. 
It also changes the value of an ace based on the player's score
"""
def calculate_score(hand):
    score = 0
    # aces counter
    aces = 0
    ace_pattern = re.compile(r'^Ace') #uses regular expression to see if an ace is drawn
    for card,value in hand.items():
        if ace_pattern.match(card):
            aces +=1
        else:
            score += value
    # now we have score of all cards not aces
    for x in range(aces): #changes the value of an ace based on the players hand
        if score + 11 <= 21:
            score += 11
        elif score + 11 > 21:
            score += 1
    return score




"""
This function prints the scoreBoard and then finds the highest value on the scoreBoard that is under 21.
The closest value to 21 that does not go over are displayed as the winners.
It then asks the user if they want to play the game again or quit the program.
"""
def end_game():
    winners = [] #initializes a winner array if there are multiple with the same score
    print("Game Over!")
    print(scoreBoard)
    max_value = max(scoreBoard.values()) #finds the max value of the array (players with over 21 are not included in array)
    for player, score in scoreBoard.items():
        if score == max_value:
            winners.append(player)
    print("Winner(s): " , winners) #displays winners 
    while True:
        play_again = input("do you want to play again? y/n: \t") #asks the user if they want to play again or end program
        if play_again == "y":
            intro()
        elif play_again == "n":
            exit() 
        else:
            print("enter either y or n")

            ## print blackslash to print out special character &


intro() #starts the program when it is run 
  

