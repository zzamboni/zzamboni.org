+++
title = "Just Enough Lua to Be Productive in Hammerspoon, Part 2"
author = ["Diego Zamboni"]
summary = "In this second article of the \"Just Enough Lua\" series, we dive into Lua's types and data structures."
date = 2017-11-01T08:16:00+01:00
tags = ["hammerspoon", "mac", "howto", "lua"]
draft = false
creator = "Emacs 26.3 (Org mode 9.3.2 + ox-hugo)"
toc = true
featured_image = "/images/lua-logo.svg"
+++

In this second article of the "Just Enough Lua" series, we dive into Lua's types and data structures.

{{% tip %}}
If you haven't already, be sure to read [the first installment of this series](/post/just-enough-lua-to-be-productive-in-hammerspoon-part-1/) to learn about the basic Lua concepts.
{{% /tip %}}


## Tables {#tables}

Table are the only compound data type in Lua, and are used to implement arrays, associative arrays (commonly called "maps" or "hashes" in other languages), modules, objects and namespaces. As you can see, it is very important to understand them!

A table in Lua is a collection of values, which can be indexed either by numbers or by arbitrary strings (the two types of indices can coexist within the same table). Let's go through a few examples that will give you an overview (you can type these in the Hammerspoon console as we go, or at the prompt of the `hs` command - keep in mind that some of the statements are broken across multiple lines here for formatting, but each statement should be type in a single line in the console).

Table literals are declared using curly braces:

```lua
> unicorns = {}  -- empty table
> people = { "Chris", "Aaron", "Diego" }  -- array
> handles = { Diego = "zzamboni",
              Chris = "cmsj",
              Aaron = "asmagill" } -- associative array
```

Indices are indicated using square brackets. Numeric indices start at 1 (not 0 as in most other languages). For identifier-like string indices, you can use the dot shortcut. Requesting a non-existent index returns `nil`:

```lua
> unicorns[1]
nil
> people[0]
nil
> people[1]
Chris
> handles['Diego']
zzamboni
> handles.Diego
zzamboni
> handles.Michael
nil
```

Within the curly-brace notation, indices that are not identifier-like (letters, numbers, underscores) need to be enclosed in quotes and square brackets. Values can be tables as well:

```lua
colors = { ["U.S."] = { "red", "white", "blue" },
           Mexico = { "green", "white", "red" },
           Germany = { "black", "red", "yellow" } }
```

