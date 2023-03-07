import pygame
import os
import random

class Card: # images are 45px x 70px

    # Constructor, given face and suit
    def __init__(self, face, suit):

        self.face = face
        self.suit = suit
        # Once I have images, based on the face and suit, set a property called imgLink or something to the path to the images in Assets
        # Giving the correct value based on the face
        match face:
            case "Two":
                self.value = 2
            case "Three":
                self.value = 3
            case "Four":
                self.value = 4
            case "Five":
                self.value = 5
            case "Six":
                self.value = 6
            case "Seven":
                self.value = 7
            case "Eight":
                self.value = 8
            case "Nine":
                self.value = 9
            case "Ten":
                self.value = 10
            case "Jack":
                self.value = 10
            case "Queen":
                self.value = 10
            case "King":
                self.value = 10
            case "Ace":
                self.value = 11
    
    # Method used to print a card
    def print(self):
        print("The " + self.face + " of " + self.suit)

    def draw(self, surface, scale, x, y):
        
        path = self.face + 'of' + self.suit + '.png'
        image = pygame.image.load(os.path.join('images/cards', path))
        width = image.get_width()
        height = image.get_height()
        
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        #FIX
        pygame.draw.rect(surface, (0,0,0), pygame.Rect((x-1), (y-1), (image.get_width() + 2), (image.get_height() + 2)))
        surface.blit(image, (x, y))


class Deck:
    
    # Constructor for a new, unshuffled deck
    def __init__(self):
        
        self.current = 0
        self.cards = []

        # Temp arrays of values needed to create the cards
        suits = ["Diamonds", "Hearts", "Spades", "Clubs"]
        faces = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]

        for i in range(4):
            for j in range(13):
                self.cards.append(Card(faces[j], suits[i]))

    def shuffle(self):

        for i in range(52):
            tempInt = random.randint(0,51)
            tempCard = self.cards[tempInt]
            self.cards[tempInt] = self.cards[i]
            self.cards[i] = tempCard

        self.current = 0


class Hand:
    
    # Constructor for an empty hand
    def __init__(self):

        self.numCards = 0
        self.wager = 0
        self.value = 0
        self.cards = []
        self.wager = 0
        self.doubled = False
        self.split = False

    # Appends a new card from the passed deck to the cards array
    def hit(self, deck):

        self.cards.append(deck.cards[deck.current])
        self.numCards = self.numCards + 1
        deck.current = deck.current + 1

        self.updateValue()

    def updateValue(self):
        
        val = 0
        numAces = 0

        for i in range(self.numCards):
            val = val + self.cards[i].value
            if self.cards[i].face == "Ace":
                numAces = numAces + 1

        if val < 22:
            self.value = val

            # This is to check for blackjack, blackjack will be represented as 22
            if val == 21 and self.numCards == 2 and numAces == 1:
                self.value = 22

        else:
            while val > 21:
                if numAces > 0:
                    numAces = numAces - 1
                    val = val - 10
                else: val = -1
            self.value = val
        

class Player:

    # Constructor for a player with no money, an empty list of hands, name
    def __init__(self, firstname, lastname):
        self.wallet = 0
        self.hands = [6]
        self.hands[0] = Hand()
        self.first = firstname
        self.last = lastname
        self.email = ''

    
  