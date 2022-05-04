#!/usr/bin/python
import pygame, os, random, sys

from GameProfile import GameProfile
from Game import Game

context = ""

options_selected = "Normal"
main_menu_options = ["Normal", "Time up", "While life", "Shop", "Lockers", "Quit"]

temp_username = "Anonyme"
profile = None
game = None

hangman_dir = os.path.dirname(os.path.realpath(__file__)) + '/'
assets_dir = hangman_dir + 'assets/'
images_dir = assets_dir + 'images/'
fonts_dir = assets_dir + 'fonts/'

i_icon = images_dir + "icon.png"


def reset():
    global profile, game
    profile.coins += game.coins_earned
    game = None


def get_random_word():
    with open(assets_dir + "words.txt") as file:
        lines = file.readlines()
        index = random.randint(0, len(lines))
        return lines[index].strip('\n')


def drawSecretWord(background, word, correct_letters):
    global game
    drawable_word = ""
    for letter in word:
        if letter in correct_letters:
            drawable_word += letter
        else:
            drawable_word += "_"
    draw_text(' '.join(drawable_word),
              (255, 255, 255) if (game.over == False or game.won == True) else (255, 0, 0),
              (320, 220), background, font2)


def draw_text(text, color, position, surface, font, centered=None, highlight=None):
    text_to_draw = font.render(text, 1, color)
    text_to_draw_position = text_to_draw.get_rect().move(position)

    if centered:
        text_to_draw_position.centerx = surface.get_rect().centerx
    if highlight:
        pygame.draw.rect(surface, (0, 0, 0), text_to_draw_position.inflate(10, 10), 0)

    surface.blit(text_to_draw, text_to_draw_position)


def draw_screen():
    global context, window, monospace, options_selected, profile, game

    background = pygame.image.load(images_dir + 'bg.png').convert()

    if "playing" in context:
        background = pygame.image.load(images_dir + 'bg-game.png').convert()

    match context:
        case "login":
            draw_text("Please login", (0, 0, 0), (0, 50), background, middst, True)
            current_user_edit = temp_username + " "
            draw_text(current_user_edit, (2, 0, 0), (0, 220), background, monospace, True)
            draw_text("Press enter to connect, leave blank if you don't want to connect", (60, 60, 60), (0, 430),
                      background,
                      font2, True)
        case "main-menu":
            draw_text("HangMan - Game", (0, 0, 0), (0, 20), background, middst, True)
            draw_text(profile.username + "(" + str(profile.id) + ")", (0, 0, 0), (500, 80), background, font2, False)
            draw_text(str(profile.coins) + " coins", (0, 0, 0), (500, 100), background, font2, False)
            option_pos_y = 170
            for option in main_menu_options:
                draw_text(option, (255, 255, 255), (50, option_pos_y), background, font2, True,
                          option == options_selected)
                option_pos_y += 40
        case "playing-normal":
            drawSecretWord(background, game.word[0], game.correct_letters)

            nn = "Won" if game.won else "Lost"
            text = 'Pick a letter, try to guess the word...' if (
                not game.over) else "You " + nn + " use return to show summary"
            draw_text(text, (255, 255, 255), (320, 180), background, font2)

            draw_text(game.incorrect_letters, (0, 0, 0), (320, 260), background, font2)
            displayGallows(background, len(game.incorrect_letters) + 1)
        case "playing-while-life":
            drawSecretWord(background, game.word[len(game.word) - 1], game.correct_letters)

            nn = "Won" if game.won else "Lost"
            text = 'Pick a letter, try to guess the word...' if (
                not game.over) else "You " + nn + " use return to show summary"
            draw_text(text, (255, 255, 255), (320, 180), background, font2)

            draw_text(game.incorrect_letters, (0, 0, 0), (320, 260), background, font2)
            draw_text(game.find_word, (0, 0, 0), (320, 300), background, font2)

            displayGallows(background, game.fail + 1)
        case "playing-time-up":
            drawSecretWord(background, game.word[len(game.word) - 1], game.correct_letters)

            draw_text(str(max(int(timer), 0)) + " second remaining", (255, 255, 255), (320, 160), background, font2)

            nn = "Won" if game.won else "Lost"
            text = 'Pick a letter, try to guess the word...' if (
                not game.over) else "You " + nn + " use return to show summary"
            draw_text(text, (255, 255, 255), (320, 180), background, font2)

            draw_text(game.incorrect_letters, (0, 0, 0), (320, 260), background, font2)
            draw_text(game.find_word, (0, 0, 0), (320, 300), background, font2)

            displayGallows(background, len(game.incorrect_letters) + 1)
        case "game-summary":
            background = pygame.image.load(images_dir + 'bg-game.png').convert()
            displaySummary(background)

    window.blit(background, (0, 0))
    pygame.display.update()


