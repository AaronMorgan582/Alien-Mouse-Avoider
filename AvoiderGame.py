import sys, pygame, math

# Starter code for an avoider game. Written by David Johnson for COMP1010 University of Utah.

# Finished game authors:
#
# Aaron Morgan (u0393600)

# This function loads a series of sprite images stored in a folder with a
# consistent naming pattern: sprite_##. It returns a list of the images.
def load_piskell_sprite(sprite_folder_name, number_of_frames):
    frames = []
    # Figure out how many digits are in the frame number
    padding = math.ceil(math.log(number_of_frames,10))
    for frame in range(number_of_frames):
        folder_and_file_name = sprite_folder_name + "/sprite_" + str(frame).rjust(padding,'0') +".png"
        frames.append(pygame.image.load(folder_and_file_name).convert_alpha())

    return frames

# This function bounces a rectangle between the start and end pos. The bounce happens over num_frame frames.
# So the bigger the num_frame value is, the slower it goes (the bounce takes more frames).
# The rect is modified to be at the new position - a rect is not returned.
# Start and end pos are tuples of (x,y) coordinates on the window. You will likely need to experiment to find
# good coordinates.
def bounce_rect_between_two_positions( rect, start_pos, end_pos, num_frame, frame_count ):
    if frame_count%num_frame < num_frame/2:
        new_pos_x = start_pos[0] + (end_pos[0] - start_pos[0]) * (frame_count%(num_frame/2))/(num_frame/2)
        new_pos_y = start_pos[1] + (end_pos[1] - start_pos[1]) * (frame_count%(num_frame/2))/(num_frame/2)
    else:
        new_pos_x = end_pos[0] + (start_pos[0] - end_pos[0]) * (frame_count%(num_frame/2))/(num_frame/2)
        new_pos_y = end_pos[1] + (start_pos[1] - end_pos[1]) * (frame_count%(num_frame/2))/(num_frame/2)

    rect.center = (new_pos_x, new_pos_y)

