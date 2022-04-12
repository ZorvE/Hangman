import tkinter as tk
import Image,ImageTk,random

secret_words = ["blueberry", "strawberry", "cherry"]
secret_choice = random.randint(0,2)
secret_word = secret_words[secret_choice]
game_is_on = True
times_pushed = 0
hidden_word = []

root = tk.Tk()
root.geometry("1200x500")
root.title("Hangman")

def send_guess():
    global game_is_on, hanging_image

    entry_content = letter_guess.get()

    if game_is_on == True:
        update_hidden_word(entry_content)

        if entry_content.isalpha():
            if entry_content == secret_word:
                game_is_on = False
                logg_guesses.configure(state="normal")
                logg_guesses.insert("end", "You guessed right! The secret word is " + secret_word + "!")
                logg_guesses.configure(state="disabled")
                letter_guess.delete(0, "end")
                hanging_image = ImageTk.PhotoImage(Image.open("free man.jpg"))
                hanging_progress.configure(image=hanging_image)

            elif len(entry_content) == 1:
                logg_guesses.configure(state="normal")
                logg_guesses.insert("end", "You entered a letter. " + entry_content + "\n")
                logg_guesses.configure(state="disabled")
                letter_guess.delete(0, "end")

            elif len(entry_content) > 1:
                logg_guesses.configure(state="normal")
                logg_guesses.insert("end", "You submitted to many symbols. Please enter just one letter." + "\n")
                logg_guesses.configure(state="disabled")
                letter_guess.delete(0, "end")

            elif len(entry_content) == 1:
                logg_guesses.configure(state="normal")
                logg_guesses.insert("end", "You did not enter a letter. Please enter one." + "\n")
                logg_guesses.configure(state="disabled")

        else:
            logg_guesses.configure(state="normal")
            logg_guesses.insert("end", "You did not enter a letter. Please enter a single letter." + "\n")
            logg_guesses.configure(state="disabled")
            letter_guess.delete(0, "end")

def reveal_clue():
    global times_pushed, clue_img

    times_pushed += 1
    print("Revealing clue! times help pushed: " + str(times_pushed))

    if times_pushed <= len(secret_words):
        clue_img = ImageTk.PhotoImage(Image.open(str(times_pushed) + secret_word + ".jpg"))
        clue_label.configure(image=clue_img)

def list_to_string(the_list):
    the_string = ""
    for item in the_list:
        the_string += item

    return the_string

def create_hidden_word():

    word_length = len(secret_word)
    count_word_length = 1

    while count_word_length <= word_length:
        hidden_word.append("*")
        count_word_length += 1

def update_hidden_word(letter_guess):
    print("Update hidden word")
    if letter_guess in secret_word:
        #creates an array of places where there are same letters
        show_place = [secret_word for secret_word, x in enumerate(secret_word) if x == letter_guess]
        amount_same_letters = len(show_place)

        count_letters = 0
        while count_letters < amount_same_letters:

            del hidden_word[show_place[count_letters]]
            hidden_word.insert(show_place[count_letters], letter_guess)
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
clue_label.grid(column=2,row=1)

clue_give_button = tk.Button(text="Give clue", command=reveal_clue)
clue_give_button.grid(column=2,row=2)

logg_guesses = tk.Text(root, state="disabled", width=30)
logg_guesses.grid(column=1,row=1)

letter_guess = tk.Entry()
letter_guess.grid(column=1,row=2)

send_guess_button = tk.Button(text="Send guess", command=send_guess)
send_guess_button.grid(column=1, row=3)

root.mainloop()