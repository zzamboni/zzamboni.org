---
title: "Getting Started With Hammerspoon"
date: 2017-08-15T21:31:31+02:00
toc: true
draft: true
tags:
- hammerspoon
- howto
- mac
---

# What is Hammerspoon?

Hammerspoon is a Mac application maintained by Chris Jones and others,
which acts as a thin layer between the operating system and a
Lua-based configuration language. Hammerspoon includes extensions for
querying and controlling many aspects of the system. Some of the
lower-level extensions are written in Objective-C, but all of them
expose a Lua API, and it is trivial to write your own extensions or
modules (called "Spoons" in Hammerspoon) to extend its
functionality. From the Hammerspoon configuration you can also execute
external commands, run AppleScript or JavaScript code using the OSA
scripting framework, establish network connections and even run
network servers; you can capture and generate keyboard events, you can
detect network changes, USB or audio devices being plugged in or out,
changes in screen or keyboard language configuration; you can draw
directly on the screen to display whatever you want; and many other
things. Take a quick look at the [Hammerspoon API index
page](http://www.hammerspoon.org/docs/index.html) to get a feeling of
its extensive capabilities. And that is only the libraries that are
built into Hammerspoon. There is an extensive and growing [collection
of Spoons](http://www.hammerspoon.org/Spoons/), modules written in
pure Lua that provide additional functionality and integration. And of
course, you can write your own code. So let’s get started!

# Installing Hammerspoon

Hammerspoon is a regular Mac application. To install it by hand, you
just need to download it from
<https://github.com/Hammerspoon/hammerspoon/releases/latest>, unzip
the downloaded file and drag it to your /Applications folder (or
anywhere else you want).

If you are automation-minded like me, you probably use
[Homebrew](https://brew.sh/) and its plugin
[Cask](https://caskroom.github.io/) to manage your applications. If
this is the case, you can use Cask to install Hammerspoon:

```console
brew cask install hammerspoon
```

When you run Hammerspoon for the first time, you will see its icon
appear in the menubar, and a notification telling you that it couldn’t
find a configuration file. Let’s fix that!

{{< figure src="/ng/figures/hammerspoon-startup.png" title="Hammerspoon's icon and first-startup notificatoin" >}}

> **Tip**
>
> If you click on the initial notification, your web browser will open
> to the excellent [Getting Started with
> Hammerspoon](http://www.hammerspoon.org/go/) page, which I highly
> recommend you read for more examples.

# Your first Hammerspoon configuration

Let us start with a few simple examples. As tradition mandates, we
will start with a "Hello World" example. Open
`$HOME/.hammerspoon/init.lua` (Hammerspoon will create the directory
upon first startup, but you need to create the file) in your favorite
editor, and type the following:

```lua
hs.hotkey.bindSpec({ { "ctrl", "cmd", "alt" }, "h" }, 
   function() 
      hs.notify.show("Hello World!", "Welcome to Hammerspoon", "") 
   end)
```

Save the file, and from the Hammerspoon icon in the menubar, select
"Reload config". Apparently nothing will happen, but if you then press
Control-Alt-Command-h on your keyboard, you will see a notification on
your screen welcoming you to the world of Hammerspoon.

{{< figure src="/ng/figures/hammerspoon-hello-world.png" title="Hello World in Hammerspoon" >}}

Although it should be fairly self-explanatory, let us dissect this
example to give you a clearer understanding of its components:

All Hammerspoon built-in extensions start with `hs.` In this case,
`hs.hotkey` is the extension that handles keyboard bindings. You can
find its documentation at
<http://www.hammerspoon.org/docs/hs.hotkey.html>, where you will see
that it allows you to easily define which functions will be called in
response to different keyboard combinations. You can even
differentiate between the keys being pressed, released or held down if
you need to. The other extension used in this example is `hs.notify`,
which allows us to interact with the macOS Notification Center to
display, react and interact with notifications.

-   Within `hs.hotkey`, the `hs.hotkey.bindSpec()` function allows you
    to bind a function to a pressed key. Its first argument is a key
    specification which consists of a list (Lua lists and table
    literals are represented using curly braces) with two elements: a
    list of the key modifiers, and the key itself. In this example, `{
    { "ctrl", "cmd", "alt" }, "h" }` represent pressing
    Ctrl-Command-Alt-h.

-   The second argument to `bindSpec()` is the function to call when
    the key is pressed. Here we are defining an inline function, so it
    does not need a name.

-   The callback function uses `hs.notify.show()` to display the
    message.Take a quick look at the `hs.notify` documentation at
    <http://www.hammerspoon.org/docs/hs.notify.html> to get an idea of
    its extensive capabilities, including configuration of all aspects
    of a notification’s appearance and buttons, and the functions to
    call upon different user actions.

Try changing the configuration to display a different message or use a
different key. After every change, you need to instruct Hammerspoon to
reload its configuration, which you can do through its menubar item.

# Debugging tools and the Hammerspoon console

As you start modifying your configuration, errors will happen, as they
always do when coding. To help in development and debugging,
Hammerspoon offers a console window where you can see any errors and
messages printed by your Lua code as it executes, and also type code
to be evaluated. It is a very useful tool while developing your
Hammerspoon configuration.

To invoke the console, you normally choose "Console…​" from the
Hammerspoon menubar item. However, this is such a common operation,
that you might find it useful to also set a key combination for
showing the console. Most of Hammerspoon’s internal functionality is
also accessible through its API. In this case, looking at the
[documentation for the main `hs`
module](http://www.hammerspoon.org/docs/hs.html) reveals that there is
an `hs.toggleConsole()` function. Using the knowledge you’ve acquired
so far, you can easily configure a hotkey for opening and hiding the
console:

``` lua
hs.hotkey.bindSpec({ { "ctrl", "cmd", "alt" }, "y" },
                   hs.toggleConsole)
```

Once you reload your configuration, you should be able to use
Ctrl-Cmd-Alt-y to open and close the console. Any Lua code you type in
the Console will be evaluated in the main Hammerspoon context, so you
can add to your configuration directly from there. This is a good way
to incrementally develop your code before committing it to the
`init.lua` file.

You may have noticed by now another common operation while developing
Hammerspoon code: reloading the configuration, which you normally have
to do from the Hammerspoon menu. So why not set up a hotkey to do that
as well? Again, the `hs` module comes to our help with the
`hs.reload()` method:

``` lua
hs.hotkey.bindSpec({ { "ctrl", "cmd", "alt" }, "r" }, hs.reload)
```

Another useful development tool is the `hs` command, which you can run
from your terminal to get a Hammerspoon console. To install it, you
can use the `hs.ipc.cliInstall()` function, which you can just add to
your `init.lua` file to check and install the command every time
Hammerspoon runs.

> **Tip**
>
> `hs.ipc.cliInstall()` creates symlinks under `/usr/local/` to the
> `hs` command and its manual page file, located inside the
> Hammerspoon application bundle. Under some circumstances
> (particularly if you build Hammerspoon from source, or if you
> install different versions of it), you may end up with broken
> symlinks. If the `hs` command stops working and `cliInstall()`
> doesn’t fix it, look for broken symlinks left behind from old
> versions of Hammerspoon. Remove them and things should work again.

Now you have all the tools for developing your Hammerspoon
configuration. In the next installmente we will look at how you can
save yourself a lot of coding by using pre-made modules.
