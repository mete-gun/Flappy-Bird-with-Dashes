import pygame
from sys import exit
import random
import json
import os
import subprocess
from tkinter import messagebox


#JUST PLAY THE GAME WHY ARE YOU LOOKING AT THE CODE!?

pygame.init()
screen = pygame.display.set_mode((1000, 620))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

cooldown = 10
last_time = 0

the_bug_in_the_beginning = False


dosya_yolu = os.path.join(os.path.dirname(__file__), "Saves/Scores.json")
# Skorları okumak
def skor_oku(dosya_adi):
    try:
        with open(dosya_adi, 'r') as dosya:
            veri = dosya.read().strip()
            if not veri:  # Dosya boşsa
                return {"en_yuksek_skor": 0, "son_skor": 0}
            return json.loads(veri)
    except FileNotFoundError:
        return {"en_yuksek_skor": 1, "son_skor": 1}  # Dosya yoksa varsayılan skorlar
    except json.JSONDecodeError:
        messagebox.showerror("Error!", "JSON File is corrupted!")
        messagebox.showinfo("Info", "Highscore and Last Score will be reset!")
        return {"en_yuksek_skor": 0, "son_skor": 0}
def skor_yaz(dosya_adi, son_skor):
    global readed
    readed["Last"] = son_skor  # Son skoru güncelle

    if son_skor > readed["High"]:  # Eğer yeni skor yüksekse High'ı güncelle
        readed["High"] = son_skor

    try:
        with open(dosya_adi, 'w') as dosya:
            json.dump(readed, dosya, indent=4)  # JSON'ı daha okunabilir kaydet
    except Exception as e:
        messagebox.showerror("Error!", f"An error occurred while saving the scores!\n{e}")

#skor_yaz("skorlar.json", son_skor)

readed = skor_oku(dosya_adi=dosya_yolu)

abc = str(readed["Last"])

#skorlar = skor_oku("skorlar.json")
#print(f"En Yüksek Skor: {skorlar['en_yuksek_skor']}")
#print(f"Son Skor: {skorlar['son_skor']}")

borular = []  

font2 = pygame.font.Font(None, 50)
font3 = pygame.font.Font(None, 50)

font2 = font2.render("Highscore: " + str(readed["High"]), True, (255, 255, 255))
font3 = font3.render("Last Score: " + str(readed["Last"]), True, (255, 255, 255))

text2 = pygame.font.Font(None, 50)
text2 = text2.render(f"Game Over.", True, (255, 255, 255))




text4 = pygame.font.Font(None, 40)
text4 = text4.render("Right Click to Restart", True, (255, 255, 255))



pipe_head = pygame.image.load("img/boru_ucu.png").convert_alpha()
pipe_body = pygame.image.load("img/boru_govde.png").convert_alpha()


def create_pipes():
    x_pos = 1000  
    h1 = random.randint(100, 400)
    h2 = 620 - 100 - h1
    borular.append([x_pos, h1, h2])  


def draw_pipes():
    for pipe in borular:
        x, h1, h2 = pipe
        screen.blit(pygame.transform.scale(pipe_head, (40, 20)), (x, h1 - 20 ))
        screen.blit(pygame.transform.scale(pipe_body, (30, h1)), (x + 5, -20))
        screen.blit(pygame.transform.scale(pipe_head, (40, 20)), (x, 650 - h2))
        screen.blit(pygame.transform.scale(pipe_body, (30, h2)), (x + 5, 650 - h2 + 20))
        pipe[0] -= 3.5
    
    borular[:] = [pipe for pipe in borular if pipe[0] > -40]

for i in range(5):
    create_pipes()

gravity = 0
started = False
start_screen = True

BG = pygame.image.load("img/BG.png")
BG = pygame.transform.scale(BG, (1100, 620))
bird = pygame.image.load("img/Bird.png").convert_alpha()
bird = pygame.transform.scale(bird, (50, 50))
bird_rect = bird.get_rect(midbottom=(100, 510))

bird_rect.height -= 10
bird_rect.width -= 10

restart_clicked = False

written = False

dashed = False

font1 = pygame.font.Font(None, 50)
font1 = font1.render("Left Click to Start and Fly", True, (255, 255, 255))

text1 = pygame.font.Font(None, 50)
text1 = text1.render("Right Click to Dash 200px forward", True, (255, 255, 255))

lost = True
points = 0

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and lost:
                gravity -= 5
                started = True

            elif event.button == 3 and not the_bug_in_the_beginning and lost:
                if not dashed:
                    bird_rect.x += 200
                    dashed = True
                    
    if lost:
        points += 0.01
                
    
    if start_screen and not started:
        screen.fill((0, 0, 0))
        screen.blit(font1, (300, 300))
        screen.blit(text1, (200, 400))
        if pygame.mouse.get_pressed()[0]:
            start_screen = False
            started = True



    #WHY THIS CODE IS WORKING IT SHOULDNT WORK 


    if not lost:
        text3 = pygame.font.Font(None, 40)
        text3 = text3.render(f"Current Score:  "f'"{int(points)}"', True, (170, 255, 160))

        if int(points) > readed["High"] and not written:  # Sadece yeni skor rekor kırınca dosyaya yaz
            readed["High"] = int(points)
            skor_yaz(dosya_yolu, int(points))
            written = True

        elif not written:
            readed["Last"] = int(points)
            skor_yaz(dosya_yolu, int(points))
            written = True

        Fener = pygame.font.Font(None, 50)
        Fener = Fener.render("Highscore: " + str(readed["High"]), True, (255, 180, 190))

        Bahce = pygame.font.Font(None, 50)
        Bahce = Bahce.render("Last Score: " + abc, True, (190, 180, 255))



        screen.fill((0, 0, 0))
        screen.blit(text2, (300, 400))
        screen.blit(text3, (290, 300))
        screen.blit(text4, (300, 500))
        screen.blit(Fener, (300, 100))
        screen.blit(Bahce, (300, 200))



        if pygame.mouse.get_pressed()[2] and not restart_clicked:
            try:
                subprocess.Popen(["python", "Main.py"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                pygame.quit()  
                exit()  
                restart_clicked = True
            except Exception as e:
                subprocess.Popen(["run", "Main.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            
    if started:

        if bird_rect.collidelist([(x, h1 - 20, 40, 20) for x, h1, h2 in borular]) != -1 or bird_rect.collidelist([(x, 650 - h2, 40, 20) for x, h1, h2 in borular]) != -1 or bird_rect.y <= 0 or bird_rect.y >= 620:
            
            bird = pygame.image.load("img/dead_bird.png").convert_alpha()
            gravity = 5
            bird = pygame.transform.scale(bird, (50, 50))
            bird = pygame.transform.rotate(bird, -80)
            
            lost = False


        if dashed:
            bird_rect.x -= 1

            if bird_rect.x <= 100:
                dashed = False

        if bird_rect.y >= 630:
            
            lost = False
            started = False
            start_screen = False
            gravity = 0
    
        gravity += 0.2
        bird_rect.y += gravity
        
        screen.blit(BG, (-20, 0))
        screen.blit(bird, bird_rect)
        draw_pipes()
       
        if len(borular) < 10 and (len(borular) == 0 or borular[-1][0] < 700):
            create_pipes()

    pygame.display.update()
    clock.tick(max(30 , 60))


