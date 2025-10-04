import random
import os

class NumberGuessingGame:
    """
    A challenging number guessing game with limited guesses and improved feedback.
    Tracks high score across multiple games.
    """
    def __init__(self, lower_bound=1, upper_bound=15, max_guesses=5, high_score_file="high_score.txt"):
        """
        Initializes the game with a random secret number within the specified range,
        sets the maximum number of allowed guesses, and loads the high score.
        """
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.max_guesses = max_guesses
        self.secret_number = random.randint(lower_bound, upper_bound)
        self.guesses_taken = 0
        self.last_guess = None
        self.high_score_file = high_score_file
        self.high_score = self.load_high_score()

    def load_high_score(self):
        """Loads the high score from a file."""
        if os.path.exists(self.high_score_file):
            with open(self.high_score_file, "r") as f:
                try:
                    return int(f.read())
                except ValueError:
                    return float('inf') # Return infinity if file content is not a valid integer
        return float('inf') # Return infinity if file doesn't exist

    def save_high_score(self):
        """Saves the current high score to a file."""
        with open(self.high_score_file, "w") as f:
            f.write(str(self.high_score))

    def update_high_score(self):
        """Updates the high score if the current game's guesses are lower."""
        if self.guesses_taken < self.high_score:
            self.high_score = self.guesses_taken
            self.save_high_score()
            print("Congratulations! You set a new high score!")

    def get_hint(self, user_guess):
        """Provides a hint based on the user's guess and the last guess."""
        if user_guess < self.secret_number:
            if self.last_guess is not None and user_guess > self.last_guess:
                return "Your guess is too low, but you're getting warmer!"
            else:
                return "Your guess is too low. Try a higher number."
        elif user_guess > self.secret_number:
            if self.last_guess is not None and user_guess < self.last_guess:
                return "Your guess is too high, but you're getting warmer!"
            else:
                return "Your guess is too high. Try a lower number."
        else:
            return "That's the number!"


    def play(self):
        """Runs the main game loop."""
        print(f"Welcome to the Number Guessing Game!")
        print(f"I'm thinking of a number between {self.lower_bound} and {self.upper_bound}.")
        print(f"You have {self.max_guesses} guesses.")
        if self.high_score != float('inf'):
            print(f"Current high score: {self.high_score} guesses.")
        else:
            print("No high score yet. Be the first to set one!")


        while self.guesses_taken < self.max_guesses:
            try:
                user_input = input(f"Guess #{self.guesses_taken + 1}: ")
                user_guess = int(user_input)

                if not (self.lower_bound <= user_guess <= self.upper_bound):
                    print(f"Please guess a number within the range {self.lower_bound} to {self.upper_bound}.")
                    continue

                self.guesses_taken += 1
                hint = self.get_hint(user_guess)
                print(hint)

                if user_guess == self.secret_number:
                    print(f"Congratulations! You guessed the number in {self.guesses_taken} guesses.")
                    self.update_high_score()
                    return

                self.last_guess = user_guess

            except ValueError:
                print("Invalid input. Please enter an integer.")

        print(f"Game over! You ran out of guesses.")
        print(f"The secret number was {self.secret_number}.")


# Run the game with more challenging parameters
game = NumberGuessingGame(lower_bound=1, upper_bound=100, max_guesses=7)
game.play()