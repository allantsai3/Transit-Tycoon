import sys
from controller import Controller
from const import *
import start_screen
import end_screen
from pygame.locals import *
import random

from game_objects.train import Train
from game_objects.station import Station
from game_objects.track import Track

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(64)
pygame.mixer.music.load("ambient.mp3")
#pygame.mixer.music.play()

pygame.display.set_caption('Gondola Tycoon 2018')

MAINSURF = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
DISPLAY_WIDTH, DISPLAY_HEIGHT = MAINSURF.get_size()

with open("nouns.txt") as F:
    nouns = F.read().splitlines()

#Our main menu function now returns our map choice, fyi
map_choice = start_screen.draw_start_screen(MAINSURF)
bg = pygame.image.load(map_choice + ".png").convert()
bg = pygame.transform.scale(bg, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
Controller.initialize(MAINSURF)
if map_choice == "tokyo":
    station1 = Station((198, 162), MAINSURF, "Mount Keefer")
    Controller.entities.append(station1)

    station2 = Station((920, 540), MAINSURF, "The Spire")
    Controller.entities.append(station2)

    station3 = Station((161, 410), MAINSURF, "The Peaks")
    Controller.entities.append(station3)

    track1 = Track(station1, station2, [(550, 250)], MAINSURF)
    Controller.instance.entities.append(track1)
    station1.addTrack(track1)

    track2 = Track(station2, station3, [(500, 500)], MAINSURF)
    Controller.instance.entities.append(track2)
    station2.addTrack(track2)

    track3 = Track(station3, station1, [], MAINSURF)
    Controller.instance.entities.append(track3)
    station3.addTrack(track3)
    station3.addTrack(track3)

    track5 = Track(station1, station3, [], MAINSURF)
    Controller.instance.entities.append(track5)
    station1.addTrack(track5)

    train1 = Train(station1, MAINSURF)
    station1.receive(train1)
    Controller.instance.entities.append(train1)

    train2 = Train(station3, MAINSURF)
    station3.receive(train2)

    Controller.instance.entities.append(train2)

selected_stations = []

if map_choice == "london":
    station1 = Station((382, 363), MAINSURF, "Wery's Pass")
    Controller.instance.entities.append(station1)

    station2 = Station((783, 155), MAINSURF, "Johnny-Old Hill")
    Controller.instance.entities.append(station2)

    station3 = Station((1040, 572), MAINSURF, "Piddlty Wellington Summmit")
    Controller.instance.entities.append(station3)

    track1 = Track(station1, station2, [(420, 211)], MAINSURF)
    Controller.instance.entities.append(track1)
    station1.addTrack(track1)

    track2 = Track(station2, station3, [(911, 402)], MAINSURF)
    Controller.instance.entities.append(track2)
    station2.addTrack(track2)

    track3 = Track(station3, station1, [(660,623)], MAINSURF)
    Controller.instance.entities.append(track3)
    station3.addTrack(track3)
    station3.addTrack(track3)

    track5 = Track(station1, station3, [], MAINSURF)
    Controller.instance.entities.append(track5)
    station1.addTrack(track5)

    train1 = Train(station1, MAINSURF)
    station1.receive(train1)
    Controller.instance.entities.append(train1)

    train2 = Train(station3, MAINSURF)
    station3.receive(train2)

    Controller.instance.entities.append(train2)

    selected_stations = []

if map_choice == "free":
    selected_stations = []

tooltip = {"msg":"", "pos":(DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2), "time":200}
ttfont = pygame.font.SysFont(None, 20)
def draw_tooltip():
    if tooltip["time"] > 0:
        text_surf = ttfont.render(tooltip["msg"], True, RED)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_y -= 10
        MAINSURF.blit(text_surf, (mouse_x, mouse_y))
        tooltip["time"] -= 1


def create_station(pos):
    if Controller.instance.currentMoney >= COST_OF_MOUNTAIN:
        random_name = "Mount " + random.choice(nouns).capitalize()
        new_station = Station(pos, Controller.surface, random_name)
        # insert at the front of list to get drawn first/at the bottom
        Controller.entities.insert(0, new_station)
        Controller.instance.addMoney(-COST_OF_MOUNTAIN)
    # TODO move the death check to every tick....
    else:
        end_screen.draw_end_screen(MAINSURF)


def create_track(start, end, breakpoints):
    surface = Controller.surface
    new_track = Track(start, end, [], surface)
    Controller.entities.append(new_track)
    # add track to start station
    start.addTrack(new_track)
    
    # add return track TODO remove this feature
    new_track2 = Track(end, start, [], surface)
    Controller.entities.append(new_track2)
    # add track to end station
    end.addTrack(new_track2)


def create_train(station, controller):
    surface = Controller.surface
    
    # can only create train at a station with tracks
    if len(station.tracks) != 0:
        new_train = Train(station, surface)
        station.receive(new_train)
        controller.entities.append(new_train)
    else:
        # TODO upgrade tooltip to something more sophisticated
        tooltip["msg"] = "Mountain not connected!"
        tooltip["pos"] = (station.x, station.y - 15)
        tooltip["time"] = 50


def clear_selected_stations(select_list):
    # TODO make all game object selectable
    # TODO encapsulate selected behaviour there
    for station in select_list:
        station.color = BLUE
    del select_list[:]

while True:  # main game loop
    
    #MAINSURF.fill(WHITE)
    MAINSURF.blit(bg,(0, 0))
    draw_tooltip()
    Controller.tick()

    keys = pygame.key.get_pressed()
    
    
    if keys[K_ESCAPE]:
        pygame.quit()
        sys.exit()
        
    if keys[K_b]:
        if len(selected_stations)==1:
            if Controller.instance.currentMoney >= TRAIN_COST:
                Controller.instance.addMoney(-TRAIN_COST)
                create_train(selected_stations[0], Controller.instance)
                clear_selected_stations(selected_stations)
            else:
                station = selected_stations[0]
                tooltip["msg"] = "NOT ENOUGH MONEY!"
                tooltip["pos"] = (station.x, station.y-15)
                tooltip["time"] = 50

    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()
            
        # left click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                clicked_on_station = None
                for entity in Controller.entities:
                    if type(entity) == Station and entity.sprite.collidepoint(mouse_pos):
                        clicked_on_station = entity
                        selected_stations.append(clicked_on_station)
                if not clicked_on_station:
                    r, g, b, a = MAINSURF.get_at(mouse_pos)
                    if b >= 230:
                        tooltip["msg"] = "CANNOT BUILD IN THE AIR!"
                        tooltip["pos"] = mouse_pos
                        tooltip["time"] = 100
                    else:
                        create_station(mouse_pos)
                else:
                    clicked_on_station.color = YELLOW
                    if len(selected_stations) == 2:
                        create_track(selected_stations[0], selected_stations[1], [])
                        clear_selected_stations(selected_stations)
            elif event.button == 2:
                pass
            elif event.button == 3:
                clear_selected_stations(selected_stations)
    if Controller.instance.currentMoney <= BANKRUPT_AMOUNT:
                break
while True:
    end_screen.draw_end_screen(MAINSURF)