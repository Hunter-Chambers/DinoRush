import pygame
import sys

import socket
import threading

from src import constants


##################################################################
### HELPER FUNCTIONS
##################################################################
def empty_function():
    pass
# end empty_funciton


##################################################################
### MAIN MENU
##################################################################
def failed_message_timer(extra):
    extra[0][0] = False
# end failed_message_timer

timer_thread = None
def connect_to_server(extras):
    global timer_thread

    pygame.event.set_blocked(None)

    extras[2].fill(extras[3])
    extras[1].draw(extras[2])
    extras[2].blit(extras[0][1][1], extras[0][1][2])
    pygame.display.flip()

    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conn.settimeout(5)

    try:
        conn.sendto(str.encode('test'), (constants.SERVER, constants.PORT))
        conn.recvfrom(constants.BUFFER_SIZE)
    except socket.error:
        conn.close()
        extras[0][0][0] = True

        if not (timer_thread is None) :
            timer_thread.cancel()
        # end if

        timer_thread = threading.Timer(3.0, failed_message_timer, args=(extras[0],))
        timer_thread.start()
    # end try/except

    pygame.event.clear()
    pygame.event.set_allowed(None)
# end connect_to_server

def quit_game():
    pygame.quit()
    sys.exit()
# end quit_game