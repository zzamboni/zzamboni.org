+++
title = "Bang-Bang (!!, !$) Shell Shortcuts in Elvish"
author = ["Diego Zamboni"]
summary = "How to set up the bash !! and !$ shortcuts for accessing the previous command in Elvish."
date = 2017-12-04T22:15:00+01:00
tags = ["elvish", "shell", "unix", "config"]
draft = false
creator = "Emacs 28.0.50 (Org mode 9.4 + ox-hugo)"
featured_image = "/images/elvish-logo.svg"
+++

(Updated on March 19th, 2018 to use the new [Elvish Package Manager](https://elvish.io/ref/epm.html))

The bash shortcuts (maybe older? I'm not sure in which shell these originated) for "last command" (`!!`) and "last argument of last command" (`!$`) are, for me at least, among the most strongly imprinted in my muscle memory, and I use them all the time. Although these shortcuts are not available in [Elvish](/post/elvish-an-awesome-unix-shell/) by default, they are easy to implement. I have written a module called [bang-bang](https://github.com/zzamboni/elvish-modules/blob/master/bang-bang.org) which you can readily use as follows:

-   Use [epm](https://elvish.io/ref/epm.html) to install my elvish-modules package (you can also add this to your `rc.elv` file to have the package installed automatically if needed):

    ```elvish
          use epm
          epm:install github.com/zzamboni/elvish-modules
    ```

-   In your `rc.elv` (see [mine](/post/my-elvish-configuration-with-commentary/) as an example), add the following to load the `bang-bang` module and to set up the appropriate keybindings:

    ```elvish
          use github.com/zzamboni/elvish-modules/bang-bang
    ```

That's it! Start a new shell window, and test how command-history mode can be invoked by the `!` key. Assuming your last command was `ls -l ~/.elvish/rc.elv`, when you press `!` you will see the following:

```text
  bang-lastcmd [A C] _
  ! ls -l .elvish/rc.elv
  0 ls
  1 -l
  2/$ .elvish/rc.elv
  Alt-! !
```

If you press `!` again, the whole last command will be inserted. If you press `$` (or `2`), only the last argument will be inserted. You can insert any other component of the previous command using its corresponding number. If you want to insert an exclamation sign, you can press `Alt-!`.

Note that by default, `Alt-!` will also be bound to trigger this mode, so you can fully replace the default ["last command" mode](https://elvish.io/learn/cookbook.html) in Elvish.

Have fun with Elvish!
