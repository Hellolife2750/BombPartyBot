import pyperclip
import time
import keyboard
import pyautogui
import random
import string
from unidecode import unidecode

import pygame

pygame.init()
pygame.mixer.init()

enableSound = pygame.mixer.Sound('SFX/enableSound.ogg')
disableSound = pygame.mixer.Sound('SFX/disableSound.ogg')

language = "en" #fr, en, es
instantType = False #taper instantanément ?

bombX, bombY = 769, 581 #position bombe sur l'écran
inputX, inputY = 425, 982 #position de la barre de saisie sur l'écran

funnyCharacters = ["🙂", "🍆", "🍑", "😁", "🥵"] #caractères spéciaux

badWords = []
usedLetters = []
allLetters = list(string.ascii_uppercase)
seconds_since_epoch = time.time()

def getUnusedLettersIn(theWord):
    unusedLetters = []
    for letter in theWord:
        if letter not in usedLetters and letter in allLetters:
            unusedLetters.append(letter)
    return unusedLetters

def containsAllLetters():
    for letter in allLetters:
        if letter not in usedLetters:
            return False
    return True
            

def addToUsedLetters(lettersList):
    global usedLetters
    for letter in lettersList:
        usedLetters.append(letter)
    if containsAllLetters():
        usedLetters = []
        


def pastFunnyCharacter(special = "A"):
    if special == "A":
        pyperclip.copy(funnyCharacters[random.randint(0, len(funnyCharacters)-1)])
    else:
        pyperclip.copy(special)
    pyautogui.hotkey('ctrl', 'v')

def activate():
    pyautogui.moveTo(bombX, bombY)
    pyautogui.leftClick()
    pyautogui.leftClick()
    pyautogui.hotkey('ctrl', 'c')

    syllable = pyperclip.paste()

    longestWord = " "*30
    longestUnusedLetters :int = 0

    with open("dictionaries/" +  language+"List.txt", "r", encoding="utf-8") as f:
        for line in f:
            testedWord = unidecode(line).upper().strip()
            
            if (syllable in testedWord) and (len(getUnusedLettersIn(testedWord)) >= longestUnusedLetters) and (testedWord not in badWords): #and (len(testedWord) < len(longestWord))
                longestWord = testedWord
                longestUnusedLetters = len(getUnusedLettersIn(testedWord))

    print(longestWord)
    pyautogui.moveTo(inputX, inputY)
    pyautogui.leftClick()
    if (instantType):
        pyperclip.copy(longestWord)
        pyautogui.hotkey('ctrl', 'v')
    else:
        for letter in longestWord:
            pyautogui.typewrite(letter)
            time.sleep(random.uniform(0.001, 0.05))
            print(letter)
    pastFunnyCharacter()  
    
    if pyautogui.pixelMatchesColor(inputX, inputY, (25, 21, 19), tolerance=5):
        keyboard.press_and_release('enter')
    time.sleep(.5)
    if pyautogui.pixelMatchesColor(inputX, inputY, (25, 21, 19), tolerance=5):
        badWords.append(longestWord)
    else:
        addToUsedLetters(getUnusedLettersIn(longestWord))


print("READY!")
enableSound.play()
while 1:
    try:
        if pyautogui.pixelMatchesColor(inputX, inputY, (25, 21, 19), tolerance=5): # Change this depending on where the input text box is on your screen
            time.sleep(random.randint(1,100)/70)
            activate()
    except:
        continue
    if keyboard.is_pressed('shift'):
        break;
    time.sleep(0.15)

disableSound.play()
pygame.time.wait(500)
pygame.quit()
print("Session time:",int(time.time()-seconds_since_epoch),"sec.")
    

