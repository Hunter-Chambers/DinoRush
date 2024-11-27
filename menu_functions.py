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
timer_thread = None

def failed_message_timer(extra):
    extra[0][0] = False
# end failed_message_timer

def connect_to_server(extras):
    global timer_thread

    pygame.event.set_blocked(None)

    extras[2].fill(extras[3])
    extras[1].draw(extras[2])
    extras[2].blit(extras[0][1][1], extras[0][1][2])
    pygame.display.flip()

    oldTimeOut = extras[4].gettimeout()
    extras[4].settimeout(5)

    try:
        extras[4].sendto(str.encode('test'), (constants.SERVER, constants.PORT))
        extras[4].recvfrom(constants.BUFFER_SIZE)
    except socket.error:
        extras[0][0][0] = True

        if not (timer_thread is None) :
            timer_thread.cancel()
        # end if

        timer_thread = threading.Timer(3.0, failed_message_timer, args=(extras[0],))
        timer_thread.start()
    # end try/except

    extras[4].settimeout(oldTimeOut)

    pygame.event.clear()
    pygame.event.set_allowed(None)
# end connect_to_server

def quit_game(conn):
    global timer_thread

    if not (timer_thread is None):
        timer_thread.cancel()
    # end if

    conn.close()

    pygame.quit()
    sys.exit()
# end quit_game