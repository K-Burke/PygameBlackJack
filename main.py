import pygame
import blackjack
import definitions
pygame.font.init()
from tinydb import TinyDB, Query
import hashlib

# ----- GENERAL -----
WIDTH, HEIGHT, CENTER = 1200, 1000, (600, 375) #750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Blackjack')
FPS = 60
db, User = TinyDB('db.json'), Query()

# ----- FONTS -----
NAME_FONT = pygame.font.SysFont('comicsans', 35)
TITLE_FONT = pygame.font.SysFont('comicsans', 100)
WAGER_FONT = pygame.font.SysFont('comicsans', 22)

# ----- COLOURS -----
MAT_COL = (74, 179, 39) # Green color for the background
BORDER_COL = (227, 208, 39)
HEADER_COL = (217, 217, 217)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# ----- Buttons and Input Boxes, defined in definitions.py -----
BUTTONS = definitions.BUTTONS
CHIPS = definitions.CHIPS
SIGNUP_INPUTS = definitions.SIGNUP_INPUT_SET
LOGIN_INPUTS = definitions.LOGIN_INPUT_SET
ADD_FUNDS_INPUTS = definitions.ADD_FUNDS_INPUT_SET
REMEMBER_ME = definitions.stay_logged_in

# ----- BLACKJACK INSTANCES -----
dealer = blackjack.Player('Dealer', 'of Cards')
player1 = blackjack.Player('Guest', 'Player')
player1.wallet = 1000
theDeck = blackjack.Deck()

def save_new_user(first, last, email, pass1, pass2, wallet):

    accepted = True

    if (first == ''):
        print("No first name provided...")
        accepted = False

    if (last == ''):
        print("No last name provided...")
        accepted = False

    # Could also check if its a valid email
    results = db.search(User.email == email)
    if len(results) > 0:
        print("A user already exists with this email...")
        accepted = False

    if (pass1 != pass2):
        print("The two passwords were not the same...")
        accepted = False

    if (password_strong(pass1) == False):
        print("The password is not strong enough...")
        accepted = False

    if (is_integer(wallet) == False):
        print("Wallet amount was not an integer...")
        accepted = False

    if (wallet < 1):
        wallet = 1

    if accepted:
        salt = 'dkei5wkb'
        temp = pass1 + salt
        hashed = hashlib.md5(temp.encode())

        db.insert({'firstname': first, 'lastname': last, 'email': email, 'password': hashed.hexdigest(), 'wallet': wallet})
        return True
    else: return False

def update_wallet(email, newWallet):
    db.update({'wallet': newWallet}, User.email == email)

def verify_password(email, password):

    salt = 'dkei5wkb'
    temp = password + salt
    hashed = hashlib.md5(temp.encode())

    results = db.search(User.email == email)
    # I am going to assume that only one record will be saved for each email

    if len(results) > 0:
        if hashed.hexdigest() == results[0]['password']:
            return True
        else: return False
    else: return False    

def password_strong(password):  # checks if the passed string has an uppercase, lowercase and number
    
    result = True

    upperCase = False
    lowerCase = False
    number = False

    for char in password:
        if (ord(char) < 91) and (ord(char) > 64):   # checks if there is an uppercase
            upperCase = True

        if (ord(char) < 123) and (ord(char) > 96):  # checks if there is a lowercase
            lowerCase = True

        if (ord(char) < 58) and (ord(char) > 47):   # checks if there is a number
            number = True

    if (upperCase == False) or (lowerCase == False) or (number == False): 
        result = False
    return result

def is_integer(number): # checks if the passed string is an integer

    result = True

    for char in number:
        if (ord(char) > 57) or (ord(char) < 48):
            result = False

    return result

