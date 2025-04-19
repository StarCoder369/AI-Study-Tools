# Import required modules and custom scripts
from flashcards import run_flashcard_generator
from ai_timer import launch_ai_timer
from ai_concept_explainer import launch_ai_concept_explainer
from customtkinter import *
import pygame


# Main class to create the UI and handle interactions
class ResponsiveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Toolkit")
        self.root.attributes("-fullscreen", True)  # Start in fullscreen mode

        # Initialize pygame for sound effects
        pygame.mixer.init()
        self.hover_sound = pygame.mixer.Sound("hover.wav")
        self.click_sound = pygame.mixer.Sound("click.mp3")

        # Setup UI layout
        self.create_layout()

    # Play hover sound when mouse enters a button
    def play_hover(self, event=None):
        self.hover_sound.play()

    # Play click sound and run function after short delay
    def play_click(self, func):
        self.click_sound.play()
        self.root.after(100, func)  # Slight delay to finish click sound before executing

    # Attach sound effects to a button's events
    def add_sound_events(self, button, func):
        button.bind("<Enter>", self.play_hover)  # Hover sound
        button.configure(command=lambda: self.play_click(func))  # Click sound + action

    # Create the UI layout and buttons
    def create_layout(self):
        # Main frame container
        main_frame = CTkFrame(master=self.root, width=600, height=650, corner_radius=50, fg_color="#0f1825")
        main_frame.pack(expand=True)
        main_frame.pack_propagate(False)

        # Title label
        title_label = CTkLabel(master=self.root, text="AI Study Tools", font=("Arial Rounded MT Bold", 35),
                               text_color="white")
        title_label.place(relx=0.5, rely=0.05, anchor="n")

        # Flashcard button
        flashcard_button = CTkButton(main_frame, height=100, width=500, corner_radius=100, text="Flashcards",
                                     font=("Arial Rounded MT Bold", 35), fg_color="#162539")
        flashcard_button.pack(pady=30)
        self.add_sound_events(flashcard_button, run_flashcard_generator)

        # Concept Explainer button
        concept_button = CTkButton(main_frame, height=100, width=500, corner_radius=100, text="Concept Explainer",
                                   font=("Arial Rounded MT Bold", 35), fg_color="#162539")
        concept_button.pack(pady=30)
        self.add_sound_events(concept_button, launch_ai_concept_explainer)

        # AI Timer button
        timer_button = CTkButton(main_frame, height=100, width=500, corner_radius=100, text="AI Timer",
                                 font=("Arial Rounded MT Bold", 35), fg_color="#162539")
        timer_button.pack(pady=30)
        self.add_sound_events(timer_button, launch_ai_timer)

        # Quit button
        quit_button = CTkButton(main_frame, height=100, width=500, corner_radius=100, text="Quit",
                                font=("Arial Rounded MT Bold", 35), fg_color="#162539")
        quit_button.pack(pady=30)
        self.add_sound_events(quit_button, self.root.quit)


# Entry point of the app
if __name__ == "__main__":
    root = CTk()
    root.configure(fg_color="#282c3f")  # Set background color
    set_default_color_theme("dark-blue")  # Set UI theme

    app = ResponsiveApp(root)  # Initialize the app

    # Load and play background music on loop
    pygame.mixer.init()
    pygame.mixer.music.load("background.wav")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    root.mainloop()  # Start the GUI event loop
