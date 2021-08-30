#!/usr/bin/env python3


from src import DinoRush


if __name__ == "__main__":
    dinoRush = DinoRush()

    while True:
        dinoRush.handle_events()
        dinoRush.update()
        dinoRush.draw()
    # end while

# end if