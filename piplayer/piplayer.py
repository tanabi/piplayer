#
# Main Source Code for PiPlayer - Basically it's all in here because
# this is a stupid simple application.
#

import getpass
import os
import random
import tornado.ioloop
import tornado.web

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

# What file is presently playing?
playlist_index = 0

# Do we have an mpg123 process?  If this is None, the player is stopped.
mpg_player = None


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

        # Did we get next / prev / play in the link?
        

        self.render("index.html", now_playing=playlist[playlist_index][:-4])


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


    # Start the web application
    app = tornado.web.Application([
            (r'/', MainHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static")
    )

    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
