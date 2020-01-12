# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 17:25:07 2017

@author: Maik Wigand
"""

import pygame,sys,xlsxwriter,configparser
import numpy as np
from time import time
from time import sleep
import random
import Tkinter as tki
import tkMessageBox
from pygame.locals import *
from pygame.compat import unichr_, unicode_

#Other Classes

#A simple black rectangle object
class CorsiBlock:
    def __init__(self, position, size, color):
        self.position = position
        self.size = size
        self.color = color
    def __render__(self, screen):
        pygame.draw.rect(screen, self.color, (self.position, self.size))
    def change_pos(self, position, screen):
        self.position = position
        self.__render__(screen)
        
class AttrDict(dict):       #Enables Access thorugh attributes as well as dictionary keys. Access as a.b instead of as a["b"]. Derived from Dict. Retrieved from Stackverflow.com
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

# Colors
# Different colors are being defined based on the RGB system
# and gray is being chosen as the background color
col_white = (250, 250, 250)
col_black = (0, 0, 0)
col_gray = (220, 220, 220)
col_red = (250, 0, 0)
col_green = (0, 200, 0)
col_blue = (0, 0, 250)
col_yellow = (250,250,0)
BACKGR_COL = col_gray


# Initializing PyGame Window, FPS Cap and clock for timers
screen_width=800
screen_height=600
SCREEN_DIM = (screen_width, screen_height)
pygame.init()
pygame.display.set_mode(SCREEN_DIM) 
pygame.display.set_caption("Corsi Block Tapping Task")
screen = pygame.display.get_surface()
screen.fill(BACKGR_COL)
font = pygame.font.Font(None, 80)
font_small = pygame.font.Font(None, 40) 
FPS = 30
clock = pygame.time.Clock()
config = configparser.ConfigParser(dict_type=AttrDict)



#Other Global Variables

#letter Lists used for save_xlsx() and write_text()
parlist = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
parlist_small = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
correctness = False
corsi_block_number=9
intro_text=[]
summary_text=[]
goodbye_text=[]
block_in=False
blocks=[]
STAY=False


def main():
    STATE = "INITIALIZE" ## WELCOME,INTRO,READY,SHOW,ASK,GOODBYE, FEEDBACK, SUMMARY, RESTORE, INITIALIZE
    participant_no=1

    # screen refresh loop
    while True:
        # setting the background color
        pygame.display.get_surface().fill(BACKGR_COL)    
        
       
        #STAY used for determining what to do when accessing config.ini failed.
        global STAY
        #STATE initialize is strictly speaking an ATC, but makes most sense appearing toward the beginning of the code
        if STATE == "INITIALIZE": #Loading all neccessary program resources and initializing variables
            #error catching used everytime when reading or writing files
            try:
               global corsi_block_number
               global intro_text
               global sumary_text
               global goodbye_text
               #try to Load from config.ini
               time_between_trials=float(load_res(0))
               max_trial_number = int(load_res(1))
               show_feedback_time= int(load_res(2))
               corsi_block_number = int(load_res(3))
               intro_text = load_text(load_res(4))
               summary_text = load_text(load_res(5))
               goodbye_text = load_text(load_res(6))
               #
               try:
                pygame.mixer.music.load('beep.mp3') #try to load sound file
               except Exception as ex3:
                make_errorbox("RES IMPORT FAILED", "Could not import beep.mp3.\n"+"ERROR MSG:\n"+"{}".format(str(ex3)))
               #setting up important variables
               current_trial_number=0
               pattern_number=1
               react_time_list = list(range(max_trial_number)) 
               time_ref=0
               showed=False
               time_diff=0
               map_set = False
               pattern_set = False
               number_correct = 0
               clicked=0
               click = False
               fail_list = list(range(max_trial_number)) #List that is used to keep track of the lenth of patterns the user failed at
               scale_score = max_trial_number
               STATE = "WELCOME"
            #if reading from config was not possible go to state "RESTORE" to ask whether to just 
            #proceed with default values one time or to create files for default settings
            except Exception as ex2:
                if STAY == True:
                    #enter when not able to access config.ini and did not create fefault files
                    intro_text = ["Welcome to the Experiment!"]
                    summary_text = ["You can save your Data in the next Window"]
                    goodbye_text = ["Thank you for Participating"]
                    time_between_trials=0.3
                    max_trial_number=9
                    show_feedback_time=1
                    corsi_block_number=9
                    
                    try:
                        pygame.mixer.music.load('beep.mp3')
                    except Exception as ex3:
                        make_errorbox("RES IMPORT FAILED", "Could not import beep.mp3.\n"+"ERROR MSG:\n"+"{}".format(str(ex3)))
                    current_trial_number=0
                    pattern_number=1
                    react_time_list = list(range(max_trial_number)) 
                    time_ref=0
                    time_diff=0
                    map_set = False
                    pattern_set = False
                    clicked=0
                    click = False
                    fail_list = list(range(max_trial_number))
                    scale_score = -1
                    STATE = "WELCOME"
                else:  
                    make_errorbox("PRESET IMPORT FAILED", "Could not import config.ini values\n"+"ERROR MSG:\n"+"{}".format(str(ex2)))
                    STATE = "RESTORE"
            
            
            
                
        
        
       
        
        
        # Interactive Transition Conditionals (ITC)
            
        # event loop (is only entered when an event occured)
        for event in pygame.event.get():
            
        #ICT Quit Events (quits the programm when the Escape button is pressed)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
                
            mouse_pos=pygame.mouse.get_pos()  #retrieving mouse cursor position
    
            #State transition to intro if any key is pressed    
            if STATE == "WELCOME":
                if event.type == pygame.KEYDOWN:
                    STATE = "INTRO"
            #start reference timer for ready state after user presses a mousebutton
            if STATE == "INTRO":
                if event.type == pygame.MOUSEBUTTONUP:
                    STATE = "READY"
                    time_ref = time()
            #saves cursor position when user presses a mousebutton
            if STATE == "ASK":
                if event.type == pygame.MOUSEBUTTONUP:
                    click = True
                    mouseX = mouse_pos[0]
                    mouseY = mouse_pos[1]   
            # Resets to initialize state and add one to the participant number
            # when the R button is pressed; Save the results in an xlsx file
            # when the S Button is pressed
            if STATE == "GOODBYE":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    participant_no+=1
                    STATE = "INITIALIZE"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    save_xlsx(react_time_list,current_trial_number, calc_avg_list(react_time_list), participant_no, calc_std(react_time_list), scale_score)
            if STATE == "SUMMARY":
                if event.type == pygame.MOUSEBUTTONUP:
                    STATE = "GOODBYE"
            # Keys for when at least one of the default settings is missing:
            # Creates new default files when the C button is pressed; Proceeds
            # with default setting without restoring the files (only for one time) when the P button
            # is pressed.
            if STATE == "RESTORE":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    create_default()
                    make_errorbox("DEFAULT CREATE", "Will create default preset and then restart.")
                    STATE = "INITIALIZE"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    STAY=True
                    STATE = "INITIALIZE"
                    
        if STATE == "ASK":
            clicked_on_black=False
            clicked_on_green=False
            if click == True: #if event handler registered a mouseclick
                #check whether a black square was clicked on, if yes: clicked_on_black = True
                for i in range(len(__map__)):
                    #check whether a black square was clicked on, if yes: black = True
                        if (__map__[i][0]) + 100 > mouseX >= (__map__[i][0]) and (__map__[i][1]) + 100 > mouseY >= (__map__[i][1]):
                            clicked+=1
                            clicked_on_black = True
                        #check whether a green square was clocked on, if yes: clicked_on_green = True
                        for i in range(len(patternmap)):
                            if (__map__[patternmap[i]][0]) + 100 > mouseX >= (__map__[patternmap[i]][0]) and (__map__[patternmap[i]][1]) + 100 > mouseY >= (__map__[patternmap[i]][1]):
                                if clicked <= pattern_number:
                                    clicked_on_green = True
                                    break
                #If user clicked on a black square (where no green square appeared),
                #refister an incorrect input - , record reaction time, go to STATE feedback etc...
                if clicked_on_black and (not clicked_on_green):
                    time_react=time()
                    time_ref = time()
                    STATE = "FEEDBACK"
                    correctness = False
                    fail_list[current_trial_number] +=1
                    print (fail_list)
                    RT = (time_react - time_present)*1000
                    react_time_list[current_trial_number-1] = RT
                # if a black square was clicked where a green square appeared,
                #check if it was clicked at the right time(conform to oder of appearance)
                #if not, register an incorrect input
                elif clicked_on_black and clicked_on_green:
                    if (__map__[patternmap[correct]][0]) + 100 > mouseX >= (__map__[patternmap[correct]][0]) and (__map__[patternmap[correct]][1]) + 100 > mouseY >= (__map__[patternmap[correct]][1]):
                        correct+=1
                    else:
                        time_react=time()
                        time_ref = time()
                        STATE = "FEEDBACK"
                        correctness = False
                        fail_list[current_trial_number-1] +=1
                        print (fail_list)
                        RT = (time_react - time_present)*1000
                        react_time_list[current_trial_number-1] = RT
                #If made as many correct inputs as there were green squares,
                #register a correct trial
                if correct == pattern_number:
                    time_react=time()
                    time_ref = time()
                    STATE = "FEEDBACK"
                    correctness = True
                    current_trial_number += 1
                    pattern_number+=1
                    RT = (time_react - time_present)*1000
                    react_time_list[current_trial_number-1] = RT
                click=False
                clicked_on_black=False
                clicked_on_green=False
    
              
            
                
        # Automatic Transition Conditionals (ATC)   

        if STATE == "WELCOME":
            for i in range(len(fail_list)): # Maybe put in INITIALIZE!!!!!!!!!!!!!!!!!!!
                fail_list[i] = 0
        
        #STATE ready used to reset variables between trials
        if STATE == "READY":
            time_diff = time() - time_ref
            if time_diff >= time_between_trials:
             #   number_correct=0
               # x=0
                clicked=0
                click=False
                #no_correct=0
                time_ref=time()
                showed=False
                correctness=False
                black_clicked = False
                map_set = False
                pattern_set = False
                STATE = "SHOW" 
        #STATE feedback shows either "correct" or "incorrect" for a certain time period
        #and if the user failed 2 times on a pattern of the same length,
        #will then calculate scale score
        if STATE == "FEEDBACK":
            time_diff = time() - time_ref
            if time_diff >= show_feedback_time:
                if check_fail(fail_list) == True:
                    scale_score = calc_scale_score(pattern_number)
                    STATE = "SUMMARY"
                elif current_trial_number < max_trial_number:
                    time_ref = time()
                    STATE = "READY"
                else:
                    STATE = "SUMMARY"
        #STATE show lets a function calculate positions for black squares and for green squares of random lengths
        if STATE == "SHOW":
            if showed == True:         
                STATE = "ASK"
                time_present=time()
                correct = 0
                green = False
                time_ref = time()
                try:
                    pygame.mixer.music.play(0)
                    pygame.mixer.music.play(0)
                except:
                    pass
                pygame.event.clear() #Makes sure clicking during show STATE does not influence ask STATE
            else:
                if map_set == False:
                    __map__=create_block_map(screen_width,screen_height, corsi_block_number)
                    map_set = True
                if pattern_set == False: 
                    patternmap = list(range(pattern_number))
                    x_list = list(range(pattern_number))
                    for i in range(pattern_number):
                        x = random.randint(0,corsi_block_number-1)
                        if current_trial_number > 1:
                            if x_list[i-1] == x:
                                while x_list[i-1] == x:
                                    x = random.randint(0,corsi_block_number-1)
                            x_list[i] = x
                            patternmap[i] = x_list[i]
                            pattern_set = True 
                        else:
                            x_list[i] = x
                            patternmap[i] = x_list[i]
                            pattern_set = True 
                    
            # ACT Quit Event #Maybe Delete
            if STATE == "quit":
                pygame.quit()
                sys.exit()   

        # Drawing conditionals - call respective draw functions
        if STATE == "INITIALIZE":
            draw_initialize()
        if STATE == "WELCOME":
            draw_welcome()
        if STATE == "INTRO":
            draw_intro()
        if STATE == "READY":
            draw_ready()
        #calls respective draw function, resets variables, manages time
        #and plays a previously loaded sound after draw function was executed
        if STATE == "SHOW": 
            if map_set == True and pattern_set==True:
                draw_show(__map__, patternmap, pattern_number, time_between_trials)
                showed=True     
        if STATE == "ASK":
            draw_ask(__map__)
        if STATE == "FEEDBACK":
            draw_feedback(correctness, RT)
        if STATE == "GOODBYE":
            draw_goodbye()
        if STATE == "SUMMARY":
            draw_summary(pattern_number,scale_score, summary_text)
        if STATE == "RESTORE":
            draw_restore()
                
    # end screen refresh loop
        pygame.display.update()
        clock.tick(FPS)
        
        
        
        
# Draw functions and other functions

#Draw Functions - Mostly draw text on screen.
def draw_initialize():
    text_surface = font.render("LOADING", True, col_black, BACKGR_COL)
    text_rectangle = text_surface.get_rect()
    text_rectangle.center = (SCREEN_DIM[0]/2.0,150)
    screen.blit(text_surface, text_rectangle)
    text_surface = font_small.render("PLEASE WAIT", True, col_black, BACKGR_COL)
    text_rectangle = text_surface.get_rect()
    text_rectangle.center = (SCREEN_DIM[0]/2.0,300)
    screen.blit(text_surface, text_rectangle)
def draw_welcome():
    text_surface = font.render("Corsi Block Tapping Task", True, col_black, BACKGR_COL)
    text_rectangle = text_surface.get_rect()
    text_rectangle.center = (SCREEN_DIM[0]/2.0,150)
    screen.blit(text_surface, text_rectangle)
    text_surface = font_small.render("Press Any Key to Continue", True, col_black, BACKGR_COL)
    text_rectangle = text_surface.get_rect()
    text_rectangle.center = (SCREEN_DIM[0]/2.0,300)
    screen.blit(text_surface, text_rectangle)
def draw_intro():
    write_text(intro_text, 200, font_small)
    text_surface = font_small.render("Left Mouseclick to Continue", True, col_black, BACKGR_COL)
    text_rectangle = text_surface.get_rect()
    text_rectangle.center = (SCREEN_DIM[0]/2.0,500)
    screen.blit(text_surface, text_rectangle)
def draw_ready():
    text_surface = font.render("READY", True, col_black, BACKGR_COL)
    text_rectangle = text_surface.get_rect()
    text_rectangle.center = (screen_width/2, screen_height/2)
    screen.blit(text_surface, text_rectangle)
#Calls block_ini() function to create a desired amount of black squares at previously calculated positions
#Once created, the blocks are moves using the block_move() function.
#After black squares are drawn on the screen, green squares are created one by one using pattern_ini()
#and drawn to the screen specifically timed.
#Between drawing green squares, black squares are drawn again in oder to make sure only 1 green
#square is visible at any point.
def draw_show(__map__, patternmap, pattern_number, time_between_trials):
    global block_in
    global blocks
    if block_in == False:
        blocks = block_ini(screen, corsi_block_number, 100, 100, __map__, col_black)
        block_in = True
        
    else:
        block_move(blocks, __map__, screen)
    for i in range (len(patternmap)):
        pattern_ini(screen, 100, 100, __map__, col_green, patternmap, corsi_block_number,col_black, time_between_trials, i)
        pygame.display.update()
        time_r=time()
        while time()-time_r<1:
            pass
        block_move(blocks, __map__, screen)
        pygame.display.update()
        time_r=time()
        while time()-time_r<0.5:
            pass
#After all green squares have been drawn to the screen once, the black suqares will be drawn again to make
#sure no green square is visible anymore.
def draw_ask(__map__):
    block_ini(screen, corsi_block_number, 100, 100, __map__, col_black)
#draw_feedback() draws either a "Correct" or an "Incorrect" on the screen depending on the input
#Furthermore, the recorded reaction time will be drawn on the screen for correct trials
def draw_feedback(correctness, reaction_time):
    if correctness == True:
        text_surface = font.render("CORRECT", True, col_black, BACKGR_COL)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (screen_width/2, screen_height/2)
        screen.blit(text_surface, text_rectangle)
        text_surface = font_small.render(str(round((reaction_time/1000),2)) + "s", True, col_black, BACKGR_COL)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (SCREEN_DIM[0]/2.0,200)
        screen.blit(text_surface, text_rectangle)
    if correctness == False:
        text_surface = font.render("INCORRECT", True, col_black, BACKGR_COL)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (screen_width/2, screen_height/2)
        screen.blit(text_surface, text_rectangle)
def draw_goodbye():
    write_text(goodbye_text, 200, font_small)
    text_surface = font_small.render("S to Save", True, col_black, BACKGR_COL)
    text_rectangle = text_surface.get_rect()
    text_rectangle.center = (SCREEN_DIM[0]/2.0,300)
    screen.blit(text_surface, text_rectangle)
    text_surface = font_small.render("R to Restart (automatically saves)", True, col_black, BACKGR_COL)
    text_rectangle = text_surface.get_rect()
    text_rectangle.center = (SCREEN_DIM[0]/2.0,350)
    screen.blit(text_surface, text_rectangle)
    text_surface = font_small.render("ESC to Exit", True, col_black, BACKGR_COL)
    text_rectangle = text_surface.get_rect()
    text_rectangle.center = (SCREEN_DIM[0]/2.0,400)
    screen.blit(text_surface, text_rectangle)
def draw_summary(pattern_number, scale_score, summary_text):
    write_text(summary_text, 200, font_small, pattern_number, scale_score, formatting= True)
    text_surface = font_small.render("Left Mouseclick to Continue", True, col_black, BACKGR_COL)
    text_rectangle = text_surface.get_rect()
    text_rectangle.center = (SCREEN_DIM[0]/2.0,500)
    screen.blit(text_surface, text_rectangle)
def draw_restore():
    write_text(["Press 'P' to proceed with default settings.","Press 'C' to create default preset."+"Press ESC to exit."], 200, font_small)
    
# Functions

#Creted 4 files and writes text into them
def create_default():
    f1=open("Intro_Text.txt","w")
    f1.write("You will be presented with a number of black rectangles.\n")
    f1.write("Some of those rectangles will then light up green.\n")
    f1.write("Please try to press the black rectangles\n")
    f1.write("that lit up in the right order after an auditive\n")
    f1.write("signal has been presented.\n")
    f1.write("\n")
    f1.write("Please try to do this as fast as possible.")
    f1.close()
    f2=open("Goodbye_Text.txt","w")
    f2.write("Thank you for participating!\n")
    f2.write("Your data will be used for\n")
    f2.write("analysis purposes only")
    f2.close()
    f3=open("Summary_Text.txt","w")
    f3.write("Your highest pattern number was: {a}\n")
    f3.write("You have a Visuo-Spatial WMC of: {b}")
    f3.close()
    f4=open("Config.ini","w")
    f4.write("[general]\n")
    f4.write("time_between_trials: 0.3\n")
    f4.write("max_trial_number: 9\n")
    f4.write("show_feedback_time: 1\n")
    f4.write("corsi_block_number: 9\n")
    f4.write("introtext_filename: Intro_Text.txt\n")
    f4.write("summarytext_filename: Summary_Text.txt\n")
    f4.write("goodbyetext_filename: Goodbye_Text.txt\n")
    f4.close
#creates a message window
def make_errorbox(arg1,arg2):
    window = tki.Tk()
    window.wm_withdraw()
    tkMessageBox.showinfo(arg1,arg2)
#opens a textfile and saves every line as an entry of a list. Returns that list
def load_text(x):
    with open(x) as f:
        text = f.read().splitlines()
    return text
#loads in the config.ini file. Depending on the input a dictionary is used
#to decide what to return from the config.ini file.
def load_res(index):
    config.read('config.ini')
    
    resources = {0: "time_between_trials",
                 1: "max_trial_number",
                 2: "show_feedback_time",
                 3: "corsi_block_number",
                 4: "introtext_filename",
                 5: "summarytext_filename",
                 6: "goodbyetext_filename",
                 7: "first_start"}
    command="config._sections.general." + resources[index]
    return eval(command)
#can print texts, where every line is an enry in a list. Furthermore useing the parameter "formatting=True"
#it is also possible to input as many desired variables v1,v2,v3...vn when referred to in the text
# by {a},{b},{c}...{z}.
def write_text(text, start, sfont, *args, **kwargs):
    kwargs.setdefault("formatting", False)
    line_number = len(text)
    i=0
    if kwargs is not None:
        f = kwargs.get("formatting", None)
        if f == True:
            m=0
            command = "sfont.render(text[x].format("
            for ar in args:
                command+="{letter}={param},".format(letter=parlist_small[m],param=ar)
                m+=1
            command = command[:-1]
            command+="),True, col_black, BACKGR_COL)"
                
            for x in range (0, line_number):
                text_surface = eval(command)
                text_rectangle = text_surface.get_rect()
                text_rectangle.center = (SCREEN_DIM[0]/2.0,start+i)
                screen.blit(text_surface, text_rectangle)
                i+=35
        else:
            for x in range (0, line_number):
                text_surface = sfont.render(text[x], True, col_black, BACKGR_COL)
                text_rectangle = text_surface.get_rect()
                text_rectangle.center = (SCREEN_DIM[0]/2.0,start+i)
                screen.blit(text_surface, text_rectangle)
                i+=35
 #Creates a file of the type XLSX. Takes input and saves it into the file.  . When not possible, present an
#error dialogue box. 
def save_xlsx(reactimes, trial_number, avgreact, participant_no, std, scale_value):
    try:
        workbook = xlsxwriter.Workbook("Data.xlsx")
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({"bold": True})
        worksheet.set_column("A:A",20)
        worksheet.set_column("B:B",20)
        worksheet.write("B1", "Respondent ID", bold)
        worksheet.write("B3", "Reaction Time (ms)", bold)
        worksheet.write("A3", "Trial Number", bold)
        worksheet.write(parlist[participant_no]+str(2), participant_no)
        for x in range(0,trial_number):
            worksheet.write("A"+str(x+4), str(x+1))
            worksheet.write("A"+str(trial_number+5), "Mean Reaction Time", bold)
            worksheet.write("A"+str(trial_number+6), "Standard Deviation", bold)
            worksheet.write("A"+str(trial_number+7), "Visuo-Spatial WMC", bold)
            worksheet.write(parlist[participant_no]+str(x+4), (str(round(reactimes[x],2))))
            worksheet.write(parlist[participant_no]+str(trial_number+5), str(round(avgreact,2)))
            worksheet.write(parlist[participant_no]+str(trial_number+6), str(round(std,2)))
            worksheet.write(parlist[participant_no]+str(trial_number+7), str(round(scale_value,2)))
        workbook.close()
        print("saved!")
        make_errorbox("SAVING SUCCESSFUL", "Your data was successfully saved!")
    except Exception as ex:
        make_errorbox("SAVING FAILED", ("Saving Failed!\n"+"Check whether the data file is closed properly.\n"+"ERROR MSG:\n"+"{}".format(str(ex))))
        print(ex)
#Calculates a mean when given a list with numerical values    
def calc_avg_list(__list__):
    return np.mean(__list__)
#Calculates a standard deviation when given a list with numerical values 
def calc_std(__list__):
    return np.std(__list__, ddof=1)
#When given a list of CorsiBlock objects, and a list of positions, will change the position attributes of the
#objects accoding the position-list.
def block_move(blocks, position, screen):
    i=0
    for b in blocks:
        b.change_pos(position[i], screen)
        i+=1
#Creates a list of CosiBlock objects of the length n and draws them to the screen.
def block_ini(screen, n, xsize,ysize, __map__, color):
    block = [CorsiBlock((__map__[i]),(xsize,ysize), color)
            for i in range (n)]
    for d in block:
        d.__render__(screen)
    return block
#Calculates the Visuo-Spatial WMC as S-1, where S is the length of a pattern the
#user has failed at twice.
def calc_scale_score(pattern_number):
    return pattern_number-1
#When given a list of numerical values, checks whether there exists an
#entry>=2. Used to check whether a user has failed a a pattern with the same
#length twice
def check_fail(fail_list):
    fail_check = False
    for i in range(len(fail_list)):
        if fail_list[i] >= 2:
            fail_check = True
    return fail_check
#Creates one CorsiBlock object and draws it to the screen.
def pattern_ini(screen, xsize, ysize, __map__, color, pattern_map, block_number,block_color, time_between_trials,x):  
    pattern = CorsiBlock((__map__[pattern_map[x]]), (xsize,ysize), color)
    pattern.__render__(screen)
#Creates a list of two dimensional positional coordinate  radiuses. Selects random coordinates 
#in the screen dimensions. Saves these values with respect to diff radius coordinates in excluded.
#Random coordinate values that exist in forbidden will not be used.
#This way create_block_map() will create a list of two dimensional coordinates that are divided by a given radius.
def create_block_map(screen_width,screen_height, amount):
    dimX = (0, screen_width-100)
    dimY = (0, screen_height-100)
    rad = 150
    diff = set()
    forbidden = set()
    __map__ = []
    for x in range(-rad, rad+1):
        for y in range(-rad, rad+1):
            if x*x + y*y <= rad*rad:
                diff.add((x,y))

    i = 0
    while i<amount:
        x = random.randrange(*dimX)
        y = random.randrange(*dimY)
        if (x,y) in forbidden: continue
        __map__.append((x,y))
        i+=1
        forbidden.update((x+dx, y+dy) for (dx,dy) in diff)
    return __map__

# RUN Main Function
main()

