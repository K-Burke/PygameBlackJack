import pygame
import os
import textinput
import checkbox
import button
pygame.font.init()

WIDTH, HEIGHT, CENTER = 1200, 1000, (600, 375)

# ----- FONTS -----
NAME_FONT = pygame.font.SysFont('comicsans', 35)
WAGER_FONT = pygame.font.SysFont('comicsans', 22)

# ----- REQUIRED COLOURS -----
BORDER_COL = (227, 208, 39)
HEADER_COL = (217, 217, 217)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# ----- BUTTONS -----
PLAY_BUTTON = button.TextButton(475, 340, 250, 100, "PLAY", (185, 30, 30), (166,141,33))
PLAY_AS_GUEST_BUTTON = button.TextButton(475, 240, 250, 100, "PLAY as GUEST", (185, 30, 30), (166, 141, 33))
LOGIN_BUTTON = button.TextButton(475, 370, 250, 100, "LOGIN", (185, 30, 30), (166,141,33))
LOGOUT_BUTTON = button.TextButton(475, 485, 250, 100, "LOGOUT", (185, 30, 30), (166,141,33))
QUIT_BUTTON = button.TextButton(475, 630, 250, 100, "QUIT", (185, 30, 30), (166,141,33))
#HIT_BUTTON = button.Button(75, 375, pygame.image.load(os.path.join('images/buttons', 'hit.png')), 1.5)
HIT_BUTTON = button.TextButton(75, 375, 150, 60, "HIT", (185, 30, 30), (166,141,33))
#STAY_BUTTON = button.Button(255, 375, pygame.image.load(os.path.join('images/buttons', 'stay.png')), 1.5)
STAY_BUTTON = button.TextButton(255, 375, 150, 60, "STAY", (185, 30, 30), (166,141,33))
#SPLIT_BUTTON = button.Button(335, 375, pygame.image.load(os.path.join('images/buttons', 'split.png')), 2.5)
SPLIT_BUTTON = button.TextButton(615, 375, 150, 60, "SPLIT", (185, 30, 30), (166,141,33))
PLACE_BET_BUTTON = button.TextButton(953, 765, 125, 50, "PLACE BET", (45, 207, 45), (0,0,0))
# turq: 77, 209, 183
SIGNUP_BUTTON = button.TextButton(475, 500, 250, 100, "SIGNUP", (185, 30, 30), (166,141,33))
SUBMIT_BUTTON = button.TextButton(475, 630, 250, 100, "SUBMIT", (185, 30, 30), (166,141,33))
CLEAR_BUTTON = button.TextButton(953, 820, 125, 50, " CLEAR ", (185, 30, 30), (255, 255, 255))
BACK_BUTTON = button.Button(10, 5, pygame.image.load(os.path.join('images/buttons', 'back.png')), 0.2)
ADD_FUNDS_BUTTON = button.Button(900, 5, pygame.image.load(os.path.join('images/buttons', 'addfunds.png')), 0.2)
DOUBLE_DOWN_BUTTON = button.TextButton(435, 375, 150, 60, "DOUBLE DOWN", (185, 30, 30), (166,141,33))

BUTTONS = [PLAY_BUTTON, PLAY_AS_GUEST_BUTTON, LOGIN_BUTTON, LOGOUT_BUTTON, QUIT_BUTTON, HIT_BUTTON, STAY_BUTTON, SPLIT_BUTTON, PLACE_BET_BUTTON, SIGNUP_BUTTON, SUBMIT_BUTTON, CLEAR_BUTTON, BACK_BUTTON, ADD_FUNDS_BUTTON, DOUBLE_DOWN_BUTTON]

HALF_CHIP = button.Button(80, 750, pygame.image.load(os.path.join('images/chips', 'half.png')), 0.52)
ONE_CHIP = button.Button(185, 750, pygame.image.load(os.path.join('images/chips', 'one.png')), 0.52)
TWO_CHIP = button.Button(290, 750, pygame.image.load(os.path.join('images/chips', 'two.png')), 0.52)
FIVE_CHIP = button.Button(395, 750, pygame.image.load(os.path.join('images/chips', 'five.png')), 0.52)
TEN_CHIP = button.Button(500, 750, pygame.image.load(os.path.join('images/chips', 'ten.png')), 0.52)
TWENTY_CHIP = button.Button(605, 750, pygame.image.load(os.path.join('images/chips', 'twenty.png')), 0.52)
FIFTY_CHIP = button.Button(715, 750, pygame.image.load(os.path.join('images/chips', 'fifty.png')), 0.52)
HUNDRED_CHIP = button.Button(820, 750, pygame.image.load(os.path.join('images/chips', 'hundred.png')), 0.52)

CHIPS = [HALF_CHIP, ONE_CHIP, TWO_CHIP, FIVE_CHIP, TEN_CHIP, TWENTY_CHIP, FIFTY_CHIP, HUNDRED_CHIP]

# ----- TEXT INPUTS -----
first_name_input = textinput.TextInput((CENTER[0] - 200), 290, 400, 35, BORDER_COL, WAGER_FONT, False, 100)
last_name_input = textinput.TextInput((CENTER[0] - 200), 365, 400, 35, BORDER_COL, WAGER_FONT, False, 100)
email_input = textinput.TextInput((CENTER[0] - 200), 440, 400, 35, BORDER_COL, WAGER_FONT, False, 100)
password_input = textinput.TextInput((CENTER[0] - 200), 515, 400, 35, BORDER_COL, WAGER_FONT, True, 100)
confirm_input = textinput.TextInput((CENTER[0] - 200), 590, 400, 35, BORDER_COL, WAGER_FONT, True, 100)
wallet_input = textinput.TextInput((CENTER[0] + 80), 650, 120, 35, BORDER_COL, WAGER_FONT, False, 100)

login_email_input = textinput.TextInput((CENTER[0] - 200), 350, 400, 35, BORDER_COL, WAGER_FONT, False, 100)
login_password_input = textinput.TextInput((CENTER[0] - 200), 450, 400, 35, BORDER_COL, WAGER_FONT, True, 100)
stay_logged_in = checkbox.CheckBox((CENTER[0] + 180), 540, 20, 20)

card_number_input = textinput.TextInput((CENTER[0] - 200), 310, 400, 35, BORDER_COL, WAGER_FONT, False, 100)
month_input = textinput.TextInput((CENTER[0] - 200), 410, 80, 35, BORDER_COL, WAGER_FONT, False, 100)
year_input = textinput.TextInput((CENTER[0] - 80), 410, 80, 35, BORDER_COL, WAGER_FONT, False, 100)
cvv_input = textinput.TextInput((CENTER[0] - 200), 510, 120, 35, BORDER_COL, WAGER_FONT, False, 100)
amount_input = textinput.TextInput((CENTER[0] - 200), 610, 240, 35, BORDER_COL, WAGER_FONT, False, 100)

SIGNUP_INPUT_SET = [first_name_input, last_name_input, email_input, password_input, confirm_input, wallet_input]
LOGIN_INPUT_SET = [login_email_input, login_password_input]
ADD_FUNDS_INPUT_SET = [card_number_input, month_input, year_input, cvv_input, amount_input]
