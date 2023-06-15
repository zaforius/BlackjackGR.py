import random
import time

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9,
          'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        cardlist = []
        for card in self.deck:
            cardlist.append(card.__str__())
        return "the deck has " + str(cardlist)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self):

        if self.value > 21:
            if self.aces > 0:
                self.value -= 10
                self.aces -= 1


class Chips:

    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("Παρακαλώ ποντάρετε μερικές μάρκες"))
        except ValueError:
            print("Αυτό δεν είναι αριθμός!")
        else:
            if chips.bet > chips.total:
                print("Δεν έχετε τόσα λεφτά...")
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop

    while True:
        decision = input("Κάρτα ή πάσο? Πατήστε 'h' για κάρτα ή 's' για πάσο...")

        if decision[0].lower() == "h":
            hit(deck, hand)
        elif decision[0].lower() == "s":
            playing = False
        else:
            print("Λάθος εντολή!")
            continue
        break


def show_some(player, dealer):
    print("\n Το χέρι του ντίλερ:")
    print(f" *Card Hidden*, {dealer.cards[1]}")
    print("\n Το χέρι του παίκτη: ")
    print(*player.cards, sep=', ')
    print("Πόντοι παίκτη =", player.value)


def show_all(player, dealer):
    print("\n Το χέρι του ντίλερ:")
    print(*dealer.cards, sep=', ')
    print("Πόντοι ντίλερ =", dealer.value)
    print("\n Το χέρι του παίκτη: ")
    print(*player.cards, sep=', ')
    print("Πόντοι παίκτη =", player.value)


def player_busts(chips):
    print("Δυστυχώς καήκατε...")
    chips.lose_bet()


def player_wins(chips):
    print("Συγχαρητήρια νικήσατε!")
    chips.win_bet()


def dealer_busts(chips):
    print("Ο ντίλερ κάηκε! Συγχαρητήρια νικήσατε!")
    chips.win_bet()


def dealer_wins(chips):
    print("Ο ντίλερ νίκησε! Δυστυχώς χάσατε...")
    chips.lose_bet()


def push():
    print("Ισοπαλία! :O")


# Set up the Player's chips
print("Καλώς ήρθατε στο Black Jack GR! \n")
time.sleep(1)
my_chips = Chips()

while True:
    try:

        print("Πόσες μάρκες έχετε; (50-500) \n")
        markes = int(input())
    except ValueError:
            print("Παρακαλώ δώστε έγκυρο αριθμό...")
    else:
        if 49 < markes < 501:
            my_chips.total = markes
            break
        elif markes == 0:
            my_chips.total = markes
            break
        else:
            print("Παρακαλώ δώστε έγκυρο αριθμό...")

while True:

    # Create & shuffle the deck, deal two cards to each player
    print("Ανακατεύουμε το deck...\n")
    deck1 = Deck()
    deck1.shuffle()
    time.sleep(1)
    print("Μοιράζουμε τις κάρτες...\n")
    player_hand = Hand()
    dealer_hand = Hand()

    hit(deck1, dealer_hand)
    hit(deck1, dealer_hand)
    hit(deck1, player_hand)
    hit(deck1, player_hand)
    time.sleep(1)

    # Prompt the Player for their bet

    print(f"Έχετε {my_chips.total} μάρκες\n")
    time.sleep(1)
    take_bet(my_chips)


    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck1, player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(my_chips)
            print(f"Έχετε {my_chips.total} μάρκες\n")
            break

    if my_chips.total < 1:
        print("Δυστυχως φαληρήσατε...")
        playing = False
        break


    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck1, dealer_hand)

        # Show all cards
        time.sleep(1)
        show_all(player_hand, dealer_hand)
        print("\n")
        time.sleep(1)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(my_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(my_chips)
        elif player_hand.value > dealer_hand.value:
            player_wins(my_chips)
        else:
            push()

        # Inform Player of their chips total
        print(f"Έχετε {my_chips.total} μάρκες\n")

    if my_chips.total < 1:
        print("Δυστυχως φαληρήσατε...")
        break



     # Ask to play aga
    if my_chips.total > 0:
        print("Θέλετε να παίξετε και άλλο χέρι; y -- n ")
        new_hand = input()
        if new_hand[0].lower() == 'y':
            playing = True
            continue
        else:
            print("Ευχαριστούμε που παίξατε!!!")
            break

















