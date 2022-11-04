# Xcfg
Xcfg is a script written in Python 3 that allows you to quickly and easily switch
between Xdefault files with a nice TUI.

## it's all about the features
Xcfg can:
* replace .Xdefaults
* read pretty names from config files
* run in both TUI and CLI
* adapt to most environments, color-wise
* disable all Xdefaults files temporarily
* run in a TTY (so long as you restart X when you're done)

## usage
you'll want to run Xcfg once, to create the `Xres` folder in your home directory.
from here, you can copy a bunch of `.Xdefault` files, and add: `! [title here]` to
the top of each, obviously replacing brackets and 'title here' with what you'd like
to call your configuration. now, you can use Xcfg two ways:

### max mode
![scrot of max mode](https://github.com/videotoblinski/Xcfg/blob/readme-things/2022-11-04-135801_756x543_scrot.png?raw=true) 

this mode is the default, just run `Xcfg` to access it. use the arrow keys to move
the cursor around and press ENTER to apply a config. press BACKSPACE to quit with
no changes, or DEL to disable all configs temporarily.


### mini mode
![scrot of min mode](https://github.com/videotoblinski/Xcfg/blob/readme-things/2022-11-04-140632_756x543_scrot.png?raw=true)

this mode is invoked like so:
```
 Xcfg --mini
```
you use your number keys to get around mini mode, just press the number key
corresponding to the menu entry you'd like to select and then press enter to select
it. follow the on-screen instructions.

# bonus
here's a scrot of max mode running in xterm :)

![scrot of max mode, in xterm](https://github.com/videotoblinski/Xcfg/blob/readme-things/2022-11-04-140846_845x553_scrot.png?raw=true)