def draw_startup(p, pag, li, lo, q, su, logged_in):

    WIN.fill(MAT_COL)

    title_text = TITLE_FONT.render("BLACKJACK!", 1, BORDER_COL)
    background_text = TITLE_FONT.render("BLACKJACK!", 1, BLACK)
    WIN.blit(background_text, ((CENTER[0] - (title_text.get_width() / 2) + 3), 18))
    WIN.blit(title_text, ((CENTER[0] - (title_text.get_width() / 2)), 15))

    pygame.draw.rect(WIN, BLACK, pygame.Rect(224, 174, (WIDTH - 448), (HEIGHT - 348)))
    pygame.draw.rect(WIN, HEADER_COL, pygame.Rect(225, 175, (WIDTH - 450), (HEIGHT - 350) ))

    if logged_in:
        welcome_text = NAME_FONT.render(("Welcome back " + player1.first + "!"), 1, BLACK)
        WIN.blit(welcome_text, ((CENTER[0] - (welcome_text.get_width() / 2)), 215))
        if p.draw(WIN, True):
            pass#pygame.event.post(pygame.event.Event(PLAY_CLICKED))
        if lo.draw(WIN, True):
            pass#pygame.event.post(pygame.event.Event(LOGOUT_CLICKED))
        if q.draw(WIN, True):
            pass#pygame.event.post(pygame.event.Event(QUIT_CLICKED))

    else: 
        if pag.draw(WIN, True):
            pass#pygame.event.post(pygame.event.Event(PLAY_AG_CLICKED))
        if li.draw(WIN, True):
            pass#pygame.event.post(pygame.event.Event(LOGIN_CLICKED))
        if su.draw(WIN, True):
            pass#pygame.event.post(pygame.event.Event(SIGNUP_CLICKED))
        if q.draw(WIN, True):
            pass#pygame.event.post(pygame.event.Event(QUIT_CLICKED))

    pygame.display.update()

def draw_signup(login, signup, add):

    WIN.fill(MAT_COL)
    draw_header(login, signup, add)

    pygame.draw.rect(WIN, BLACK, pygame.Rect(224, 174, (WIDTH - 448), (HEIGHT - 348)))
    pygame.draw.rect(WIN, HEADER_COL, pygame.Rect(225, 175, (WIDTH - 450), (HEIGHT - 350) ))

    title_text = NAME_FONT.render("SIGN UP", False, BLACK)
    first_text = WAGER_FONT.render("First Name:", False, BLACK)
    last_text = WAGER_FONT.render("Last Name:", False, BLACK)
    email_text = WAGER_FONT.render("Email:", False, BLACK)
    password_text = WAGER_FONT.render("Password:", False, BLACK)
    confirm_text = WAGER_FONT.render("Confirm Password:", False, BLACK)
    wallet_text = WAGER_FONT.render("Enter Budget:", False, BLACK)
    WIN.blit(title_text, ((CENTER[0] - (title_text.get_width()/2)), 200))
    WIN.blit(first_text, ((CENTER[0] - 200), 260))
    WIN.blit(last_text, ((CENTER[0] - 200), 335))
    WIN.blit(email_text, ((CENTER[0] - 200), 410))
    WIN.blit(password_text, ((CENTER[0] - 200), 485))
    WIN.blit(confirm_text, ((CENTER[0] -200), 560))
    WIN.blit(wallet_text, ((CENTER[0] - 200), 650))

    for input in SIGNUP_INPUTS:
        input.draw(WIN)
    BUTTONS[10].set_position(475, 710)
    BUTTONS[10].draw(WIN, True)

    pygame.display.update()

def draw_login(login, signup, add):
    
    WIN.fill(MAT_COL)
    draw_header(login, signup, add)

    pygame.draw.rect(WIN, BLACK, pygame.Rect(224, 174, (WIDTH - 448), (HEIGHT - 348)))
    pygame.draw.rect(WIN, HEADER_COL, pygame.Rect(225, 175, (WIDTH - 450), (HEIGHT - 350)))

    title_text = NAME_FONT.render("LOGIN", False, BLACK)
    email_text = WAGER_FONT.render("Email:", False, BLACK)
    password_text = WAGER_FONT.render("Password:", False, BLACK)
    remember_text = WAGER_FONT.render("Stay Logged In:", False, BLACK)
    WIN.blit(title_text, ((CENTER[0] - (title_text.get_width()/2)), 230))
    WIN.blit(email_text, ((CENTER[0] - 200), 320))
    WIN.blit(password_text, ((CENTER[0] - 200), 420))
    WIN.blit(remember_text, ((CENTER[0] - 200), 540))

    LOGIN_INPUTS[0].draw(WIN)
    LOGIN_INPUTS[1].draw(WIN)
    REMEMBER_ME.draw(WIN)
    BUTTONS[10].set_position(475, 630)
    BUTTONS[10].draw(WIN, True)

    pygame.display.update()

