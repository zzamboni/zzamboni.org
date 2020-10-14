+++
title = "Just Enough Lua to Be Productive in Hammerspoon, Part 1"
author = ["Diego Zamboni"]
summary = "Hammerspoon's configuration files are written in Lua, so a basic knowledge of the language is very useful to be an effective user of Hammerspoon. In this two-part article I will show you the basics of Lua so you can read and write Hammerspoon configuration. Along the way you will discover that Lua is a surprisingly powerful language."
date = 2017-10-21T20:36:00+02:00
tags = ["hammerspoon", "mac", "howto", "lua"]
draft = false
creator = "Emacs 28.0.50 (Org mode 9.4 + ox-hugo)"
toc = true
featured_image = "/images/lua-logo.svg"
+++

Hammerspoon's configuration files are written in Lua, so a basic knowledge of the language is very useful to be an effective user of Hammerspoon. In this 2-part article I will show you the basics of Lua so you can read and write Hammerspoon configuration. Along the way you will discover that Lua is a surprisingly powerful language.

Lua is a scripting language created in 1993, and focused from the beginning in being an embedded language for extending other applications. It is easy to learn and use while having pretty powerful features, and is frequently used in games, but also in [many other applications](https://en.wikipedia.org/wiki/List%5Fof%5Fapplications%5Fusing%5FLua) including, of course, Hammerspoon.

The purpose of this section is to give you a quick overview of the Lua features and peculiarities you may find most useful for developing Hammerspoon policies. I assume you are a programmer who knows some other C-like language--if you already know C, Java, Ruby, Python, Perl, Javascript or some similar language, picking up Lua should be pretty easy. Instead of detailing every structure, I will focus on the aspects that are most different or that are most likely to trip you up as you learn it.


## Flow control {#flow-control}

Lua includes all the common flow-control structures you might expect.  Some examples:

```lua
  local info = "No package selected"
  if pkg and pkg ~= "" then
     info, st = hs.execute("/usr/local/bin/brew info " .. pkg)
     if st == nil then
        info = "No information found about formula '" .. pkg .. "'!"
     end
  end
```

In this example, in addition to the [if](https://www.lua.org/manual/5.3/manual.html#3.3.4) statement, you can see in the line that runs [`hs.execute`](https://www.hammerspoon.org/docs/hs#execute) that Lua functions can return multiple values (which is not the same as returning an array, which counts as a single value). Within the function, this is implemented simply by separating the values with commas in the `return` statement, like this: `return val1, val2`. You can also see in action the following operators:

-   `==` for equality;

-   `~=` for inequality (in this respect it differs from most C-like languages, which use `!=`);

-   `..` for string concatenation;

-   `and` for the logical AND operation (by extension, you can deduct that `or` and `not` are also available).

<!--listend-->

```lua
  local doReload = false
  for _,file in pairs(files) do
     if file:sub(-4) == ".lua" and (not string.match(file, '/[.]#')) then
        doReload = true
     end
  end
```

In this example we see the [for](https://www.lua.org/manual/5.3/manual.html#3.3.5) statement in its so-called _generic form_:

```lua
  for <var> in <expression> do <block> end
```

This statement loops the variables over the values returned by the expressions, executing the block with each the consecutive value until it becomes `nil`.

{{% tip %}}
Strictly speaking, `expression` is executed once and its value must be an _iterator function_, which returns one new value from the sequence every time it is called, returning `nil` at the end.
{{% /tip %}}

The `for` statement also has a _numeric form_:

```lua
  for <var> = <first>,<last>,<inc> do <block> end
```

This form loops the variable from the first to the last value, incrementing it by the given increment (defaults to 1) at each iteration.

Going back to our example, we can also learn the following:

-   The [`pairs()`](https://www.lua.org/manual/5.3/manual.html#pdf-pairs) function, which loops over a table. We will learn more about Lua tables below, but they can be used to represent both regular and associative arrays. `pairs()` treats the `files` variable as an associative array, and returns in each iteration a key/value pair of its contents.

-   The `_` variable, while not special per se, is used by convention in Lua for "throwaway values". In this case we are not interested in the key in each iteration, just the value, so we assign the key to `_`, never to be used again.

-   Our first glimpse into the Lua [string library](https://www.lua.org/manual/5.3/manual.html#6.4), and the two ways in which it can be used:
    -   In `file:sub(-4)`, the colon indicates the object-oriented notation (see "Lua dot-vs-colon method access" below). This invokes the [`string.sub()`](https://www.lua.org/manual/5.3/manual.html#pdf-string.sub) function, automatically passing the `file` variable as its first argument. This statement is equivalent to `string.sub(file, -4)`.

    -   In `string.match(file, '/')`, we see the function notation used to call [`string.match()`](https://www.lua.org/manual/5.3/manual.html#pdf-string.match). Since the `file` variable is being passed as the first argument, you could rewrite this statement as `file:match('/[.]')`. In practice, I've found myself using both notations somewhat exchangeably - feel free to use whichever you find most comfortable.


## Dot-vs-colon method access in Lua {#dot-vs-colon-method-access-in-lua}

You will notice that sometimes, functions contained within a module are called with a dot, and others with a colon. The latter is Lua's object-method-call notation, and its effect is to pass the object on which the method is being called as an implicit first argument called `self`. This is simply a syntactic shortcut, i.e. the following two are equivalent:

```lua
  file:match('/[.]')
  string.match(file, '/')
```

Note that in the second statement, we are calling the method using the dot notation, and explicitly passing the object as the first argument.  Normally you would use colon notation, but when you need a function pointer, you need to use the dot notation.


## Functions {#functions}

Functions are defined using the `function` keyword.

```lua
  function leftDoubleClick(modifiers)
     local pos=hs.mouse.getAbsolutePosition() -- <1>
     hs.eventtap.event.newMouseEvent(
       hs.eventtap.event.types.leftMouseDown, pos, modifiers) -- <2>
        :setProperty(hs.eventtap.event.properties.mouseEventClickState, 2)
        :post() -- <3>
     hs.eventtap.event.newMouseEvent( -- <4>
       hs.eventtap.event.types.leftMouseUp, pos, modifiers):post()
  end
```

In this example we can also see some examples of the Hammerspoon library in action, in particular two extremely powerful libraries: [`hs.mouse`](https://www.hammerspoon.org/docs/hs.mouse) for interacting with the mouse pointer, and [`hs.eventtap`](https://www.hammerspoon.org/docs/hs.eventtap), which allows you to both intercept and generate arbitrary system events, including key pressed and mouse clicks. This function simulates a double click on the current pointer position:

1.  We first get the current position of the mouse pointer using [`hs.mouse.getAbsolutePosition`](https://www.hammerspoon.org/docs/hs.mouse#getAbsolutePosition).

2.  We create a new mouse event of type [`leftMouseDown`](https://www.hammerspoon.org/docs/hs.eventtap.event#types) in the obtained coordinates and with the given modifiers.

3.  By convention, most Hammerspoon API methods return the same object on which they operate. This allows us to chain the calls as shown: `setProperty()` is called on the `hs.eventtap` object returned by `newMouseEvent` to set its type to a double click, and `post()` is called on the result to issue the event.

4.  Since we are generating system events directly, we also need to take care of generating a "mouse up" event at the end.

Function parameters are always optional, and those not passed will default to `nil`, so you need to do proper validation. In this example, the function can be called as `leftDoubleClick()`, without any parameters, which means the `modifiers` parameter might have a `nil` value. Looking at the [documentation for `newMouseEvent()`](https://www.hammerspoon.org/docs/hs.eventtap.event#newMouseEvent), we see that the parameter is optional, so for this particular function our use is OK.

You should try this function to see that it works. Adding it to you `~/.hammerspoon/init.lua` function will make Hammerspoon define it the next time you reload your configuration. You could then try calling it from the console, but the easiest is to bind a hotkey that will generate a double click. For example:

```lua
  hs.hotkey.bindSpec({ { "cmd", "ctrl", "alt" }, "p" },
                     leftDoubleClick)
```

Once you reload your config, you can generate a double click by moving the cursor where you want it and pressing <kbd>Ctrl​-​⌘​-​Alt​-​p</kbd>. While this is a contrived example, the ability to generate events like this is immensely powerful in automating your system.

{{% tip %}}

By now you have seen that we are using <kbd>Ctrl​-​⌘​-​Alt</kbd> very frequently in our keybindings. To avoid having to type this every time, and since the modifiers are defined as an array, you can define them as variable. For example, I have the following at the top of my `init.lua`:

```lua
  hyper = {"cmd","alt","ctrl"}
  shift_hyper = {"cmd","alt","ctrl","shift"}
```

Then I simply use `hyper` or `shift_hyper` in my key binding declarations:

```lua
  hs.hotkey.bindSpec({ hyper, "p" }, leftDoubleClick)
```

{{% /tip %}}


## Until next time! {#until-next-time}

In the [next installment](/post/just-enough-lua-to-be-productive-in-hammerspoon-part-2/), we will dive into Lua's types and data structures. In the meantime, feel free to explore and learn on your own. If you need more information, I can recommend the following resources, which I have found useful:

-   [The Lua 5.3 Reference Manual](http://www.lua.org/manual/5.3/), available at the official [Lua website](http://www.lua.org).

-   [The Lua Wiki](http://lua-users.org/wiki/), a community-maintained wiki with many descriptions, tips, examples and tutorials.
