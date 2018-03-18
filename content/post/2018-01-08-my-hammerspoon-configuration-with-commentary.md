+++
title = "My Hammerspoon Configuration, With Commentary"
author = ["Zamboni Diego"]
date = 2018-01-08T13:31:00+01:00
tags = ["hammerspoon", "config", "howto"]
draft = false
creator = "Emacs 25.3.2 (Org mode 9.1.7 + ox-hugo)"
toc = true
featured_image = "/images/hammerspoon.png"
summary = "In my ongoing series of literate config files, I present to you my Hammerspoon configuration file."
+++

In my [ongoing](../my-elvish-configuration-with-commentary/) [series](../my-emacs-configuration-with-commentary) of [literate](http://www.howardism.org/Technical/Emacs/literate-programming-tutorial.html) config files, I present to you my [Hammerspoon](http://www.hammerspoon.org/) configuration file. You can see the generated file at <https://github.com/zzamboni/dot-hammerspoon/blob/master/init.lua>. As usual, this is just a snapshot at this time, you can see the current version of my configuration [in GitHub](https://github.com/zzamboni/dot-hammerspoon/blob/master/init.org).


## General variables and configuration {#general-variables-and-configuration}

Global log level. Per-spoon log level can be configured in each
`Install:andUse` block below.

```lua
hs.logger.defaultLogLevel="info"
```

I use `hyper` and `shift_hyper` as the modifiers for most of my key
bindings, so I define them as variables here for easier referencing.

```lua
hyper = {"cmd","alt","ctrl"}
shift_hyper = {"cmd","alt","ctrl","shift"}
```

Set up an abbreviation for `hs.drawing.color.x11` since I use it
repeatedly later on.

```lua
col = hs.drawing.color.x11
```

Work's logo, which I use in some of my Seal shortcuts later on.

```lua
swisscom_logo = hs.image.imageFromPath(hs.configdir .. "/files/swisscom_logo_2x.png")
```


## Spoon Management {#spoon-management}

Set up SpoonInstall - this is the only spoon that needs to be manually
installed (it is already there if you check out this repository), all
the others are installed and configured automatically.

```lua
hs.loadSpoon("SpoonInstall")
```

Configuration of my personal spoon repository, which contains Spoons
that have not been merged in the main repo.  See the descriptions at
<https://zzamboni.github.io/zzSpoons/>.

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

This is just a shortcut to make the declarations below look more
readable, i.e. `Install:andUse` instead of `spoon.SpoonInstall:andUse`.

```lua
Install=spoon.SpoonInstall
```


## URL Dispatching to site-specific browsers {#url-dispatching-to-site-specific-browsers}

The [URLDispatcher](http://www.hammerspoon.org/Spoons/URLDispatcher.html) spoon makes it possible to open URLs with different
browsers. I have created different site-specific browsers using
[Epichrome](https://github.com/dmarmor/epichrome), which allows me to keep site-specific bookmarks, search
settings, etc.

```lua
Install:andUse("URLDispatcher",
               {
                 config = {
                   url_patterns = {
                     { "https?://issue.swisscom.ch", "org.epichrome.app.SwisscomJira" },
                     { "https?://issue.swisscom.com", "org.epichrome.app.SwisscomJira" },
                     { "https?://jira.swisscom.com", "org.epichrome.app.SwisscomJira" },
                     { "https?://wiki.swisscom.com", "org.epichrome.app.SwisscomWiki" },
                     { "https?://collaboration.swisscom.com", "org.epichrome.app.SwisscomCollab" },
                     { "https?://smca.swisscom.com", "org.epichrome.app.SwisscomTWP" },
                     { "https?://portal.corproot.net", "com.google.Chrome" },
                     { "https?://app.opsgenie.com", "org.epichrome.app.OpsGenie" },
                   },
                   default_handler = "com.google.Chrome"
                 },
                 start = true
               }
)
```


## Window and screen manipulation {#window-and-screen-manipulation}

The [WindowHalfAndThirds](http://www.hammerspoon.org/Spoons/WindowHalfsAndThirds.html) spoon sets up multiple key bindings for
manipulating the size and position of windows.

```lua
Install:andUse("WindowHalfsAndThirds",
               {
                 config = {
                   use_frame_correctness = true
                 },
                 hotkeys = 'default'
               }
)
```

The [WindowScreenLeftAndRight](http://zzamboni.org/zzSpoons/WindowScreenLeftAndRight.html) spoon sets up key bindings for moving
windows between multiple screens.

```lua
Install:andUse("WindowScreenLeftAndRight",
               {
                 hotkeys = 'default'
               }
)
```

The [WindowGrid](http://www.hammerspoon.org/Spoons/WindowGrid.html) spoon sets up a key binding (`Hyper-g` here) to overlay a
grid that allows resizing windows by specifying their opposite
corners.

```lua
Install:andUse("WindowGrid",
               {
                 config = { gridGeometries = { { "6x4" } } },
                 hotkeys = {show_grid = {hyper, "g"}},
                 start = true
               }
)
```

The [ToggleScreenRotation](http://www.hammerspoon.org/Spoons/ToggleScreenRotation.html) spoon sets up a key binding to rotate the
external screen (the spoon can set up keys for multiple screens if
needed, but by default it rotates the first external screen).

```lua
Install:andUse("ToggleScreenRotation",
               {
                 hotkeys = { first = {hyper, "f15"} }
               }
)
```


## Organization and Productivity {#organization-and-productivity}

The [UniversalArchive](http://www.hammerspoon.org/Spoons/UniversalArchive.html) spoon sets up a single key binding (`Ctrl-Cmd-a`)
to archive the current item in Evernote, Mail and Outlook.

```lua
Install:andUse("UniversalArchive",
               {
                 config = {
                   evernote_archive_notebook = ".Archive",
                   outlook_archive_folder = "Archive (On My Computer)",
                   archive_notifications = false
                 },
                 hotkeys = { archive = { { "ctrl", "cmd" }, "a" } }
               }
)
```

The [SendToOmniFocus](http://www.hammerspoon.org/Spoons/SendToOmniFocus.html) spoon sets up a single key binding (`Hyper-t`) to
send the current item to OmniFocus from multiple applications.

```lua
Install:andUse("SendToOmniFocus",
               {
                 config = {
                   quickentrydialog = false,
                   notifications = false
                 },
                 hotkeys = {
                   send_to_omnifocus = { hyper, "t" }
                 },
                 fn = function(s)
                   s:registerApplication("Swisscom Collab", { apptype = "chromeapp", itemname = "tab" })
                   s:registerApplication("Swisscom Wiki", { apptype = "chromeapp", itemname = "wiki page" })
                   s:registerApplication("Swisscom Jira", { apptype = "chromeapp", itemname = "issue" })
                 end
               }
)
```

The [EvernoteOpenAndTag](http://www.hammerspoon.org/Spoons/EvernoteOpenAndTag.html) spoon sets up some missing key bindings for
note manipulation in Evernote.

```lua
Install:andUse("EvernoteOpenAndTag",
               {
                 hotkeys = {
                   open_note = { hyper, "o" },
                   ["open_and_tag-+work,+swisscom"] = { hyper, "w" },
                   ["open_and_tag-+personal"] = { hyper, "p" },
                   ["tag-@zzdone"] = { hyper, "z" }
                 }
               }
)
```

The [TextClipboardHistory](http://www.hammerspoon.org/Spoons/TextClipboardHistory.html) spoon implements a clipboard history, only
for text items. It is invoked with `Cmd-Shift-v`.

```lua
Install:andUse("TextClipboardHistory",
               {
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

The [Hammer](https://zzamboni.github.io/zzSpoons/Hammer.html) spoon (get it? hehe) is a simple wrapper around some common
Hamerspoon configuration variables. Note that this gets loaded from my
personal repo, since it's not in the official repository.

```lua
Install:andUse("Hammer",
               {
                 repo = 'zzspoons',
                 config = { auto_reload_config = false },
                 hotkeys = {
                   config_reload = {hyper, "r"},
                   toggle_console = {hyper, "y"}
                 },
                 start = true
               }
)
```

The [Caffeine](http://www.hammerspoon.org/Spoons/Caffeine.html) spoon allows preventing the display and the machine from
sleeping. I use it frequently when playing music from my machine, to
avoid having to unlock the screen whenever I want to change the music.

```lua
Install:andUse("Caffeine", {
                 start = true,
                 hotkeys = {
                   toggle = { hyper, "1" }
                 }
})
```

The [MenubarFlag](http://www.hammerspoon.org/Spoons/MenubarFlag.html) spoon colorizes the menubar according to the selected
keyboard language or layout (Functionality inspired by [ShowyEdge](https://pqrs.org/osx/ShowyEdge/index.html.en). I
use English, Spanish and German, so those are the colors I have
defined.

```lua
Install:andUse("MenubarFlag",
               {
                 config = {
                   colors = {
                     ["U.S."] = { },
                     Spanish = {col.green, col.white, col.red},
                     German = {col.black, col.red, col.yellow},
                   }
                 },
                 start = true
               }
)
```

The [MouseCircle](http://www.hammerspoon.org/Spoons/MouseCircle.html) spoon shows a circle around the mouse pointer when
triggered. I have it disabled for now because I have the macOS
[shake-to-grow feature](https://support.apple.com/kb/PH25507?locale=en_US&viewlocale=en_US) enabled.

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

One of my original bits of Hammerspoon code, now made into a spoon
(although I keep it disabled, since I don't really use it). The
[ColorPicker](http://www.hammerspoon.org/Spoons/ColorPicker.html) spoon shows a menu of the available color palettes, and
when you select one, it draws swatches in all the colors in that
palette, covering the whole screen. You can click on any of them to
copy its name to the clipboard, or cmd-click to copy its RGB code.

```lua
Install:andUse("ColorPicker",
               {
                 disable = true,
                 hotkeys = {
                   show = { shift_hyper, "c" }
                 },
                 config = {
                   show_in_menubar = false,
                 },
                 start = true,
               }
)
```

I use Homebrew, and when I run `brew update`, I often wonder about what
some of the formulas shown are (names are not always obvious). The
[BrewInfo](http://www.hammerspoon.org/Spoons/BrewInfo.html) spoon allows me to point at a Formula or Cask name and press
`Hyper-b` or `Hyper-c` (for Casks) to have the output of the `info` command
in a popup window, or the same key with `Shift-Hyper` to open the URL of
the Formula/Cask.

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
                   -- brew cask info
                   show_brew_cask_info = {hyper, "c"},
                   open_brew_cask_url = {shift_hyper, "c"},
                 }
               }
)
```

The KSheet spoon traverses the current application's menus and builds
a cheatsheet of the keyboard shortcuts, showing it in a nice popup
window.

```lua
Install:andUse("KSheet",
               {
                 hotkeys = {
                   toggle = { hyper, "/" }
}})
```


## Other applications {#other-applications}

The [ToggleSkypeMute](http://www.hammerspoon.org/Spoons/ToggleSkypeMute.html) spoon sets up the missing keyboard bindings for
toggling the mute button on Skype and Skype for Business. I'm not
fully happy with this spoon - it should auto-detect the application
instead of having separate keys for each application, and it could be
extended to more generic use.

```lua
Install:andUse("ToggleSkypeMute",
               {
                 hotkeys = {
                   toggle_skype = { shift_hyper, "v" },
                   toggle_skype_for_business = { shift_hyper, "f" }
                 }
               }
)
```

The [HeadphoneAutoPause](http://www.hammerspoon.org/Spoons/HeadphoneAutoPause.html) spoon implements auto-pause/resume for iTunes,
Spotify and others when the headphones are unplugged.

```lua
Install:andUse("HeadphoneAutoPause",
               {
                 start = true
               }
)
```


## Seal {#seal}

The [Seal](http://www.hammerspoon.org/Spoons/Seal.html) spoon is a powerhouse - it implements a Spotlight-like
launcher, but which allows for infinite configurability of what can be
done or searched from the launcher window. I use Seal as my default
launcher, triggered with `Cmd-space`, although I still keep Spotlight
around under `Hyper-space`, mainly for its search capabilities.

We start by loading the spoon, and specifying which plugins we want.

```lua
Install:andUse("Seal",
               {
                 hotkeys = { show = { {"cmd"}, "space" } },
                 fn = function(s)
                   s:loadPlugins({"apps", "calc", "safari_bookmarks", "screencapture", "useractions"})
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

The `useractions` Seal plugin allows me to define my own shortcuts. For
example, a bookmark to the Hammerspoon documentation page:

```lua
["Hammerspoon docs webpage"] = {
  url = "http://hammerspoon.org/docs/",
  icon = hs.image.imageFromName(hs.image.systemImageNames.ApplicationIcon),
},
```

Or to manually trigger my work/non-work transition scripts (see
below):

```lua
["Leave corpnet"] = {
  fn = function()
    spoon.WiFiTransitions:processTransition('foo', 'corpnet01')
  end,
  icon = swisscom_logo,
},
["Arrive in corpnet"] = {
  fn = function()
    spoon.WiFiTransitions:processTransition('corpnet01', 'foo')
  end,
  icon = swisscom_logo,
},
```

Or to translate things using dict.leo.org:

```lua
["Translate using Leo"] = {
  url = "http://dict.leo.org/ende/index_de.html#/search=${query}",
  icon = 'favicon',
  keyword = "leo",
}
```


## Network transitions {#network-transitions}

The [WiFiTransitions](http://www.hammerspoon.org/Spoons/WiFiTransitions.html) spoon allows triggering arbitrary actions when the
SSID changes. I am interested in the change from my work network
(corpnet01) to other networks, mainly because at work I need a proxy
for all connections to the Internet. I have two applications which
don't handle these transitions gracefully on their own: Spotify and
Adium. So I have written a couple of functions for helping them along.

The `reconfigSpotifyProxy` function quits Spotify, updates the proxy
settings in its config file, and restarts it.

```lua
function reconfigSpotifyProxy(proxy)
  local spotify = hs.appfinder.appFromName("Spotify")
  local lastapp = nil
  if spotify then
    lastapp = hs.application.frontmostApplication()
    spotify:kill()
    hs.timer.usleep(40000)
  end
  --   hs.notify.show(string.format("Reconfiguring %sSpotify", ((spotify~=nil) and "and restarting " or "")), string.format("Proxy %s", (proxy and "enabled" or "disabled")), "")
  -- I use CFEngine to reconfigure the Spotify preferences
  cmd = string.format("/usr/local/bin/cf-agent -K -f %s/files/spotify-proxymode.cf%s", hs.configdir, (proxy and " -DPROXY" or " -DNOPROXY"))
  output, status, t, rc = hs.execute(cmd)
  if spotify and lastapp then
    hs.timer.doAfter(3,
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

The `reconfigAdiumProxy` function uses AppleScript to tell Adium about
the change without having to restart it.

```lua
function reconfigAdiumProxy(proxy)
  --   hs.notify.show("Reconfiguring Adium", string.format("Proxy %s", (proxy and "enabled" or "disabled")), "")
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
```

The configuration for the WiFiTransitions spoon invoked these
functions with the appropriate parameters.

```lua
Install:andUse("WiFiTransitions",
               {
                 config = {
                   actions = {
                     -- { -- Test action just to see the SSID transitions
                     --    fn = function(_, _, prev_ssid, new_ssid)
                     --       hs.notify.show("SSID change", string.format("From '%s' to '%s'", prev_ssid, new_ssid), "")
                     --    end
                     -- },
                     { -- Enable proxy in Spotify and Adium config when joining corp network
                       to = "corpnet01",
                       fn = {hs.fnutils.partial(reconfigSpotifyProxy, true),
                             hs.fnutils.partial(reconfigAdiumProxy, true),
                       }
                     },
                     { -- Disable proxy in Spotify and Adium config when leaving corp network
                       from = "corpnet01",
                       fn = {hs.fnutils.partial(reconfigSpotifyProxy, false),
                             hs.fnutils.partial(reconfigAdiumProxy, false),
                       }
                     },
                   }
                 },
                 start = true,
               }
)
```


## Pop-up translation {#pop-up-translation}

I live in Switzerland, and my German is far from perfect, so the
[PopupTranslateSelection](http://www.hammerspoon.org/Spoons/PopupTranslateSelection.html) spoon helps me a lot. It allows me to select
some text and, with a keystroke, translate it to any of three
languages using Google Translate. Super useful! Usually, Google's
auto-detect feature works fine, so the `translate_to_<lang>` keys are
sufficient. I have some `translate_<from>_<to>` keys set up for certain
language pairs for when this doesn't quite work (I don't think I've
ever needed them).

```lua
local wm=hs.webview.windowMasks
Install:andUse("PopupTranslateSelection",
               {
                 config = {
                   popup_style = wm.utility|wm.HUD|wm.titled|wm.closable|wm.resizable,
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


## Miscellaneous stuff {#miscellaneous-stuff}

In my `init-local.lua` file I keep some experimental or private stuff
that I don't want to publish in my main config.

```lua
local localstuff=loadfile(hs.configdir .. "/init-local.lua")
if localstuff then
  localstuff()
end
```


## End-of-config animation {#end-of-config-animation}

The [FadeLogo](http://www.hammerspoon.org/Spoons/FadeLogo.html) spoon simply shows an animation of the Hammerspoon logo
to signal the end of the config load.

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
