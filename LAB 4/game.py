# Task 3 — Multi-round bankroll DONE
from cards import Deck, hand_value

class Blackjack:
    def __init__(self):
        # TASK 3: Persistent Bankroll
        # Starting chips initialized to 100; persists across multiple rounds.
        self.chips = 100
        self.deck = Deck()

    def show(self, player, dealer, hide=True):
        # TASK 4: Clear Display & Feedback
        # Displays dealer hidden card during player turn and reveals on stand.
        if hide:
            shown_dealer = [f"{dealer[0][0]}{dealer[0][1]}", "??"]
            print("Dealer:", " ".join(shown_dealer))
        else:
            shown_dealer = [f"{r}{s}" for r, s in dealer]
            print("Dealer:", " ".join(shown_dealer), f"(= {hand_value(dealer)})")
        
        print("Player:", " ".join(f"{r}{s}" for r, s in player), "=", hand_value(player))

    def get_wager(self):
        """Prompts for wager and validates input against available chips."""
        while True:
            print(f"\nCurrent Chips: {self.chips}")
            val = input(f"Enter wager (1-{self.chips}) or 'q' to quit: ").strip().lower()
            if val == "q":
                return None
            if val.isdigit():
                wager = int(val)
                if 1 <= wager <= self.chips:
                    return wager
            print("Invalid wager amount. Please enter a valid whole number within your bankroll.")

    def round(self):
        """Executes one round of Blackjack from wager to settlement."""
        wager = self.get_wager()
        if wager is None:
            return False

        # Deal initial hands
        player = [self.deck.draw(), self.deck.draw()]
        dealer = [self.deck.draw(), self.deck.draw()]

        print("\n--- New Round ---")
        self.show(player, dealer, hide=True)

        pv = hand_value(player)
        dv = hand_value(dealer)

        # Check Natural Blackjacks
        player_bj = (pv == 21)
        dealer_bj = (dv == 21)

        if player_bj or dealer_bj:
            print("\n--- Round Outcome ---")
            self.show(player, dealer, hide=False)
            if player_bj and dealer_bj:
                print("Both player and dealer have Natural Blackjack! Push.")
            elif player_bj:
                print(f"Natural Blackjack! You win {wager} chips.")
                self.chips += wager
            else:
                print(f"Dealer has Natural Blackjack! You lose {wager} chips.")
                self.chips -= wager
            return True

        # Player Turn
        busted = False
        while hand_value(player) < 21:
            key = input("[h]it [s]tand [q]uit: ").strip().lower()
            if key == "q":
                print("Quitting game...")
                return False
            elif key == "h":
                card = self.deck.draw()
                player.append(card)
                print(f"--> You drew {card[0]}{card[1]}")
                self.show(player, dealer, hide=True)
                if hand_value(player) > 21:
                    print(f"\nBust! Hand exceeded 21. You lost {wager} chips.")
                    self.chips -= wager
                    busted = True
                    break
            elif key == "s":
                break
            else:
                print("Invalid command! Type 'h' to hit, 's' to stand, or 'q' to quit.")

        if busted:
            return True

        # Dealer Turn
        print("\nDealer reveals cards:")
        self.show(player, dealer, hide=False)

        while hand_value(dealer) < 17:
            card = self.deck.draw()
            dealer.append(card)
            print(f"--> Dealer draws {card[0]}{card[1]}")
            self.show(player, dealer, hide=False)

        # Final Settlement
        pv = hand_value(player)
        dv = hand_value(dealer)

        print("\n--- Round Outcome ---")
        if dv > 21:
            print(f"Dealer busts! You win {wager} chips.")
            self.chips += wager
        elif pv > dv:
            print(f"You win! Won {wager} chips.")
            self.chips += wager
        elif pv < dv:
            print(f"Dealer wins! You lose {wager} chips.")
            self.chips -= wager
        else:
            print("Push! Game tied. Your bet is returned.")

        return True

    def run(self):
        """Main game control loop."""
        print("==========================================")
        print("    Welcome to Scenario 18 - Blackjack    ")
        print("==========================================")
        while self.chips > 0:
            if not self.round():
                break
            if self.chips <= 0:
                print("\nYou ran out of chips! Game over.")
                break
            again = input("\nPlay another round? [y/n]: ").strip().lower()
            if again != "y":
                break
        print(f"\nFinal Bankroll: {self.chips} chips. Thanks for playing!")