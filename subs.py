import tkinter as tk
from tkinter import simpledialog

# i'm so sorry for the horrendous code

ROOT = tk.Tk()

ROOT.withdraw()
init_setup = False

try:
    file = open("9x_tracker.cfg")

except:
    init_setup = True
    file = open("9x_tracker.cfg", "w")

if init_setup:
    apiKey = simpledialog.askstring(title="Setup",
                                      prompt="What's your API Key?:")

    channelID = simpledialog.askstring(title="Setup",
                                      prompt="What's your channel ID?:")

    goal = int(simpledialog.askstring(title="Setup",
                                      prompt="What's your current subscriber goal?:"))

    file.write(apiKey + "\n" + channelID + "\n" + str(goal) + "\n")
    file.close()

else:
    config = file.read().split("\n")
    file.close()

    apiKey = config[0]
    channelID = config[1]
    goal = int(config[2])
        

req = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channelID}&key={apiKey}"

import requests
import pygame
import time
import sys
import win32gui
import win32con
import os
import time

def gradientRect( window, left_colour, right_colour, target_rect ):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
    pygame.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 0,1 ) )            # left colour line
    pygame.draw.line( colour_rect, right_colour, ( 1,0 ), ( 1,1 ) )            # right colour line
    colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )  # stretch!
    window.blit( colour_rect, target_rect )   

pygame.init()

cdinfo = pygame.display.Info()
ypos = (cdinfo.current_h - 50) + 5
xpos = (cdinfo.current_w // 2) - (300 // 2)

os.environ['SDL_VIDEO_WINDOW_POS'] = f"{xpos},{ypos}"

clock = pygame.time.Clock()

request = requests.get(req)

subcount = int(request.json()["items"][0]["statistics"]["subscriberCount"])
viewcount = int(request.json()["items"][0]["statistics"]["viewCount"])
vidcount = int(request.json()["items"][0]["statistics"]["viewCount"])

last_subcount = subcount
fanfare = pygame.mixer.Sound("fanfare.mp3")
failure = pygame.mixer.Sound("boowomp.mp3")

window = pygame.display.set_mode((300, 42), pygame.NOFRAME)

font = pygame.font.SysFont("JetBrains Mono Regular", 24, bold=False)

frames_since_update = 0

start = time.time()
mode = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    if time.time() > start + 5: # cycle mode
        mode += 1
        mode %= 3
        start = time.time()
    
    request = requests.get(req)

    window.fill((255, 255, 255))

    goalRect = pygame.Rect((0, 0), ((subcount / goal) * 300, 50))
    gradientRect(window, (255, 128, 0), (255, 0, 255), goalRect)

    borderRect = pygame.Rect((0, 0), window.get_size())
    pygame.draw.rect(window, (255, 255, 255), borderRect, 4)
    
    subcount = int(request.json()["items"][0]["statistics"]["subscriberCount"])
    viewcount = int(request.json()["items"][0]["statistics"]["viewCount"])
    vidcount = int(request.json()["items"][0]["statistics"]["videoCount"])
    
    if subcount > last_subcount:
        last_subcount = subcount
        fanfare.play()

    elif subcount < last_subcount:
        last_subcount = subcount
        failure.play()

    if mode == 0:
        count = font.render(f"{subcount:,} subs", False, (0, 0, 0))

    if mode == 1:
        count = font.render(f"{viewcount:,} views", False, (0, 0, 0))

    if mode == 2:
        count = font.render(f"{vidcount:,} videos", False, (0, 0, 0))
    
    count_rect = count.get_rect()
    win_rect = pygame.Rect((0, 0), window.get_size())

    count_rect.centerx = win_rect.centerx
    count_rect.centery = win_rect.centery

    window.blit(count, (count_rect.x, count_rect.y))

    pygame.display.update()

    win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    clock.tick(60)
