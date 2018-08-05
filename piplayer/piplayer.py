#
# Main Source Code for PiPlayer - Basically it's all in here because
# this is a stupid simple application.
#

import getpass
import logging
import os
import random
import subprocess
import threading
import time
import tornado.ioloop
import tornado.web

from mutagen.mp3 import MP3

#####################################################################
#
# Configuration - in a perfect world, I'd make this load a file.
# In my lazy half-arsed world, it's going to be hard coded variables.
#
#####################################################################

# Where are our MP3's?
music_dir = "/home/%s/Music" % getpass.getuser()


#####################################################################
#
# Globals - Mostly system state items
#
#####################################################################

# Our play list - this will be loaded before the web service starts.
# This means if files are added, we have to restart the service.
playlist = []

# What file is presently displayed?
playlist_index = 0

# Do we have an mpg123 process?  If this is None, the player is stopped.
mpg_player = None

# This threading event is used to trigger when the player starts from
# a stopped state.
start_event = threading.Event()

# When did the song start?
song_started_at = 0

# How long is the song?
song_length = 0

#####################################################################
#
# Tornado Handlers
#
#####################################################################

class MainHandler(tornado.web.RequestHandler):
    """
    We'll just do this all in one class; there's simply not much
    to this, after all.
    """

    def get(self):
        """
        Render the default template, which will show the status
        of the system and provide buttons for control.

        You can have 'next', 'prev', and 'play' in the URL as query
        parameters.  Play toggles play vs. stop, next/previous do
        the obvious actions.
        """

        global playlist_index
        global mpg_player
        global start_event
        global playlist
        global song_started_at
        global song_length

        # Did we get next / prev / play in the link?
        if self.get_argument('next', None) is not None:
            # Do we need to kick mpg123?
            #
            # Doing this will cause the mpg123 thread to advance
            # to the next song automatically, so there is nothing
            # to do.
            if mpg_player is not None:
                mpg_player.kill()

                # Sleep for the briefest of moments to give
                # the player time to update.
                time.sleep(0.5)
            else:
                # Because mpg123 isn't running, we have to manually
                # advance the song.
                playlist_index += 1

                # Did we fall off the end?
                if playlist_index >= len(playlist):
                    playlist_index = 0

        elif self.get_argument('prev', None) is not None:
            # Do we need to kick mpg123?
            if mpg_player is not None:
                # We need to go back *two* steps since when we
                # kick the player, it will push us up one.
                playlist_index -= 2

                # Did we fall off the end?
                if playlist_index < -1:
                    playlist_index = (len(playlist) - 2)

                mpg_player.kill()

                # Sleep for the briefest of moments to give
                # the player time to update.
                time.sleep(0.5)
            else:
                # Otherwise, just go back one.
                playlist_index -= 1

                # Did we fall off the end?
                if playlist_index < 0:
                    playlist_index = (len(playlist) - 1)

        elif self.get_argument('play', None) is not None:
            # Toggle mpg123
            if mpg_player is None:
                # Start
                mpg_player = start_mpg_process()
                start_event.set()
            else:
                # Stop
                temp = mpg_player
                mpg_player = None
                temp.kill()

        # How much time is left with the song, if it's playing?
        song_remaining = 0

        if mpg_player is not None:
            # Calculate it in milliseconds for Javascript setTimeout
            song_remaining = int(((song_started_at + song_length) \
                             - time.time()) * 1000)

            if song_remaining < 0:
                song_remaining = 0

        self.render("index.html",
                    now_playing=playlist[playlist_index][:-4],
                    is_playing=(mpg_player is not None),
                    song_remaining=song_remaining
        )


#####################################################################
#
# mpg123 Management Thread
#
#####################################################################

def start_mpg_process():
    """
    This starts the mpg123 process and then returns the Popen object.
    """

    global playlist
    global playlist_index
    global song_length
    global song_started_at

    song_length = MP3(playlist[playlist_index]).info.length

    my_proc = subprocess.Popen(
                        [
                            'mpg123',
                            '-q',
                            playlist[playlist_index]
                        ],
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
    )

    song_started_at = time.time()
    return my_proc

def mpg_manager():
    """
    This method is designed to run as a python thread, and will manage
    the mpg123 process.
    """

    global mpg_player
    global playlist_index
    global playlist

    while True:
        if mpg_player is None:
            start_event.wait()
            start_event.clear() # Reset state
        else:
            mpg_player.wait()

            # Has it become none?
            if mpg_player is None:
                continue

            # Play the next song
            playlist_index += 1

            # Did we wrap around?
            if playlist_index >= len(playlist):
                playlist_index = 0

            mpg_player = start_mpg_process()


#####################################################################
#
# Main / Startup
#
#####################################################################

def main():
    """
    Initialize the playlist and then start our web application.
    """

    os.chdir(music_dir)

    for item in os.listdir(music_dir):
        # Only load files that end in MP3
        if item[-4:].lower() == ".mp3":
            playlist.append(item)

    # If playlist is empty ... we've got no songs.  I don't really want
    # to bother with this case too much right now.
    if len(playlist) == 0:
        playlist.append("No songs - Upload to %s and restart" % music_dir)
    else:
        # Randomize it
        random.shuffle(playlist)

    # Start the MPG manager thread
    t = threading.Thread(target=mpg_manager)
    t.start()

    # Start the web application
    app = tornado.web.Application([
            (r'/', MainHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static")
    )

    # Disable access log messages
    logging.getLogger('tornado.access').disabled = True

    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
