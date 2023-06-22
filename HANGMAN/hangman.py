def addPart(wrong):
  global lives
  if wrong:
    lives+=1
  if lives==0:
    printHangman(hangman0)
  elif lives==1:
    printHangman(hangman1)
  elif lives==2:
    printHangman(hangman2)
  elif lives==3:
    printHangman(hangman3)
  elif lives==4:
    printHangman(hangman4)
  elif lives==5:
    printHangman(hangman5)


def guessLetter():
  guess = max(set(letterPool), key=letterPool.count)
  return guess

def narrowChoices():
  #This function narrows down the word choices by length, correct guesses, and incorrect guesses
  global blanks
  global words

  #Eliminate based on length
  for word in list(words.keys()):
    if len(word)!=len(blanks):
      del words[word]

  #Eliminate based on guesses
  for word in list(words.keys()):
    for index,letter in enumerate(word):
      if (blanks[index]!=' ' and blanks[index]!=word[index]) or (blanks[index]==' ' and letter in usedLetters):
        del words[word]
        break

  if len(words)==1:
    blanks = list(words.keys())[0]
  if words == {}:
    print('Something went wrong. Your word might not be in the library')


def narrowLetters():
  #This function gets all the letters that are in the remaining words
  global letterPool
  letterPool = []
  for word in list(words.keys()):
    for letter in word:
      if letter not in usedLetters:
        letterPool.append(letter)

def printBlanks():
  #This function nicely displays the current state of the word
  print()
  for i in blanks:
    if i==' ':
      print('_ ',end='')
    else:
      print(i+' ',end='')
  #print the indices below for ease of use
  print('\n'+' '.join(str(x) for x in list(range(numBlanks)))+'\n')

def printHangman(hangman):
  for row in hangman:
    print(''.join(row))


lives = 0
hangmen = []
hangman0 = \
  [['  ___ '],\
  ['     |'],\
  ['     |'],\
  ['     |'],\
  ['_____|']]
hangman1 = \
  [['  ___ '],\
  ['  O  |'],\
  ['     |'],\
  ['     |'],\
  ['_____|']]
hangman2 = \
  [['  ___ '],\
  ['  O  |'],\
  ['  |  |'],\
  ['     |'],\
  ['_____|']]
hangman3 = \
  [['  ___ '],\
  ['  O  |'],\
  [' /|\ |'],\
  ['     |'],\
  ['_____|']]
hangman4 = \
  [['  ___ '],\
  ['  O  |'],\
  [' /|\ |'],\
  [' /   |'],\
  ['_____|']]
hangman5 = \
  [['  ___ '],\
  ['  O  |'],\
  [' /|\ |'],\
  [' / \ |'],\
  ['_____|']]


words = {}
with open('wordchoices.txt','r') as f:
  for i in range(10000):
    s,word,freq = f.readline().split('\t') #removes '\n' from the end of the word
    freq = float(freq)  #some values have decimals
    words[word] = freq



blanks = []
usedLetters = ['.',',',"'"]
while True: 
  numBlanks = input('Please enter the number of letters in your word: ')
  if numBlanks.isdigit():
    if int(numBlanks)>0:
      break
    else:
      print('The number must make sense!')
  else:
    print('Please enter a number.')
numBlanks = int(numBlanks)
blanks = [' ']*numBlanks
addPart(False)
printBlanks()
narrowChoices()
narrowLetters()

gameOver = False
while ' ' in blanks: #while the word is not totally filled out
  guessed = guessLetter()
  usedLetters.append(guessed)

  #Presents guess and gets a response from the player
  while True:
    response = input('Is the letter '+guessed.upper()+' in your word? ').lower()
    if response in['y','n','yes','no','nah','aye aye captain']:
      break
    else:
      print('Please enter yes(y) or no(n).\n')


  #Handles the response from the player
  if response in['y','yes','aye aye captain']:
    while True: #Ensure a valid index response (can be multiple indices)
      index = input('\nWhich space(s) is it in (starting with 0 and separated with spaces)? ').split()
      if any([not i.isdigit() or int(i)>numBlanks-1 or int(i)<0 or blanks[int(i)]!=' ' for i in index]):
        print('Please indicate a blank space.')
      else:
        index = [int(x) for x in index]
        addPart(False)
        for i in index:
          blanks[i] = guessed
        break
  else:
    print('\noh...\n')
    addPart(True)
    if lives>5:
      gameOver = True
      print('You win!')
      break
  printBlanks()
  narrowChoices()
  narrowLetters()

#When there is only one possible word left,
while True and not gameOver: #Ensure a valid response
  answer = input('Is your word \"'+''.join(blanks)+'\"? ').lower()
  if answer in['y','yes','aye aye captain']:
    #print('\n'+''.join(blanks))
    addPart(False)
    printBlanks()
    print('Thanks for playing!')
    break
  elif answer in['n','no','nah']:
    print('Then your word is probably not in my library, or something else has gone wrong.')
    break
  else:
    print('Please enter yes(y) or no(n).\n')