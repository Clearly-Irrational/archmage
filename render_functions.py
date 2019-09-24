import tcod

#Draw all entities in the list
def render_all(source_con, dest_con, entities_list, screen_width, screen_height):
    #Draw all entities in the list
    for entity in entities_list:
        draw_entity(source_con, entity)

    #Overlay the source console onto the destination console
    source_con.blit(dest=dest_con, width=screen_width, height=screen_height)

#Clear all entities in the list
def clear_all(source_con, entities_list):
    for entity in entities_list:
        clear_entity(source_con, entity)

#Draw a single entity on the source console
def draw_entity(source_con, entity):
#    libtcod.console_set_default_foreground(con, entity.color)
    source_con.default_fg = (entity.color)
    #Draw this entity on the source console
    tcod.console_put_char(source_con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)

#Erase the entity so it won't smear on the next update
def clear_entity(source_con, entity):
    tcod.console_put_char(source_con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