def draw_add_funds(login, signup, add):
    
    WIN.fill(MAT_COL)
    draw_header(login, signup, add)

    pygame.draw.rect(WIN, BLACK, pygame.Rect(224, 174, (WIDTH - 448), (HEIGHT - 348)))
    pygame.draw.rect(WIN, HEADER_COL, pygame.Rect(225, 175, (WIDTH - 450), (HEIGHT - 350)))

    title_text = NAME_FONT.render("ADD FUNDS", False, BLACK)
    ccn_text = WAGER_FONT.render("Card Number:", False, BLACK)
    #expire_text = WAGER_FONT.render("Expiry Date:", False, BLACK)
    month_text = WAGER_FONT.render("Month:", False, BLACK)
    year_text = WAGER_FONT.render("Year:", False, BLACK)
    cvv_text = WAGER_FONT.render("CVV:", False, BLACK)
    amount_text = WAGER_FONT.render("Amount:", False, BLACK)

    WIN.blit(title_text, ((CENTER[0] - (title_text.get_width()/2)), 200))
    WIN.blit(ccn_text, ((CENTER[0] - 200), 280))
    WIN.blit(month_text, ((CENTER[0] - 200), 380))
    WIN.blit(year_text, ((CENTER[0] - 80), 380))
    WIN.blit(cvv_text, ((CENTER[0] - 200), 480))
    WIN.blit(amount_text, ((CENTER[0] - 200), 580))

    for input in ADD_FUNDS_INPUTS:
        input.draw(WIN)

    BUTTONS[10].set_position(475, 690)
    BUTTONS[10].draw(WIN, True)

    pygame.display.update()

def draw_borders():

    # FUTURE FIX: there is a better way to do this, i dont need this many layers (i think). 
    # You can just add a param to the pygame.draw.rect(surface, color, thing, x) where x is the border width.
    # This makes the rect not filled in, and creates just a border of width x pixels
    layer1 = pygame.Rect(74, 449, 1037, 237)
    layer2 = pygame.Rect(75, 450, 1035, 235)
    layer3 = pygame.Rect(89, 464, 1007, 207)
    layer4 = pygame.Rect(90, 465, 1005, 205)
    
    pygame.draw.rect(WIN, BLACK, layer1)
    pygame.draw.rect(WIN, BORDER_COL, layer2)
    pygame.draw.rect(WIN, BLACK, layer3)
    pygame.draw.rect(WIN, MAT_COL, layer4)

    layer1 = pygame.Rect(74, 114, 1037, 237)
    layer2 = pygame.Rect(75, 115, 1035, 235)
    layer3 = pygame.Rect(89, 129, 1007, 207)
    layer4 = pygame.Rect(90, 130, 1005, 205)

    pygame.draw.rect(WIN, BLACK, layer1)
    pygame.draw.rect(WIN, BORDER_COL, layer2)
    pygame.draw.rect(WIN, BLACK, layer3)
    pygame.draw.rect(WIN, MAT_COL, layer4)
    
def draw_header(login, signup, add):

    pygame.draw.rect(WIN, BLACK, pygame.Rect(0, 0, WIDTH, 55))
    pygame.draw.rect(WIN, BORDER_COL, pygame.Rect(1, 0, WIDTH - 2, 54))
    pygame.draw.rect(WIN, BLACK, pygame.Rect(4, 0, WIDTH - 8, 51))
    pygame.draw.rect(WIN, HEADER_COL, pygame.Rect(5, 0, WIDTH - 10, 50))

    title_text = NAME_FONT.render("BLACKJACK!", 1, BORDER_COL)
    background_text = NAME_FONT.render("BLACKJACK!", 1, BLACK)
    WIN.blit(background_text, ((CENTER[0] - (title_text.get_width() / 2) + 2), 3))
    WIN.blit(title_text, ((CENTER[0] - (title_text.get_width() / 2)), 1))

    if (login == False) and (signup == False):
        name_text = NAME_FONT.render((player1.first + " " + player1.last), 1, BLACK)
        WIN.blit(name_text, (70,0))
        wallet_text = NAME_FONT.render(("Wallet: " + str(player1.wallet)), 1, BLACK)
        WIN.blit(wallet_text, ((WIDTH - wallet_text.get_width() - 35),0))

        if (add == False):
            BUTTONS[13].set_position((WIDTH - wallet_text.get_width() - 85), 5 )
            BUTTONS[13].draw(WIN)

    BUTTONS[12].draw(WIN)

