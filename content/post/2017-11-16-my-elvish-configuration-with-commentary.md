+++
title = "My Elvish Configuration With Commentary"
author = ["Diego Zamboni"]
summary = "In this blog post I will walk you through my current Elvish configuration file, with running commentary about the different sections."
date = 2017-11-16T20:21:00+01:00
tags = ["config", "howto", "literateprogramming", "literateconfig", "elvish"]
draft = false
creator = "Emacs 28.2 (Org mode 9.7.11 + ox-hugo)"
toc = true
featured_image = "/images/elvish-logo.svg"
+++

{{< leanpubbook book="lit-config" style="float:right" >}}

Last update: **October 30, 2024**

In this blog post I will walk you through my current [Elvish](http://elvish.io) configuration file, with running commentary about the different sections.

This is also my first blog post written using [org-mode](http://orgmode.org/), which I have started using for writing and documenting my code, using [literate programming](http://www.howardism.org/Technical/Emacs/literate-programming-tutorial.html). The content below is included unmodified from my [rc.org file](https://github.com/zzamboni/dot-elvish/blob/master/rc.org) (as of the date shown above), from which the [rc.elv](https://github.com/zzamboni/dot-elvish/blob/master/rc.elv) file is directly generated.

If you are interested in writing your own Literate Config files, check out my new book [Literate Config](https://leanpub.com/lit-config) on Leanpub!

Without further ado...


## Module loading {#module-loading}

Load a number of commonly-used modules so that they are available in my interactive session.

Load the bundled [re](https://elv.sh/ref/re.html) module to have access to regular expression functions.

```elvish
use re
```

The bundled [readline-binding](https://elv.sh/ref/readline-binding.html) module associates some Emacs-like keybindings for manipulation of the command line.

```elvish
use readline-binding
```

The bundled `path` module contains path manipulation functions.

```elvish
use path
```

The bundled `str` and `math` modules for string manipulation and math operations.

```elvish
use str
use math
```


## Paths {#paths}

First we set up the executable paths. We set the `GOPATH` environment variable while we are at it, since we need to use it as part of the path.

```elvish
# Where all the Go stuff is
if (path:is-dir ~/Dropbox/Personal/devel/go) {
  set E:GOPATH = ~/Dropbox/Personal/devel/go
} else {
  set E:GOPATH = ~/go
}
# Optional paths, add only those that exist
var optpaths = [
  ~/.emacs.d/bin
  /usr/local/opt/coreutils/libexec/gnubin
  /usr/local/opt/texinfo/bin
  /usr/local/opt/python/libexec/bin
  /usr/local/go/bin
  ~/Work/automated-security-helper
  ~/.toolbox/bin
]
var optpaths-filtered = [(each {|p|
      if (path:is-dir $p) { put $p }
} $optpaths)]

set paths = [
  ~/bin
  $E:GOPATH/bin
  $@optpaths-filtered
  /usr/local/bin
  /usr/local/sbin
  /usr/sbin
  /sbin
  /usr/bin
  /bin
]
```

My work machine setup blocks `proxy.golang.org`, so I configure for all modules to be downloaded directly from their source.

```elvish
set E:GONOPROXY = "*"
```

I have a quick sanity check because sometimes certain paths disappear depending on new versions, etc. This prints a warning when opening a new shell, if there are any non-existing directories in `$paths`. We need some wrapping around `path:eval-symlinks` to avoid seeing warnings when the directory does not exist.

```elvish
each {|p|
  if (not (path:is-dir &follow-symlink $p)) {
    echo (styled "Warning: directory "$p" in $paths no longer exists." red)
  }
} $paths
```


## Package installation {#package-installation}

The bundled [epm](https://elv.sh/ref/epm.html) module allows us to install and manage Elvish packages.

```elvish
use epm
```

For now I use these packages:

-   [github.com/zzamboni/elvish-modules](https://github.com/zzamboni/elvish-modules) contains all my modules except completions and themes. Maybe these should be separated eventually, but for now this works fine.
-   [github.com/zzamboni/elvish-themes](https://github.com/zzamboni/elvish-themes) contains my prompt themes (only [chain](https://github.com/zzamboni/elvish-themes/blob/master/chain.org) for now).
-   [github.com/zzamboni/elvish-completions](https://github.com/zzamboni/elvish-completions) contains my completer definitions.
-   [github.com/xiaq/edit.elv](https://github.com/xiaq/edit.elv), which includes the `smart-matcher` module used below.
-   [github.com/muesli/elvish-libs](https://github.com/muesli/elvish-libs) for the git utilities module.
-   [github.com/iwoloschin/elvish-packages](https://github.com/iwoloschin/elvish-packages) for the update.elv package.

<!--listend-->

```elvish
epm:install &silent-if-installed         ^
github.com/zzamboni/elvish-modules     ^
github.com/zzamboni/elvish-completions ^
github.com/xiaq/edit.elv               ^
github.com/muesli/elvish-libs          ^
github.com/iwoloschin/elvish-packages
```

The modules within each package get loaded individually below.


## Automatic proxy settings {#automatic-proxy-settings}

When I am in the office, I need to use a proxy to access the Internet. For macOS applications, the proxy is set automatically using a company-provided PAC file. For the environment variables `http_proxy` and `https_proxy`, commonly used by command-line programs, the [proxy](https://github.com/zzamboni/modules.elv/blob/master/proxy.org) module allows me to define a test which determines when the proxy should be used, so that the change is done automatically. We load this early on so that other modules which need to access the network get the correct settings already.

First, we load the module and set the proxy host.

```elvish
use github.com/zzamboni/elvish-modules/proxy
set proxy:host = "http://aproxy.corproot.net:8080"
```

Next, we set the test function to enable proxy auto-setting. In my case, the `/etc/resolv.conf` file contains the `corproot.net` domain (set through DHCP) when I'm in the corporate network, so I can check for that.

```elvish
proxy:test = {
  and ?(test -f /etc/resolv.conf) ^
  ?(egrep -q '^(search|domain).*(corproot.net|company.com)' /etc/resolv.conf)
}
```

We run an initial check so that other commands in rc.org get the correctd settings already, even before the first prompt.

```elvish
proxy:autoset
```


## General modules and settings {#general-modules-and-settings}

I add a couple of keybindings which are missing from the default `readline-binding` module:

-   `Alt-backspace` to delete small-word
    ```elvish
      set edit:insert:binding[Alt-Backspace] = $edit:kill-small-word-left~
    ```

-   `Alt-d` to delete the small-word under the cursor
    ```elvish
      set edit:insert:binding[Alt-d] = $edit:kill-small-word-right~
    ```

-   I also bind "[instant preview mode](https://elv.sh/ref/edit.html#edit-instantstart)" to <kbd>Alt-m</kbd>. This is useful to see the results of a command while you are typing it.
    ```elvish
      set edit:insert:binding[Alt-m] = $edit:-instant:start~
    ```

-   Limit the height of location and history mode so that they don't cover the whole screen.
    ```elvish
      set edit:max-height = 20
    ```


## 1Password {#1password}

My `1pass` module provides some wrappers for interacting with the [1Password command line utility](https://support.1password.com/command-line/).

```elvish
use github.com/zzamboni/elvish-modules/1pass
```

Read aliases defined by the `op plugin` command. See <https://blog.1password.com/shell-plugins/> for more details about  `op` shell plugins.

```elvish
1pass:read-aliases
```

I haven't gotten around to write an `op` plugin for this, so I still use my `lazy-vars` module to read the credentials for my [750words command-line client](https://github.com/zzamboni/750words-client).

```elvish
use github.com/zzamboni/elvish-modules/lazy-vars

set E:USER_750WORDS = diego@zzamboni.org
lazy-vars:add-var PASS_750WORDS { 1pass:get-password "750words.com" }
lazy-vars:add-alias 750words-client.py [ PASS_750WORDS ]
```


## Aliases and miscellaneous functions {#aliases-and-miscellaneous-functions}

Elvish does not have built-in alias functionality, but this is implemented easily using the [alias](https://github.com/zzamboni/modules.elv/blob/master/alias.org) module, which stores the alias definitions as functions under [~/.elvish/aliases/](https://github.com/zzamboni/dot-elvish/tree/master/aliases) and loads them automatically.

```elvish
use github.com/zzamboni/elvish-modules/alias
```

For reference, I define here a few of my commonly-used aliases. Some of them are defined only if the corresponding external binary exists, I define a couple of functions to help with this.

```elvish
fn have-external { |prog|
  put ?(which $prog >/dev/null 2>&1)
}
fn only-when-external { |prog lambda|
  if (have-external $prog) { $lambda }
}
```

```elvish
only-when-external dfc {
  alias:new dfc e:dfc -p -/dev/disk1s4,devfs,map,com.apple.TimeMachine
}
only-when-external vagrant {
  alias:new v vagrant
}
only-when-external hub {
  alias:new git hub
}
```

Use `bat` as my default pager, if installed. I love the `bat` `man` configuration for [using `bat` as the pager for `man` pages](https://github.com/sharkdp/bat#man).

```elvish
only-when-external bat {
  alias:new cat bat
  alias:new more bat --paging always
  set E:MANPAGER = "sh -c 'col -bx | bat -l man -p'"
}
```

Open man pages as PDF, I gathered this tip from <https://twitter.com/MrAhmadAwais/status/1279066968981635075>. Neat but not very useful for daily use, particularly with the `bat` integration above.

```elvish
fn manpdf {|@cmds|
  each {|c|
    man -t $c | open -f -a /System/Applications/Preview.app
  } $cmds
}
```


## Completions {#completions}

The [smart-matcher](https://github.com/xiaq/edit.elv/blob/master/smart-matcher.elv) module tries prefix match, smart-case prefix match, substring match, smart-case substring match, subsequence match and smart-case subsequence match automatically.

```elvish
use github.com/xiaq/edit.elv/smart-matcher
smart-matcher:apply
```

Other possible values for `edit:completion:matcher` are `[p]{ edit:match-prefix &smart-case $p }` for smart-case completion (if your pattern is entirely lower case it ignores case, otherwise it's case sensitive).  `&smart-case` can be replaced with `&ignore-case` to make it always case-insensitive.

I now use the universal Carapace completer module for most commends instead of custom-built Elvish completions:

```elvish
# Enable the universal command completer if available.
# See https://github.com/rsteube/carapace-bin
if (has-external carapace) {
  eval (carapace _carapace | slurp)
}
```

One exception is the `ssh` completer, I like my custom version from the  [elvish-completions](https://github.com/zzamboni/elvish-completions) package better, because it completes hostnames from `~/.ssh/config` instead of from `~/.ssh/known_hosts`.

```elvish
use github.com/zzamboni/elvish-completions/ssh
```


## Prompt theme {#prompt-theme}


### Starship {#starship}

I now use  [Starship](https://starship.rs/) for my prompt.

```elvish
#   eval (starship init elvish | sed 's/except/catch/')
# Temporary fix for use of except in the output of the Starship init code
eval (/usr/local/bin/starship init elvish --print-full-init | slurp)
```

You can find my current Starship config file at <https://gitlab.com/zzamboni/mac-setup/-/blob/master/files/homefiles/.config/starship.toml>.


### Chain {#chain}

I developed the [chain](https://github.com/zzamboni/theme.elv/blob/master/chain.org) prompt theme, ported from the fish theme at <https://github.com/oh-my-fish/theme-chain>. This whole section is disabled since I switched to [Starship](https://starship.rs/), but left here for reference.

```elvish
epm:install &silent-if-installed github.com/zzamboni/elvish-themes
use github.com/zzamboni/elvish-themes/chain
chain:bold-prompt = $false
```

I set the color of the directory segment, the prompt chains and the prompt arrow in my prompt to a session-identifying color (a different color for each session).

```elvish
chain:segment-style = [
  &dir=          session
  &chain=        session
  &arrow=        session
  &git-combined= session
  &git-repo=     bright-blue
]
```

Customize some of the glyphs for the font I use in my terminal. I use the [Fira Code](https://github.com/tonsky/FiraCode) font which includes ligatures, so I disable the last chain, and set the `arrow` segment to a combination of characters which shows up as a nice arrow.

```elvish
chain:glyph[arrow]  = "|>"
chain:show-last-chain = $false
```


### Other prompt settings {#other-prompt-settings}

Elvish has a [comprehensive mechanism](https://elv.sh/ref/edit.html#prompts) for displaying prompts with useful information while avoiding getting blocked by prompt functions which take too long to finish. For the most part the defaults work well. One change I like to make is to change the [stale prompt transformer](https://elv.sh/ref/edit.html#stale-prompt) function to make the prompt dim when stale (the default is to show the prompt in inverse video):

```elvish
set edit:prompt-stale-transform = {|x| styled $x "bright-black" }
```

Another possibility is to make the prompt stay the same when stale - useful to avoid distractions (disabled for now):

```elvish
#  edit:prompt-stale-transform = $all~
```

I also like the continuous update of the prompt as I type (by default it only updates on Enter and on `$pwd` changes, but I like also git status changes to be updated automatically), so I increase its eagerness.

```elvish
set edit:-prompt-eagerness = 10
```


## iTerm2 shell integration support {#iterm2-shell-integration-support}

The `iterm2` module provides support for iTerm2's [Shell Integration](https://iterm2.com/documentation-shell-integration.html) features. Note that `iterm2:init` must be called after setting up the prompt, hence this is done after loading the `chain` module above.

```elvish
use github.com/zzamboni/elvish-modules/iterm2
iterm2:init
set edit:insert:binding[Ctrl-L] = $iterm2:clear-screen~
```


## Long-running-command notifications {#long-running-command-notifications}

The [long-running-notifications](https://github.com/zzamboni/modules.elv/blob/master/long-running-notifications.org) module allows for producing a notification when a command takes longer than a certain time to finish (by default the period is 10 seconds). The module automatically detects when [terminal-notifier](https://github.com/julienXX/terminal-notifier) is available on macOS and uses it to produce Mac-style notifications, otherwise it prints a notification on the terminal.

```elvish
use github.com/zzamboni/elvish-modules/long-running-notifications
```


## Directory and command navigation and history {#directory-and-command-navigation-and-history}

Elvish comes with built-in location and command history modes, and these are the main mechanism for accessing prior directories and commands. The weight-keeping in location mode makes the most-used directories automatically raise to the top of the list over time.

I have decades of muscle memory using <kbd>!!</kbd> and <kbd>!$</kbd> to insert the last command and its last argument, respectively. The [bang-bang](https://github.com/zzamboni/elvish-modules/blob/master/bang-bang.org) module allows me to keep using them.

```elvish
use github.com/zzamboni/elvish-modules/bang-bang
```

The [dir](https://github.com/zzamboni/modules.elv/blob/master/dir.org) module implements a directory history and some related functions. I alias the `cd` command to `dir:cd` so that any directory changes are kept in the history. I also alias `cdb` to `dir:cdb` function, which allows changing to the base directory of the argument.

```elvish
use github.com/zzamboni/elvish-modules/dir
alias:new cd &use=[github.com/zzamboni/elvish-modules/dir] dir:cd
alias:new cdb &use=[github.com/zzamboni/elvish-modules/dir] dir:cdb
```

`dir` also implements a custom directory history chooser, which I bind to <kbd>Alt-i</kbd> (I have found I don't use this as much as I thought I would - the built-in location mode works nicely).

```elvish
set edit:insert:binding[Alt-i] = $dir:history-chooser~
```

I bind `Alt-b/f` to `dir:left-small-word-or-prev-dir` and `dir:right-small-word-or-next-dir` respectively, which "do the right thing" depending on the current content of the command prompt: if it's empty, they move back/forward in the directory history, otherwise they move through the words of the current command. In my terminal setup, `Alt-left/right` also produce `Alt-b/f`, so these bindings work for those keys as well.

```elvish
set edit:insert:binding[Alt-b] = $dir:left-small-word-or-prev-dir~
set edit:insert:binding[Alt-f] = $dir:right-small-word-or-next-dir~
```

The following makes the location and history modes be case-insensitive by default:

```elvish
set edit:insert:binding[Ctrl-R] = {
  edit:histlist:start
  edit:histlist:toggle-case-sensitivity
}
```

I use [eza](https://github.com/eza-community/eza) as a replacement for the `ls` command, so I alias `ls` to it. Unfortunately, `eza` does not understand the `-t` option to sort files by modification time, so I explicitly look for the `-lrt` and `-lrta` option combinations (which I use very often, and _always_ trip me off) and replace them with the correct options for `eza`. All other options are passed as-is.

```elvish
only-when-external eza {
  var eza-ls~ = { |@_args|
    use github.com/zzamboni/elvish-modules/util
    e:eza --color-scale --git --group-directories-first (each {|o|
        util:cond [
          { eq $o "-lrt" }  "-lsnew"
          { eq $o "-lrta" } "-alsnew"
          :else             $o
        ]
    } $_args)
  }
  edit:add-var ls~ $eza-ls~
}
```


## Dynamic terminal title {#dynamic-terminal-title}

The [terminal-title](https://github.com/zzamboni/elvish-modules/blob/master/terminal-title.org) module handles setting the terminal title dynamically according to the current directory or the current command being executed.

```elvish
use github.com/zzamboni/elvish-modules/terminal-title
```


## Loading private settings {#loading-private-settings}

The `private` module sets up some private settings such as authentication tokens. This is not on github :) The `$private-loaded` variable gets set to `$ok` if the module was loaded correctly.

```elvish
var private-loaded = ?(use private)
```


## O'Reilly Atlas {#o-reilly-atlas}

I sometimes use the [O'Reilly Atlas](https://atlas.oreilly.com/) publishing platform. The [atlas](https://github.com/zzamboni/modules.elv/blob/master/atlas.org) module contains some useful functions for triggering and accessing document builds.

```elvish
use github.com/zzamboni/elvish-modules/atlas
```


## OpsGenie {#opsgenie}

I used OpsGenie at work for a while, so I put together the [opsgenie](https://github.com/zzamboni/elvish-modules/blob/master/opsgenie.org) library to make API operations easier. I don't actively use or maintain this anymore.

```elvish
use github.com/zzamboni/elvish-modules/opsgenie
```


## LeanPub {#leanpub}

I use [LeanPub](https://leanpub.com/help/api) for publishing my books, so I have written a few utility functions. I don't use this regularly, I have much better integration using Hammerspoon and CircleCI, I wrote about it in my blog: [Automating Leanpub book publishing with Hammerspoon and CircleCI](https://zzamboni.org/post/automating-leanpub-book-publishing-with-hammerspoon-and-circleci/). The Leanpub API key is fetched from 1Password when needed.

```elvish
use github.com/zzamboni/elvish-modules/leanpub
set leanpub:api-key-fn = { 1pass:get-item leanpub &fields=["API key"] }
```


## TinyTeX {#tinytex}

Tiny module with some utility functions for using [TinyTeX](https://yihui.org/tinytex/).

```elvish
use github.com/zzamboni/elvish-modules/tinytex
```


## Conda integration {#conda-integration}

Conda integration for Elvish. This is not yet in the main Conda distribution, but in a PR: <https://github.com/conda/conda/pull/10731>

The following block will get added to `rc.elv` by `conda init elvish`. Having it tangled out allows me to control where in the file it appears, since Conda only replaces/updates it instead of adding it again.

```elvish
if (path:is-dir ~/Dropbox/Personal/devel/conda/devenv/bin) {
  set @paths = ~/Dropbox/Personal/devel/conda/devenv/bin $@paths
}
only-when-external conda {
  conda config --set auto_activate_base false
  # >>> conda initialize >>>
  # !! Contents within this block are managed by 'conda init' !!
  eval (~/Dropbox/Personal/devel/conda/devenv/bin/conda "shell.elvish" "hook" | upgrade-scripts-for-0.17 -lambda | slurp)"; conda activate aws"
  # <<< conda initialize <<<
}
```

I can configure Conda to deactivate itself, or to set a default environment, through some files in my home directory.

```elvish
conda-deactivate = ~/.conda-deactivate
conda-default-env = ~/.conda-default-env

if (path:is-regular $conda-deactivate) {
  conda deactivate
} else {
  if (path:is-regular $conda-default-env) {
    conda activate (cat $conda-default-env)
  }
}
```


## PyEnv {#pyenv}

I do some manual setup for [PyEnv](https://github.com/pyenv/pyenv), since it does not yet have built-in support for Elvish.

```elvish
only-when-external pyenv {
  set paths = [ ~/.pyenv/shims $@paths ]
  set-env PYENV_SHELL elvish
}
```


## Environment variables {#environment-variables}

Default options to `less`.

```elvish
set E:LESS = "-i -R"
```

Use vim as the editor from the command line (although I am an [Emacs](https://github.com/zzamboni/dot-emacs/blob/master/init.org) fan, I still sometimes use vim for quick editing).

```elvish
set E:EDITOR = "vim"
```

Locale setting.

```elvish
set E:LC_ALL = "en_US.UTF-8"
```

`PKG_CONFIG` configuration.

```elvish
set E:PKG_CONFIG_PATH = "/usr/local/opt/icu4c/lib/pkgconfig"
```


## Git repository summary {#git-repository-summary}

The `git-summary` module allows displaying the git status of multiple repositories in a single list. I use it to keep track of the status of my commonly-used repos. I load the module as `gs` to make it easier to call its functions.

```elvish
use github.com/zzamboni/elvish-modules/git-summary gs
```

Stop `gitstatusd` from staying in the background, since it's only used for this purpose.

```elvish
set gs:stop-gitstatusd-after-use = $true
```

Customize the command used for finding git repos for `git-summary:summary-status &all`, to ignore some uninteresting repos. List of directories to exclude is defined in `$git-summary-repos-to-exclude`.

```elvish
var git-summary-repos-to-exclude = ['.emacs.d*' .cargo Library/Caches Dropbox/Personal/devel/go/src]
var git-summary-fd-exclude-opts = [(each {|d| put -E $d } $git-summary-repos-to-exclude)]
set gs:find-all-user-repos-fn = {
  fd -H -I -t d $@git-summary-fd-exclude-opts '^.git$' ~ | each $path:dir~
}
```


## Utility functions {#utility-functions}

The [util](https://github.com/zzamboni/elvish-modules/blob/master/util.org) module includes various utility functions.

```elvish
use github.com/zzamboni/elvish-modules/util
```

I use muesli's git utilities module.

```elvish
use github.com/muesli/elvish-libs/git
```

The [update.elv](https://github.com/iwoloschin/elvish-packages/blob/master/update.elv) package prints a message if there are new commits in Elvish after the running version.

```elvish
use github.com/iwoloschin/elvish-packages/update
set update:curl-timeout = 3
update:check-commit &verbose
```

Set up electric delimiters in the command line.

```elvish
use github.com/zzamboni/elvish-modules/util-edit
util-edit:electric-delimiters
```

ASCII spinners and TTY escape code generation.

```elvish
use github.com/zzamboni/elvish-modules/spinners
use github.com/zzamboni/elvish-modules/tty
```


## Work-specific stuff {#work-specific-stuff}

I have a private library which contains some work-specific functions.

```elvish
use work
```
