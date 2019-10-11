def third_eye(state, color_palette, indoors):
    if indoors == True:
        if state == 'open_eye':
            interface_skin = 'Graph'
            color_palette.set_color('light_wall', 50, 110, 160)
            color_palette.set_color('light_ground', 255, 255, 255)
            color_palette.set_color('dark_wall', 70, 130, 180)
            color_palette.set_color('dark_ground', 235, 235, 235)
    #        print("Opening third eye")
            return interface_skin
        elif state == 'close_eye':
            interface_skin = 'Tutorial'
            color_palette.set_color('light_wall', 130, 110, 50)
            color_palette.set_color('light_ground', 200, 180, 50)
            color_palette.set_color('dark_wall', 0, 0, 100)
            color_palette.set_color('dark_ground', 50, 50, 150)
    #        print("Closing third eye")
            return interface_skin
    else:
        if state == 'open_eye':
            interface_skin = 'Graph'
            color_palette.set_color('light_water', 195, 195, 195)
            color_palette.set_color('light_shallows', 205, 205, 205)
            color_palette.set_color('light_sand', 215, 215, 215)
            color_palette.set_color('light_plains', 225, 225, 225)
            color_palette.set_color('light_hills', 235, 235, 235)
            color_palette.set_color('light_mountain', 245, 245, 245)
            color_palette.set_color('light_snow', 255, 255, 255)
            color_palette.set_color('dark_water', 170, 170, 170)
            color_palette.set_color('dark_shallows', 180, 180, 180)
            color_palette.set_color('dark_sand', 190, 190, 190)
            color_palette.set_color('dark_plains', 200, 200, 200)
            color_palette.set_color('dark_hills', 210, 210, 210)
            color_palette.set_color('dark_mountain', 220, 220, 220)
            color_palette.set_color('dark_snow', 230, 230, 230)
            color_palette.set_color('tree_green', 185, 185, 185)
    #        print("Opening third eye")
            return interface_skin
        elif state == 'close_eye':
            interface_skin = 'Tutorial'
            color_palette.set_color('light_water', 0, 0, 255)
            color_palette.set_color('light_shallows', 100, 100, 255)
            color_palette.set_color('light_sand', 255, 232, 165)
            color_palette.set_color('light_plains', 0, 255, 0)
            color_palette.set_color('light_hills', 127, 101, 63)
            color_palette.set_color('light_mountain', 127, 127, 127)
            color_palette.set_color('light_snow', 255, 255, 255)
            color_palette.set_color('dark_water', 0, 0, 191)
            color_palette.set_color('dark_shallows', 63, 63, 255)
            color_palette.set_color('dark_sand', 255, 219, 114)
            color_palette.set_color('dark_plains', 0, 191, 0)
            color_palette.set_color('dark_hills', 94, 75, 47)
            color_palette.set_color('dark_mountain', 95, 95, 95)
            color_palette.set_color('dark_snow', 223, 223, 223)
            color_palette.set_color('tree_green', 0, 63, 0)
    #        print("Closing third eye")
            return interface_skin
