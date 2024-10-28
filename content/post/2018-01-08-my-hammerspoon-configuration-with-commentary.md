+++
title = "My Hammerspoon Configuration, With Commentary"
author = ["Diego Zamboni"]
summary = "In my ongoing series of literate config files, I present to you my Hammerspoon configuration file."
date = 2018-01-08T13:31:00+01:00
tags = ["config", "howto", "literateprogramming", "literateconfig", "hammerspoon"]
draft = false
creator = "Emacs 28.2 (Org mode 9.7.11 + ox-hugo)"
toc = true
featured_image = "/images/hammerspoon.jpg"
+++

{{< leanpubbook book="lit-config" style="float:right" >}}

{{< leanpubbook book="learning-hammerspoon" style="float:right" >}}

Last update: **October 28, 2024**

In my [ongoing](../my-elvish-configuration-with-commentary/) [series](../my-emacs-configuration-with-commentary) of [literate](http://www.howardism.org/Technical/Emacs/literate-programming-tutorial.html) config files, I present to you my [Hammerspoon](http://www.hammerspoon.org/) configuration file. You can see the generated file at <https://github.com/zzamboni/dot-hammerspoon/blob/master/init.lua>. As usual, this is just a snapshot at the time shown above, you can see the current version of my configuration [in GitHub](https://github.com/zzamboni/dot-hammerspoon/blob/master/init.org).

If you are interested in writing your own Literate Config files, check out my new book [Literate Config](https://leanpub.com/lit-config) on Leanpub!

If you want to learn more about Hammerspoon, check out my book [Learning Hammerspoon](https://leanpub.com/learning-hammerspoon)!


## General variables and configuration {#general-variables-and-configuration}

Global log level. Per-spoon log level can be configured in each `Install:andUse` block below.

```lua
hs.logger.defaultLogLevel="info"
```

I use `hyper`, `shift_hyper` and `ctrl_cmd` as the modifiers for most of my key bindings, so I define them as variables here for easier use.

```lua
hyper       = {"cmd","alt","ctrl"}
shift_hyper = {"cmd","alt","ctrl","shift"}
ctrl_cmd    = {"cmd","ctrl"}
```

Set up an abbreviation for `hs.drawing.color.x11` since I use it repeatedly later on.

```lua
col = hs.drawing.color.x11
```

Work's logo, which I use in some of my Seal shortcuts later on.

```lua
work_logo = hs.image.imageFromPath(hs.configdir .. "/files/work_logo_2x.png")
```


## Spoon Management {#spoon-management}

Set up SpoonInstall - this is the only spoon that needs to be manually installed (it is already there if you check out this repository), all the others are installed and configured automatically.

```lua
hs.loadSpoon("SpoonInstall")
```

Configuration of my personal spoon repository, which contains Spoons that have not been merged in the main repo.  See the descriptions at <https://zzamboni.github.io/zzSpoons/>.

```lua
spoon.SpoonInstall.repos.zzspoons = {
  url = "https://github.com/zzamboni/zzSpoons",
  desc = "zzamboni's spoon repository",
}
```

I prefer sync notifications, makes them easier to read.

```lua
spoon.SpoonInstall.use_syncinstall = true
```

This is just a shortcut to make the declarations below look more readable, i.e. `Install:andUse` instead of `spoon.SpoonInstall:andUse`.

```lua
Install=spoon.SpoonInstall
```


## BetterTouchTool integration (experimental) {#bettertouchtool-integration--experimental}

I'm currently working on a new [BetterTouchTool.spoon](https://github.com/zzamboni/Spoons/tree/spoon/BetterTouchTool/Source/BetterTouchTool.spoon) which provides integration with the [BetterTouchTool AppleScript API](https://docs.bettertouchtool.net/docs/apple_script.html). This is in heavy development! See the configuration for the Hammer spoon in [System and UI](#system-and-ui) for an example of how to use it.

```lua
-- Install:andUse("BetterTouchTool", { loglevel = 'debug' })
-- BTT = spoon.BetterTouchTool
```


## URL dispatching to site-specific browsers {#url-dispatching-to-site-specific-browsers}

The [URLDispatcher](http://www.hammerspoon.org/Spoons/URLDispatcher.html) spoon makes it possible to open URLs with different browsers. Currently I use the following:

-   Different Chrome profiles for various work-related purposes (e.g. one profile for each of my customers, another one for internal sites), which allows me to keep site-specific bookmarks, search settings, etc.;
-   Brave for non-work browsing. I also use the `url_redir_decoders` parameter to rewrite some URLs before they are opened, both to redirect certain URLs directly to their corresponding applications (instead of going through the web browser) and to fix a bug I have experienced in opening URLs from PDF documents using Preview.

The `URLDispatcher` spoon requires application IDs, so I define a function which gets the path of the application and returns its ID.

```lua
-- Returns the bundle ID of an application, given its path.
function appID(app)
  if hs.application.infoForBundlePath(app) then
    return hs.application.infoForBundlePath(app)['CFBundleIdentifier']
  end
end
```

The `chromeProfile` function returns a function which opens a URL with the given Chrome Profile, and which can be used directly as the value in the `url_patterns` parameter below.

```lua
-- Returns a function that takes a URL and opens it in the given Chrome profile
-- Note: the value of `profile` must be the name of the profile directory under
-- ~/Library/Application Support/Google/Chrome/
function chromeProfile(profile)
  return function(url)
    hs.task.new("/usr/bin/open", nil, { "-n",
                                        "-a", "Google Chrome",
                                        "--args",
                                        "--profile-directory="..profile,
                                        url }):start()
  end
end
```

First I define variables containing the application IDs of the various applications that might be used to open URLs (not all of these are currently used, but I leave them here for convenience).

```lua
-- Define the IDs of the various applications used to open URLs
chromeBrowser  = appID('/Applications/Google Chrome.app')
braveBrowser   = appID('/Applications/Brave Browser.app')
safariBrowser  = appID('/Applications/Safari.app')
firefoxBrowser = appID('/Applications/Firefox.app')
arcBrowser     = appID('/Applications/Arc.app')
teamsApp       = appID('/Applications/Microsoft Teams.app')
quipApp        = appID('/Applications/Quip.app')
chimeApp       = appID('/Applications/Amazon Chime.app')
```

The `browsers` array stores the browsers used for different sets of URLs. I store them here mostly for readability and convenience, I can then refer to things like `browsers.work` in the configuration below.

```lua
-- Define my default browsers for various purposes
browsers = {
  default    = arcBrowser,
  awsConsole = firefoxBrowser,
  work       = chromeProfile("Default"),
  customer1  = chromeProfile("Profile 1")
}
```

Similarly, I store in an array the paths (relative to `~/.hammerspoon`) of the files in which I store the lists of URLs to be opened by different browsers. This avoids having to include (potentially private or sensitive) URLs in my public configuration file. Since URLDispatcher automatically reloads the files when they are updated, this also makes it possible to update the lists without restarting Hammerspoon every time.

```lua
-- Read URL patterns from text files
URLfiles = {
  work      = "local/work_urls.txt",
  customer1 = "local/customer1_urls.txt"
}
```

Finally, I load and configure URLDispatcher.

```lua
Install:andUse("URLDispatcher",
               {
                 config = {
                   default_handler = browsers.default,
                   url_patterns = {
                     -- URLs that get redirected to applications
                     { "https://quip%-amazon%.com/"      , quipApp },
                     { "https://teams%.microsoft%.com/"  , teamsApp },
                     { "chime://"                        , chimeApp },
                     -- Customer-specific URLs open in their own Chrome profile
                     { URLfiles.customer1                , browsers.customer1 },
                     -- AWS console URLs open by default in Firefox because it
                     -- has better plugins to improve the experience. This comes
                     -- after customer1 URLs because I have patterns for that
                     -- customer's accounts to open in its corresponding
                     -- profile.
                     { ".*%.console%.aws%.amazon%.com/.*", browsers.awsConsole },
                     -- Work-related URLs open in the default Chrome profile
                     { URLfiles.work                     , browsers.work },
                   },
                   url_redir_decoders = {
                     -- URLs opened from within MS Teams are normally sent
                     -- through a redirect which messes the matching, so we
                     -- extract the final URL before dispatching it. The final
                     -- URL is passed as parameter "url" to the redirect URL,
                     -- which makes it easy to extract it using a function-based
                     -- decoder.
                     { "MS Teams links", function(_, _, params) return params.url end, nil, true, "Microsoft Teams" },
                     -- URLs within a tracking link
                     { "awstrack.me links", "https://.*%.awstrack%.me/.-/(.*)", "%1" },
                     -- Chime meeting URLs get rewritten to open in the Chime app
                     { "Chime meeting links", "https://chime%.aws/(%d+)", "chime://meeting?pin=%1" }
                   }
                 },
                 start = true,
                 loglevel = 'debug'
               }
)
```


## Window and screen manipulation {#window-and-screen-manipulation}

The [WindowHalfsAndThirds](http://www.hammerspoon.org/Spoons/WindowHalfsAndThirds.html) spoon sets up multiple key bindings for manipulating the size and position of windows. This was one of the first spoons I wrote, and I still use it for window resizing.

```lua
Install:andUse("WindowHalfsAndThirds",
               {
                 config = {
                   use_frame_correctness = true
                 },
                 hotkeys = 'default',
--                 loglevel = 'debug'
               }
)
```

The [WindowGrid](http://www.hammerspoon.org/Spoons/WindowGrid.html) spoon sets up a key binding (`Hyper-g` here) to overlay a grid that allows resizing windows by specifying their opposite corners.

```lua
myGrid = { w = 6, h = 4 }
Install:andUse("WindowGrid",
               {
                 config = { gridGeometries =
                              { { myGrid.w .."x" .. myGrid.h } } },
                 hotkeys = {show_grid = {hyper, "g"}},
                 start = true
               }
)
```

The [WindowScreenLeftAndRight](http://www.hammerspoon.org/Spoons/WindowScreenLeftAndRight.html) spoon sets up key bindings for moving windows between multiple screens.

```lua
Install:andUse("WindowScreenLeftAndRight",
               {
                 config = {
                   animationDuration = 0
                 },
                 hotkeys = 'default',
--                 loglevel = 'debug'
               }
)
```

The [ToggleScreenRotation](http://www.hammerspoon.org/Spoons/ToggleScreenRotation.html) spoon sets up a key binding to rotate the external screen (the spoon can set up keys for multiple screens if needed, but by default it rotates the first external screen).

```lua
Install:andUse("ToggleScreenRotation",
               {
                 hotkeys = { first = {hyper, "f15"} }
               }
)
```


## Organization and Productivity {#organization-and-productivity}


### Universal Archiving {#universal-archiving}

The [UniversalArchive](http://www.hammerspoon.org/Spoons/UniversalArchive.html) spoon sets up a single key binding (`Ctrl-Cmd-a`) to archive the current item in Evernote, Mail and Outlook.

```lua
Install:andUse("UniversalArchive",
               {
                 config = {
                   evernote_archive_notebook = ".Archive",
                   archive_notifications = false,
                   outlook_archive_folder = "Archive (myemail@work.com)"
                 },
                 hotkeys = { archive = { { "ctrl", "cmd" }, "a" } }
               }
)
```


### Filing to Omnifocus {#filing-to-omnifocus}

**Note:** I no longer use OmniFocus so the Spoon below is diabled, but this section is still here as an example.

The [SendToOmniFocus](http://www.hammerspoon.org/Spoons/SendToOmniFocus.html) spoon sets up a single key binding (`Hyper-t`) to send the current item to OmniFocus from multiple applications. We use the `fn` attribute of `Install:andUse` to call a function which registers some of the Epichrome site-specific-browsers I use, so that the Spoon knows how to collect items from them.

```lua
function chrome_item(n)
  return { apptype = "chromeapp", itemname = n }
end
```

```lua
function OF_register_additional_apps(s)
  s:registerApplication("Collab", chrome_item("tab"))
  s:registerApplication("Wiki", chrome_item("wiki page"))
  s:registerApplication("Jira", chrome_item("issue"))
  s:registerApplication("Brave Browser Dev", chrome_item("page"))
end
```

```lua
Install:andUse("SendToOmniFocus",
               {
                 disable = true,
                 config = {
                   quickentrydialog = false,
                   notifications = false
                 },
                 hotkeys = {
                   send_to_omnifocus = { hyper, "t" }
                 },
                 fn = OF_register_additional_apps,
               }
)
```


### Capturing to Org mode {#capturing-to-org-mode}

I now use Org-mode for task tracking and capturing. The following snippet runs the `~/.emacs.d/bin/org-capture` script to bring up an Emacs window which allows me to capture things from anywhere in the system. The code is a bit convoluted because it needs to capture the current window and restore it after the org-capture window closes, otherwise Emacs is brought to the front.

```lua
org_capture_path = os.getenv("HOME").."/.hammerspoon/files/org-capture.lua"
script_file = io.open(org_capture_path, "w")
script_file:write([[local win = hs.window.frontmostWindow()
local o,s,t,r = hs.execute("~/.emacs.d/bin/org-capture", true)
if not s then
  print("Error when running org-capture: "..o.."\n")
end
win:focus()
]])
script_file:close()

hs.hotkey.bindSpec({hyper, "t"},
  function ()
    hs.task.new("/bin/bash", nil, { "-l", "-c", "/usr/local/bin/hs "..org_capture_path }):start()
  end
)
```


### Evernote filing and tagging {#evernote-filing-and-tagging}

The [EvernoteOpenAndTag](http://www.hammerspoon.org/Spoons/EvernoteOpenAndTag.html) spoon sets up some missing key bindings for note manipulation in Evernote. I no longer use Evernote for GTD, so I have it disabled for now.

```lua
Install:andUse("EvernoteOpenAndTag",
               {
                 disable = true,
                 hotkeys = {
                   open_note = { hyper, "o" },
                   ["open_and_tag-+work"] = { hyper, "w" },
                   ["open_and_tag-+personal"] = { hyper, "p" },
                   ["tag-@zzdone"] = { hyper, "z" }
                 }
               }
)
```


### Clipboard history {#clipboard-history}

The [TextClipboardHistory](http://www.hammerspoon.org/Spoons/TextClipboardHistory.html) spoon implements a clipboard history, only for text items. It is invoked with `Cmd-Shift-v`.

**Note:** This is disabled for the moment as I experiment with BetterTouchTool's built-in clipboard history, which I have bound to the same key combination for consistency in my workflow.

```lua
Install:andUse("TextClipboardHistory",
               {
                 disable = true,
                 config = {
                   show_in_menubar = false,
                 },
                 hotkeys = {
                   toggle_clipboard = { { "cmd", "shift" }, "v" } },
                 start = true,
               }
)
```


## System and UI {#system-and-ui}


### General Hammerspoon utilities {#general-hammerspoon-utilities}

The `BTT_restart_Hammerspoon` function sets up a BetterTouchTool widget which also executes the `config_reload` action from the spoon. This gets assigned to the `fn` config parameter in the configuration of the Hammer spoon below, which has the effect of calling the function with the Spoon object as its parameter.

This is still manual - the `uuid` parameter contains the ID of the BTT widget to configure, and for now you have to get it by hand from BTT and paste it here.

```lua
function BTT_restart_hammerspoon(s)
  BTT:bindSpoonActions(s, {
                         config_reload = {
                           kind = 'touchbarButton',
                           uuid = "FF8DA717-737F-4C42-BF91-E8826E586FA1",
                           name = "Restart",
                           icon = hs.image.imageFromName(
                             hs.image.systemImageNames.ApplicationIcon),
                           color = hs.drawing.color.x11.orange,
  }})
end
```

The [Hammer](https://zzamboni.github.io/zzSpoons/Hammer.html) spoon (get it? hehe) is a simple wrapper around some common Hammerspoon configuration variables. Note that this gets loaded from my personal repo, since it's not in the official repository.

```lua
Install:andUse("Hammer",
               {
                 repo = 'zzspoons',
                 config = { auto_reload_config = false },
                 hotkeys = {
                   config_reload = {hyper, "r"},
                   toggle_console = {hyper, "y"}
                 },
--                 fn = BTT_restart_Hammerspoon,
                 start = true
               }
)
```


### Caffeine: Control system/display sleep {#caffeine-control-system-display-sleep}

The [Caffeine](http://www.hammerspoon.org/Spoons/Caffeine.html) spoon allows preventing the display and the machine from sleeping. I use it frequently when playing music from my machine, to avoid having to unlock the screen whenever I want to change the music. In this case we also create a function `BTT_caffeine_widget` to configure the widget to both execute the corresponding function, and to set its icon according to the current state.

```lua
function BTT_caffeine_widget(s)
  BTT:bindSpoonActions(s, {
                         toggle = {
                           kind = 'touchbarWidget',
                           uuid = '72A96332-E908-4872-A6B4-8A6ED2E3586F',
                           name = 'Caffeine',
                           widget_code = [[
do
  title = " "
  icon = hs.image.imageFromPath(spoon.Caffeine.spoonPath.."/caffeine-off.pdf")
  if (hs.caffeinate.get('displayIdle')) then
    icon = hs.image.imageFromPath(spoon.Caffeine.spoonPath.."/caffeine-on.pdf")
  end
  print(hs.json.encode({ text = title,
                         icon_data = BTT:hsimageToBTTIconData(icon) }))
end
      ]],
                           code = "spoon.Caffeine.clicked()",
                           widget_interval = 1,
                           color = hs.drawing.color.x11.black,
                           icon_only = true,
                           icon_size = hs.geometry.size(15,15),
                           BTTTriggerConfig = {
                             BTTTouchBarFreeSpaceAfterButton = 0,
                             BTTTouchBarItemPadding = -6,
                           },
                         }
  })
end
```

```lua
Install:andUse("Caffeine", {
                 start = true,
                 hotkeys = {
                   toggle = { hyper, "1" }
                 },
--                 fn = BTT_caffeine_widget,
})
```


### Colorize menubar according to keyboard layout {#colorize-menubar-according-to-keyboard-layout}

The [MenubarFlag](http://www.hammerspoon.org/Spoons/MenubarFlag.html) spoon colorizes the menubar according to the selected keyboard language or layout (functionality inspired by [ShowyEdge](https://pqrs.org/osx/ShowyEdge/index.html.en)). I use English, Spanish and German, so those are the colors I have defined.

```lua
Install:andUse("MenubarFlag",
               {
                 config = {
                   colors = {
                     ["U.S."] = { },
                     Spanish = {col.green, col.white, col.red},
                     ["Latin American"] = {col.green, col.white, col.red},
                     German = {col.black, col.red, col.yellow},
                   }
                 },
                 start = true
               }
)
```


### Locating the mouse {#locating-the-mouse}

The [MouseCircle](http://www.hammerspoon.org/Spoons/MouseCircle.html) spoon shows a circle around the mouse pointer when triggered. I have it disabled for now because I have the macOS [shake-to-grow feature](https://support.apple.com/kb/PH25507?locale=en_US&viewlocale=en_US) enabled.

```lua
Install:andUse("MouseCircle",
               {
                 disable = true,
                 config = {
                   color = hs.drawing.color.x11.rebeccapurple
                 },
                 hotkeys = {
                   show = { hyper, "m" }
                 }
               }
)
```


### Finding colors {#finding-colors}

One of my original bits of Hammerspoon code, now made into a spoon (although I keep it disabled, since I don't really use it). The [ColorPicker](http://www.hammerspoon.org/Spoons/ColorPicker.html) spoon shows a menu of the available color palettes, and when you select one, it draws swatches in all the colors in that palette, covering the whole screen. You can click on any of them to copy its name to the clipboard, or cmd-click to copy its RGB code.

```lua
Install:andUse("ColorPicker",
               {
                 disable = true,
                 hotkeys = {
                   show = { hyper, "z" }
                 },
                 config = {
                   show_in_menubar = false,
                 },
                 start = true,
               }
)
```


### Homebrew information popups {#homebrew-information-popups}

I use Homebrew, and when I run `brew update`, I often wonder about what some of the formulas shown are (names are not always obvious). The [BrewInfo](http://www.hammerspoon.org/Spoons/BrewInfo.html) spoon allows me to point at a Formula or Cask name and press `Hyper-b` or `Hyper-c` (for Casks) to have the output of the `info` command in a popup window, or the same key with `Shift-Hyper` to open the URL of the Formula/Cask.

```lua
Install:andUse("BrewInfo",
               {
                 config = {
                   brew_info_style = {
                     textFont = "Inconsolata",
                     textSize = 14,
                     radius = 10 }
                 },
                 hotkeys = {
                   -- brew info
                   show_brew_info = {hyper, "b"},
                   open_brew_url = {shift_hyper, "b"},
                   -- brew cask info - not needed anymore, the above now do both
                   -- show_brew_cask_info = {shift_hyper, "c"},
                   -- open_brew_cask_url = {hyper, "c"},
                 }
               }
)
```


### Displaying keyboard shortcuts {#displaying-keyboard-shortcuts}

The [KSheet](http://www.hammerspoon.org/Spoons/KSheet.html) spoon traverses the current application's menus and builds a cheatsheet of the keyboard shortcuts, showing it in a nice popup window.

```lua
Install:andUse("KSheet",
               {
                 hotkeys = {
                   toggle = { hyper, "/" }
}})
```


### TimeMachine backup monitoring {#timemachine-backup-monitoring}

The [TimeMachineProgress](http://www.hammerspoon.org/Spoons/TimeMachineProgress.html) spoon shows an indicator about the progress of the ongoing Time Machine backup. The indicator disappears when there is no backup going on.

```lua
Install:andUse("TimeMachineProgress",
               {
                 start = true
               }
)
```


### Disabling Turbo Boost {#disabling-turbo-boost}

The TurboBoost spoon shows an indicator of the CPU's Turbo Boost status, and allows disabling/enabling. This requires [Turbo Boost Switcher](https://github.com/rugarciap/Turbo-Boost-Switcher) to be installed.

(disabled because I ended up buying _Turbo Boost Switcher Pro_ - it's a great utility and offers a few great extra features for an excellent price, it deserves our support)

```lua
Install:andUse("TurboBoost",
               {
                 disable = true,
                 config = {
                   disable_on_start = true
                 },
                 hotkeys = {
                   toggle = { hyper, "0" }
                 },
                 start = true,
                 --                   loglevel = 'debug'
               }
)
```


### Unmounting external disks on sleep {#unmounting-external-disks-on-sleep}

The `EjectMenu` spoon automatically ejects all external disks before the system goes to sleep. I use this to avoid warnings from macOS when I close my laptop and disconnect it from my hub without explicitly unmounting my backup disk before. I disable the menubar icon, which is shown by default by the Spoon.

```lua
Install:andUse("EjectMenu", {
                 config = {
                   eject_on_lid_close = false,
                   eject_on_sleep = false,
                   show_in_menubar = true,
                   notify = true,
                 },
                 hotkeys = { ejectAll = { hyper, "=" } },
                 start = true,
--                 loglevel = 'debug'
})
```


## Other applications {#other-applications}

The [HeadphoneAutoPause](http://www.hammerspoon.org/Spoons/HeadphoneAutoPause.html) spoon implements auto-pause/resume for iTunes, Spotify and others when the headphones are unplugged. Note that this goes unused since I started using wireless headphones.

```lua
Install:andUse("HeadphoneAutoPause",
               {
                 start = true,
                 disable = true,
               }
)
```


## Seal application launcher/controller {#seal-application-launcher-controller}

The [Seal](http://www.hammerspoon.org/Spoons/Seal.html) spoon is a powerhouse. It implements a Spotlight-like launcher, but which allows for infinite configurability of what can be done or searched from the launcher window. I use Seal as my default launcher, triggered with `Cmd-space`, although I still keep Spotlight around under `Hyper-space`, mainly for its search capabilities.

We start by loading the spoon, and specifying which plugins we want.

```lua
Install:andUse("Seal",
               {
                 hotkeys = { show = { {"alt"}, "space" } },
                 fn = function(s)
                   s:loadPlugins({"apps", "calc", "safari_bookmarks",
                                  "screencapture", "useractions"})
                   s.plugins.safari_bookmarks.always_open_with_safari = false
                   s.plugins.useractions.actions =
                     {
                         <<useraction-definitions>>
                     }
                   s:refreshAllCommands()
                 end,
                 start = true,
               }
)
```

The `useractions` Seal plugin allows me to define my own shortcuts. For example, a bookmark to the Hammerspoon documentation page:

```lua
["Hammerspoon docs webpage"] = {
  url = "http://hammerspoon.org/docs/",
  icon = hs.image.imageFromName(hs.image.systemImageNames.ApplicationIcon),
},
```

Or to manually trigger my work/non-work transition scripts (see below):

```lua
["Leave corpnet"] = {
  fn = function()
    spoon.WiFiTransitions:processTransition('foo', 'corpnet01')
  end,
  icon = work_logo,
},
["Arrive in corpnet"] = {
  fn = function()
    spoon.WiFiTransitions:processTransition('corpnet01', 'foo')
  end,
  icon = work_logo,
},
```

Or to translate things using [dict.leo.org](https://dict.leo.org/):

```lua
["Translate using Leo"] = {
  url = "http://dict.leo.org/englisch-deutsch/${query}",
  icon = 'favicon',
  keyword = "leo",
}
```


## Network transitions {#network-transitions}

The [WiFiTransitions](http://www.hammerspoon.org/Spoons/WiFiTransitions.html) spoon allows triggering arbitrary actions when the SSID changes. I am interested in the change from my work network (corpnet01) to other networks, mainly because at work I need a proxy for all connections to the Internet. I have two applications which don't handle these transitions gracefully on their own: Spotify and Adium. So I have written a couple of functions for helping them along.

The `reconfigSpotifyProxy` function quits Spotify, updates the proxy settings in its config file, and restarts it.

```lua
function reconfigSpotifyProxy(proxy)
  local spotify = hs.appfinder.appFromName("Spotify")
  local lastapp = nil
  if spotify then
    lastapp = hs.application.frontmostApplication()
    spotify:kill()
    hs.timer.usleep(40000)
  end
  -- I use CFEngine to reconfigure the Spotify preferences
  cmd = string.format(
    "/usr/local/bin/cf-agent -K -f %s/files/spotify-proxymode.cf%s",
    hs.configdir, (proxy and " -DPROXY" or " -DNOPROXY"))
  output, status, t, rc = hs.execute(cmd)
  if spotify and lastapp then
    hs.timer.doAfter(
      3,
      function()
        if not hs.application.launchOrFocus("Spotify") then
          hs.notify.show("Error launching Spotify", "", "")
        end
        if lastapp then
          hs.timer.doAfter(0.5, hs.fnutils.partial(lastapp.activate, lastapp))
        end
    end)
  end
end
```

The `reconfigAdiumProxy` function uses AppleScript to tell Adium about the change without having to restart it - only if Adium is already running.

```lua
function reconfigAdiumProxy(proxy)
  app = hs.application.find("Adium")
  if app and app:isRunning() then
    local script = string.format([[
  tell application "Adium"
    repeat with a in accounts
      if (enabled of a) is true then
        set proxy enabled of a to %s
      end if
    end repeat
    go offline
    go online
  end tell
  ]], hs.inspect(proxy))
    hs.osascript.applescript(script)
  end
end
```

Functions to stop applications that  are disallowed in the work network.

```lua
function stopApp(name)
  app = hs.application.get(name)
  if app and app:isRunning() then
    app:kill()
  end
end

function forceKillProcess(name)
  hs.execute("pkill " .. name)
end

function startApp(name)
  hs.application.open(name)
end
```

The configuration for the WiFiTransitions spoon invoked these functions with the appropriate parameters.

```lua
Install:andUse("WiFiTransitions",
               {
                 config = {
                   actions = {
                     -- { -- Test action just to see the SSID transitions
                     --    fn = function(_, _, prev_ssid, new_ssid)
                     --       hs.notify.show("SSID change",
                     --          string.format("From '%s' to '%s'",
                     --          prev_ssid, new_ssid), "")
                     --    end
                     -- },
                     { -- Enable proxy config when joining corp network
                       to = "corpnet01",
                       fn = {hs.fnutils.partial(reconfigSpotifyProxy, true),
                             hs.fnutils.partial(reconfigAdiumProxy, true),
                             hs.fnutils.partial(forceKillProcess, "Dropbox"),
                             hs.fnutils.partial(stopApp, "Evernote"),
                       }
                     },
                     { -- Disable proxy config when leaving corp network
                       from = "corpnet01",
                       fn = {hs.fnutils.partial(reconfigSpotifyProxy, false),
                             hs.fnutils.partial(reconfigAdiumProxy, false),
                             hs.fnutils.partial(startApp, "Dropbox"),
                       }
                     },
                   }
                 },
                 start = true,
               }
)
```


## Pop-up translation {#pop-up-translation}

I live in Switzerland, and my German is far from perfect, so the [PopupTranslateSelection](http://www.hammerspoon.org/Spoons/PopupTranslateSelection.html) spoon helps me a lot. It allows me to select some text and, with a keystroke, translate it to any of three languages using Google Translate. Super useful! Usually, Google's auto-detect feature works fine, so the `translate_to_<lang>` keys are sufficient. I have some `translate_<from>_<to>` keys set up for certain language pairs for when this doesn't quite work (I don't think I've ever needed them).

```lua
local wm=hs.webview.windowMasks
Install:andUse("PopupTranslateSelection",
               {
                 disable = true,
                 config = {
                   popup_style = wm.utility|wm.HUD|wm.titled|
                     wm.closable|wm.resizable,
                 },
                 hotkeys = {
                   translate_to_en = { hyper, "e" },
                   translate_to_de = { hyper, "d" },
                   translate_to_es = { hyper, "s" },
                   translate_de_en = { shift_hyper, "e" },
                   translate_en_de = { shift_hyper, "d" },
                 }
               }
)
```

I am now testing [DeepLTranslate](http://www.hammerspoon.org/Spoons/DeepLTranslate.html), based on PopupTranslateSelection but which uses the [DeepL translator](https://www.deepl.com/en/translator) (this is disabled because I have the DeepL app installed, which binds its own global hotkeys).

```lua
Install:andUse("DeepLTranslate",
               {
                 disable = true,
                 config = {
                   popup_style = wm.utility|wm.HUD|wm.titled|
                     wm.closable|wm.resizable,
                 },
                 hotkeys = {
                   translate = { hyper, "e" },
                 }
               }
)
```


## Leanpub integration {#leanpub-integration}

The Leanpub spoon provides monitoring of book build jobs. You can read more about how I use this in my blog post [Automating Leanpub book publishing with Hammerspoon and CircleCI](https://zzamboni.org/post/automating-leanpub-book-publishing-with-hammerspoon-and-circleci/).

```lua
Install:andUse("Leanpub",
               {
                 config = {
                   watch_books = {
                     -- api_key gets set in init-local.lua like this:
                     -- spoon.Leanpub.api_key = "my-api-key"
                     { slug = "learning-hammerspoon" },
                     { slug = "learning-cfengine" },
                     { slug = "emacs-org-leanpub" },
                     -- { slug = "be-safe-on-the-internet" },
                     { slug = "lit-config"  },
                     { slug = "zztestbook" },
                     -- { slug = "cisspexampreparationguide" },
                   },
                   books_sync_to_dropbox = true,
                 },
                 start = true,
                 -- loglevel = 'debug'
})
```


## Showing application keybindings {#showing-application-keybindings}

The KSheet spoon provides for showing the keybindings for the currently active application.

```lua
Install:andUse("KSheet", {
                 hotkeys = {
                   toggle = { hyper, "/" }
                 }
})
```


## Loading private configuration {#loading-private-configuration}

In `init-local.lua` I keep experimental or private stuff (like API tokens) that I don't want to publish in my main config. This file is not committed to any publicly accessible git repositories.

```lua
local localfile = hs.configdir .. "/local/init-local.lua"
if hs.fs.attributes(localfile) then
  dofile(localfile)
end
```


## End-of-config animation {#end-of-config-animation}

The [FadeLogo](http://www.hammerspoon.org/Spoons/FadeLogo.html) spoon simply shows an animation of the Hammerspoon logo to signal the end of the config load.

```lua
Install:andUse("FadeLogo",
               {
                 config = {
                   default_run = 1.0,
                 },
                 start = true
               }
)
```

If you don't want to use FadeLogo, you can have a regular notification.

```lua
-- hs.notify.show("Welcome to Hammerspoon", "Have fun!", "")
```
