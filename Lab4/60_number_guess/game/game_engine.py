import random
import pygame
from game.text_box import TextBox

class GameEngine:
    # Task 4: Maximum number of valid attempts
    MAX_ATTEMPTS = 10

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.secret_number = random.randint(1, 100)
        self.attempts = 0

        # Task 2: Possible range
        self.min_possible = 1
        self.max_possible = 100

        # Task 3: Recent guess history
        self.guess_history = []
        self.max_history = 5

        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)
        self.game_won = False
        self.game_over = False

        self.input_box = TextBox(width // 2 - 110, 150, 120, 48)
        self.submit_btn = pygame.Rect(width // 2 + 25, 150, 100, 48)

        self.font_title = pygame.font.SysFont(None, 42)
        self.font_medium = pygame.font.SysFont(None, 28)
        self.font_btn = pygame.font.SysFont(None, 26)

    def submit_guess(self):
        # Task 4: Stop accepting guesses after game ends
        if self.game_won or self.game_over:
            return

        # BUG SYMPTOM:
        # Submitting an empty input box crashes the game immediately.
        # Task 1: Prevent empty-input crash
        if not self.input_box.text.strip():
            self.feedback_msg = "Please enter a number."
            self.feedback_color = (240, 200, 80)
            return

        guess = int(self.input_box.text)
        
        self.attempts += 1
        self.input_box.clear()

        if guess < self.secret_number:
            # Task 2: Narrow lower boundary
            self.min_possible = max(self.min_possible, guess + 1)

            # Task 3: Add guess to history
            self.guess_history.append((guess, "TOO LOW"))
            self.guess_history = self.guess_history[-self.max_history:]

            self.feedback_msg = f"TOO LOW! (Guess was {guess})"
            self.feedback_color = (80, 160, 240)
        elif guess > self.secret_number:
            # Task 2: Narrow upper boundary
            self.max_possible = min(self.max_possible, guess - 1)

            # Task 3: Add guess to history
            self.guess_history.append((guess, "TOO HIGH"))
            self.guess_history = self.guess_history[-self.max_history:]
            self.feedback_msg = f"TOO HIGH! (Guess was {guess})"
            self.feedback_color = (240, 100, 80)
        else:
            # Task 3: Add correct guess to history
            self.guess_history.append((guess, "CORRECT"))
            self.guess_history = self.guess_history[-self.max_history:]

            self.feedback_msg = f"CORRECT! Found in {self.attempts} attempts."
            self.feedback_color = (80, 220, 90)
            self.game_won = True

        # Task 4: End game after 10 valid attempts
        if self.attempts >= self.MAX_ATTEMPTS and not self.game_won:
            self.game_over = True
            self.feedback_msg = f"GAME OVER! The number was {self.secret_number}."
            self.feedback_color = (240, 100, 80)

    def reset(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)
        self.game_won = False
        self.game_over = False
        self.min_possible = 1
        self.max_possible = 100
        self.guess_history = []
        self.input_box.clear()

    def handle_event(self, event):
        self.input_box.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit_guess()
            elif event.key == pygame.K_r and (self.game_won or self.game_over):
                self.reset()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.submit_btn.collidepoint(event.pos):
                self.submit_guess()

    def update(self):
        pass

    def render(self, screen):
        screen.fill((30, 34, 42))

        title_surf = self.font_title.render("Number Guessing Arena", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 35))

        attempts_surf = self.font_medium.render(
            f"Attempts: {self.attempts} / {self.MAX_ATTEMPTS}",
            True,
            (180, 185, 195)
        )
        screen.blit(attempts_surf, (self.width // 2 - attempts_surf.get_width() // 2, 95))

        range_surf = self.font_medium.render(f"Possible range: {self.min_possible} - {self.max_possible}", True, (180, 185, 195))
        screen.blit(range_surf, (self.width // 2 - range_surf.get_width() // 2, 120))

        # Task 3: Display recent guess history
        history_title = self.font_medium.render("Recent guesses:", True, (180, 185, 195))
        screen.blit(history_title, (60, 240))
        for i, (guess, result) in enumerate(self.guess_history):
            history_text = self.font_medium.render(f"{guess}: {result}", True, (180, 185, 195))
            screen.blit(history_text, (60, 275 + i * 32))

        self.input_box.render(screen)

        pygame.draw.rect(screen, (50, 150, 80), self.submit_btn, border_radius=6)
        pygame.draw.rect(screen, (220, 220, 220), self.submit_btn, width=2, border_radius=6)
        btn_text = self.font_btn.render("SUBMIT", True, (255, 255, 255))
        screen.blit(
            btn_text,
            (self.submit_btn.centerx - btn_text.get_width() // 2, self.submit_btn.centery - btn_text.get_height() // 2),
        )

        feedback_surf = self.font_medium.render(self.feedback_msg, True, self.feedback_color)
        screen.blit(feedback_surf, (self.width // 2 - feedback_surf.get_width() // 2, 235))

        if self.game_won:
            restart_surf = self.font_medium.render("Press [R] to Start a New Game", True, (255, 220, 80))
            screen.blit(restart_surf, (self.width // 2 - restart_surf.get_width() // 2, 295))