def draw_betting(half, one, two, five, ten, twenty, fifty, hundred, pb_but, cl_but, login, signup, add):
    
    WIN.fill(MAT_COL)
    draw_borders()
    draw_header(login, signup, add)

    pygame.draw.rect(WIN, BLACK, pygame.Rect(73, 714, 1037, 167))
    pygame.draw.rect(WIN, HEADER_COL, pygame.Rect(74, 715, 1035, 165))

    wager_text = WAGER_FONT.render(("Wager: " + str(player1.hands[0].wager)), 1, BLACK)
    WIN.blit(wager_text, (965, 725))

    if pb_but.draw(WIN, True):
        pass#pygame.event.post(pygame.event.Event(PLACE_BET_CLICKED))
    cl_but.draw(WIN, True)

    if half.draw(WIN):
        pass#pygame.event.post(pygame.event.Event(HALF_CLICKED))
    if one.draw(WIN):
        pass#pygame.event.post(pygame.event.Event(ONE_CLICKED))
    if two.draw(WIN):
        pass#pygame.event.post(pygame.event.Event(TWO_CLICKED))
    if five.draw(WIN):
        pass#pygame.event.post(pygame.event.Event(FIVE_CLICKED))
    if ten.draw(WIN):
        pass#pygame.event.post(pygame.event.Event(TEN_CLICKED))
    if twenty.draw(WIN):
        pass#pygame.event.post(pygame.event.Event(TWENTY_CLICKED))
    if fifty.draw(WIN):
        pass#pygame.event.post(pygame.event.Event(FIFTY_CLICKED))
    if hundred.draw(WIN):
        pass#pygame.event.post(pygame.event.Event(HUNDRED_CLICKED))

    pygame.display.update()

def draw_cards(player, dealer, playDone):

    for i in range(player.numCards):
        x_off = 105 + (130 * i)
        player.cards[i].draw(WIN, 2.5, x_off, 480)

    if playDone == False:
        dealer.cards[0].draw(WIN, 2.5, 105, 145)
        temp = blackjack.Card("back", "card")
        temp.draw(WIN, 2.5, 235, 145)
    else: 
        for i in range(dealer.numCards):
            x_off = 105 + (130 * i)
            dealer.cards[i].draw(WIN, 2.5, x_off, 145)

def deal_hand():
    
    theDeck.shuffle()
    player1.hands[0] = blackjack.Hand()
    dealer.hands[0] = blackjack.Hand()
    player1.hands[0].hit(theDeck)
    dealer.hands[0].hit(theDeck)
    player1.hands[0].hit(theDeck)
    dealer.hands[0].hit(theDeck)
    
def draw_game(playDone, hit, stay, login, signup, add, doubled):
    
    WIN.fill(MAT_COL)
    draw_borders()
    draw_header(login, signup, add)
    draw_cards(player1.hands[0], dealer.hands[0], playDone)
    
    if (playDone == False) and (hit != None) and (stay != None):
        hit.draw(WIN, True)
            
        stay.draw(WIN, True)
            
        # if player1.hands[0].numCards == 2, and those cards have the same face, you can split.

        # If the players cards have just been dealt, they can double
        if (doubled == False) and (player1.hands[0].numCards == 2) and (player1.hands[0].value < 21):
            BUTTONS[14].draw(WIN, True)

    if player1.hands[0].value == -1:
        player_value = WAGER_FONT.render("BUST!", 1, RED)
    elif player1.hands[0].value == 22:
        player_value = WAGER_FONT.render("BLACKJACK!", 1, GREEN)
    elif player1.hands[0].value == 21:
        player_value = WAGER_FONT.render("21", 1, GREEN)
    else:
        player_value = WAGER_FONT.render(str(player1.hands[0].value), 1, BLACK)

    if playDone == False:
        dealer_value = WAGER_FONT.render("?", 1, BLACK)
    elif dealer.hands[0].value == -1:
        dealer_value = WAGER_FONT.render("BUST!", 1, RED)
    elif dealer.hands[0].value == 22:
        dealer_value = WAGER_FONT.render("BLACKJACK!", 1, GREEN)
    elif dealer.hands[0].value == 21:
        dealer_value = WAGER_FONT.render("21", 1, GREEN)
    else:
        dealer_value = WAGER_FONT.render(str(dealer.hands[0].value), 1, BLACK)

    WIN.blit(player_value, (1110 - player_value.get_width(), 385))
    WIN.blit(dealer_value, (1110 - dealer_value.get_width(), 65))

    pygame.display.update()

