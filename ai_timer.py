import time
import threading
import tkinter as tk
import random
import ollama
from customtkinter import *
import pygame

# Initialize sound effects
pygame.mixer.init()
click_sound = pygame.mixer.Sound("click.mp3")
hover_sound = pygame.mixer.Sound("hover.wav")

# List of fallback motivational quotes (in case AI call fails)
fallback_quotes = [
    "You're making steady progress. Keep pushing.",
    "Every second counts! Stay focused.",
    "You're doing great! Stay on track.",
    "Keep going. You're building momentum.",
    "You're one step closer to your goal.",
    "Stay strong. You’ve got this.",
    "Small steps lead to big wins.",
    "What you're doing now matters.",
    "One second at a time. Keep moving.",
    "Progress is happening right now.",
    "Keep grinding. It’s working.",
    "This moment is a part of the story.",
    "Real work happens when no one's watching.",
    "Keep your head down. Keep building.",
    "Greatness comes from repetition.",
    "You’re in the zone. Stay there.",
    "Trust the process. You’re on track.",
    "Success is forged in silence.",
    "Focus now, shine later.",
    "You are becoming unstoppable."
]

# Creates a styled button with sound on click and hover
def create_button(parent, text, command):
    button = CTkButton(parent, text=text, font=("Arial Rounded MT Bold", 18), command=lambda: [click_sound.play(), command()], width=250, height=50, corner_radius=50)
    button.pack(pady=15)

    def on_enter(event):
        hover_sound.play()

    button.bind("<Enter>", on_enter)
    return button

# Picks a random fallback quote
def get_fallback_quote():
    return random.choice(fallback_quotes)

# Gets a motivational quote from the AI (or fallback if it fails)
def get_motivational_quote(total_seconds, total_minutes):
    prompt = (
        f"There are {total_seconds} seconds left in a {total_minutes}-minute study session. "
        f"Give ONE short, motivating sentence that makes me feel progress is being made. "
        f"No math, no quotes, no extra things. Just one direct, motivating sentence. "
    )

    result = {"quote": None}

    def fetch_quote():
        try:
            response = ollama.chat(model='phi', messages=[
                {'role': 'user', 'content': prompt}
            ])
            result["quote"] = response['message']['content'].strip()
        except Exception:
            result["quote"] = get_fallback_quote()

    # Run quote fetching in a thread with timeout
    quote_thread = threading.Thread(target=fetch_quote)
    quote_thread.start()
    quote_thread.join(timeout=15)

    if result["quote"] is None:
        result["quote"] = get_fallback_quote()

    return result["quote"]

# Main function to launch the AI timer
def launch_ai_timer():
    # First screen: ask for study duration
    def show_timer_input_screen():
        timer_input_frame = CTk()
        timer_input_frame.title("AI Timer")
        timer_input_frame.geometry("600x400")
        timer_input_frame.configure(fg_color="#282c3f")

        label = CTkLabel(timer_input_frame, text="Enter study timer duration (minutes):", font=("Segoe UI", 24))
        label.pack(pady=30)

        timer_input = CTkEntry(timer_input_frame, font=("Arial Rounded MT Bold", 16), width=200)
        timer_input.pack(pady=10)

        error_label = CTkLabel(timer_input_frame, text="", font=("Arial Rounded MT Bold", 16), text_color="red")
        error_label.pack()

        # Handle timer duration input
        def get_duration():
            try:
                mins = int(timer_input.get())
                timer_input_frame.destroy()
                start_ai_timer(mins)
            except ValueError:
                error_label.configure(text="Please enter a valid number.")

        # Start button with sound and input validation
        start_button = CTkButton(timer_input_frame, text="Start Timer",
                                 command=lambda: [click_sound.play(), get_duration()],
                                 corner_radius=50, width=250, height=50, font=("Arial Rounded MT Bold", 18))
        start_button.pack(pady=30)

        def on_enter_start(event):
            hover_sound.play()

        start_button.bind("<Enter>", on_enter_start)
        timer_input_frame.mainloop()

    # Starts the actual timer with countdown and quotes
    def start_ai_timer(duration_minutes):
        app = CTk()
        app.title("AI Timer")
        app.geometry("800x600")
        app.configure(fg_color="#282c3f")

        # Countdown display
        countdown_label = CTkLabel(app, text="Time left: 00:00", font=("Segoe UI", 35))
        countdown_label.pack(pady=25)

        # Motivational quote display
        quote_label = CTkLabel(app, text="", wraplength=700, font=("Arial Rounded MT Bold", 25),
                               anchor="center", justify="center")
        quote_label.pack(pady=30, expand=True)

        # State tracking
        state = {'running': False, 'paused': False, 'time_left': duration_minutes * 60}

        # Recursively schedule next quote between 15–30 seconds
        def schedule_quote():
            if state['running']:
                threading.Thread(target=generate_quote, daemon=True).start()
                delay = random.randint(15000, 30000)
                app.after(delay, schedule_quote)

        # Update timer every second
        def update_timer():
            def tick():
                if state['time_left'] > 0 and state['running']:
                    if not state['paused']:
                        minutes, seconds = divmod(state['time_left'], 60)
                        time_str = f"{minutes:02}:{seconds:02}"
                        countdown_label.configure(text=f"Time left: {time_str}")
                        state['time_left'] -= 1
                    app.after(1000, tick)
                elif state['running']:
                    countdown_label.configure(text="✅ Time’s up!")
                    state['running'] = False
            tick()

        # Generate and display a new quote
        def generate_quote():
            quote = get_motivational_quote(state['time_left'], duration_minutes)
            quote_label.configure(text=quote)

        # Start timer logic
        def start_timer():
            state['running'] = True
            threading.Thread(target=update_timer, daemon=True).start()
            threading.Thread(target=generate_quote, daemon=True).start()
            schedule_quote()

        # Pause and resume toggle
        def toggle_pause():
            state['paused'] = not state['paused']
            pause_button.configure(text="Resume Timer" if state['paused'] else "Pause Timer")

        # Reset the timer to original duration
        def reset_timer():
            state['running'] = False
            app.destroy()
            start_ai_timer(duration_minutes)

        # Start the timer and build UI
        start_timer()
        pause_button = create_button(app, "Pause Timer", toggle_pause)
        create_button(app, "Reset Timer", reset_timer)

        app.mainloop()

    # Launch the input screen
    show_timer_input_screen()
