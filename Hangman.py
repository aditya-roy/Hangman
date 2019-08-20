#!/usr/bin/env python
# coding: utf-8

# In[1]:


from string import ascii_lowercase
import random
import string
import numpy as np


# In[2]:


lines = open("C:\\Users\\admin\\Downloads\\Assignment for DATA SCIENCE Profile\\words.txt").readlines()


# # Task 1

# In[3]:


def get_random_word():
    for i in range(0,len(lines)):
        lines[i]=lines[i].rstrip()
    return random.choice(lines)

def get_display_word(word, idxs):
    """Get the word suitable for display."""
    displayed_word = ''.join([letter if idxs[i] else '_ ' for i, letter in enumerate(word)])
    return displayed_word.strip()

def get_next_letter(remaining_letters):
    """Get the user-inputted next letter."""
    if len(remaining_letters) == 0:
        raise ValueError('There are no remaining letters')
    while True:
        next_letter = random.choice(string.ascii_lowercase)
        if next_letter not in remaining_letters:
            print('{0} has been guessed before'.format(next_letter))
        else:
            remaining_letters.remove(next_letter)
            return next_letter

def play_hangman():
    print('Starting Hangman...')
    attempts_remaining = 6
    # Selecting all the words from the dictionary one by one..
    print('Selecting a word...')
    word = get_random_word()
    print()
    idxs = [letter not in ascii_lowercase for letter in word]
    remaining_letters = set(ascii_lowercase)
    wrong_letters = []
    word_solved = False
    while attempts_remaining > 0 and not word_solved:
        # Print current game state
        print('Guess: {0}'.format(get_display_word(word, idxs)))
        print('Attempts Remaining: {0}'.format(attempts_remaining))
        print('Missed: {0}'.format(' '.join(wrong_letters)))
        # Guessing the next letter
        next_letter = get_next_letter(remaining_letters)
        # Check if letter guess is in word
        if next_letter in word:
            # Guessed correctly
            print('{0} is in the word!'.format(next_letter))
            # Reveal matching letters
            for i in range(len(word)):
                if word[i] == next_letter:
                    idxs[i] = True
        else:
            # Guessed incorrectly
            print('{0} is NOT in the word!'.format(next_letter))
            # Decreasing the number of attempts left and append letter to wrong guesses
            attempts_remaining -= 1
            wrong_letters.append(next_letter)

        # Check if word is completely solved
        if False not in idxs:
            word_solved = True
        print()
        
    print('The word is {0}'.format(word))
    if word_solved:
        print('The program won')
        return True
    else:
        print('The program lost')
        return False
        
if __name__ == '__main__':
    play_hangman()


# # Task 2

# In[4]:


file1 = open("file1.txt","a")
for i in range(0,len(lines)):
    file1.write(lines[i])


# In[5]:


file1 = open("file1.txt","r")
a=file1.read()


# ### using random letter generation

# In[6]:


def get_display_word(word, idxs):
    """Get the word suitable for display."""
    displayed_word = ''.join([letter if idxs[i] else '_ ' for i, letter in enumerate(word)])
    return displayed_word.strip()

def get_next_letter(remaining_letters):
    if len(remaining_letters) == 0:
        raise ValueError('There are no remaining letters')
    while True:
        next_letter = random.choice(string.ascii_lowercase)
        if next_letter not in remaining_letters:
            print('{0} has been guessed before'.format(next_letter))
        else:
            remaining_letters.remove(next_letter)
            return next_letter

def play_hangman(w):
    print('Starting Hangman...')
    attempts_remaining = 6
    # Selecting all the words from the dictionary one by one..
    print('Selecting a word...')
    word = w
    print()
    idxs = [letter not in ascii_lowercase for letter in word]
    remaining_letters = set(ascii_lowercase)
    wrong_letters = []
    word_solved = False
    while attempts_remaining > 0 and not word_solved:
        # Print current game state
        print('Guess: {0}'.format(get_display_word(word, idxs)))
        print('Attempts Remaining: {0}'.format(attempts_remaining))
        print('Missed: {0}'.format(' '.join(wrong_letters)))
        # Guessing the next letter
        next_letter = get_next_letter(remaining_letters)
        # Check if letter guess is in word
        if next_letter in word:
            # Guessed correctly
            print('{0} is in the word!'.format(next_letter))
            # Reveal matching letters
            for i in range(len(word)):
                if word[i] == next_letter:
                    idxs[i] = True
        else:
            # Guessed incorrectly
            print('{0} is NOT in the word!'.format(next_letter))
            # Decreasing the number of attempts left and append letter to wrong guesses
            attempts_remaining -= 1
            wrong_letters.append(next_letter)

        # Check if word is completely solved
        if False not in idxs:
            word_solved = True
        print()
        
    print('The word is {0}'.format(word))
    if word_solved:
        print('The program won')
        return True
    else:
        print('The program lost')
        return False
        
