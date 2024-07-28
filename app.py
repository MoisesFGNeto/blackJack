import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,'Queen':10, 'King':10, 'Ace':11}
playing = True

class Card:
    def __init__(self, suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit 

class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
    	    for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        return "The deck has:\n" + "\n".join(str(card) for card in self.deck)

    def __len__(self):
        return len(self.deck)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def __str__(self):
        return str(self.value)

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

        # Track Aces
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        # IF TOTAL VALUE > 21 AND I STILL HAVE AN ACE
        # THAN CHANGE MY ACE TO BE A 1 INSTEAD OF AN 11
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
    
class Chips:

    def __init__(self, total=100):
        self.total = total # This can be set to a default value or supplied by a user input.
        self.bet = 0
    
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def take_bet(self):
    while True:
        try:
            self.bet = int(input("How many chips would you like to bet? "))
        except ValueError:
            print("Sorry please provide a integer")
        else:
            if self.bet > self.total:
                print("Sorry, you do not have enough chips! You have: {}".format(self.total))
            else:
                break

def hit(deck, hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing

    while True:
        x = input("Hit or Stand? Enter 'h' or 's'. ")

        if x[0].lower() == 'h':
            hit(deck,hand)
        
        elif x[0].lower() == 's':
            print("Player Stands Dealer's turn ")
            playing = False
        
        else: 
            print("Sorry, I did not understand that, Please enter h or s only!")
            continue

        break

def show_some(player,dealer):
    # Show only ONE of the dealer's cards
    print("\n Dealer's Hand:")
    print("First card hidden!")
    print(dealer.cards[1])  

    # Show all (2 cards) of the player's hand/cards
    print("\n Player's hand:")
    for card in player.cards:
        print(card)


def show_all(player,dealer):
    # Show all de dealer's cards
    print("\n Dealer's hand:", *dealer.cards, sep='\n')
    # Calculate and display value (J+K == 20)
    print(f"Value of dealer's hand is :{dealer.value}")
    # Show all the players cards
    print("\n Players's hand:")
    print("\n Dealer's hand:", *dealer.cards, sep='\n')
    print(f"Value of player's hand is :{player.value}")

def player_busts(player,dealer,chips):
    print("BUST PLAYER")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("PLAYER WINS!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("PLAYER WINS! DEALER BUSTED")
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print('DEALER WINS')
    chips.lose_bet()

def push(player,dealer):
    print("Dealer and player tie! It's a PUSH")

while True:
    # Print an opening statement
    print("Welcome to BLACKJACK GAME!")

    # Create & shuffle the deck, deal two cards to each player and dealer.
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Player's chips
    player_chips = Chips()

    # Prompt the player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)

    while playing: # Recall this variable from our hit_or_stand function
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand,player_chips)
            break
    
    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck,dealer_hand)
        
        #Show all cards
        show_all(player_hand,dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)

        else:
            push(player_hand,dealer_hand) 
    
    # Inform Player of their chips total 
    print(f"\nPlayer's winnings stand at {player_chips.total}")
    
    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    
    if new_game[0].lower()=='y':
        playing=True
        continue
    else:
        print("Thanks for playing!")
        break