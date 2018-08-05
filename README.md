# PiPlayer

This is a tornado-based Python "webserver" that's really designed to be used as a back-end to a Raspberry Pi Music Player.  You can set up your Pi in "kiosk mode", and play music off it with this.  Its intended to be used with Adafruit's TFT screens.

I built this to use in my car :)

## How to Use It

This looks for music in /home/{Your user}/Music right now, and just loads any files that end in .mp3 out of that directory.  It then opens port 8080 and you can connect there to control the audio.

Click the arrows for next/previous, or click the song title for start/stop.

It doesn't, at present, ever reload the song list so you have to restart the service for it to do that.

## How to set it up

I use an adafruit 2.8" touch screen and follow the instructions to set it up:

https://learn.adafruit.com/adafruit-pitft-28-inch-resistive-touchscreen-display-raspberry-pi?view=all#easy-install-2

I make sure 'mpg123' is installed and 'python3'.  Then I set it up in kiosk mode.  Note when you set up X, you need to use FRAMEBUFFER=/dev/fb1 to use the tiny screen instead of the HDMI port.

https://die-antwort.eu/techblog/2017-12-setup-raspberry-pi-for-kiosk-mode/

These are not very good instructions but I kind of don't care since I made this just for me :)  If anyone else wants to use this, I'm happy to guide you through it and document better, but otherwise its just a waste time.


