+++
title = "Using and writing completions in Elvish"
author = ["Diego Zamboni"]
summary = "Like other Unix shells, Elvish has advanced command-argument completion capabilities. In this article I will explore the existing completions, and show you how you can create your own (and contribute them back to the community!)"
date = 2018-06-13T20:25:00+02:00
tags = ["elvish", "shell", "completions", "unix", "config"]
draft = false
creator = "Emacs 26.2 (Org mode 9.2.3 + ox-hugo)"
toc = true
featured_image = "/images/elvish-logo.svg"
+++

Like other Unix shells, [Elvish](https://elvish.io/) has advanced command-argument completion capabilities. In this article I will explore the existing completions, and show you how you can create your own (and contribute them back to the community).


## Using existing completions {#using-existing-completions}

There is a growing body of shell completions that you can simply load and use.

Elvish has a still-small but growing collection of completions that have been created by its users. These are a few that I know of (let me know if you know others!):

-   My own [zzamboni/elvish-completions](https://github.com/zzamboni/elvish-completions) package, which contains completions for [git](https://github.com/zzamboni/elvish-completions/blob/master/git.org) (providing automatically-generated completions for all commands and their options, plus hand-crafted argument completions for many of them), [ssh](https://github.com/zzamboni/elvish-completions/blob/master/ssh.org), [vcsh](https://github.com/zzamboni/elvish-completions/blob/master/vcsh.org), [cd](https://github.com/zzamboni/elvish-completions/blob/master/cd.org), and a few of Elvish's [built-in functions and modules](https://github.com/zzamboni/elvish-completions/blob/master/builtins.org). It also contains [comp](https://github.com/zzamboni/elvish-completions/blob/master/comp.org), a framework for building completers, which we will explore in more detail below. To use any of these modules, you just need to install the elvish-completions package, and then load the modules you want. For example:

    ```elvish
    epm:install &silent-if-installed github.com/zzamboni/elvish-completions
    use github.com/zzamboni/elvish-completions/vcsh
    use github.com/zzamboni/elvish-completions/cd
    use github.com/zzamboni/elvish-completions/ssh
    use github.com/zzamboni/elvish-completions/builtins
    use github.com/zzamboni/elvish-completions/git
    ```
-   xiaq's [edit.elv/compl/go.elv](https://github.com/xiaq/edit.elv/blob/master/compl/go.elv), which provides extensive hand-crafted completions for `go`. You can also install this one as an Elvish package:

    ```elvish
    epm:install &silent-if-installed github.com/xiaq/edit.elv
    use github.com/xiaq/edit.elv/compl/go
    go:apply
    ```
-   occivink's [completers.elv](https://github.com/occivink/config/blob/master/.elvish/lib/completers.elv) file, which contains completers for `kak`, `ssh`, `systemctl`, `ffmpeg` and a few other commands.
-   Tw's [completer/](https://github.com/tw4452852/MyConfig/tree/master/config/.elvish/lib/completer) files, which contains completions for `adb`, `git` and `ssh`.
-   SolitudeSF's [completers.elv](https://github.com/SolitudeSF/dot/blob/master/elvish/lib/completers.elv) file, which contains completers for `cd`, `kak`, `kitty`, `git`, `man`, `pkill` and quite a few other commands.

As of this writing, there is no "official" collection of Elvish completions, so feel free to look at the existing ones and choose/use the ones that work best for you.

Since the collection is not yet very big, it's likely you will want to build your own completions. This is what the next section is about.


## Creating your own completions {#creating-your-own-completions}

Elvish has a simple but powerful argument-completion mechanism. You can find the full documentation [in the Elvish reference](https://elvish.io/ref/edit.html#completion-api), but let's take a quick look here.


### Basic (built-in) argument completion mechanisms {#basic--built-in--argument-completion-mechanisms}

Command argument completion in Elvish is implemented by functions stored inside `$edit:completion:arg-completer`. This variable is a map in which the indices are command names, and the values are functions which must receive a variable number of arguments. When the user types `cat` <kbd>Space</kbd> <kbd>Tab</kbd>, the function stored in `$edit:completion:arg-completer[cat]` (if any) is called, as follows:

```elvish
$edit:completion:arg-completer[cat] cat ''
```

The function receives the full current command line as arguments, including the current argument, which might be empty as in the example above, or be a partially typed string. For example, if the user types `cat f` <kbd>Tab</kbd>, the completer function will be called like this:

```elvish
$edit:completion:arg-completer[cat] cat 'f'
```

The completion function must use its arguments to determine the appropriate completions at that point, and return them by one of the following methods (which can be combined):

-   Output the completions to stdout, one per line;
-   Output the completions to the data stream (using `put`);
-   Output the completions using the `edit:complex-candidate` command, which can additionally specify a suffix to append to the completion in the completion menu or in the returned value, and a style to use (as accepted by `edit:styled`). The full syntax of `edit:complex-candidate` is as follows:

    ```elvish
    edit:complex-candidate &code-suffix='' &display-suffix='' &style='' $string
    ```

    `$string` is the option to display; `&code-suffix` indicates a suffix to be appended to the completion string when the user selects it; `&display-suffix` indicates a suffix to be shown in the completion menu (but which is not returned as part of the completion); and `&style` indicates a text style to use in the completion menu.

Keep in mind that the options returned by the completion function are additionally filtered by what the user has typed so far. This means that the last argument can usually be ignored, since Elvish will automatically do the filtering. An exception to this is if you want to return different _types of things_ depending on what the user has typed already. For example, if the last argument start with `-`, you may want to return the possible command-line options, and return regular argument completions otherwise.

**Example #1:** A very simple completer for the `brew` command:

```elvish
edit:completion:arg-completer[brew] = [@cmd]{
  len = (count $cmd)
  if (eq $len 2) {
    if (has-prefix $cmd[-1] -) {
      put '--version' '--verbose'
    } else {
      put install uninstall
    }
  } elif (eq $len 3) {
    brew search | eawk [l @f]{ put $@f }
  }
}
```

If the function receives two arguments, we check to see if the last argument begins with a dash. If so, we return the possible command-line options, otherwise we return the two commands `install` and `uninstall`. If we receive three arguments (i.e. we are past the initial command), we return the list of possible packages to install or uninstall.

You may noticed that there are many cases that this simple function does not handle correctly. For example, if you type `brew --verbose` <kbd>Space</kbd> <kbd>Tab</kbd>, you get the list of packages as completion, which does not make sense at that point. We will look at more complex and complete completion functions next.

The first step to more complex completions is the `edit:complete-getopt` command, which allows us to specify a sequence of positional completion functions. The general syntax of the command is:

```elvish
edit:complete-getopt $args $opts $handlers
```

Please see [its documentation](https://elvish.io/ref/edit.html#editcomplete-getopt) for a full description of the arguments.

**Example #2:** The completer for `brew` shown before can be specified like this:

```elvish
edit:completion:arg-completer[brew] = [@cmd]{
  edit:complete-getopt $cmd[1:] \
  [[&long=version] [&long=verbose]] \
  [
    [_]{ put install uninstall }
    [_]{ brew search | eawk [_ @f]{ put $@f } }
    ...
  ]
}
```

This new completer overcomes a few of the limitations in our previous attempt. For one, the `install` and `uninstall` commands are now properly completed even if you specify options before. Furthermore, the `...` at the end of the handler list indicates that the previous one (the package names) will be repeated for all further arguments - this makes it possible to complete multiple package names to install or uninstall. However, it still has some limitations! For example, it will give you all existing packages as possible arguments to `uninstall`, which only accepts already installed packages.

In addition to `complete-getopt`, Elvish includes a few other functions to help build completers:

-   `edit:complete-filename` produces a listing of all the files and directories in the directory of its argument, and is the default completion function when no other completer is specified. See its [documentation](https://elvish.io/ref/edit.html#editcomplete-filename) for full details.
-   `edit:complete-sudo` provides completions for commands like `sudo` which take a command as their first argument. It is the default completer for the `sudo` command, so that if you type `sudo` <kbd>Space</kbd> <kbd>Tab</kbd>, you get a list of all the commands on your execution path. It can be reused for other commands, for example `time`:

    ```elvish
    edit:completion:arg-completer[time] = $edit:complete-sudo~
    ```

Finally, note that if `$edit:completion:arg-completer['']` exists, it will be called as a fall-back completer if no command-specific argument completer exists. You can see that the default completer is `edit:complete-filename`, as mentioned before:

```elvish
~> put $edit:completion:arg-completer['']
▶ $edit:complete-filename~
```

With the tools you know so far, you can already create fairly complex completers. In the next section, we will explore `comp`, an external library I wrote to make it easier to specify complex completion trees.


### Complex completions using the `comp` framework {#complex-completions-using-the-comp-framework}

The built-in completion functions make it possible to build any completer you want. However, you might realize that for more complex cases, the specifications can be quite complex. For this reason, I wrote [the `comp` library](https://github.com/zzamboni/elvish-completions/blob/master/comp.org) as a framework to more easily specify completion functions. The basic Elvish mechanisms and functions are still used in the backend, so you can rest assured about their compatibility with the basic mechanisms.

As a first step, if you haven't done so already, you should install the `elvish-completions` package using [epm](https://elvish.io/ref/epm.html):

```elvish
use epm
epm:install github.com/zzamboni/elvish-completions
```

From the file where you will define your completions (or from your interactive session if you just want to play with it), load the `comp` module:

```elvish
use github.com/zzamboni/elvish-completions/comp
```

The main entry points for this module are `comp:item`, `comp:sequence` and `comp:subcommands`. Each one receives a single argument containing a  "completion definition", which indicates how the completions will be produced. Each one receives a different kind of completion structure, and returns a ready-to-use completion function, which can be assigned directly to an element of `$edit:completion:arg-completer`. A simple example:

```elvish
edit:completion:arg-completer[foo] = (comp:item [ bar baz ])
```

If you type this in your terminal, and then type `foo<space>` and press <kbd>Tab</kbd>, you will see the appropriate completions:

```text
> foo <Tab>
 COMPLETING argument _
 bar  baz
```

To create completions for new commands, your main task is to define the corresponding completion definition. The different types of definitions and functions are explained below, with examples of the different available structures and features.

**Note:** the main entry points return a ready-to-use argument handler function. If you ever need to expand a completion definition directly (maybe for some advanced usage), you can call `comp:-expand-item`, `comp:-expand-sequence` and `comp:-expand-subcommands`, respectively. These functions all take the definition structure and the current command line, and return the appropriate completions at that point.

We now look at the different types of completion definitions understood by `comp`.


#### Items {#items}

The base building block is the "item", can be one of the following:

-   An array containing all the potential completions (it can be empty, in which case no completions are provided). This is useful for providing a static list of completions.
-   A function which returns the potential completions (it can return nothing, in which case no completions are provided). The function should have one of the following arities, which affect which arguments will be passed to it (other arities are not valid, and in that case the item will not be executed):
    -   If it takes no arguments, no arguments are passed to it.
    -   If it takes a single argument, it gets the current (last) component of the command line `@cmd`; this is just like the handler functions understood by the `edit:complete-getopt` command.
    -   If it takes a rest argument, it gets the full current command line (the contents of `@cmd`); this is just like the functions assigned to `$edit:completion:arg-completer`.

**Example #3:** a simple completer for `cd`

In this case, we define a function which receives the current "stem" (the part of the filename the user has typed so far) and offers all the relevant files, then filters those which are directories, and returns them as completion possibilities. We pass the function directly as a completion item to `comp:-expand`.

```elvish
fn complete-dirs [arg]{ put {$arg}* | each [x]{ if (-is-dir $x) { put $x } } }
edit:completion:arg-completer[cd] = (comp:item $complete-dirs~)
```

For file and directory completion, you can use the utility function `comp:files` instead of defining your own function (see [Utility functions](#utility-functions)). `comp:files` uses `edit:complete-filename` in the backend but offers a few additional filtering options:

```elvish
edit:completion:arg-completer[cd] = (comp:item [arg]{ comp:files $arg &dirs-only })
```


#### Sequences and command-line options {#sequences-and-command-line-options}

Completion items can be aggregated in a _sequence of items_ and used with the `comp:sequence` function when you need to provide different completions for different positional arguments of a command, including support for command-line options at the beginning of the command (`comp:sequence` uses `edit:complete-getopt` in the backend, but provides a few additional convenient features). The definition structure in this case has to be an array of items, which will be applied depending on their position within the command parameter sequence. If the the last element of the list is the string `...` (three periods), the next-to-last element of the list is repeated for all later arguments. If no completions should be provided past the last argument, simply omit the periods. If a sequence should produce no completions at all, you can use an empty list `[]`. If any specific elements of the sequence should have no completions, you can specify `{ comp:empty }` or `[]` as its value.

If the `&opts` option is passed to the `comp:sequence` function, it must contain a single definition item which produces a list of command-line options that are allowed at the beginning of the command, when no other arguments have been provided. Options can be specified in either of the following formats:

-   As a string which gets converted to a long-style option; e.g. `all` to specify the `--all` option. The string must not contain the dashes at the beginning.
-   As a map in the style of `complete-getopt`, which may contain the following keys:
    -   `short` for the short one-letter option;
    -   `long` for the long-option string;
    -   `desc` for a descriptive string which gets shown in the completion menu;
    -   `arg-mandatory` or `arg-optional`: either one but not both can be set to `$true` to indicate whether the option takes a mandatory or optional argument;
    -   `arg-completer` can be specified to produce completions for the option argument. If specified, it must contain completion item as described in [Items](#items), and which will be expanded to provide completions for that argument's values.

Simple example of a completion data structure for option `-t` (long form `--type`), which has a mandatory argument which can be `elv`, `org` or `txt`:

```text
[ &short=t
  &long=type
  &desc="Type of file to show"
  &arg-mandatory=$true
  &arg-completer= [ elv org txt ]
]
```

**Note:** options are only offered as completions when the use has typed a dash as the first character. Otherwise the argument completers are used.

**Example #4:** we can improve on the previous completer for `cd` by preventing more than one argument from being completed (only the first argument will be completed using `complete-dirs`, since the list does not end with `...`):

```elvish
edit:completion:arg-completer[cd] = (comp:sequence [ [arg]{ comp:files $arg &dirs-only }])
```

**Example #5:** a simple completer for `ls` with a subset of its options. Note that `-l` and `-R` are only provided as completions when you have not typed any filenames yet. Also note that we are using [comp:files](#utility-functions) to provide the file completions, and the `...` at the end of the sequence to use the same completer for all further elements.

```elvish
ls-opts = [
  [ &short=l                 &desc='use a long listing format' ]
  [ &short=R &long=recursive &desc='list subdirectories recursively' ]
]
edit:completion:arg-completer[ls] = (comp:sequence &opts=$ls-opts [ $comp:files~ ... ])
```

**Example #6:** See the [ssh completer](https://github.com/zzamboni/elvish-completions/blob/master/ssh.org) for a real-world example of using sequences.


#### Subcommands {#subcommands}

Finally, completion sequences can be aggregated into _subcommand structures_ using the `comp:subcommands` function, to provide completion for commands such as `git`, which accept multiple subcommands, each with their own options and completions. In this case, the definition is a map indexed by subcommand names. The value of each element can be a `comp:item`,  a `comp:sequence` or another `comp:subcommands` (to provide completion for sub-sub-commands, see the example below for `vagrant`). The `comp:subcommands` function can also receive the `&opts` option to generate any available top-level options.

**Example #7:** let us reimplement our completer for the `brew` package manager, but now with support for the `install`, `uninstall` and `cat` commands. `install` and `cat` gets as completions all available packages (the output of the `brew search` command), while `uninstall` only completes installed packages (the output of `brew list`). Note that for `install` and `uninstall` we automatically extract command-line options from their help messages using the `comp:extract-opts` function (wrapped into the `-brew-opts` function), and pass them as the `&opts` option in the corresponding sequence functions. Also note that all `&opts` elements get initialized at definition time (they are arrays), whereas the sequence completions get evaluated at runtime (they are lambdas), to automatically update according to the current packages. The `cat` command sequence allows only one option. The load-time initialization of the options incurs a small delay, and you could replace these with lambdas as well so that the options are computed at runtime. Note also the usage of the `comp:decorate` function to colorize the package names in different colors for each command.

```elvish
fn -brew-opts [cmd]{
  brew $cmd -h | take 1 | \
  comp:extract-opts &regex='--(\w[\w-]*)' &regex-map=[&long= 1]
}
brew-completions = [
  &install= (comp:sequence &opts= [ (-brew-opts install) ] \
    [ { brew search | comp:decorate &style=green } ... ]
  )
  &uninstall= (comp:sequence &opts= [ (-brew-opts uninstall) ] \
    [ { brew list | comp:decorate &style=red }   ... ]
  )
  &cat= (comp:sequence [{ brew search | comp:decorate &style=blue }])
]
edit:completion:arg-completer[brew] = (comp:subcommands \
  &opts= [ version verbose ] $brew-completions
)
```

Note that in contrast to our previous `brew` completer, this definition is much more expressive, accurate, and much easier to extend.

**Example #8:** a simple completer for a subset of `vagrant`, which receives commands which may have subcommands and options of their own. Note that the value of `&up` is a `comp:sequence`, but the value of `&box` is another `comp:subcommands` which includes the completions for `box add` and `box remove`. Also note the use of the `comp:extract-opts` function to extract the command-line arguments automatically from the help messages. The output of the `vagrant` help messages matches the default format expected by `comp:extract-opts`, so we don't even have to specify a regular expression like for `brew`.

**Tip:** note that the values of `&opts` are functions (e.g. `{ vagrant-up -h | comp:extract-opts }`) instead of arrays (e.g. `( vagrant up -h | comp:extract-opts )`). As mentioned in the previous example, both are valid, but in the latter case they are all initialized at load time (when the data structure is defined), which might introduce a delay, particularly with more command definitions. By using functions the options are only extracted at runtime when the completion is requested. For further optimization, `vagrant-opts` could be made to memoize the values so that the delay only occurs the first time.

```elvish
vagrant-completions = [
  &up= (comp:sequence [] \
    &opts= { vagrant up -h | comp:extract-opts }
  )
  &box= (comp:subcommands [
      &add= (comp:sequence [] \
        &opts= { vagrant box add -h | comp:extract-opts }
      )
      &remove= (comp:sequence [ { \
            vagrant box list | eawk [_ @f]{ put $f[0] } \
        } ... ] \
        &opts= { vagrant box remove -h | comp:extract-opts }
      )
])]

edit:completion:arg-completer[vagrant] = (comp:subcommands \
  &opts= [ version help ] $vagrant-completions
)
```

**Example #9:** See the [git completer](https://github.com/zzamboni/elvish-completions/blob/master/git.org) for a real-world subcommand completion example, which also shows how extensively auto-population of subcommands and options can be done by extracting information from help messages.


#### Utility functions {#utility-functions}

The `comp` module includes a few utility functions, some of which you have seen already in the examples.

`comp:decorate` maps its input through `edit:complex-candidate` with the given options. Can be passed the same options as [edit:complex-candidate](https://elvish.io/ref/edit.html#argument-completer). In addition, if `&suffix` is specified, it is used to set both `&display-suffix` and `&code-suffix`. Input can be given either as arguments or through the pipeline:

```elvish
> comp:decorate &suffix=":" foo bar
▶ (edit:complex-candidate foo &code-suffix=: &display-suffix=: &style='')
▶ (edit:complex-candidate bar &code-suffix=: &display-suffix=: &style='')
> put foo bar | comp:decorate &style="red"
▶ (edit:complex-candidate foo &code-suffix='' &display-suffix='' &style=31)
▶ (edit:complex-candidate bar &code-suffix='' &display-suffix='' &style=31)
```

`comp:extract-opts` takes input from the pipeline and extracts command-line option data structures from its output. By default it understand the following common formats:

```text
-o, --option                Option description
-p, --print[=<what>]        Option with an optional argument
    --select <type>         Option with a mandatory argument
```

Typical use would be to populate an `&opts` element with something like this:

```elvish
comp:sequence &opts= { vagrant -h | comp:extract-opts } [ ... ]
```

The regular expression used to extract the options can be specified with the `&regex` option. Its default value (which parses the common formats shown above) is:

```elvish
&regex='^\s*(?:-(\w),?\s*)?(?:--?([\w-]+))?(?:\[=(\S+)\]|[ =](\S+))?\s*?\s\s(\w.*)$'
```

The mapping of capture groups from the regex to option components is defined by the `&regex-map` option. Its default value (which also shows the available fields) is:

```elvish
&regex-map=[&short=1 &long=2 &arg-optional=3 &arg-mandatory=4 &desc=5]
```

At least one of `short` or `long` must be present in `regex-map`. The `arg-optional` and `arg-mandatory` groups, if present, are handled specially: if any of them is not empty, then its contents is stored as `arg-desc` in the output, and the corresponding `arg-mandatory` / `arg-optional` is set to `$true`.

If `&fold` is `$true`, then the input is preprocessed to join option descriptions which span more than one line (the heuristic is not perfect and may not work in all cases, also for now it only joins one line after the option).


## Contributing your completions {#contributing-your-completions}

So you have created a brand-new completion function and would like to share it with the Elvish community. Nothing could be easier! You have two main options:

-   Publish them on your own. For example, if you put your `.elv` files into their own repository in GitHub or Gitlab, they are ready to be installed and used using [epm](https://elvish.io/ref/epm.html).
-   Contribute it to an existing repository (for example [elvish-completions](https://github.com/zzamboni/elvish-completions)). Just add your files, submit a pull request, and you are done.

I hope you have found this tutorial useful. Please let me know in the comments if you have any questions, feedback or if you find something that is incorrect.

Now, go have fun with Elvish!
