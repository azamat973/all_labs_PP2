import pygame
import os

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Music Player")

MUSIC_FOLDER = "music"
music_files = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp3")]

if not music_files:
    raise Exception("В папке 'music' нет MP3-файлов!")

current_track = 0
is_paused = False

def play_music():

    global is_paused
    pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, music_files[current_track]))
    pygame.mixer.music.play()
    print(f" Playing: {music_files[current_track]}")
    is_paused = False

play_music()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if is_paused:
                    pygame.mixer.music.unpause()
                    print("▶ Resumed")
                    is_paused = False
                else:
                    pygame.mixer.music.pause()
                    print("⏸ Paused")
                    is_paused = True
            elif event.key == pygame.K_s:
                pygame.mixer.music.stop()
                print("⏹ Stopped")
            elif event.key == pygame.K_RIGHT:
                current_track = (current_track + 1) % len(music_files)
                play_music()
            elif event.key == pygame.K_LEFT:
                current_track = (current_track - 1) % len(music_files)
                play_music()

pygame.quit()
