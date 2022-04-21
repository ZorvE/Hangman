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
wrong_guesses = 0
allowed_guesses = len(secret_word) - 2
allowed_clues = 3
right_answer_point = 7


root = tk.Tk()
root.geometry("1400x500")
root.title("Hangman")


def send_guess():
    global game_is_on, hanging_image, guesses, word_progress, wrong_guesses

    entry_content = letter_guess.get()
    if wrong_guesses == allowed_guesses:
        game_is_on = False
        logg_wrong_guesses.configure(state="normal")
        logg_wrong_guesses.insert("end", "You guessed to many times! You lost." + "\n")
        logg_wrong_guesses.configure(state="disabled")
        letter_guess.delete(0, "end")

    if game_is_on:
        progress_test_before = word_progress
        update_hidden_word(entry_content)
        progress_test_after = list_to_string(hidden_word)

        if progress_test_before == progress_test_after:
            guess_is_wrong()

        word_progress = list_to_string(hidden_word)
        if entry_content.isalpha():
            if entry_content == secret_word or list_to_string(hidden_word) == secret_word:

                game_is_on = False
                logg_wrong_guesses.configure(state="normal")
                logg_wrong_guesses.insert("end", "You guessed right! The secret word is " + secret_word + "!")
                logg_wrong_guesses.configure(state="disabled")
                letter_guess.delete(0, "end")
                hanging_image = ImageTk.PhotoImage(Image.open("free man.jpg"))
                hanging_progress.configure(image=hanging_image)

            elif len(entry_content) == 1:
                guesses += 1

                logg_wrong_guesses.configure(state="normal")
                logg_wrong_guesses.insert("end", entry_content + "\n")
                logg_wrong_guesses.configure(state="disabled")
                letter_guess.delete(0, "end")

            elif len(entry_content) > 1:
                logg_wrong_guesses.configure(state="normal")
                logg_wrong_guesses.insert("end", "You submitted to many symbols. Please enter just one letter." + "\n")
                logg_wrong_guesses.configure(state="disabled")
                letter_guess.delete(0, "end")

            elif len(entry_content) < 1:
                logg_wrong_guesses.configure(state="normal")
                logg_wrong_guesses.insert("end", "You did not enter a letter. Please enter one." + "\n")
                logg_wrong_guesses.configure(state="disabled")

        else:
            logg_wrong_guesses.configure(state="normal")
            logg_wrong_guesses.insert("end", "You did not enter a letter. Please enter a single letter." + "\n")
            logg_wrong_guesses.configure(state="disabled")
            letter_guess.delete(0, "end")


def reveal_clue():
    global clue_level, clue_img, right_answer_point
    clue_level += 1

    if clue_level <= allowed_clues:
        clue_amount.set(str(clue_level) + "/" + str(allowed_clues))
        clue_img = ImageTk.PhotoImage(Image.open(str(clue_level) + secret_word + ".jpg"))
        clue_label.configure(image=clue_img)
        right_answer_point -= 2
        point_amount.set("Points for the right answer: " + str(right_answer_point))


def guess_is_wrong():
    global wrong_guesses, hanging_image, hanging_progress, allowed_guesses
    wrong_guesses += 1
    guess_amount.set(str(wrong_guesses) + "/" + str(allowed_guesses))

    ####
    # Räkna upp vilka felgissningar som varit?, eventuell hindra att gissa på samma?
    ####

    image_change_factor = wrong_guesses*(16/allowed_guesses)

    hanging_image = ImageTk.PhotoImage(Image.open("hanged man " + str(round(image_change_factor)) + ".jpg"))
    hanging_progress.configure(image=hanging_image)


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

word_progress = list_to_string(hidden_word)

revealed_letters = tk.StringVar()
revealed_letters.set(list_to_string(hidden_word))
word_progress_label = tk.Label(textvariable=revealed_letters)
word_progress_label.grid(column=1, row=0)

hanging_image = ImageTk.PhotoImage(Image.open("hanged man 0.jpg"))
hanging_progress = tk.Label(image=hanging_image)
hanging_progress.grid(column=0, row=1)

clue_img = ImageTk.PhotoImage(Image.open("no help.jpg"))
clue_label = tk.Label(image=clue_img)
clue_label.grid(column=2, row=1)

clue_give_button = tk.Button(text="Give clue", command=reveal_clue)
clue_give_button.grid(column=2, row=2)

logg_wrong_guesses = tk.Text(root, state="disabled", width=50)
logg_wrong_guesses.grid(column=1, row=1)

letter_guess = tk.Entry()
letter_guess.grid(column=1, row=2)

send_guess_button = tk.Button(text="Send guess", command=send_guess)
send_guess_button.grid(column=1, row=3)

guess_amount = tk.StringVar()
guess_amount.set(str(wrong_guesses) + "/" + str(allowed_guesses))
word_progress_label = tk.Label(textvariable=guess_amount)
word_progress_label.grid(column=0, row=0)

clue_amount = tk.StringVar()
clue_amount.set(str(clue_level) + "/" + str(allowed_clues))
clue_progress = tk.Label(textvariable=clue_amount)
clue_progress.grid(column=2, row=0)

point_amount = tk.StringVar()
point_amount.set("Points for the right answer: " + str(right_answer_point))
point_display = tk.Label(textvariable=point_amount)
point_display.grid(column=3, row=1)

root.mainloop()
