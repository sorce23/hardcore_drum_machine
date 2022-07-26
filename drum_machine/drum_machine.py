import pygame
from pygame import mixer
pygame.init()

WIDTH = 720
HEIGHT = 480

black = (0, 0, 0)
white = (255, 255, 255)
dark_gray = (50, 50, 50)
gray = (135, 135, 135)
green = (10, 148, 10)
gold = (212, 175, 55)
blue = (0, 255, 255)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("DRUM_machine")
label_font = pygame.font.Font('ArthurGothic.ttf', 22)
medium_font = pygame.font.Font('futura.ttf', 16)

fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 7
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
active_list = [1 for _ in range(instruments)]
bpm = 180
playing = True
active_length = 0
active_beat = 1
beat_changed = True
save_menu = False
load_menu = False
saved_beats = []
file = open('saved_beats.txt', 'r')
for line in file:
    saved_beats.append(line)
beat_name = ''
typing = False

# load in sounds
hi_hat = mixer.Sound('sounds/hh closed.wav')
snare = mixer.Sound('sounds/snare.wav')
bassdrum = mixer.Sound('sounds/kick_01.wav')
crash = mixer.Sound('sounds/crash.wav')
clap = mixer.Sound('sounds/clap.wav')
ride = mixer.Sound('sounds/ride.wav')
kick = mixer.Sound('sounds/kick_02.wav')
pygame.mixer.set_num_channels(instruments * 4)


def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                bassdrum.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                ride.play()
            if i == 6:
                kick.play()