With non-identifier indices, you cannot use the dot-notation. Also, to see a table within the Hammerspoon console, use [`hs.inspect`](https://www.hammerspoon.org/docs/hs.inspect):

```lua
> colors["U.S."]
table: 0x618000470400
> hs.inspect(colors.Mexico)
{ "green", "white", "red" }
> hs.inspect(colors)
{
  Germany = { "black", "red", "yellow" },
  Mexico = { "green", "white", "red" },
  ["U.S."] = { "red", "white", "blue" }
}
```

Iteration through an array is commonly done using the [`ipairs()`](https://www.lua.org/manual/5.3/manual.html#pdf-ipairs) functions. Note that it will only iterate through contiguous numeric indices starting at 1, so that it does not work well with "sparse" tables.

```lua
> for i,v in ipairs(people) do print(i, v) end
1   Chris
2   Aaron
3   Diego
> people[4]='John'
> for i,v in ipairs(people) do print(i, v) end
1   Chris
2   Aaron
3   Diego
4   John
> people[7]='Mike'
> for i,v in ipairs(people) do print(i, v) end
1   Chris
2   Aaron
3   Diego
4   John
> hs.inspect(people)
{ "Chris", "Aaron", "Diego", "John",
  [7] = "Mike"
}
```

The [`pairs()`](https://www.lua.org/manual/5.3/manual.html#pdf-pairs) function, on the other hand, will iterate through all the elements in the table (both numeric and string indices), but does not guarantee their order. Both numeric and string indices can be mixed in a single table (although this gets confusing quickly unless you access everything using [`pairs()`](https://www.lua.org/manual/5.3/manual.html#pdf-pairs)).

```lua
> for i,v in pairs(people) do print(i,v) end
1   Chris
2   Aaron
3   Diego
4   John
7   Mike
> for i,v in ipairs(handles) do print(i,v) end
<no output>
> for i,v in pairs(handles) do print(i,v) end
Aaron   asmagill
Diego   zzamboni
Chris   cmsj
> handles[1]='whoa'  -- assign the first numeric index
> hs.inspect(handles)
{ "whoa",
  Aaron = "asmagill",
  Chris = "cmsj",
  Diego = "zzamboni"
}
> for i,v in ipairs(handles) do print(i,v) end
1   whoa
```

The built-in [table](https://www.lua.org/manual/5.3/manual.html#6.6) module includes a number of useful table-manipulation functions, including the following:

-   [`table.concat()`](https://www.lua.org/manual/5.3/manual.html#pdf-table.concat) for joining the values of a list in a single string (equivalent to `join` in other languages). This only joins the elements that would be returned by [`ipairs()`](https://www.lua.org/manual/5.3/manual.html#pdf-ipairs).

    ```lua
    > table.concat(people, ", ")
    Chris, Aaron, Diego, John
    ```

-   [`table.insert()`](https://www.lua.org/manual/5.3/manual.html#pdf-table.insert) adds an element to a list, by default adding it to the end.

    ```lua
    > hs.inspect(people)
    { "Chris", "Aaron", "Diego", "John", "Bill",
      [7] = "Mike"
    }
    > table.insert(people, "George")
    > hs.inspect(people)
    { "Chris", "Aaron", "Diego", "John", "Bill", "George", "Mike" }
    ```

    Note how in the last example, the contiguous indices have finally caught up to 7, so the last element is no longer shown separately (and will now be included by [`ipairs()`](https://www.lua.org/manual/5.3/manual.html#pdf-ipairs), [`table.concat()`](https://www.lua.org/manual/5.3/manual.html#pdf-table.concat), etc.

-   [`table.remove()`](https://www.lua.org/manual/5.3/manual.html#pdf-table.remove) removes an element from a list, by default the last one. It returns the removed element.

    ```lua
    > for i=1,4 do print(table.remove(people)) end
    Mike
    George
    Bill
    John
    > hs.inspect(people)
    { "Chris", "Aaron", "Diego" }
    ```

Notable omissions from the language and the [table](https://www.lua.org/manual/5.3/manual.html#6.6) module are "get keys" and "get values" functions, common in other languages. This may be explained by the flexible nature of Lua tables, so that those functions would need to behave differently depending on the contents of the table. If you need them, you can easily build your own. For example, if you want to get a sorted list of the keys in a table, you can use this function:

```lua
function sortedkeys(tab)
  local keys={}
  for k,v in pairs(tab) do table.insert(keys, k) end
  table.sort(keys)
  return keys
end
```


## Tables as namespaces {#tables-as-namespaces}

Functions in Lua are first-class objects, which means they can be used like any other value. This means that functions can be stored in tables, and this is how namespaces (or "modules") are implemented in Lua. We can inspect an manipulate them like any other table. Let us look at the [table](https://www.lua.org/manual/5.3/manual.html#6.6) library itself. First, the module itself is a table:

```lua
> table
table: 0x61800046f740
```

Second, we can inspect its contents using the functions we know:

```lua
> hs.inspect(table)
{
  concat = <function 1>,
  insert = <function 2>,
  move = <function 3>,
  pack = <function 4>,
  remove = <function 5>,
  sort = <function 6>,
  sortedkeys = <function 7>,
  unpack = <function 8>
}
```

The function values themselves are opaque (we cannot see their code), but we can easily extend the module. For example, we could add our `sortedkeys()` function above to the `table` module for consistency. Lua allows us to specify the namespace of a function in its declaration:

```lua
function table.sortedkeys(tab)
  local keys={}
  for k,v in pairs(tab) do table.insert(keys, k) end
  table.sort(keys)
  return keys
end
```

All the Hammerspoon modules are implemented the same way:

```lua
> type(hs)
table
> type(hs.mouse)
table
> hs.inspect(hs.mouse)
{
  get = <function 1>,
  getAbsolutePosition = <function 2>,
  getButtons = <function 3>,
  getCurrentScreen = <function 4>,
  getRelativePosition = <function 5>,
  set = <function 6>,
  setAbsolutePosition = <function 7>,
  setRelativePosition = <function 8>,
  trackingSpeed = <function 9>
}
```

The common way of defining a new module in Lua is to create an empty table, and populate it with functions or variables as needed. For example, let's put our [double-click generator](/post/just-enough-lua-to-be-productive-in-hammerspoon-part-1/#functions) in a module. Create the file `~/.hammerspoon/doubleclick.lua` with the following contents:

```lua
local mod={}

mod.default_modifiers={}

function mod.leftDoubleClick(modifiers)
  modifiers = modifiers or mod.default_modifiers
  local pos=hs.mouse.getAbsolutePosition()
  hs.eventtap.event.newMouseEvent(
    hs.eventtap.event.types.leftMouseDown, pos, modifiers)
    :setProperty(hs.eventtap.event.properties.mouseEventClickState, 2)
    :post()
  hs.eventtap.event.newMouseEvent(
    hs.eventtap.event.types.leftMouseUp, pos, modifiers):post()
end

function mod.bindto(keyspec)
  hs.hotkey.bindSpec(keyspec, mod.leftDoubleClick)
end

return mod
```

You can then, from the console, do the following:

```lua
> doubleclick=require('doubleclick')
> doubleclick.bindto({ {"ctrl", "alt", "cmd"}, "p" })
19:53:53     hotkey: Disabled previous hotkey ⌘⌃⌥P
             hotkey: Enabled hotkey ⌘⌃⌥P
```

You have written and loaded your first Lua module. Let's try it out!  Press <kbd>Ctrl​-​⌘​-​Alt​-​p</kbd> while your cursor is over a word in your terminal or web browser, to select it as if you had double-clicked it. You can also change the modifiers used with it. For example, did you know that Cmd-double-click can be used to open URLs from the macOS Terminal application?

```lua
> doubleclick.default_modifiers={cmd=true}
```

Now try pressing <kbd>Ctrl​-​⌘​-​Alt​-​p</kbd> while your pointer is over a URL displayed on your Terminal (you can just type one yourself to test), and it will open in your browser.

Note that the name `doubleclick` does not have any special meaning---it is a regular variable to which you assigned the value returned by `require('doubleclick')`, which is the value of the `mod` variable created within the module file (note that within the module file you use the local variable name to refer to functions and variables within itself). You could assign it to any name you want:

```lua
> a=require('doubleclick')
> a.leftDoubleClick()
```

The argument of the [`require()`](https://www.lua.org/manual/5.3/manual.html#pdf-require) function is the name of the file to load, without the `.lua` extension. Hammerspoon by default adds your `~/.hammerspoon/` directory to its load path, along with any other default directories in your system. You can view the places where Hammerspoon will look for files by examining the `package.path` variable. On my machine I get the following:

```text
> package.path
/Users/zzamboni/.hammerspoon/?.lua;/Users/zzamboni/.hammerspoon/?/
init.lua;/Users/zzamboni/.hammerspoon/Spoons/?.spoon/init.lua;/usr/
local/share/lua/5.3/?.lua;/usr/local/share/lua/5.3/?/init.lua;/usr/
local/lib/lua/5.3/?.lua;/usr/local/lib/lua/5.3/?/init.lua;./?.lua;
./?/init.lua;/Users/zzamboni/Dropbox/Personal/devel/hammerspoon/
hammerspoon/build/Hammerspoon.app/Contents/Resources/extensions/?.lua;
/Users/zzamboni/Dropbox/Personal/devel/hammerspoon/hammerspoon/build/
Hammerspoon.app/Contents/Resources/extensions/?/init.lua
```

{{% tip %}}

Hammerspoon automatically loads any modules under the `hs` namespace the first time you use them. For example, when you use [`hs.application`](https://www.hammerspoon.org/docs/hs.application) for the first time, you will see a message in the console:

```lua
> hs.application.get("Terminal")
2017-10-31 06:47:15: -- Loading extension: application
hs.application: Terminal (0x61000044dfd8)
```

If you want to avoid these messages, you need to explicitly load the modules and assign them to variables, as follows:

```lua
> app=require('hs.application')
> app.get("Terminal")
hs.application: Terminal (0x610000e49118)
```

This avoids the console message and has the additional benefit of allowing you to use `app` (you can use whatever variable you want) instead of typing `hs.application` in your code. This is a matter of taste---I usually prefer to have the full descriptive names (makes the code easier to read), but when dealing with some of the longer module names (e.g. [`hs.distributednotifications`](https://www.hammerspoon.org/docs/hs.distributednotifications)), this technique can be useful.

{{% /tip %}}


## Patterns {#patterns}

If you are familiar with regular expressions, you know how powerful they are for examining and manipulating strings in any programming language.  Lua has [patterns](https://www.lua.org/manual/5.3/manual.html#6.4.1), which fulfill many of the same functions but have a different syntax and some limitations. They are used by many functions in the string library like [`string.find()`](https://www.lua.org/manual/5.3/manual.html#pdf-string.find) and [`string.match()`](https://www.lua.org/manual/5.3/manual.html#pdf-string.match).

The following are some differences and similarities you need to be aware of when using patterns:

-   The dot (`.`) represents any character, just like in regexes.

-   The asterisk (`*`), plus sign (`+`) and question mark (`?`) represent "zero or more", "one or more" and "one or none" of the previous character, just like in regexes. Unlike regexes, these characters can only be applied to a single character and not to a whole capture group (i.e. the regex `(foo)+` is not possible).

-   Alternations, represented by the vertical bar (`|`) in regexes, are not supported.

-   The caret (`^`) and dollar sign (`$`) represent "beginning of string" and "end of string", just like in regexes.

-   The dash (`-`) represents a non-greedy "zero or more" (i.e. match the shortest possible string instead of the longest one) of the previous character, unlike in regexes, in which it's commonly indicate by a question mark following the corresponding `*` or `+` The regex `.*?` is equivalent to the Lua pattern `.-`.

-   The escape character is the ampersand (`%`) instead of the backslash (`\`).

-   Most character classes are represented by the same characters, but preceded by ampersand. For example `%d` for digits, `%s` for spaces, `%w` for alphanumeric characters.

For most common use cases, Lua patterns are enough, you just have to be aware of their differences. If you encounter something that really cannot be done, you can always resort to libraries like [Lrexlib](http://rrthomas.github.io/lrexlib/), which provide interfaces to real regex libraries. Unfortunately these are not included in Lua, so you would need to install them on your own.

Patterns, just like regular expressions, are commonly used for string manipulation, using primarily functions from the [string](https://www.lua.org/manual/5.3/manual.html#6.4) library.


## String manipulation {#string-manipulation}

Lua includes the [string](https://www.lua.org/manual/5.3/manual.html#6.4) library to implement common string manipulation functions, including pattern matching. All of these functions can be called either as regular functions, with the string as the first argument, or as method calls on the string itself, using the colon syntax (which, as we saw [before](/post/just-enough-lua-to-be-productive-in-hammerspoon-part-1/#dot-vs-colon-method-access-in-lua), gets converted to the same call). For example, the following two are equivalent:

```lua
string.find(a, "^foo")
a:find("^foo")
```

You can find the full documentation in the [Lua reference manual](https://www.lua.org/manual/5.3/manual.html#6.4) and many other examples in the [Lua-users wiki String Library Tutorial](http://lua-users.org/wiki/StringLibraryTutorial). The following is a partial list of some of the functions I have found most useful:

-   [`string.find(str, pat, pos, plain)`](https://www.lua.org/manual/5.3/manual.html#pdf-string.find) finds the pattern within the string. By default the search starts at the beginning of the string, but can be modified with the `pos` argument (index starts at 1, as with the tables). By default `pat` is intepreted as a Lua pattern, but this can be disabled by passing `plain` as a true value. If the pattern is not found, returns `nil`.  If the pattern is found, the function returns the start and end position of the pattern within the string. Furthermore, if the pattern contains parenthesis capture groups, all groups are returned as well.  For example:

    ```lua
    > string.find("bah", "ah")
    2   3
    > string.find("bah", "foo")
    nil
    > string.find("bah", "(ah)")
    2   3   ah
    > p1, p2, g1, g2 = string.find("bah", "(b)(ah)")
    > p1,p2,g1,g2
    1   3   b   ah
    ```

    Note that the return value is not a table, but rather multiple values, as shown in the last example.

    {{% tip %}}

It can sometimes be convenient to handle multiple values as a table or as separate entities, depending on the circumstances. For example, you may have a programmatically-constructed pattern with a variable number of capture groups, so you cannot know to how many variables you need to assign the result. In this case, the [`table.pack()`](https://www.lua.org/manual/5.3/manual.html#pdf-table.pack) and [`table.unpack()`](https://www.lua.org/manual/5.3/manual.html#pdf-table.unpack) functions can be useful.

[`table.pack()`](https://www.lua.org/manual/5.3/manual.html#pdf-table.pack) takes a variable number of arguments and returns them in a table which contains an array component containing the values, plus an index `n` containing the total number of elements:

```lua
> res = table.pack(string.find("bah", "(b)(ah)"))
> res
table: 0x608000c76e80
> hs.inspect(res)
{ 1, 3, "b", "ah",
  n = 4
}
```

[`table.unpack()`](https://www.lua.org/manual/5.3/manual.html#pdf-table.unpack) does the opposite, expanding an array into separate values which can be assigned to separate values as needed, or passed as arguments to a function:

```lua
> args={"bah", "(b)(ah)"}
> string.find(args)
[string "return string.find(args)"]:1:
  bad argument #1 to 'find' (string expected, got table)
> string.find(table.unpack(args))
1   3   b   ah
```

{{% /tip %}}

-   [`string.match(str, pat, pos)`](https://www.lua.org/manual/5.3/manual.html#pdf-string.match) is similar to `string.find`, but it does not return the positions, rather it returns the part of the string matched by the pattern, or if the pattern contains capture groups, returns the captured segments:

    ```lua
    > string.match("bah", "ah")
    ah
    > string.match("bah", "foo")
    nil
    > string.match("bah", "(b)(ah)")
    b   ah
    ```

-   [`string.gmatch(str, pat)`](https://www.lua.org/manual/5.3/manual.html#pdf-string.gmatch) returns a function that returns the next match of `pat` within `str` every time it is called, returning `nil` when there are no more matches. If `pat` contains capture groups, they are returned on each iteration.

    ```lua
    > a="Hammerspoon is awesome!"
    > f=string.gmatch(a, "(%w+)")
    > f()
    Hammerspoon
    > f()
    is
    > f()
    awesome
    > f()
    ```

    Most commonly, this is used inside a loop:

    ```lua
    > for cap in string.gmatch(a, "%w+") do print(cap) end
    Hammerspoon
    is
    awesome
    ```

-   [`string.format(formatstring, …​)`](https://www.lua.org/manual/5.3/manual.html#pdf-string.format) formats a sequence of values according to the given format string, following the same formatting rules as the ISO C `sprintf()` function.  It additionally supports a new format character `%q`, which formats a string value in a way that can be read back by Lua, escaping or quoting characters as needed (for example quotes, newlines, etc.).

-   [`string.len(str)`](https://www.lua.org/manual/5.3/manual.html#pdf-string.len) returns the length of the string.

-   [`string.lower(str)`](https://www.lua.org/manual/5.3/manual.html#pdf-string.lower) and [`string.upper(str)`](https://www.lua.org/manual/5.3/manual.html#pdf-string.upper) convert the string to lower and uppercase, respectively.

-   [`string.gsub(str, pat, rep, n)`](https://www.lua.org/manual/5.3/manual.html#pdf-string.gsub) is a very powerful string-replacement function which hides considerably more power than its simple syntax would lead you to believe. In general, it replaces all (or the first `n`) occurrences of `pat` in `str` with the replacement `rep`. However, `rep` can take any of the following values:

    -   A string which is used for the replacement. If the string contains _%m_, where _m_ is a number, the it is replaced by the m-th captured group (or the whole match if _m_ is zero).

    -   A table which is consulted for the replacement values, using the first capture group as a key (or the whole match if there are no captures). For example:

        ```lua
        > a="Event type codes: leftMouseDown=$leftMouseDown, rightMouseDown=$rightMouseDown, mouseMoved=$mouseMoved"
        > a:gsub("%$(%w+)", hs.eventtap.event.types)
        Event type codes: leftMouseDown=1, rightMouseDown=3, mouseMoved=5   3
        ```

    -   A function which is executed with the captured groups (or the whole match) as an argument, and whose return value is used as the replacement. For example, using the `os.getenv` function, we can easily replace environment variables by their values in a string:

        ```lua
        > a="Hello $USER, your home directory is $HOME"
        > a:gsub("%$(%w+)", os.getenv)
        Hello zzamboni, your home directory is /Users/zzamboni  2
        ```

    Note that `gsub` returns the modified string as its first return value, and the number of replacements it made as the second (`2` in the example above). If you don't need the number, you can simply ignore it (you don't even need to assign it). Also note that `gsub` does not modify the original string, only returns a copy with the changes:

    ```lua
    > b = a:gsub("%$(%w+)", os.getenv)
    > b
    Hello zzamboni, your home directory is /Users/zzamboni
    > a
    Hello $USER, your home directory is $HOME
    ```


## Keep learning! {#keep-learning}

You know now enough Lua to start being productive with Hammerspoon.  You'll pick up more details as you play with it. If you need more information, I can recommend the following resources, which I have found useful:

-   [The Lua 5.3 Reference Manual](http://www.lua.org/manual/5.3/), available at the official [Lua website](http://www.lua.org).

-   [The Lua Wiki](http://lua-users.org/wiki/), a community-maintained wiki with many descriptions, tips, examples and tutorials.

Have fun!
