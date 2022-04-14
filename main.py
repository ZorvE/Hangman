import tkinter as tk
import Image
import ImageTk
import random

secret_words = ["blueberry", "strawberry", "cherry"]
secret_choice = random.randint(0, 2)
secret_word = secret_words[secret_choice]
game_is_on = True
clue_level = 0
hidden_word = []
guesses = 0
allowed_guesses = len(secret_word) - 2
allowed_clues = 3

root = tk.Tk()
root.geometry("1200x500")
root.title("Hangman")


def send_guess():
    global game_is_on, hanging_image, guesses

    entry_content = letter_guess.get()
    if guesses == allowed_guesses:
        game_is_on = False
        logg_guesses.configure(state="normal")
        logg_guesses.insert("end", "You guessed to many times! You lost.")
        logg_guesses.configure(state="disabled")
        letter_guess.delete(0, "end")

    if game_is_on:

        update_hidden_word(entry_content)

        if entry_content.isalpha():
            if entry_content == secret_word or list_to_string(hidden_word) == secret_word:

                game_is_on = False
                logg_guesses.configure(state="normal")
                logg_guesses.insert("end", "You guessed right! The secret word is " + secret_word + "!")
                logg_guesses.configure(state="disabled")
                letter_guess.delete(0, "end")
                hanging_image = ImageTk.PhotoImage(Image.open("free man.jpg"))
                hanging_progress.configure(image=hanging_image)

            elif len(entry_content) == 1:
                guesses += 1
                guess_amount.set(str(guesses) + "/" + str(allowed_guesses))
                logg_guesses.configure(state="normal")
                logg_guesses.insert("end", entry_content + "\n")
                logg_guesses.configure(state="disabled")
                letter_guess.delete(0, "end")

            elif len(entry_content) > 1:
                logg_guesses.configure(state="normal")
                logg_guesses.insert("end", "You submitted to many symbols. Please enter just one letter." + "\n")
                logg_guesses.configure(state="disabled")
                letter_guess.delete(0, "end")

            elif len(entry_content) < 1:
                logg_guesses.configure(state="normal")
                logg_guesses.insert("end", "You did not enter a letter. Please enter one." + "\n")
                logg_guesses.configure(state="disabled")

        else:
            logg_guesses.configure(state="normal")
            logg_guesses.insert("end", "You did not enter a letter. Please enter a single letter." + "\n")
            logg_guesses.configure(state="disabled")
            letter_guess.delete(0, "end")


def reveal_clue():
    global clue_level, clue_img

    clue_level += 1

    if clue_level <= allowed_clues:
        clue_amount.set(str(clue_level) + "/" + str(allowed_clues))
        clue_img = ImageTk.PhotoImage(Image.open(str(clue_level) + secret_word + ".jpg"))
        clue_label.configure(image=clue_img)


def list_to_string(the_list):
    the_string = ""
    for item in the_list:
        the_string += item

    return the_string


def create_hidden_word():
    global hidden_word

    word_length = len(secret_word)
    count_word_length = 1

    while count_word_length <= word_length:
        hidden_word.append("*")
        count_word_length += 1


def update_hidden_word(guess_entry):
    print("Update hidden word")
    global secret_word, hidden_word
    if guess_entry in secret_word:
        show_place = [secret_word for secret_word, x in enumerate(str(secret_word)) if x == guess_entry]
        amount_same_letters = len(show_place)

        count_letters = 0
        while count_letters < amount_same_letters:

            del hidden_word[show_place[count_letters]]
            hidden_word.insert(show_place[count_letters], guess_entry)
            count_letters += 1

        revealed_letters.set(list_to_string(hidden_word))


create_hidden_word()

print(secret_word)

revealed_letters = tk.StringVar()
revealed_letters.set(list_to_string(hidden_word))
word_progress = tk.Label(textvariable=revealed_letters)
word_progress.grid(column=1, row=0)

hanging_image = ImageTk.PhotoImage(Image.open("hanged man.jpg"))
hanging_progress = tk.Label(image=hanging_image)
hanging_progress.grid(column=0, row=1)

clue_img = ImageTk.PhotoImage(Image.open("no help.jpg"))
clue_label = tk.Label(image=clue_img)
clue_label.grid(column=2, row=1)

clue_give_button = tk.Button(text="Give clue", command=reveal_clue)
clue_give_button.grid(column=2, row=2)

logg_guesses = tk.Text(root, state="disabled", width=30)
logg_guesses.grid(column=1, row=1)

letter_guess = tk.Entry()
letter_guess.grid(column=1, row=2)

send_guess_button = tk.Button(text="Send guess", command=send_guess)
send_guess_button.grid(column=1, row=3)

guess_amount = tk.StringVar()
guess_amount.set(str(guesses) + "/" + str(allowed_guesses))
word_progress = tk.Label(textvariable=guess_amount)
word_progress.grid(column=0, row=0)

clue_amount = tk.StringVar()
clue_amount.set(str(clue_level) + "/" + str(allowed_clues))
clue_progress = tk.Label(textvariable=clue_amount)
clue_progress.grid(column=2, row=0)

root.mainloop()