def draw_grid(clicks, beat, actives):
    left_box = pygame.draw.rect(screen, green, [0, 0, 100, HEIGHT - 100], 5)
    bottom_box = pygame.draw.rect(screen, gold, [0, HEIGHT - 100, WIDTH, 100], 5)
    boxes = []
    colors = [gray, white, gray]
    hi_hat_text = label_font.render('Hi Hat', True, colors[actives[0]])
    screen.blit(hi_hat_text, (20, 16))
    snare_text = label_font.render('Snare', True, colors[actives[1]])
    screen.blit(snare_text, (20, 70))
    bassdrum_text = label_font.render('BassDrum', True, colors[actives[2]])
    screen.blit(bassdrum_text, (3, 124))
    crash_text = label_font.render('Crash', True, colors[actives[3]])
    screen.blit(crash_text, (20, 178))
    clap_text = label_font.render('Clap', True, colors[actives[4]])
    screen.blit(clap_text, (20, 232))
    ride_text = label_font.render('Ride', True, colors[actives[5]])
    screen.blit(ride_text, (20, 286))
    kick_text = label_font.render('Kick', True, colors[actives[5]])
    screen.blit(kick_text, (20, 340))
    for i in range(instruments):
        pygame.draw.line(screen, green, (0, (i * 54) + 54), (99, (i * 54) + 54), 3)

    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                if actives[j] == 1:
                    color = green
                else:
                    color = dark_gray
            rect = pygame.draw.rect(screen, color, [i * ((WIDTH - 100) // beats) + 105,
                                                    (j * 54) + 5, ((WIDTH - 100) // beats) - 5,
                                                    ((HEIGHT - 100) // instruments) - 5], 0, 3)
            pygame.draw.rect(screen, gold, [i * ((WIDTH - 100) // beats) + 100, (j * 54),
                                             ((WIDTH - 100) // beats), ((HEIGHT - 100) // instruments)], 5, 5)
            pygame.draw.rect(screen, black, [i * ((WIDTH - 100) // beats) + 100, (j * 54),
                                             ((WIDTH - 100) // beats), ((HEIGHT - 103) // instruments)], 2, 5)
            boxes.append((rect, (i, j)))

        active = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 100) // beats) + 100, 0, ((WIDTH - 100) // beats), instruments * 54], 2, 2)
    return boxes


def draw_save_menu(beat_name, typing):
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render('SAVE MENU: Enter a Name for Current Beat', True, white)
    saving_btn = pygame.draw.rect(screen, gray, [WIDTH // 2 - 100, HEIGHT * 0.25, 200, 50], 0, 5)
    saving_txt = label_font.render('Save Beat', True, white)
    screen.blit(saving_txt, (WIDTH // 2 - 50, HEIGHT * 0.25 + 20))
    screen.blit(menu_text, (200, 10))
    exit_btn = pygame.draw.rect(screen, gray, [WIDTH - 100, HEIGHT - 50, 90, 45], 0, 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH - 90, HEIGHT - 40))
    if typing:
        pygame.draw.rect(screen, dark_gray, [200, 100, 300, 100], 0, 5)
    entry_rect = pygame.draw.rect(screen, gray, [200, 100, 300, 100], 5, 5)
    entry_text = medium_font.render(f'{beat_name}', True, white)
    screen.blit(entry_text, (215, 125))
    return exit_btn, saving_btn, entry_rect


def draw_load_menu():
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    exit_btn = pygame.draw.rect(screen, gray, [WIDTH - 100, HEIGHT - 50, 90, 45], 0, 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH - 80, HEIGHT - 35))
    return exit_btn


run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat, active_list)
    # lower menu buttons
    play_pause = pygame.draw.rect(screen, gray, [25, HEIGHT - 75, 100, 50], 0, 5)
    play_text = medium_font.render('Play/Pause', True, white)
    screen.blit(play_text, (35, HEIGHT - 65))

    if playing:
        play_text2 = medium_font.render('Playing', True, dark_gray)
    else:
        play_text2 = medium_font.render('Paused', True, dark_gray)
    screen.blit(play_text2, (35, HEIGHT - 50))
    # bpm stuff
    bpm_rect = pygame.draw.rect(screen, gray, [150, HEIGHT - 75, 100, 50], 5, 5)
    bpm_text = medium_font.render('BPM', True, white)
    screen.blit(bpm_text, (185, HEIGHT - 65))
    bpm_text2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text2, (185, HEIGHT - 50))
    bpm_add_rect = pygame.draw.rect(screen, gray, [255, HEIGHT - 75, 24, 24], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, gray, [255, HEIGHT - 50, 24, 24], 0, 5)
    add_text = medium_font.render('+', True, white)
    sub_text = medium_font.render('-', True, white)
    screen.blit(add_text, (261, HEIGHT - 74))
    screen.blit(sub_text, (264, HEIGHT - 50))
    # beats stuff
    beats_rect = pygame.draw.rect(screen, gray, [300, HEIGHT - 75, 100, 50], 5, 5)
    beats_text = medium_font.render('Beats', True, white)
    screen.blit(beats_text, (330, HEIGHT - 65))
    beats_text2 = label_font.render(f'{beats}', True, white)
    screen.blit(beats_text2, (345, HEIGHT - 50))
    beats_add_rect = pygame.draw.rect(screen, gray, [405, HEIGHT - 75, 24, 24], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, gray, [405, HEIGHT - 50, 24, 24], 0, 5)
    add_text = medium_font.render('+', True, white)
    sub_text = medium_font.render('-', True, white)
    screen.blit(add_text, (411, HEIGHT - 74))
    screen.blit(sub_text, (414, HEIGHT - 50))
    # instrument boxes
    instrument_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i * 54), (100, 54))
        instrument_rects.append(rect)
    # save and load stuff
    save_button = pygame.draw.rect(screen, gray, [450, HEIGHT - 75, 100, 24], 0, 5)
    save_text = medium_font.render('Save Beat', True, white)
    screen.blit(save_text, (460, HEIGHT - 70))
    load_button = pygame.draw.rect(screen, gray, [450, HEIGHT - 50, 100, 24], 0, 5)
    load_text = medium_font.render('Load Beat', True, white)
    screen.blit(load_text, (460, HEIGHT - 45))

    # clear bord
    clear_button = pygame.draw.rect(screen, gray, [575, HEIGHT - 75, 100, 50], 0, 5)
    clear_text = medium_font.render('CLEAR', True, white)
    screen.blit(clear_text, (600, HEIGHT - 60))

    if save_menu:
        exit_button, saving_button, entry_rectangle = draw_save_menu(beat_name, typing)
    if load_menu:
        exit_button = draw_load_menu()

    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 1
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 1
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            elif clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
            elif save_button.collidepoint(event.pos):
                save_menu = True
            elif load_button.collidepoint(event.pos):
                load_menu = True
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1
        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True
                beat_name = ''
                typing = False
            if entry_rectangle.collidepoint(event.pos):
                if typing:
                    typing = False
                elif not typing:
                    typing = True
        if event.type == pygame.TEXTINPUT and typing:
            beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name) > 0 and typing:
                beat_name = beat_name[:-1]

    beat_length = 3600 // bpm

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()
pygame.quit()
