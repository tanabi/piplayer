# PiPlayer

This is a tornado-based Python "webserver" that's really designed to be used as a back-end to a Raspberry Pi Music Player.  You can set up your Pi in "kiosk mode", and play music off it with this.  Its intended to be used with Adafruit's TFT screens.

I built this to use in my car :)

## How to Use It

This looks for music in /home/{Your user}/Music right now, and just loads any files that end in .mp3 out of that directory.  It then opens port 8080 and you can connect there to control the audio.

Click the arrows for next/previous, or click the song title for start/stop.

It doesn't, at present, ever reload the song list so you have to restart the service for it to do that.

## How to set it up

