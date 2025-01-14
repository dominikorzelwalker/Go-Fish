import random
import time
import pickle


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
            return None
    
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

    def draw_card(self, deck):
        card = deck.draw_card()

        if card:  # Check if card is not None
            print(f"You drew a {card}!")
            if self.hand[card] == 3:
                print(f"Well done on making a set of {card}'s!")
                self.hand[card] = 0 
                self.score += 1
            else:
                self.hand[card] += 1
        else:
            print(f"There are no more cards in the deck.")

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
        print(f"my cards are: {my_cards}")

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
            print(f"There are no more cards in the deck.")

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


class QLearningBot(PlayerBot):

    def __init__(self, name, score, deck, alpha, gamma, epsilon):
        super().__init__(name, score, deck)
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.Q_table = {}
        self.action_map = {i + 2: deck.ranks[i] for i in range(0, 13)}
        self.Q_table_load()

    def state(self, deck):
        return tuple(self.hand[rank] for rank in deck.ranks)

    def possible_actions(self, state):
        return [i + 2 for i, no_of_cards in enumerate(state) if no_of_cards > 0]

    def action_number_to_card(self, action_number):
        return self.action_map[action_number]

    def choose_action(self, state):

        if not self.possible_actions(state):
            print("Bot has no actions available, so will draw a card.")
            return self.draw_card(self.deck)
        
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.possible_actions(state))
        
        else:
            Q_values = self.Q_table.get(state, {})
            if not Q_values:
                return random.choice(self.possible_actions(state))
            else:
                return max(Q_values, key = Q_values.get)

    def Q_table_save(self, filename="Q_table.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.Q_table, f)

    def Q_table_load(self, filename="Q_table.pkl"):
        try:
            with open(filename, "rb") as f:
                self.Q_table = pickle.load(f)
        except FileNotFoundError:
            print("No saved Q-table found. Using empty Q-table.")

    def Q_table_update(self, current_state, next_state, action, reward):

        Q_value_future = max(self.Q_table.get(next_state, {}).values(), default=0)
        Q_value_old = self.Q_table.get(current_state, {}).get(action, 0)

        Q_value_new = Q_value_old + self.alpha * (reward + self.gamma * Q_value_future - Q_value_old)

        if current_state not in self.Q_table:
            self.Q_table[current_state] = {}

        self.Q_table[current_state][action] = Q_value_new

    def ask_card(self, opponent_hand, deck):
        state = self.state(deck)
        action_number = self.choose_action(state)
        ask_card = self.action_number_to_card(action_number)
        print(f"Q Learning Bot asks for a {ask_card}!")

        cards_taken = False
        reward = 0

        if opponent_hand[ask_card] > 0:
            cards_taken = True
            self.hand[ask_card] += opponent_hand[ask_card]
            opponent_hand[ask_card] = 0
            if self.hand[ask_card] == 4:
                print(f"Q Learning Bot made a set of {ask_card}'s!")
                self.hand[ask_card] = 0
                self.score += 1
                reward = 10
            else:
                reward = 1
        else:
            print(f"Opponent does not hold any {ask_card}'s. You must draw.")
            self.draw_card(deck)
            reward = -1

        next_state = self.state(deck)
        self.Q_table_update(state, next_state, action_number, reward)
        self.Q_table_save()

        return cards_taken
    

def gofish_game():
    deck = Deck()
    player0 = PlayerHuman("Human", 0, deck) 
    player1 = QLearningBot("Q-learning Bot", 0, deck, alpha=0.1, gamma=0.9, epsilon=0.1) 

    player1.Q_table_load()

    players = [player0, player1]

    pointer = 0  

    while deck.deck_length() > 0 or sum(player.cards_number() for player in players) > 0:
        current_player = players[pointer]
        opponent = players[(pointer + 1) % len(players)]

        print("\n" + "="*120)
        print(f"\n========================")
        print(f" {current_player.name}'s Turn")
        print(f"========================")

        cards_taken = current_player.ask_card(opponent.hand, deck)

        print(f"\n========================")
        print(f"Current Game State:")
        print(f"Deck Length: {deck.deck_length()} cards remaining.")
        print(f"Scores: {player0.name}: {player0.score}, {player1.name}: {player1.score}")
        print(f"{player0.name}'s Hand: {player0.hand}")  # Show human player's hand
        print(f"========================")

        time.sleep(5) 

        if not cards_taken:
            pointer = (pointer + 1) % 2  

    print("\n========================")
    print(f"Game Over!")
    for player in players:
        print(f"{player.name} scored {player.score} sets.")
    print("========================")
    
    if player0.score > player1.score:
        print(f"{player0.name} wins!")
    else:
        print(f"{player1.name} wins!")

    player1.Q_table_save()


gofish_game()
