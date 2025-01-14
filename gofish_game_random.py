import random
import time


class Deck: 

    ranks = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]

    def __init__(self):
        self.cards = []

        for rank in self.ranks:
            for i in range(4):
                self.cards.append(rank)

        random.shuffle(self.cards)

    def draw_card(self):
        if self.cards:
            return self.cards.pop()
        else:
            None

    def print_deck(self):
        for card in self.cards:
            print(card)

    def deck_length(self):
        return len(self.cards)


class Player:

    def __init__(self, name, score, deck):
        self.name = name
        self.hand = {rank: 0 for rank in deck.ranks}
        
        for i in range(7):
            card = deck.draw_card()
            self.hand[card] += 1
        
        self.score = score

    def cards_number(self):
        return sum(self.hand.values())


class PlayerHuman(Player):

    def draw_card(self, deck):
        card = deck.draw_card()

        if card:
            print(f"You drew a {card}!")
            if self.hand[card] == 3:
                print(f"Well done on making a set of {card}'s!")
                self.hand[card] = 0 
                self.score += 1
            else:
                self.hand[card] += 1
        else:
            print(f"There are no more cards in the deck.")

    def ask_card(self, opponent_hand, deck):
        print(f"Your current hand is: {self.hand}")
        my_cards = [rank for rank in self.hand.keys() if self.hand[rank] > 0]
        print(f"The cards you can ask for are: {my_cards}")

        if my_cards:
            while True:
                try:
                    random_card = input("Which card shall you ask for?")
                    if random_card in my_cards:
                        break
                    else:
                        print("You do not hold that card, try again.")
                except ValueError:
                    print("Invalid, try again.")

            cards_taken = False

            if opponent_hand[random_card] > 0:
                cards_taken = True
                print(f"Well done, you have just collected {opponent_hand[random_card]} {random_card}'s!")
                self.hand[random_card] += opponent_hand[random_card]
                opponent_hand[random_card] = 0

                if self.hand[random_card] == 4:
                    print(f"Well done on completing a set!")
                    self.hand[random_card] = 0
                    self.score += 1

            if cards_taken:
                print("You get another turn to ask for a card!")

            if not cards_taken:
                print(f"Opponent does not hold any {random_card}'s. You must draw.")
                self.draw_card(deck)

            return cards_taken

        else:
            self.draw_card(deck)
            return False


class PlayerBot(Player):

    def draw_card(self, deck):
        card = deck.draw_card()

        if card:
            if self.hand[card] == 3:
                print(f"Bot made a set of {card}'s!")
                self.hand[card] = 0
                self.score += 1
            else:
                self.hand[card] += 1
        else:
            print("There are no more cards in the deck.")

    def ask_card(self, opponent_hand, deck):
        my_cards = [rank for rank in self.hand.keys() if self.hand[rank] > 0]

        if my_cards:
            random_card = random.choice(my_cards)
            print(f"Bot asks for a {random_card}!")

            cards_taken = False
            if opponent_hand[random_card] > 0:
                cards_taken = True
                self.hand[random_card] += opponent_hand[random_card]
                opponent_hand[random_card] = 0

                if self.hand[random_card] == 4:
                    print(f"Bot made a set of {random_card}'s!")
                    self.hand[random_card] = 0
                    self.score += 1

            if cards_taken:
                print("Bot gets another turn to ask for a card!")

            else:
                print(f"Opponent does not hold any {random_card}'s. You must draw.")
                self.draw_card(deck)

            return cards_taken
        else:
            self.draw_card(deck)
            return False
    

def gofish_game():

    deck = Deck()
    player0 = PlayerHuman("Human", 0, deck)
    player1 = PlayerBot("Bot", 0, deck)

    players = [player0, player1]

    pointer = 0

    while deck.deck_length() or sum(player.cards_number() for player in players):
        current_player = players[pointer]
        opponent = players[(pointer + 1) % 2]

        print(f"\n========================")
        print(f" {current_player.name}'s Turn")
        print(f"========================")

        cards_taken = current_player.ask_card(opponent.hand, deck)

        print(f"\n========================")
        print(f"Current Game State:")
        print(f"Deck Length: {deck.deck_length()} cards remaining.")
        print(f"Scores: {player0.name}: {player0.score}, {player1.name}: {player1.score}")
        print(f"{player0.name}'s Hand: {player0.hand}")  
        print(f"========================")

        time.sleep(5)

        if not cards_taken:
            pointer = (pointer + 1) % 2

    # Output final scores
    print("\n========================")
    print(f"Game Over!")
    for player in players:
        print(f"{player.name} scored {player.score} sets.")
    print("========================")

    # Determine the winner
    if player0.score > player1.score:
        print(f"{player0.name} wins!")
    else:
        print(f"{player1.name} wins!")


gofish_game()
