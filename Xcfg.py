#!/usr/bin/python3
import os
from sys import argv
import shutil

# if this value is 1024, it restarts
# if this value is None, it exits without error
# otherwise, it prints the value and exits with status 386
EXECERR = 1024

# standard configuration directory
cfgdir = os.path.expanduser("~")+"/Xres/"

# create the config folder and exit if it doesn't exist
if not os.path.isdir(cfgdir):
  os.mkdir(cfgdir)
  print("Created Xres folder.")
  print("Copy Xresources files into this directory to switch between them with Xcfg.")
  exit(0)

# get a list of all installed config files
cfg = os.listdir(cfgdir)

# if there are none, exit (configuring nothing is pointless)
if cfg == []:
  print("No Xresources files found within {0}.".format(cfgdir))
  exit(1)

# set up configs dict
configs = {}

# get a dict of all configs and their pretty names
for i in cfg: # for every file in ~/Xres
  try:
    with open(cfgdir+i) as config:   # open,
      contents = config.read()       # read,
      config.close()                 # close.
      lines = contents.split("\n")   # get first line.
      if lines[0][0] == "!":         # if it's a comment,
        configs[i] = lines[0][2:]    # get everything past "! ".
      else:                          # otherwise,
        configs[i] = i               # set pretty name to dirty name.
  except:
    print("FAILED to open {0}".format(i)) # bad bad bad bad

def Menu(window, options, selattr, nrmattr):
  # Display a menu.
  cursor = 0
  while True:
    # Y which the menu starts at.
    baseY = 7
    wsize = window.getmaxyx()
    eye = 0

    # Draw every option
    for i in options:
      attr = nrmattr

      # If the current option is the cursor, highlight it
      if eye == cursor:
        attr = selattr

      # Full-width string
      optionLabel = ("   "+options[i]).ljust(wsize[1]-2)

      # Draw option label and option name at x24
      window.addstr(baseY, 1, optionLabel, attr)
      window.addstr(baseY, 24, i, attr)

      # Increment for next entry.
      baseY += 1
      eye += 1

    # Handle input.
    window.refresh()
    key = window.getch()
    if key == curses.KEY_UP or key == 65:
      cursor -= 1
      if (cursor == -1):
        cursor = len(options) - 1
    elif key == curses.KEY_DOWN or key == 66:
      cursor += 1
      if cursor == len(options):
        cursor = 0
    elif key == curses.KEY_ENTER or key == ord('\n'):
      return cursor
    elif key == curses.KEY_BACKSPACE or key == 127:
      return -1
    elif key == curses.KEY_DC or key == 126:
      return -12