if __name__ == '__main__':
    correct=0
    incorrect=0
    for i in range(0,len(lines)):
        lines[i]=lines[i].rstrip()
        if(play_hangman(lines[i])):
            correct+=1
        else:
            incorrect+=1
    accuracy=(float(correct)/float(correct+incorrect))*100
    print(accuracy)


# In[7]:


print("Accuracy is {0}".format(accuracy))


# ### Using Probability to generate the next letter

# In[8]:


def transitionTable(data, k=1):
    T = {}
    # Work
    for i in range(len(data)-k):
        X = data[i:i+k]
        Y = data[i+k]
        
        if T.get(X) is None:
            T[X] = {}
            T[X][Y] = 1
        elif T[X].get(Y) is None:
            T[X][Y] = 1
        else:
            T[X][Y]+=1            
    return T
test = transitionTable(a)

def probability(T):
    for kx in T.keys(): # This will go to every substring
        norm_factor = sum(T[kx].values()) # Denominator
        for val in T[kx].keys():
            T[kx][val]/=norm_factor
    return T
test_probab = probability(test)


# In[9]:


def get_display_word(word, idxs):
    """Get the word suitable for display."""
    displayed_word = ''.join([letter if idxs[i] else '_ ' for i, letter in enumerate(word)])
    return displayed_word.strip()

def get_next_letter(remaining_letters):
    if len(remaining_letters) == 0:
        raise ValueError('There are no remaining letters')
    prev_letter='a'
    while True:
        next_char = list(test_probab[prev_letter].keys())
        probab = list(test_probab[prev_letter].values())
        next_letter= np.random.choice(next_char, p=probab)
        prev_letter=next_letter
        if next_letter not in remaining_letters:
            print('{0} has been guessed before'.format(next_letter))
        else:
            remaining_letters.remove(next_letter)
            return next_letter

def play_hangman(w):
    print('Starting Hangman...')
    attempts_remaining = 6
    # Selecting all the words from the dictionary one by one..
    print('Selecting a word...')
    word = w
    print()
    idxs = [letter not in ascii_lowercase for letter in word]
    remaining_letters = set(ascii_lowercase)
    wrong_letters = []
    word_solved = False
    while attempts_remaining > 0 and not word_solved:
        # Print current game state
        print('Guess: {0}'.format(get_display_word(word, idxs)))
        print('Attempts Remaining: {0}'.format(attempts_remaining))
        print('Missed: {0}'.format(' '.join(wrong_letters)))
        # Guessing the next letter
        next_letter = get_next_letter(remaining_letters)
        # Check if letter guess is in word
        if next_letter in word:
            # Guessed correctly
            print('{0} is in the word!'.format(next_letter))
            # Reveal matching letters
            for i in range(len(word)):
                if word[i] == next_letter:
                    idxs[i] = True
        else:
            # Guessed incorrectly
            print('{0} is NOT in the word!'.format(next_letter))
            # Decreasing the number of attempts left and append letter to wrong guesses
            attempts_remaining -= 1
            wrong_letters.append(next_letter)

        # Check if word is completely solved
        if False not in idxs:
            word_solved = True
        print()
        
    print('The word is {0}'.format(word))
    if word_solved:
        print('The program won')
        return True
    else:
        print('The program lost')
        return False
        
if __name__ == '__main__':
    correct=0
    incorrect=0
    for i in range(0,len(lines)):
        lines[i]=lines[i].rstrip()
        if(play_hangman(lines[i])):
            correct+=1
        else:
            incorrect+=1
    accuracy=(float(correct)/float(correct+incorrect))*100
    print(accuracy)


# In[10]:


print("Accuracy is {0}".format(accuracy))


# ### After using probability to predict the next letter we can see that accuracy has increased as compared to what it was when we used random model to predict the output
# ### Another thing that can be observed is that if we increase the number of guesses then accuracy will increase.
