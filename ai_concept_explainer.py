# Import necessary libraries
import ollama  # Used to get local AI models
import threading  # Allows background execution without freezing UI
from customtkinter import *  # UI framework
import pygame  # For playing sound effects

# Function to get concept explanation using the AI model
def get_concept_explanation(prompt, display_widget):
    # Enable and update the text widget to show "Thinking..."
    display_widget.configure(state="normal")
    display_widget.delete("1.0", "end")
    display_widget.insert("end", "Thinking 🤔...\n")
    display_widget.configure(state="disabled")

    # Function to run the AI request in a separate thread
    def fetch():
        try:
            # Build the user query with instructions for explanation
            query = (
                f"Explain the following in a simple, clear way, as if to a student: {prompt}.\n"
                f"Include a real-world analogy if appropriate. If it is asking you to solve something, do it step by step. "
                f"If not a word or math problem, then do not include any math or word problems that do not relate to the topic provided. "
                f"Do not include any math or word problems when not asked. This is very important."
            )
            # Send the query to the model
            response = ollama.chat(model="phi", messages=[
                {"role": "user", "content": query}
            ])
            # Extract and clean the response content
            answer = response['message']['content'].strip()
        except Exception:
            # Fallback message in case of error
            answer = "Something went wrong. Please try again or check your connection."

        # Display the AI's answer
        display_widget.configure(state="normal")
        display_widget.delete("1.0", "end")
        display_widget.insert("end", answer)
        display_widget.configure(state="disabled")

    # Run the fetch function in a new thread
    threading.Thread(target=fetch).start()


# Function to launch the concept explainer window
def launch_ai_concept_explainer():
    # Initialize the main window
    window = CTk()
    window.title("AI Concept Explainer")
    window.geometry("800x600")
    window.configure(fg_color="#282c3f")

    # Initialize sound system
    pygame.mixer.init()
    hover_sound = pygame.mixer.Sound("hover.wav")
    click_sound = pygame.mixer.Sound("click.mp3")

    # Function to play hover sound
    def play_hover(event=None):
        hover_sound.play()

    # Function to play click sound, then run a function
    def play_click(func):
        click_sound.play()
        window.after(100, func)

    # Label prompting user input
    label = CTkLabel(window, text="Input any concept or problem below:", font=("Arial Rounded MT Bold", 20))
    label.place(relx=0.5, rely=0.075, anchor="n")

    # Text entry for user to input the concept/question
    input_entry = CTkEntry(window, font=("Arial Rounded MT Bold", 14), width=800)
    input_entry.place(relx=0.5, rely=0.125, anchor="n")

    # Text area to display the explanation
    output_text = CTkTextbox(window, font=("Arial", 18), width=800, height=650, fg_color="#0f1825", corner_radius=50)
    output_text.place(relx=0.5, rely=0.5, anchor="center")
    output_text.configure(state="disabled")

    # Button to trigger the explanation
    explain_button = CTkButton(
        window, width=250, height=50, text="Explain It", corner_radius=50,
        font=("Arial Rounded MT Bold", 17)
    )
    explain_button.place(relx=0.5, rely=0.92, anchor="s")
    explain_button.bind("<Enter>", play_hover)  # Add hover sound
    explain_button.configure(command=lambda: play_click(  # Add click sound and run logic
        lambda: get_concept_explanation(input_entry.get(), output_text)
    ))

    # Start the GUI event loop
    window.mainloop()