def main():

    # Initialize pygame
    pygame.init()

    map = pygame.image.load("Alien Avoider Map 1.png")

    # Store window width and height in different forms for easy access
    map_size = map.get_size()
    map_rect = map.get_rect()

    # set the background color to something more pleasing than black
    background_color = 0, 0, 0

    # create the window
    screen = pygame.display.set_mode(map_size)

    map = map.convert()

    # Load the sprite frames from the folder
    player = load_piskell_sprite("Cursor",11)
    player_rect = player[0].get_rect()

    # The frame tells which sprite frame to draw
    frame_count = 0;

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Get a font - there is some problem on my Mac that makes this pause for 10s of seconds sometimes.
    # I will see if I can find a fix.
    myfont = pygame.font.SysFont('Cambria', 24)


    # Hide the arrow cursor and replace it with a sprite. Don't make this big or the checking for collisions
    # gets more complicated than just looking at the color under the cursor tip.
    pygame.mouse.set_visible(False)

    started = False
    Transition = False
    next_level = False
    finished = False
    Jonesy = False

    Jones_finish = False
    Jones_finish_two = False
    end_screen = False
    end_screen_two = False

    is_alive = True

    while is_alive:

        screen.blit(map, map_rect)

        bad_guy = load_piskell_sprite("Alien", 13)
        bad_guy_rect = bad_guy[0].get_rect()

        fire = load_piskell_sprite("Fire", 6)
        fire_2 = load_piskell_sprite("Fire", 6)
        fire_3 = load_piskell_sprite("Fire", 6)

        larger_fire = pygame.transform.scale2x(fire[frame_count%len(fire)])
        larger_fire_rotated = pygame.transform.rotate(larger_fire, 45)

        fire_rect = fire[4].get_rect()
        fire_2_rect = fire[4].get_rect()
        fire_3_rect = fire[4].get_rect()
        larger_fire_rect = fire[4].get_rect()

        fire_rect.center = (349, 363)
        fire_2_rect.center = (427, 427)
        fire_3_rect.center = (500, 427)
        larger_fire_rect.center = (221, 322)

        fire_rotated = pygame.transform.rotate(fire[frame_count%len(fire)], -45)

        screen.blit(fire_rotated, fire_rect)
        screen.blit(fire_2[frame_count%len(fire)], fire_2_rect)
        screen.blit(fire_3[frame_count%len(fire)], fire_3_rect)
        screen.blit(larger_fire_rotated, larger_fire_rect)

        bounce_rect_between_two_positions(bad_guy_rect, (478,89), (293, 98), 200, frame_count)
        screen.blit(bad_guy[frame_count%len(bad_guy)], bad_guy_rect)

        pos = pygame.mouse.get_pos()
        color_at_cursor = screen.get_at(pos)

        player_rect.center = pygame.mouse.get_pos()
        screen.blit(player[(frame_count//10)%len(player)], player_rect)

        label = myfont.render("Time:", True, (255,255,0))
        screen.blit(label, (20,550))
        time_elapsed = myfont.render(str(round(pygame.time.get_ticks()/1000)), True, (255, 255,0))
        screen.blit(time_elapsed, (100, 550))

        frame_count += 1
        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False
            if event.type == pygame.MOUSEBUTTONDOWN and color_at_cursor == (14, 209, 69, 255):
                started = True
            if started == True:
                if color_at_cursor == (150, 150, 150, 255) or color_at_cursor == (19, 13, 13, 255) or color_at_cursor == (235, 52, 37, 255):
                    is_alive = False
                    finished = True
                if color_at_cursor == (236, 28, 36, 255):
                    is_alive = False
                    Transition = True

    while Transition:

        transition_level = pygame.image.load("Transition.png")
        transition_size = transition_level.get_size()
        transition_rect = transition_level.get_rect()

        transition_screen = pygame.display.set_mode(transition_size)
        transition_level = transition_level.convert()

        transition_screen.blit(transition_level,transition_rect)

        pygame.display.update()
        pygame.time.delay(4000)

        Transition = False
        next_level = True
        pygame.mouse.set_pos([609, 91])

    while next_level:

        level_two = pygame.image.load("Alien Avoider Map 2.png")
        two_size = level_two.get_size()
        two_rect = level_two.get_rect()

        two_screen = pygame.display.set_mode(two_size)
        level_two = level_two.convert()

        two_screen.blit(level_two, two_rect)

        the_cat = load_piskell_sprite("Jones", 9)
        the_cat_rect = the_cat[0].get_rect()
        the_cat_rect.center = (108, 298)
        screen.blit(the_cat[frame_count%len(the_cat)], the_cat_rect)

        fire = load_piskell_sprite("Fire", 6)
        fire_2 = load_piskell_sprite("Fire", 6)
        fire_3 = load_piskell_sprite("Fire", 6)

        larger_fire = pygame.transform.scale2x(fire[frame_count%len(fire)])
        larger_fire_rotated = pygame.transform.rotate(larger_fire, 45)

        fire_rect = fire[4].get_rect()
        fire_2_rect = fire[4].get_rect()
        fire_3_rect = fire[4].get_rect()
        larger_fire_rect = fire[4].get_rect()

        fire_rect.center = (354, 323)
        fire_2_rect.center = (174, 260)
        fire_3_rect.center = (500, 334)
        larger_fire_rect.center = (155, 65)

        fire_rotated = pygame.transform.rotate(fire[frame_count%len(fire)], 180)
        fire_2_rotated = pygame.transform.rotate(fire_2[frame_count%len(fire_2)], -90)

        screen.blit(fire_rotated, fire_rect)
        screen.blit(fire_2_rotated, fire_2_rect)
        screen.blit(fire_3[frame_count%len(fire)], fire_3_rect)
        screen.blit(larger_fire_rotated, larger_fire_rect)

        bad_guy = load_piskell_sprite("Alien", 13)
        bad_guy_rect = bad_guy[0].get_rect()
        bad_guy_flipped = pygame.transform.flip(bad_guy[frame_count%len(bad_guy)], True, False)

        bounce_rect_between_two_positions(bad_guy_rect, (338,81), (338, 306), 200, frame_count)
        screen.blit(bad_guy_flipped, bad_guy_rect)

        pos = pygame.mouse.get_pos()
        color_at_cursor = screen.get_at(pos)

        player_rect.center = pygame.mouse.get_pos()
        screen.blit(player[(frame_count//10)%len(player)], player_rect)

        label = myfont.render("Time:", True, (255,255,0))
        screen.blit(label, (20,550))
        time_elapsed = myfont.render(str(round(pygame.time.get_ticks()/1000)), True, (255, 255,0))
        screen.blit(time_elapsed, (100, 550))

        frame_count += 1
        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and color_at_cursor == (14, 209, 69, 255):
                started = True

            if started == True:
                if color_at_cursor == (150, 150, 150, 255) or color_at_cursor == (19, 13, 13, 255) or color_at_cursor == (235, 52, 37, 255):
                    next_level = False
                    finished = True
                if color_at_cursor == (88, 63, 41, 255) or color_at_cursor == (19, 12, 6, 255):
                    Jonesy = True
                    next_level = False
                if color_at_cursor == (236, 28, 36, 255):
                    next_level = False
                    end_screen = True

    while Jonesy:

        started = True
        level_two = pygame.image.load("Alien Avoider Map 2.png")
        two_size = level_two.get_size()
        two_rect = level_two.get_rect()

        two_screen = pygame.display.set_mode(two_size)
        level_two = level_two.convert()

        two_screen.blit(level_two, two_rect)

        fire = load_piskell_sprite("Fire", 6)
        fire_2 = load_piskell_sprite("Fire", 6)
        fire_3 = load_piskell_sprite("Fire", 6)

        larger_fire = pygame.transform.scale2x(fire[frame_count%len(fire)])
        larger_fire_rotated = pygame.transform.rotate(larger_fire, 45)

        fire_rect = fire[4].get_rect()
        fire_2_rect = fire[4].get_rect()
        fire_3_rect = fire[4].get_rect()
        larger_fire_rect = fire[4].get_rect()

        fire_rect.center = (354, 323)
        fire_2_rect.center = (174, 260)
        fire_3_rect.center = (500, 334)
        larger_fire_rect.center = (155, 65)

        fire_rotated = pygame.transform.rotate(fire[frame_count%len(fire)], 180)
        fire_2_rotated = pygame.transform.rotate(fire_2[frame_count%len(fire_2)], -90)

        screen.blit(fire_rotated, fire_rect)
        screen.blit(fire_2_rotated, fire_2_rect)
        screen.blit(fire_3[frame_count%len(fire)], fire_3_rect)
        screen.blit(larger_fire_rotated, larger_fire_rect)

        bad_guy = load_piskell_sprite("Alien", 13)
        bad_guy_rect = bad_guy[0].get_rect()
        bad_guy_flipped = pygame.transform.flip(bad_guy[frame_count%len(bad_guy)], True, False)

        bounce_rect_between_two_positions(bad_guy_rect, (338,81), (338, 306), 200, frame_count)
        screen.blit(bad_guy_flipped, bad_guy_rect)

        pos = pygame.mouse.get_pos()
        color_at_cursor = screen.get_at(pos)

        player_rect.center = pygame.mouse.get_pos()
        screen.blit(player[(frame_count//10)%len(player)], player_rect)

        label = myfont.render("Time:", True, (255,255,0))
        screen.blit(label, (20,550))
        time_elapsed = myfont.render(str(round(pygame.time.get_ticks()/1000)), True, (255, 255,0))
        screen.blit(time_elapsed, (100, 550))

        frame_count += 1
        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if started == True:
                if color_at_cursor == (150, 150, 150, 255) or color_at_cursor == (19, 13, 13, 255) or color_at_cursor == (235, 52, 37, 255):
                    Jonesy = False
                    finished = True
                if color_at_cursor == (236, 28, 36, 255):
                    Jonesy = False
                    Jones_finish = True

    while Jones_finish:
        Jones_end = pygame.image.load("End Screen (best).png")
        Jones_size = Jones_end.get_size()
        Jones_rect = Jones_end.get_rect()

        Jones_end_screen = pygame.display.set_mode(Jones_size)
        Jones_end = Jones_end.convert()

        Jones_end_screen.blit(Jones_end,Jones_rect)

        pygame.display.update()
        pygame.time.delay(6000)

        Jones_finish = False
        Jones_finish_two = True

    while Jones_finish_two:

        Jones_end_two = pygame.image.load("End Screen (best) part 2.png")
        Jones_two_size = Jones_end_two.get_size()
        Jones_two_rect = Jones_end_two.get_rect()

        Jones_two_screen = pygame.display.set_mode(Jones_two_size)
        Jones_end_two = Jones_end_two.convert()

        Jones_two_screen.blit(Jones_end_two, Jones_two_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    while end_screen:
        end = pygame.image.load("End Screen.png")
        end_size = end.get_size()
        end_rect = end.get_rect()

        end_display = pygame.display.set_mode(end_size)
        end = end.convert()

        end_display.blit(end, end_rect)
        pygame.display.update()
        pygame.time.delay(6000)

        end_screen = False
        end_screen_two = True

    while end_screen_two:
        end_two = pygame.image.load("End Screen part 2.png")
        end_two_size = end_two.get_size()
        end_two_rect = end_two.get_rect()

        end_two_display = pygame.display.set_mode(end_two_size)
        end_two = end_two.convert()

        end_two_display.blit(end_two, end_two_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    while finished:
        game_over = pygame.image.load("GameOver.png")
        over_size = game_over.get_size()
        over_rect = game_over.get_rect()

        over_screen = pygame.display.set_mode(over_size)
        game_over = game_over.convert()

        over_screen.blit(game_over, over_rect)


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


    pygame.quit()
    sys.exit()

# Start the program
main()