def displayGallows(background, state):
    global profile, game
    img = pygame.image.load(images_dir + "gallows/" + profile.gallows_equipped + "/" + str(
        state) + ".png").convert_alpha()
    background.blit(img, (10, 10))


def displaySummary(background):
    draw_text("Game Summary", (0, 0, 0), (0, 20), background, middst, True)

    nn = "Won" if game.won else "Lost"
    title_text = 'You ' + nn + '!'
    draw_text(title_text, (0, 0, 0), (0, 100), background, font2, True)

    pygame.draw.line(background, (0, 0, 0), (25, 150), (625, 150), 4)
    pygame.draw.line(background, (0, 0, 0), (25, 300), (625, 300), 4)
    pygame.draw.line(background, (0, 0, 0), (25, 430), (625, 430), 4)

    if game.mode == "normal":
        draw_text("Incorrect letter used : " + str(len(game.incorrect_letters)), (0, 0, 0), (25, 160),
                  background,
                  font2, True)
        draw_text("Letter in word : " + str(len(game.word[0])), (0, 0, 0), (25, 260), background, font2, True)
        draw_text("You trove the word: " + game.word[0], (0, 0, 0), (0, 400), background, font2, True)
    elif game.mode == "while-life":
        draw_text("You find words : " + str(len(game.word) - 1), (0, 0, 0), (25, 160), background, font2, True)
        draw_text("You trove the words : " + game.find_word, (0, 0, 0), (0, 200), background, font2, True)
        draw_text("You don't trove the word : " + game.word[len(game.word) - 1], (0, 0, 0), (0, 240), background,
                  font2, True)
    elif game.mode == "time-up":
        draw_text("Incorrect letter used : " + str(len(game.incorrect_letters)), (0, 0, 0), (25, 160),
                  background,
                  font2, True)
        draw_text("Time used to find : " + str(max(60 - int(timer), 0)), (0, 0, 0), (25, 180), background, font2, True)
        draw_text("the word is : " + game.word[0], (0, 0, 0), (0, 200), background, font2, True)

    draw_text("SCORE    :          " + str(game.score), (0, 0, 0), (25, 340), background, font2, True)
    draw_text("COINS    :          " + str(game.coins_earned), (0, 0, 0), (25, 360), background, font2, True)
    draw_text("If you want to replay Y else N", (0, 0, 0), (0, 450), background, font2, True)


def previous_option_main():
    global options_selected
    current_index = main_menu_options.index(options_selected)
    if current_index > 0:
        options_selected = main_menu_options[current_index - 1]
    else:
        options_selected = main_menu_options[len(main_menu_options) - 1]


def next_option_main():
    global options_selected
    current_index = main_menu_options.index(options_selected)
    if current_index < len(main_menu_options) - 1:
        options_selected = main_menu_options[current_index + 1]
    else:
        options_selected = main_menu_options[0]


def loadProfile(username):
    global profile
    if username == "Anonyme":
        profile = GameProfile()
        profile.id = 0
        profile.username = username
        profile.coins = 0

        profile.purchased_avatars = []
        profile.purchased_gallows = []

        profile.avatar_equipped = "default"
        profile.gallows_equipped = "default"
    else:
        profile = GameProfile()
        profile.id = 0
        profile.username = username
        profile.coins = 0

        profile.purchased_avatars = []
        profile.purchased_gallows = []

        profile.avatar_equipped = "default"
        profile.gallows_equipped = "default"


def setupGame(mode):
    global game
    game = Game()
    game.mode = mode
    game.word = []
    game.word.append(get_random_word())
    print(game.word)
    game.find_word = ""
    game.incorrect_letters = ""
    game.correct_letters = ""
    game.score = 0
    game.fail = 0
    game.coins_earned = 0
    game.over = False
    game.won = False


