import re
import ollama
import customtkinter as ctk
from tkinter import filedialog, messagebox
import pygame  # For sound effects

# Init sound system
pygame.mixer.init()

# Load sound files
hover_sound = pygame.mixer.Sound("hover.wav")
click_sound = pygame.mixer.Sound("click.mp3")

# Use Ollama to generate 5 flashcards from input text
def generate_flashcards(text):
    prompt = f"""
Create exactly 5 study flashcards from the article below.

Each flashcard should be formatted as:
1. Question
- Answer

Be concise but informative.

Do not include any sentences that are not included in the format provided. Do not make answers too long, more than 5 sentences is too much.
Only include information from the article. No math problems, no word problems, nothing extra. Only things from the article provided.
After the 5 questions, stop writing. Do not write anything before or after the five questions.
Make sure the questions and answers are complete.
Article:
{text}
"""
    try:
        response = ollama.chat(model='phi', messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        return f"ERROR: {e}"

# Extract Q&A from raw output
def parse_flashcards(raw_text):
    lines = raw_text.strip().splitlines()
    flashcards = []
    current_q = None
    current_a = []

    for line in lines:
        line = line.strip()
        match = re.match(r"^\d+\.\s*(.*)\?", line)
        if match:
            if current_q and current_a:
                flashcards.append({'question': current_q, 'answer': ' '.join(current_a).strip()})
            current_q = match.group(1)
            current_a = []
            continue

        if line.startswith("Answer:"):
            current_a = [line.replace("Answer:", "").strip()]
            continue

        if line.startswith("-"):
            cleaned_line = line.lstrip("-").strip()
            if cleaned_line:
                current_a.append(cleaned_line)

    if current_q and current_a:
        flashcards.append({'question': current_q, 'answer': ' '.join(current_a).strip()})

    return flashcards

# Display flashcards in a flip-style UI
def show_flashcards(flashcard_data):
    flashcard_window = ctk.CTkToplevel()
    flashcard_window.title("Flashcards Viewer")
    flashcard_window.geometry("800x600")
    flashcard_window.configure(fg_color="#282c3f")

    current_index = [0]
    showing_question = [True]
    content_var = ctk.StringVar()
    font_size = 26

    label = ctk.CTkLabel(
        flashcard_window,
        textvariable=content_var,
        font=("Arial Rounded MT Bold", font_size),
        wraplength=1000,
        justify="center"
    )
    label.pack(expand=True, fill="both", padx=40, pady=(60, 20))

    button_frame = ctk.CTkFrame(flashcard_window)
    button_frame.pack(side="bottom", fill="x", pady=20)

    # Update flashcard content
    def update_card():
        card = flashcard_data[current_index[0]]
        text = card['question'] if showing_question[0] else card['answer']
        prefix = "Q: " if showing_question[0] else "A: "
        content_var.set(prefix + text)

    def flip():
        showing_question[0] = not showing_question[0]
        update_card()

    def next_card():
        if current_index[0] < len(flashcard_data) - 1:
            current_index[0] += 1
            showing_question[0] = True
            update_card()

    def prev_card():
        if current_index[0] > 0:
            current_index[0] -= 1
            showing_question[0] = True
            update_card()

    def play_hover_sound(event):
        hover_sound.play()

    def play_click_sound():
        click_sound.play()

    # Buttons: Prev / Flip / Next
    prev_button = ctk.CTkButton(button_frame, text="Previous", command=prev_card, width=150, font=("Arial Rounded MT Bold", 24))
    prev_button.pack(side="left", padx=20)
    prev_button.bind("<Enter>", play_hover_sound)
    prev_button.configure(command=lambda: [prev_card(), play_click_sound()])

    flip_button = ctk.CTkButton(button_frame, text="Flip", command=flip, width=150, font=("Arial Rounded MT Bold", 24))
    flip_button.pack(side="left", padx=20)
    flip_button.bind("<Enter>", play_hover_sound)
    flip_button.configure(command=lambda: [flip(), play_click_sound()])

    next_button = ctk.CTkButton(button_frame, text="Next", command=next_card, width=150, font=("Arial Rounded MT Bold", 24))
    next_button.pack(side="left", padx=20)
    next_button.bind("<Enter>", play_hover_sound)
    next_button.configure(command=lambda: [next_card(), play_click_sound()])

    flashcard_window.bind("<Escape>", lambda e: flashcard_window.attributes("-fullscreen", False))
    update_card()

# Main UI to input or load text and trigger generation
def run_flashcard_generator():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Flashcard Generator")
    root.geometry("800x600")
    root.configure(fg_color="#282c3f")
    ctk.CTkLabel(root, text="Paste Article Text:", font=("Arial Rounded MT Bold", 20)).pack(anchor="w", padx=30, pady=(25, 20))

    text_input = ctk.CTkTextbox(root, height=300, wrap="word", font=("Arial Rounded MT Bold", 14), corner_radius=35)
    text_input.pack(fill="both", expand=True, padx=30)

    # Load text from file
    def browse_file():
        file_path = filedialog.askopenfilename(title="Select an Article File", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                text_input.delete("1.0", "end")
                text_input.insert("end", content)

    # Generate flashcards from input
    def generate():
        content = text_input.get("1.0", "end").strip()
        if not content:
            messagebox.showwarning("Missing Text", "Please paste or load article content first.")
            return
        raw = generate_flashcards(content)
        if raw.startswith("ERROR"):
            messagebox.showerror("AI Error", raw)
            return
        data = parse_flashcards(raw)
        if not data:
            messagebox.showwarning("No Flashcards", "Flashcard generation failed. Please try again.")
            return
        show_flashcards(data)

    def play_hover_sound(event):
        hover_sound.play()

    def play_click_sound():
        click_sound.play()

    # Buttons for browsing and generating
    button_frame = ctk.CTkFrame(root, bg_color="transparent", fg_color="transparent")
    button_frame.pack(fill="x", padx=10, pady=10)

    browse_button = ctk.CTkButton(button_frame, text="Browse File", command=browse_file, corner_radius=50, width=160, height=50)
    browse_button.pack(side="left", padx=17.5)
    browse_button.bind("<Enter>", play_hover_sound)
    browse_button.configure(command=lambda: [browse_file(), play_click_sound()])

    generate_button = ctk.CTkButton(button_frame, text="Generate Flashcards", command=generate, corner_radius=50, width=160, height=50)
    generate_button.pack(side="right", padx=17.5)
    generate_button.bind("<Enter>", play_hover_sound)
    generate_button.configure(command=lambda: [generate(), play_click_sound()])

    root.mainloop()