def Main(stdscr):
  global EXECERR # we need to be able to set it from within main

  # quit if terminal is too small
  if stdscr.getmaxyx()[1] < 48 or stdscr.getmaxyx()[0] < 24:
    EXECERR = "Your terminal is too small for Xcfg's TUI mode.\nInvoke Xcfg with --mini to invoke CLI mode."
    return

  # Default values for 'dumb' terminals.
  fx_selected = curses.A_REVERSE
  fx_normal = None
  fx_disabled = None

  # If we have colors, get some colors going.
  if curses.has_colors():
    # Default color values.
    blue = curses.COLOR_BLUE
    ylow = curses.COLOR_YELLOW
    gren = curses.COLOR_GREEN

    # If our terminal supports custom colors, change the default eye-searing
    # blue and yellow to a much nicer navy blue and cream yellow:
    if curses.can_change_color():
      curses.init_color(2, 25, 25, 200)
      curses.init_color(3, 900, 900, 750)
      curses.init_color(4, 500, 900, 500)
      blue = 2
      ylow = 3
      gren = 4

    # Set up color pairs.
    curses.init_pair(1, blue, ylow)
    curses.init_pair(2, ylow, blue)
    curses.init_pair(3, gren, blue)

    # Preset attribute values.
    fx_selected = curses.color_pair(1)
    fx_normal = curses.color_pair(2)
    fx_disabled = curses.color_pair(3)

  # stdscr must be refreshed before any windows can be, due to a bug
  stdscr.refresh()

  # Create main window.
  scrsize = stdscr.getmaxyx()
  MainWin = curses.newwin(scrsize[0]-2, scrsize[1]-2, 1, 1)

  # Pretty up main window
  MainWin.bkgdset(0, fx_normal)
  MainWin.clear()
  MainWin.border()
  MainWin.addstr(1,2,"X Configuration Manager")
  MainWin.addstr(3,4,"UP/DOWN = move cursor, ENTER = enable selected config")
  MainWin.addstr(4,4,"DEL = disable configs, BACKSPACE = cancel and exit Xcfg")

  # Menu stuff
  MainWin.addstr(6,4,"Pretty Name", fx_disabled)
  MainWin.addstr(6,24,"Filename", fx_disabled)
  MainWin.refresh()

  # Run menu subroutine.
  val = Menu(MainWin, configs, fx_selected, fx_normal)
  if (val == -1):
    EXECERR = "No changes to your X configuration have been made."
    return
  elif (val == -12):
    for i in configs:
      os.system("xrdb -remove \""+cfgdir+"/"+i+"\"")
      print("Disabled {0}".format(i))
    EXECERR = "Your X configuration has been temporarily disabled."
    return

  # Display selected X configuration.
  MainWin.clear()
  MainWin.border()
  MainWin.addstr(1,2,"X Configuration Manager")
  MainWin.addstr(3,4,"Configuration selected:")
  fname = list(configs)[val]
  pname = configs[fname]
  MainWin.addstr(4,6,pname)
  MainWin.addstr(6,4,"Is this OK? (y/n)")

  # Get yes or no
  malcolm = None
  while True:
    yn = MainWin.getch()
    if yn == ord('y') or yn == ord('Y'):
      break
    elif yn == ord('n') or yn == ord('N'):
      EXECERR = 1024
      return

  # attempt to back up Xdefaults
  try:
    shutil.copy(os.path.expanduser("~")+"/.Xdefaults", os.path.expanduser("~")+"/.Tmpdefaults")
  except:
    EXECERR = "You didn't have a previous configuration file, so it wasn't backed up."

  # attempt to copy new Xdefaults
  try:
    shutil.copy(cfgdir+"/"+fname, os.path.expanduser("~")+"/.Xdefaults")
    os.system("xrdb -load \""+cfgdir+"/"+fname+"\"")
  except:
    EXECERR = "Failed to copy and enable new Xdefaults."
    return

  EXECERR = None

# menu for mini mode
def MiniMenu(options):
  x = 1
  for i in options:
    print(str(x).rjust(4)+") "+i)  # example: "    1) Test"
    x += 1                         # i forgot this bit earlier
  while True:
    # attempt to parse input as int, if we fail, print ?
    try:
      choice = int(input("\n> "))
    except:
      print("?")
      continue

    # if choice is in bounds, return it
    if choice > 0 and choice <= len(options):
      return choice - 1
    else: # otherwise, yea you know what this does
      print("?")

if len(argv) == 2:
  if argv[1] == "--mini":
    print("Welcome to Xcfg!")
    options = [
      "Switch config",
      "Temporarily disable config",
      "Quit"
    ]
    opt = MiniMenu(options)
    if opt == 0:
      print("Please select an X configuration.")

      figs = []
      for i in configs:
        figs.append("{0} ({1})".format(configs[i], i))
      cfg = MiniMenu(figs)
      fname = list(configs)[cfg]
      pname = configs[fname]

      # attempt to back up previous config
      try:
        shutil.copy(os.path.expanduser("~")+"/.Xdefaults", os.path.expanduser("~")+"/.Tmpdefaults")
      except:
        print("You didn't have a previous configuration file, so it wasn't backed up.")

      # attempt to install new Xdefaults
      try:
        shutil.copy(cfgdir+"/"+fname, os.path.expanduser("~")+"/.Xdefaults")
        os.system("xrdb -load \""+cfgdir+"/"+fname+"\"")
      except:
        print("Failed to copy and enable new Xdefaults.")
        exit(1)

      # TADA.WAV
      print("Sucessfully installed new Xdefaults!")
    elif opt == 1:
      for i in configs:
        # xrdb disable each config, temporarily
        os.system("xrdb -remove \""+cfgdir+"/"+i+"\"")
        print("Disabled {0}".format(i))

    # errors will exit themselves, so it's safe to exit here
    exit(0)

# Start curses program
import curses
from curses import wrapper
while EXECERR == 1024:
  wrapper(Main)

# If we have an error, print it.
if EXECERR != None:
  print(EXECERR)
  exit(386)
else:
  # YIPPEE!!
  print("Configuration changes have been updated.")
  print("Restart your window manager for changes to take effect.")
  exit(0)
