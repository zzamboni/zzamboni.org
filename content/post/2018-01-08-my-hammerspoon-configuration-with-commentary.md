+++
title = "My Hammerspoon Configuration, With Commentary"
author = ["Diego Zamboni"]
summary = "In my ongoing series of literate config files, I present to you my Hammerspoon configuration file."
date = 2018-01-08T13:31:00+01:00
tags = ["config", "howto", "literateprogramming", "literateconfig", "hammerspoon"]
draft = false
creator = "Emacs 26.2 (Org mode 9.2.5 + ox-hugo)"
toc = true
featured_image = "/images/hammerspoon.png"
+++

Last update: **September 10, 2019**

In my [ongoing](../my-elvish-configuration-with-commentary/) [series](../my-emacs-configuration-with-commentary) of [literate](http://www.howardism.org/Technical/Emacs/literate-programming-tutorial.html) config files, I present to you my [Hammerspoon](http://www.hammerspoon.org/) configuration file. You can see the generated file at <https://github.com/zzamboni/dot-hammerspoon/blob/master/init.lua>. As usual, this is just a snapshot at the time shown above, you can see the current version of my configuration [in GitHub](https://github.com/zzamboni/dot-hammerspoon/blob/master/init.org).

If you want to learn more about Hammerspoon, check out my book [Learning Hammerspoon](https://leanpub.com/learning-hammerspoon)!


## General variables and configuration {#general-variables-and-configuration}

Global log level. Per-spoon log level can be configured in each `Install:andUse` block below.

```lua
hs.logger.defaultLogLevel="info"
```

I use `hyper` and `shift_hyper` as the modifiers for most of my key bindings, so I define them as variables here for easier referencing.

```lua
hyper = {"cmd","alt","ctrl"}
shift_hyper = {"cmd","alt","ctrl","shift"}
```

Set up an abbreviation for `hs.drawing.color.x11` since I use it repeatedly later on.

```lua
col = hs.drawing.color.x11
```

Work's logo, which I use in some of my Seal shortcuts later on.

```lua
swisscom_logo = hs.image.imageFromPath(hs.configdir .. "/files/swisscom_logo_2x.png")
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


## BetterTouchTool {#bettertouchtool}

I'm currently working on a new [BetterTouchTool.spoon](https://github.com/zzamboni/Spoons/tree/spoon/BetterTouchTool/Source/BetterTouchTool.spoon) which provides integration with the [BetterTouchTool AppleScript API](https://docs.bettertouchtool.net/docs/apple%5Fscript.html). This is in heavy development! See the configuration for the Hammer spoon in [System and UI](#system-and-ui) for an example of how to use it.

```lua
Install:andUse("BetterTouchTool", { loglevel = 'debug' })
BTT = spoon.BetterTouchTool
```


## URL Dispatching to site-specific browsers {#url-dispatching-to-site-specific-browsers}

The [URLDispatcher](http://www.hammerspoon.org/Spoons/URLDispatcher.html) spoon makes it possible to open URLs with different browsers. I have created different site-specific browsers using [Epichrome](https://github.com/dmarmor/epichrome), which allows me to keep site-specific bookmarks, search settings, etc.

```lua
JiraApp = "org.epichrome.app.SwisscomJ995"
WikiApp = "org.epichrome.app.SwisscomWiki"
Install:andUse("URLDispatcher",
               {
                 config = {
                   url_patterns = {
                     { "https?://issue.swisscom.ch",                       JiraApp },
                     { "https?://issue.swisscom.com",                      JiraApp },
                     { "https?://jira.swisscom.com",                       JiraApp },
                     { "https?://wiki.swisscom.com",                       WikiApp },
                     { "https?://collaboration.swisscom.com",              "org.epichrome.app.SwisscomCollab" },
                     { "https?://smca.swisscom.com",                       "org.epichrome.app.SwisscomTWP" },
                     { "https?://portal.corproot.net",                     "com.apple.Safari" },
                     { "https?://app.opsgenie.com",                        "org.epichrome.app.OpsGenie" },
                     { "https?://app.eu.opsgenie.com",                     "org.epichrome.app.OpsGenie" },
                     { "https?://fiori.swisscom.com",                      "com.apple.Safari" },
                     { "https?://pmpgwd.apps.swisscom.com/fiori",  "com.apple.Safari" },
                     { "https?://.*webex.com",  "com.google.Chrome" },
                   },
                   -- default_handler = "com.google.Chrome"
                   -- default_handler = "com.electron.brave"
                   default_handler = "com.brave.Browser.dev"
                 },
                 start = true
               }
)
```


## Window and screen manipulation {#window-and-screen-manipulation}

The [WindowHalfsAndThirds](http://www.hammerspoon.org/Spoons/WindowHalfsAndThirds.html) spoon sets up multiple key bindings for manipulating the size and position of windows.

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

The [WindowScreenLeftAndRight](http://www.hammerspoon.org/Spoons/WindowScreenLeftAndRight.html) spoon sets up key bindings for moving windows between multiple screens.

```lua
Install:andUse("WindowScreenLeftAndRight",
               {
                 hotkeys = 'default'
               }
)
```

The [WindowGrid](http://www.hammerspoon.org/Spoons/WindowGrid.html) spoon sets up a key binding (`Hyper-g` here) to overlay a grid that allows resizing windows by specifying their opposite corners.

```lua
Install:andUse("WindowGrid",
               {
                 config = { gridGeometries = { { "6x4" } } },
                 hotkeys = {show_grid = {hyper, "g"}},
                 start = true
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

The [UniversalArchive](http://www.hammerspoon.org/Spoons/UniversalArchive.html) spoon sets up a single key binding (`Ctrl-Cmd-a`) to archive the current item in Evernote, Mail and Outlook.

```lua
Install:andUse("UniversalArchive",
               {
                 config = {
                   evernote_archive_notebook = ".Archive",
                   outlook_archive_folder = "Archive (diego.zamboni@swisscom.com)",
                   archive_notifications = false
                 },
                 hotkeys = { archive = { { "ctrl", "cmd" }, "a" } }
               }
)
```

The [SendToOmniFocus](http://www.hammerspoon.org/Spoons/SendToOmniFocus.html) spoon sets up a single key binding (`Hyper-t`) to send the current item to OmniFocus from multiple applications.

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
                   s:registerApplication("Brave Browser Dev", { apptype = "chromeapp", itemname = "page" })
                 end
               }
)
```

The [EvernoteOpenAndTag](http://www.hammerspoon.org/Spoons/EvernoteOpenAndTag.html) spoon sets up some missing key bindings for note manipulation in Evernote.

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

The [TextClipboardHistory](http://www.hammerspoon.org/Spoons/TextClipboardHistory.html) spoon implements a clipboard history, only for text items. It is invoked with `Cmd-Shift-v`.

This is disabled for the moment as I experiment with BetterTouchTool's built-in clipboard history, which I have bound to the same key combination for consistency in my workflow.

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

The [Hammer](https://zzamboni.github.io/zzSpoons/Hammer.html) spoon (get it? hehe) is a simple wrapper around some common Hamerspoon configuration variables. Note that this gets loaded from my personal repo, since it's not in the official repository.

```lua
Install:andUse("Hammer",
               {
                 repo = 'zzspoons',
                 config = { auto_reload_config = false },
                 hotkeys = {
                   config_reload = {hyper, "r"},
                   toggle_console = {hyper, "y"}
                 },
                 fn = function(s)
                   BTT:bindSpoonActions(s,
                                        { config_reload = {
                                            kind = 'touchbarButton',
                                            uuid = "FF8DA717-737F-4C42-BF91-E8826E586FA1",
                                            name = "Restart",
                                            icon = hs.image.imageFromName(hs.image.systemImageNames.ApplicationIcon),
                                            color = hs.drawing.color.x11.orange,
                                        }
                   })
                 end,
                 start = true
               }
)
```

The [Caffeine](http://www.hammerspoon.org/Spoons/Caffeine.html) spoon allows preventing the display and the machine from sleeping. I use it frequently when playing music from my machine, to avoid having to unlock the screen whenever I want to change the music.

```lua
Install:andUse("Caffeine", {
                 start = true,
                 hotkeys = {
                   toggle = { hyper, "1" }
                 },
                 fn = function(s)
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
  print(hs.json.encode({ text = title, icon_data = BTT:hsimageToBTTIconData(icon) }))
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
})
```

The [MenubarFlag](http://www.hammerspoon.org/Spoons/MenubarFlag.html) spoon colorizes the menubar according to the selected keyboard language or layout (functionality inspired by [ShowyEdge](https://pqrs.org/osx/ShowyEdge/index.html.en)). I use English, Spanish and German, so those are the colors I have defined.

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

The [MouseCircle](http://www.hammerspoon.org/Spoons/MouseCircle.html) spoon shows a circle around the mouse pointer when triggered. I have it disabled for now because I have the macOS [shake-to-grow feature](https://support.apple.com/kb/PH25507?locale=en%5FUS&viewlocale=en%5FUS) enabled.

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

One of my original bits of Hammerspoon code, now made into a spoon (although I keep it disabled, since I don't really use it). The [ColorPicker](http://www.hammerspoon.org/Spoons/ColorPicker.html) spoon shows a menu of the available color palettes, and when you select one, it draws swatches in all the colors in that palette, covering the whole screen. You can click on any of them to copy its name to the clipboard, or cmd-click to copy its RGB code.

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
                   -- brew cask info
                   show_brew_cask_info = {hyper, "c"},
                   open_brew_cask_url = {shift_hyper, "c"},
                 }
               }
)
```

The [KSheet](http://www.hammerspoon.org/Spoons/KSheet.html) spoon traverses the current application's menus and builds a cheatsheet of the keyboard shortcuts, showing it in a nice popup window.

```lua
Install:andUse("KSheet",
               {
                 hotkeys = {
                   toggle = { hyper, "/" }
}})
```

The [TimeMachineProgress](http://www.hammerspoon.org/Spoons/TimeMachineProgress.html) spoon shows an indicator about the progress of the ongoing Time Machine backup. The indicator disappears when there is no backup going on.

```lua
Install:andUse("TimeMachineProgress",
               {
                 start = true
               }
)
```


## Other applications {#other-applications}

The [ToggleSkypeMute](http://www.hammerspoon.org/Spoons/ToggleSkypeMute.html) spoon sets up the missing keyboard bindings for toggling the mute button on Skype and Skype for Business. I'm not fully happy with this spoon - it should auto-detect the application instead of having separate keys for each application, and it could be extended to more generic use.

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

The [HeadphoneAutoPause](http://www.hammerspoon.org/Spoons/HeadphoneAutoPause.html) spoon implements auto-pause/resume for iTunes, Spotify and others when the headphones are unplugged.

```lua
Install:andUse("HeadphoneAutoPause",
               {
                 start = true
               }
)
```


## Seal {#seal}

The [Seal](http://www.hammerspoon.org/Spoons/Seal.html) spoon is a powerhouse - it implements a Spotlight-like launcher, but which allows for infinite configurability of what can be done or searched from the launcher window. I use Seal as my default launcher, triggered with `Cmd-space`, although I still keep Spotlight around under `Hyper-space`, mainly for its search capabilities.

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

The `useractions` Seal plugin allows me to define my own shortcuts. For example, a bookmark to the Hammerspoon documentation page:

```lua
["Hammerspoon docs webpage"] = {
  url = "https://hammerspoon.org/docs/",
  icon = hs.image.imageFromName(hs.image.systemImageNames.ApplicationIcon),
},
```

Or to manually trigger my work/non-work transition scripts (see below):

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

The `reconfigAdiumProxy` function uses AppleScript to tell Adium about the change without having to restart it - only if Adium is already running.

```lua
function reconfigAdiumProxy(proxy)
  --   hs.notify.show("Reconfiguring Adium", string.format("Proxy %s", (proxy and "enabled" or "disabled")), "")
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

The configuration for the WiFiTransitions spoon invoked these functions with the appropriate parameters.

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

I live in Switzerland, and my German is far from perfect, so the [PopupTranslateSelection](http://www.hammerspoon.org/Spoons/PopupTranslateSelection.html) spoon helps me a lot. It allows me to select some text and, with a keystroke, translate it to any of three languages using Google Translate. Super useful! Usually, Google's auto-detect feature works fine, so the `translate_to_<lang>` keys are sufficient. I have some `translate_<from>_<to>` keys set up for certain language pairs for when this doesn't quite work (I don't think I've ever needed them).

```lua
local wm=hs.webview.windowMasks
Install:andUse("PopupTranslateSelection",
               {
                 disable = true,
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

I am now testing [DeepLTranslate](http://www.hammerspoon.org/Spoons/DeepLTranslate.html), based on PopupTranslateSelection but which uses the [DeepL translator](https://www.deepl.com/en/translator).

```lua
Install:andUse("DeepLTranslate",
               {
                 config = {
                   popup_style = wm.utility|wm.HUD|wm.titled|wm.closable|wm.resizable,
                 },
                 hotkeys = {
                   translate = { hyper, "e" },
                 }
               }
)
```


## Leanpub integration {#leanpub-integration}

The Leanpub spoon provides monitoring of book build jobs.

```lua
Install:andUse("Leanpub",
               {
                 config = {
                   watch_books = {
                     -- api_key gets set in init-local.lua like this:
                     -- spoon.Leanpub.api_key = "my-api-key"
                     { slug = "learning-hammerspoon" },
                     { slug = "learning-cfengine" },
                     { slug = "zztestbook" },
                   }
                 },
                 start = true,
})
```


## Loading private configuration {#loading-private-configuration}

In `init-local.lua` I keep experimental or private stuff (like API tokens) that I don't want to publish in my main config. This file is not committed to any publicly-accessible git repositories.

```lua
local localfile = hs.configdir .. "/init-local.lua"
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