def evaluate_round(logged_in):
    
    if player1.hands[0].value == 22 and dealer.hands[0].value != 22:
        player1.wallet = player1.wallet + (2.5 * player1.hands[0].wager)
        print("Player wins with blackjack!")

    elif player1.hands[0].value == -1 or dealer.hands[0].value > player1.hands[0].value:
        player1.hands[0] = blackjack.Hand()
        print("Player loses...")
    
    else:
        if dealer.hands[0].value == -1 or dealer.hands[0].value < player1.hands[0].value:
            player1.wallet = player1.wallet + (2 * player1.hands[0].wager)
            player1.hands[0] = blackjack.Hand()
            print("Player wins...")
        elif dealer.hands[0].value == player1.hands[0].value:
            player1.wallet = player1.wallet + player1.hands[0].wager
            player1.hands[0] = blackjack.Hand()
            print("It was a draw...")
    
    if logged_in:
        update_wallet(player1.email, player1.wallet)

    deal_hand()

def main():
    clock = pygame.time.Clock()

    #Initializing required states
    startup = True
    signup = False
    login = False
    add = False
    logged_in = False
    bet_placed = False
    doubled = False
    playerDone = False
    
    # This is where we check if someone clicked stay signed in...
    res = db.search(User.firstname == "Saved")
    if len(res) > 0:
        if res[0]['email'] != "":
            res = db.search(User.email == res[0]['email'])
            player1.first = res[0]['firstname']
            player1.last = res[0]['lastname']
            player1.email = res[0]['email']
            player1.wallet = res[0]['wallet']

            logged_in = True
            startup = True

    run = True
    while run:

        clock.tick(FPS)
        
        # This is where the events will be handled
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:

                # Handles the user clicking each of the buttons (not actually using events, but they still work that way)
                # CLICKED THE PLAY BUTTON:
                if BUTTONS[0].background.collidepoint(event.pos) and startup and logged_in:
                    print("Playing...")
                    startup = False
                    deal_hand()
                # CLICKED THE PLAY AS GUEST BUTTON:
                elif BUTTONS[1].background.collidepoint(event.pos) and startup and (logged_in == False):
                    print("Playing as guest...")
                    startup = False
                    deal_hand()
                # CLICKED THE LOGIN BUTTON:
                elif BUTTONS[2].background.collidepoint(event.pos) and startup and (logged_in == False):
                    startup = False
                    login = True
                # CLICKED THE LOGOUT BUTTON:
                elif BUTTONS[3].background.collidepoint(event.pos) and startup and logged_in:

                    db.remove(User.firstname == 'Saved')

                    player1.first = "Guest"
                    player1.last = "Player"
                    player1.email = ''
                    player1.wallet = 1000
                    startup = True
                    logged_in = False
                    print("Logging out...")
                # CLICKED THE QUIT BUTTON:
                elif BUTTONS[4].background.collidepoint(event.pos) and startup:
                    pygame.event.post(pygame.QUIT)
                # CLICKED THE HIT BUTTON:
                elif BUTTONS[5].background.collidepoint(event.pos) and (startup == False) and bet_placed:
                    player1.hands[0].hit(theDeck)
                    print("Player hits...")

                    if player1.hands[0].value == -1:
                        print("Player busts...")
                        draw_game(playerDone, None, None, login, signup, add, doubled)
                        pygame.time.delay(3000)
                        evaluate_round(logged_in)
                        bet_placed = False
                        playerDone = False
                    
                    if player1.hands[0].value == 21 or player1.hands[0].value == 22:
                        playerDone = True
                        draw_game(playerDone, None, None, login, signup, add, doubled)
                        pygame.time.delay(1500)
                        print("Player stays...")

                        while dealer.hands[0].value < 17 and dealer.hands[0].value != -1:
                            dealer.hands[0].hit(theDeck)
                            draw_game(playerDone, None, None, login, signup, add, doubled)
                            pygame.time.delay(1500)
                    
                        pygame.time.delay(2000)
                        evaluate_round(logged_in)
                        bet_placed = False
                        playerDone = False
                # CLICKED THE STAY BUTTON:
                elif BUTTONS[6].background.collidepoint(event.pos) and (startup == False) and bet_placed:
                    playerDone = True
                    draw_game(playerDone, None, None, login, signup, add, doubled)
                    pygame.time.delay(1500)
                    print("Player stays...")

                    while dealer.hands[0].value < 17 and dealer.hands[0].value != -1:
                        dealer.hands[0].hit(theDeck)
                        draw_game(playerDone, None, None, login, signup, add, doubled)
                        pygame.time.delay(1500)
                    
                    pygame.time.delay(2000)
                    evaluate_round(logged_in)
                    bet_placed = False
                    playerDone = False
                # CLICKED THE SPLIT BUTTON:
                elif BUTTONS[7].background.collidepoint(event.pos) and (startup == False) and bet_placed:
                    pass
                # CLICKED THE PLACE BET BUTTON:
                elif BUTTONS[8].background.collidepoint(event.pos) and (startup == False) and (bet_placed == False):
                    if player1.hands[0].wager > 0:
                        player1.wallet -= player1.hands[0].wager
                        if logged_in:
                            update_wallet(player1.email, player1.wallet)
                        bet_placed = True

                        if player1.hands[0].value == 22:
                            playerDone = True
                            draw_game(playerDone, None, None, login, signup, add, doubled)
                            pygame.time.delay(1500)
                            print("Player stays...")

                            while dealer.hands[0].value < 17 and dealer.hands[0].value != -1:
                                dealer.hands[0].hit(theDeck)
                                draw_game(playerDone, None, None, login, signup, add, doubled)
                                pygame.time.delay(1500)
                    
                            pygame.time.delay(2000)
                            evaluate_round(logged_in)
                            bet_placed = False
                            playerDone = False
                # CLICKED THE SIGN UP BUTTON:
                elif BUTTONS[9].background.collidepoint(event.pos) and startup and (logged_in == False):
                    startup = False
                    signup = True
                # CLICKED THE SUBMIT BUTTON (on the LOGIN PAGE):
                elif BUTTONS[10].background.collidepoint(event.pos) and (startup == False) and (logged_in == False) and (signup == False) and login:

                    if verify_password(LOGIN_INPUTS[0].content, LOGIN_INPUTS[1].content):
                        
                        results = db.search(User.email == LOGIN_INPUTS[0].content)
                        
                        player1.first = results[0]['firstname']
                        player1.last = results[0]['lastname']
                        player1.email = results[0]['email']
                        player1.wallet = results[0]['wallet']

                        if REMEMBER_ME.checked:
                            REMEMBER_ME.toggle()
                            db.insert({'firstname': 'Saved', 'email': results[0]['email']})

                        login = False
                        logged_in = True
                        startup = True

                    LOGIN_INPUTS[0].content = ''
                    LOGIN_INPUTS[1].content = ''
                # CLICKED THE SUBMIT BUTTON (on the SIGNUP PAGE):
                elif BUTTONS[10].background.collidepoint(event.pos) and (startup == False) and (logged_in == False) and (login == False) and signup:
                    try:
                        wal = int(SIGNUP_INPUTS[5].content)
                    except ValueError:
                        wal = 100 # 100 will be default if they don't correctly input an int

                    if save_new_user(SIGNUP_INPUTS[0].content, SIGNUP_INPUTS[1].content, SIGNUP_INPUTS[2].content, SIGNUP_INPUTS[3].content, SIGNUP_INPUTS[4].content, wal):
                        player1.first = SIGNUP_INPUTS[0]
                        player1.last = SIGNUP_INPUTS[1]
                        player1.email = SIGNUP_INPUTS[2]
                        player1.wallet = wal

                        signup = False
                        logged_in = True
                        
                    for inputs in SIGNUP_INPUTS:
                        inputs.content = ''
                # CLICKED THE SUBMIT BUTTON (on the ADD FUNDS PAGE):
                elif BUTTONS[10].background.collidepoint(event.pos) and (startup == False) and (login == False) and add:
                    # Doesn't actaully need to have anything in the credit card info part
                    try: 
                        wal = int(ADD_FUNDS_INPUTS[4].content)
                    except ValueError:
                        wal = 1 # 1 will be default if they don't correctly input an int

                    player1.wallet += wal
                    for input in ADD_FUNDS_INPUTS:
                        input.content = ''
                    if logged_in:
                        update_wallet(player1.email, player1.wallet)
                    add = False
                # CLICKED THE CLEAR BUTTON:
                elif BUTTONS[11].background.collidepoint(event.pos) and (startup == False) and (bet_placed == False):
                    player1.hands[0].wager = 0
                # CLICKED THE BACK BUTTON:
                elif BUTTONS[12].rect.collidepoint(event.pos):
                    if login:
                        login = False
                        for input in LOGIN_INPUTS:
                            input.content = ''
                    elif signup:
                        signup = False
                        for input in SIGNUP_INPUTS:
                            input.content = ''
                    elif add:
                        add = False
                        ADD_FUNDS_INPUTS[0].content = ''
                    startup = True
                # CLICKED THE ADD FUNDS BUTTON:
                elif BUTTONS[13].rect.collidepoint(event.pos):
                    add = True
                # CLICKED THE DOUBLE DOWN BUTTON:
                elif BUTTONS[14].background.collidepoint(event.pos):
                    doubled = True
                    playerDone = True

                    player1.wallet -= player1.hands[0].wager
                    player1.hands[0].wager = (2 * player1.hands[0].wager)

                    player1.hands[0].hit(theDeck)

                    draw_game(playerDone, None, None, login, signup, add, doubled)
                    pygame.time.delay(1500)

                    if player1.hands[0].value == -1:
                        print("Player busts...")
                        draw_game(playerDone, None, None, login, signup, add, doubled)
                        pygame.time.delay(3000)
                        evaluate_round(logged_in)
                        bet_placed = False
                        playerDone = False
                        doubled = False

                    else:
                        while dealer.hands[0].value < 17 and dealer.hands[0].value != -1:
                            dealer.hands[0].hit(theDeck)
                            draw_game(playerDone, None, None, login, signup, add, doubled)
                            pygame.time.delay(1500)
                        evaluate_round(logged_in)
                        bet_placed = False
                        playerDone = False
                        doubled = False
                    print("hello")

                # Handles the user clicking each of the chips
                if CHIPS[0].rect.collidepoint(event.pos) and (startup == False) and (bet_placed == False) and (login == False):
                    if player1.hands[0].wager + 0.5 <= player1.wallet:
                        player1.hands[0].wager = player1.hands[0].wager + 0.5
                elif CHIPS[1].rect.collidepoint(event.pos) and (startup == False) and (bet_placed == False) and (login == False):
                    if player1.hands[0].wager + 1 <= player1.wallet:
                        player1.hands[0].wager = player1.hands[0].wager + 1
                elif CHIPS[2].rect.collidepoint(event.pos) and (startup == False) and (bet_placed == False) and (login == False):
                    if player1.hands[0].wager + 2 <= player1.wallet:
                        player1.hands[0].wager = player1.hands[0].wager + 2
                elif CHIPS[3].rect.collidepoint(event.pos) and (startup == False) and (bet_placed == False) and (login == False):
                    if player1.hands[0].wager + 5 <= player1.wallet:
                        player1.hands[0].wager = player1.hands[0].wager + 5
                elif CHIPS[4].rect.collidepoint(event.pos) and (startup == False) and (bet_placed == False) and (login == False):
                    if player1.hands[0].wager + 10 <= player1.wallet:
                        player1.hands[0].wager = player1.hands[0].wager + 10
                elif CHIPS[5].rect.collidepoint(event.pos) and (startup == False) and (bet_placed == False) and (login == False):
                    if player1.hands[0].wager + 20 <= player1.wallet:
                        player1.hands[0].wager = player1.hands[0].wager + 20
                elif CHIPS[6].rect.collidepoint(event.pos) and (startup == False) and (bet_placed == False) and (login == False):
                    if player1.hands[0].wager + 50 <= player1.wallet:
                        player1.hands[0].wager = player1.hands[0].wager + 50
                elif CHIPS[7].rect.collidepoint(event.pos) and (startup == False) and (bet_placed == False) and (login == False):
                    if player1.hands[0].wager + 100 <= player1.wallet:
                        player1.hands[0].wager = player1.hands[0].wager + 100

                # Handles the user focussing on the login inputs.
                if login:
                    for input in LOGIN_INPUTS:
                        if input.rect.collidepoint(event.pos):
                            input.active = True
                        else: input.active = False

                    if REMEMBER_ME.rect.collidepoint(event.pos):
                        REMEMBER_ME.toggle()

                # Handles the user focussing on the signup inputs.
                if signup:
                    for input in SIGNUP_INPUTS:
                        if input.rect.collidepoint(event.pos):
                            input.active = True
                        else: input.active = False

                # Handles the user focussing on the add funds inputs.
                if add:
                    for input in ADD_FUNDS_INPUTS:
                        if input.rect.collidepoint(event.pos):
                            input.active = True
                        else: input.active = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_TAB:
                    if signup: 
                        x = 0
                        for i in range(len(SIGNUP_INPUTS)):
                            if (SIGNUP_INPUTS[i].active):
                                SIGNUP_INPUTS[i].active = False
                                if (i + 1) < len(SIGNUP_INPUTS):
                                    x = i + 1
                        SIGNUP_INPUTS[x].active = True

                    elif login:
                        x = 0
                        for i in range(len(LOGIN_INPUTS)):
                            if (LOGIN_INPUTS[i].active):
                                LOGIN_INPUTS[i].active = False
                                if (i + 1) < len(LOGIN_INPUTS):
                                    x = i + 1
                        LOGIN_INPUTS[x].active = True

                    elif add:
                        x = 0
                        for i in range(len(ADD_FUNDS_INPUTS)):
                            if (ADD_FUNDS_INPUTS[i].active):
                                ADD_FUNDS_INPUTS[i].active = False
                                if (i + 1) < len(ADD_FUNDS_INPUTS):
                                    x = i + 1
                        ADD_FUNDS_INPUTS[x].active = True
                    
                else:
                    # If the user is focussed on a login input, enable typing in the input
                    for input in LOGIN_INPUTS:
                        if input.active:
                            if event.key == pygame.K_BACKSPACE:
                                input.content = input.content[:-1]
                            else: 
                                input.content += event.unicode
                            
                    # If the user is focussed on a signup input, enable typing in the input
                    for input in SIGNUP_INPUTS:
                        if input.active:
                            if event.key == pygame.K_BACKSPACE:
                                input.content = input.content[:-1]
                            else: 
                                input.content += event.unicode

                    # If the user is focussed on a funds input, enable typing in the input
                    for input in ADD_FUNDS_INPUTS:
                        if input.active:
                            if event.key == pygame.K_BACKSPACE:
                                input.content = input.content[:-1]
                            else: 
                                input.content += event.unicode
                          
            if event.type == pygame.QUIT:
                run = False
                pygame.QUIT()

        if startup:
            draw_startup(BUTTONS[0], BUTTONS[1], BUTTONS[2], BUTTONS[3], BUTTONS[4], BUTTONS[9], logged_in)
        elif signup:
            draw_signup(login, signup, add)
        elif login:
            draw_login(login, signup, add)
        elif add:
            draw_add_funds(login, signup, add)
        else: 
            if bet_placed:
                draw_game(playerDone, BUTTONS[5], BUTTONS[6], login, signup, add, doubled)
            else:
                draw_betting(CHIPS[0], CHIPS[1], CHIPS[2], CHIPS[3], CHIPS[4], CHIPS[5], CHIPS[6], CHIPS[7], BUTTONS[8], BUTTONS[11], login, signup, add)
    
    main()

if __name__ == "__main__":
    main()