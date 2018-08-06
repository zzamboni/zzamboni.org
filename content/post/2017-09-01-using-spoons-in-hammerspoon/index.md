+++
title = "Using Spoons in Hammerspoon"
author = ["Diego Zamboni"]
summary = "In this second article about Hammerspoon, we look into _Spoons_, modules written in Lua which can be easily installed and loaded into Hammerspoon to provide ready-to-use functionality. Spoons provide a predefined API to configure and use them. They are also a good way to share your own work with other users."
date = 2017-09-01T17:55:00+02:00
tags = ["hammerspoon", "mac", "howto", "spoons"]
draft = false
creator = "Emacs 26.1 (Org mode 9.1.13 + ox-hugo)"
toc = true
featured_image = "/images/hammerspoon.png"
+++

In this second article about Hammerspoon, we look into _Spoons_, modules written in Lua which can be easily installed and loaded into Hammerspoon to provide ready-to-use functionality. Spoons provide a predefined API to configure and use them. They are also a good way to share your own work with other users.

See also the [first article in this series](/post/getting-started-with-hammerspoon/).


## Using a Spoon to locate your mouse {#using-a-spoon-to-locate-your-mouse}

As a first example, we will use the [MouseCircle](http://www.hammerspoon.org/Spoons/MouseCircle.html) spoon, which allows us to set up a hotkey that displays a color circle around the current location of the mouse pointer for a few seconds, to help you locate it.

To install the spoon, download its zip file from <https://github.com/Hammerspoon/Spoons/raw/master/Spoons/MouseCircle.spoon.zip>, unpack it, and double-click on the resulting `MouseCircle.spoon` file.  Hammerspoon will install the Spoon under `~/.hammerspoon/Spoons/`.

{{< figure src="mousecircle.png" >}}

Once a Spoon is installed, you need to use the `hs.loadSpoon()` function to load it. Type the following in the Hammerspoon console, or add it to your `init.lua` file and reload the configuration:

```lua
hs.loadSpoon("MouseCircle")
```

After a spoon is loaded, and depending on what it does, you may need to configure it, assign hotkeys, and start it. A spoon's API is available through the `spoon.<SpoonName>` namespace. To learn the API you need to look at the spoon documentation page. In the case of MouseCircle, a look at <http://www.hammerspoon.org/Spoons/MouseCircle.html> reveals that it has two methods (`bindHotkeys()` and `show()`) and one configuration variable (`color`) available under `spoon.MouseCircle`.

The first API call is `spoon.MouseCircle:bindHotkeys()`, which allows us to set up a hotkey that shows the mouse locator circle around the location of the mouse pointer. Let's say we wanted to bind the mouse circle to <kbd>Ctrl​-​⌘​-​Alt​-​d</kbd>. According to the MouseCircle documentation, the name for this action is `show`, so we can do the following:

```lua
spoon.MouseCircle:bindHotkeys({
  show = { { "ctrl", "cmd", "alt" }, "d" }
})
```

Once you do this, press the hotkey and you should see a red circle appear around the mouse cursor, and fade away after 3 seconds.

{{% tip %}}
All spoons which offer the possibility of binding hotkeys have to expose it through the same API:

```lua
spoon.SpoonName:bindHotkeys({ action1 = keySpec1,
                              action2 = keySpec2, ... })
```

Each `actionX` is a name defined by the spoon, which refers to something that can be bound to a hotkey, and each `keySpecX` is a table with two elements: a list of modifiers and the key itself, such as `{ { "ctrl", "cmd", "alt" }, "d" }`.
{{% /tip %}}

The second API call in the MouseCircle spoon is `show()`, which triggers the functionality of showing the locator circle directly. Let's try it -- type the following in the console:

```lua
spoon.MouseCircle:show()
```

Most spoons are structured like this: you can set up hotkeys to trigger the main functionality, but you can also trigger it via method calls.  Normally you won't use these methods, but their availability makes it possible for you to use spoon functionality from our own configuration, or from other spoons, to create further automation.

`spoon.MouseCircle.color` is a public configuration variable exposed by the spoon, which specifies the color that will be used to draw the circle. Colors are defined according to the documentation for the [`hs.drawing.color`](http://www.hammerspoon.org/docs/hs.drawing.color) module. Several color collections are supported, including the OS X system collections and a few defined by Hammerspoon itself. Color definitions are stored in Lua tables indexed by their name. For example, you can view the [`hs.drawing.color.hammerspoon`](http://www.hammerspoon.org/docs/hs.drawing.color#hammerspoon) table, including the color definitions, by using the convenient [`hs.inspect`](http://www.hammerspoon.org/docs/hs.inspect) method on the console:

```lua
> hs.inspect(hs.drawing.color.hammerspoon)
{
  black = {
    alpha = 1,
    blue = 0.0,
    green = 0.0,
    red = 0.0
  },
  green = {
    alpha = 1,
    blue = 0.0,
    green = 1.0,
    red = 0.0
  },
  osx_red = {
    alpha = 1,
    blue = 0.302,
    green = 0.329,
    red = 0.996
  },
  osx_green = {
...
```

{{% tip %}}

Lua does not include a function to easily get the keys of a table so you have to use the [`pairs()`](https://www.lua.org/manual/5.3/manual.html#pdf-pairs) function to loop over the key/value pairs of the table. The [`hs.inspect`](http://www.hammerspoon.org/docs/hs.inspect) function is convenient, but to get just the list of tables and the color names, without the color definitions themselves, you can use the following code (if you type this in the console you have to type it all in a single line -- and beware, the output is a long list):

```lua
for listname,colors in pairs(hs.drawing.color.lists()) do
  print(listname)
  for color,def in pairs(colors) do
    print("  " .. color)
  end
end
```

{{% /tip %}}

If we wanted to make the circle green, we can assign the configuration value like this:

```lua
spoon.MouseCircle.color = hs.drawing.color.hammerspoon.green
```

The next time you invoke the `show()` method, either directly or through the hotkey, you will see the circle in the new color.

{{% tip %}}

(We will look at this in more detail in a future installment about Lua, but in case you were wondering...)

You may have noticed that the configuration variable was accessed with a dot (`spoon.MouseCircle.color`), and we also used it for some function calls earlier (e.g. [`hs.notify.show`](http://www.hammerspoon.org/docs/hs.notify#show), whereas for the `show()` method we used a colon (`spoon.MouseCircle:show()`). The latter is Lua's object-method-call notation, and its effect is to pass the object on which the method is being called as an implicit first argument called `self`. This is simply a syntactic shortcut, i.e. the following two are equivalent:

```lua
spoon.MouseCircle:show()
spoon.MouseCircle.show(spoon.MouseCircle)
```

Note that in the second statement, we are calling the method using the dot notation, and explicitly passing the object as the first argument.  Normally you would use colon notation, but the alternative can be useful when constructing function pointers. For example, if you wanted to manually bind a second key to show the mouse circle, you might initially try to use the following:

```lua
hs.hotkey.bindSpec({ {"ctrl", "alt", "cmd" }, "p" },
                   spoon.MouseCircle:show)
```

But this results in an error. The correct way is to wrap the call in an anonymous function:

```lua
hs.hotkey.bindSpec({ {"ctrl", "alt", "cmd" }, "p" },
                   function() spoon.MouseCircle:show() end)
```

Alternatively, you can use the [`hs.fnutils.partial`](http://www.hammerspoon.org/docs/hs.fnutils#partial) function to construct a function pointer that includes the correct first argument:

```lua
hs.hotkey.bindSpec({ {"ctrl", "alt", "cmd" }, "p" },
                   hs.fnutils.partial(spoon.MouseCircle.show,
                                      spoon.MouseCircle))
```

This is more verbose than the previous example, but the technique can be useful sometimes. Although Lua is not a full functional language, it supports using functions as first-class values, and the [`hs.fnutils`](http://www.hammerspoon.org/docs/hs.fnutils) extension includes a number of functions that make it easy to use them.

{{% /tip %}}

By now you know enough to use spoons with Hammerspoon's native capabilities: [look for the ones you want](http://www.hammerspoon.org/Spoons/), download and install them by hand, and configure them in your `init.lua` using their configuration variables and API. In the next sections you will learn more about the minimum API of spoons, and how to install and configure spoons in a more automated way.


## The Spoon API {#the-spoon-api}

The advantage of using spoons is that you can count on them to adhere to a [defined API](https://github.com/Hammerspoon/hammerspoon/blob/master/SPOONS.md#api-conventions), which makes it easier to automate their use. Although each spoon is free to define additional variable and methods, the following are standard:

-   `SPOON:init()` is called automatically (if it exists) by [`hs.loadSpoon`](http://www.hammerspoon.org/docs/hs#loadSpoon) after loading the spoon, and can be used to initialize variables or anything else needed by the Spoon.

-   `SPOON:start()` should exist if the spoon requires any ongoing or background processes such as timers or watchers of any kind.

-   `SPOON:stop()` should exist if `start()` does, to stop any background processes that were started by `start()`.

-   `SPOON:bindHotkeys(map)` is exposed by spoons which allow binding hotkeys to certain actions. Its `map` argument is a Lua table with key/value entries of the following form: `ACTION = { MODS, KEY }`, where ACTION is a string defined by the spoon (multiple such actions can be defined), MODS is a list of key modifiers (valid values are `"cmd"`, `"alt"`, `"ctrl"` and `"shift"`), and KEY is the key to be bound, as shown in our previous example. All available actions for a spoon should be listed in its documentation.


## Automated Spoon installation and configuration {#automated-spoon-installation-and-configuration}

Once you develop a complex Hammerspoon configuration using spoons, you may start wondering if there is an easy way to manage them. There are no built-in mechanisms for automatically installing spoons, but you can use a spoon called [SpoonInstall](http://www.hammerspoon.org/Spoons/SpoonInstall.html) that implements this functionality. You can download it from <http://www.hammerspoon.org/Spoons/SpoonInstall.html>. Once installed, you can use it to declaratively install, configure and run spoons. For example, with SpoonInstall you can use the MouseCircle spoon as follows:

```lua
hs.loadSpoon("SpoonInstall")
spoon.SpoonInstall:andUse("MouseCircle", {
                  config = {
                     color = hs.drawing.color.osx_red,
                  },
                  hotkeys = {
                     show = { { "ctrl", "cmd", "alt"}, "d" }
                  }})
```

If the MouseCircle spoon is not yet installed, `spoon.SpoonInstall:andUse()` will automatically download and install it, and set its configuration variables and hotkeys according to the declaration.

If there is nothing to configure in the spoon, `spoon.SpoonInstall:andUse("SomeSpoon")` does exactly the same as `hs.loadSpoon("SomeSpoon")`. But if you want to set configuration variables, hotkey bindings or other parameters, the following keys are recognized in the map provided as a second parameter:

-   `config` is a Lua table containing keys corresponding to configuration variables in the spoon. In the example above, `config = { color = hs.drawing.color.osx_red }` has the same effect as setting `spoon.MouseCircle.color = hs.drawing.color.osx_red`

-   `hotkeys` is a Lua table with the same structure as the mapping parameter passed to the `bindHotkeys` method of the spoon. In our example above, `hotkeys = { show = { { "ctrl", "cmd", "alt"}, "d" } }` automatically triggers a call to `spoon.MouseCircle:bindHotkeys({ show = { { "ctrl", "cmd", "alt"}, "d" } })`.

-   `loglevel` sets the log level of the `logger` attribute within the spoon, if it exists. The valid values for this attribute are 'nothing', 'error', 'warning', 'info', 'debug', or 'verbose'.

-   `start` is a boolean value which indicates whether to call the Spoon's `start()` method (if it has one) after configuring everything else.

-   `fn` specifies a function which will be called with the freshly-loaded Spoon object as its first argument. This can be used to execute other startup or configuration actions that are not covered by the other attributes. For example, if you use the [Seal](http://www.hammerspoon.org/Spoons/Seal) spoon (a configurable launcher), you need to call its `loadPlugins()` method to specify which Seal plugins to use. You can achieve this with something like this:

    ```lua
    spoon.SpoonInstall:andUse("Seal",
      { hotkeys = { show = { {"cmd"}, "space" } },
        fn = function(s)
                 s:loadPlugins({"apps", "calc", "safari_bookmarks"})
             end,
             start = true,
      })
    ```

-   `repo` indicates the repository from where the Spoon should be installed if needed. Defaults to `"default"`, which indicates the official Spoon repository at <http://www.hammerspoon.org/Spoons/>. I keep a repository of unofficial Spoons at <http://zzamboni.org/zzSpoons/>, and others may be available by the time you read this.

-   `disable` can be set to `true` to disable the Spoon (easier than commenting it out when you want to temporarily disable a spoon) in your configuration.

{{% tip %}}

You can assign functions and modules to variables to improve readability of your code. For example, in my `init.lua` file I make the following assignment:

```lua
Install=spoon.SpoonInstall
```

Which allows me to write `Install:andUse("MouseCircle", …​ )`, which is shorter and easier to read.

{{% /tip %}}


### Managing repositories and spoons using SpoonInstall {#managing-repositories-and-spoons-using-spooninstall}

Apart from the `andUse()` "all-in-one" method, SpoonInstall has methods for specific repository- and spoon-maintenance operations. As of this writing, there are two Spoon repositories: the official one at <http://www.hammerspoon.org/Spoons/>, and my own at <http://zzamboni.org/zzSpoons/>, where I host some unofficial and in-progress Spoons.

The configuration variable used to specify repositories is `SpoonInstall.repos`. Its default value is the following, which configures the official repository identified as "default":

```lua
{
  default = {
      url = "https://github.com/Hammerspoon/Spoons",
      desc = "Main Hammerspoon Spoon repository",
  }
}
```

To configure a new repository, you can define an extra entry in this variable. The following code creates an entry named "zzspoons" for my Spoon repository:

```lua
spoon.SpoonInstall.repos.zzspoons = {
   url = "https://github.com/zzamboni/zzSpoons",
   desc = "zzamboni's spoon repository",
}
```

After this, both "zzspoons" and "default" can be used as values to the `repo` attribute in the `andUse()` method, and in any of the other methods that take a repository identifier as a parameter. You can find the full API documentation at <http://www.hammerspoon.org/Spoons/SpoonInstall.html>.


## Conclusion {#conclusion}

Spoons are a great mechanism for structuring your Hammerspoon configuration. If you want an example of a working configuration based almost exclusively on Spoons, you can view my own Hammerspoon configuration at <https://github.com/zzamboni/dot-hammerspoon>.