def calculate_score(mode):
    global game
    if mode == "playing-normal":
        game.score = max(len(game.word[0]) - len(game.incorrect_letters), 0)
        game.coins_earned = max((game.score * 10), 0)
    elif mode == "playing-while-life":
        game.score = max((len(game.word) * 2) - game.fail, 0)
        game.coins_earned = max((game.score * 10), 0)
    elif mode == "playing-time-up":
        if game.won == True:
            game.score = max((len(game.word[0]) - len(game.incorrect_letters) * timer), 0)
            game.coins_earned = max((game.score * 10), 0)


def handleEventOnGame(event):
    global context, timer
    key_pressed = chr(event.key)
    if not game.over:
        if key_pressed in "abcdefghijklmnopqrstuvwxyz0123456789":
            secret_word = game.word[len(game.word) - 1]
            correct_letters = game.correct_letters
            incorrect_letters = game.incorrect_letters

            if key_pressed in secret_word:
                if key_pressed not in correct_letters:
                    game.correct_letters = correct_letters + key_pressed
                    found_all_letters = True
                    for i in range(len(secret_word)):
                        if secret_word[i] not in game.correct_letters:
                            found_all_letters = False
                    if found_all_letters:
                        if not context == "playing-while-life":
                            game.won = True
                            game.over = True
                        else:
                            game.find_word = game.find_word + " " + secret_word
                            game.word.append(get_random_word())
                            print(game.word)
                            game.correct_letters = ""
                            game.incorrect_letters = ""
                            game.won = True
            elif key_pressed not in incorrect_letters:
                game.incorrect_letters = incorrect_letters + key_pressed
                game.fail = game.fail + 1
                if game.fail == 9:
                    game.over = True
                    game.won = False
                    timer = 0
    else:
        if event.key == pygame.K_RETURN:
            calculate_score(context)
            context = "game-summary"


pygame.init()
pygame_icon = pygame.image.load(i_icon)
pygame.display.set_icon(pygame_icon)

clock = pygame.time.Clock()
timer = 120
dt = 0

middst = pygame.font.Font(fonts_dir + 'middst.ttf', 56)
font2 = pygame.font.Font(None, 24)
monospace = pygame.font.SysFont("monospace", 60)

context = "login"

window = pygame.display.set_mode((640, 480), pygame.DOUBLEBUF)

while True:
    draw_screen()

    if context == "playing-time-up":
        if not game.over:
            timer -= dt
        if timer <= 0:
            game.over = True
            game.won = False
        dt = clock.tick(30) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:

            match context:
                case "login":
                    if event.key < 256:
                        key_pressed = chr(event.key)
                        if event.key == pygame.K_BACKSPACE:
                            temp_username = temp_username[:-1]
                        elif event.key == pygame.K_RETURN:
                            loadProfile(temp_username)
                            context = "main-menu"
                        elif key_pressed in 'abcdefghijklmnopqrstuvwxyz0123456789':
                            temp_username += key_pressed
                        else:
                            print("Invalid character")
                case "main-menu":
                    if event.key == pygame.K_DOWN:
                        next_option_main()
                    elif event.key == pygame.K_UP:
                        previous_option_main()
                    elif event.key == pygame.K_RETURN:
                        match options_selected:
                            case "Normal":
                                setupGame("normal")
                                context = "playing-normal"
                            case "Time up":
                                setupGame("time-up")
                                context = "playing-time-up"
                                timer = 60
                            case "While life":
                                setupGame("while-life")
                                context = "playing-while-life"
                            case "Quit":
                                sys.exit(0)
                    else:
                        print("Invalid key")
                case "playing-normal":
                    if event.key < 256:
                        handleEventOnGame(event)
                case "playing-time-up":
                    if event.key < 256:
                        handleEventOnGame(event)
                case "playing-while-life":
                    if event.key < 256:
                        handleEventOnGame(event)
                case "game-summary":
                    if event.key < 256:
                        key_pressed = chr(event.key)

                        if key_pressed == "y":
                            reset()
                            context = "main-menu"
                        elif key_pressed == "n":
                            sys.exit(0)
                        else:
                            print("Invalid key")