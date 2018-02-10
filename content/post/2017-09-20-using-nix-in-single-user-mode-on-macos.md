---
title: Using Nix's "Single-user Mode" on macOS
date: 2017-09-20T18:24:47
tags:
- tips
- macos
- nix
- howto
featured_image: /images/nixos-logo.png
---

Here is how to set up Nix in single-user mode on macOS.

<!--more-->

{{% tip %}} Thanks to
[Alexander](https://disqus.com/by/alexander_vorobiev/) (see [his
comment below](http://disq.us/p/1q17rj6)), a much easier and cleaner
alternative (I have not tested it):

> The original single user setup is still in the install script (so far)
> so it is actually pretty easy to use it. Here are the steps:
>
> 1. Open <https://nixos.org/releases/> and find the latest version
> 2. Download the tarball.
> 3. Unpack it somewhere
> 4. Open the install script and comment the lines (the if statement)
>    for multiuser Darwin setup. In that particular version the lines
>    are 26-35.
> 5. Create the /nix directory (sudo mkdir /nix) and change the
>    ownerwhip to yourself (sudo chown youruserid /nix). Those are the
>    only commands you need sudo rights for.
> 6. run the install script ./install

{{% /tip %}}

I have been playing with the [Nix package
manager](https://nixos.org/nix/) lately (I will write more about it
some other time). On macOS, Nix mandatorily installs itself in
"multi-user mode" in macOS, which means that the build/install process
is actually run under central control by a set of special build
accounts. This allows concurrent users to build packages without
breaking things, but for a single-user system like mine, it doesn't
add much value. Furthermore, it was inconvenient because my
command-line proxy settings (i.e. the `http_proxy` and related
environment variables) did not get properly picked up by the daemon
when it changed dynamically, as it does often through the day as I
move between home, office and other networks.

So, with the help of several nice people on the `##nix-darwin` IRC
channel, I figured out how to revert my installation to single-user
Nix mode. Here it is:

Install and configure Nix [as
documented](https://nixos.org/nix/manual/#chap-quick-start), or like I
did, with `brew cask install nix` (I know---the irony of using
Homebrew to install Nix!)

Next, we need to unload and stop the nix daemon:

```shell
sudo launchctl unload /Library/LaunchDaemons/org.nixos.nix-daemon.plist
sudo launchctl stop org.nixos.nix-daemon
```

Change the ownership of the entire `/nix` directory to your
personal user:

```shell
chown -R yourusername /nix
```

Change your configuration to unset the `NIX_REMOTE` environment
variable. This is set automatically if you use `bash` because the Nix
installation adds it to `/etc/profile`, so you will have to unset it
manually in your own configuration, or modify the system files (I
leave that part up to you according to your setup). I use the Elvish
shell, so you can use my [nix.elv
library](https://github.com/zzamboni/vcsh_elvish/blob/master/.elvish/lib/nix.elv),
which I load from my
[rc.elv](https://github.com/zzamboni/vcsh_elvish/blob/master/.elvish/rc.elv#L82-L86)
file like this:

```shell
# Set up Nix environment
use nix
nix:multi-user-setup
# Work without the daemon
E:NIX_REMOTE = ""
```

Remove the following line from `/etc/nix/nix.conf`:

```shell
build-users-group = nixbld
```

That's it! You should now be able to run `nix-env` and all other Nix
commands and they will operate directly, without going through the
daemon.

Once you are convinced that things are working fine, and to fully
cleanup the multi-user install, you can remove the Nix build group and
users with these commands:

```shell
sudo dscl . -delete /Users/nixbld1
sudo dscl . -delete /Users/nixbld2
sudo dscl . -delete /Users/nixbld3
sudo dscl . -delete /Users/nixbld4
sudo dscl . -delete /Users/nixbld5
sudo dscl . -delete /Users/nixbld6
sudo dscl . -delete /Users/nixbld7
sudo dscl . -delete /Users/nixbld8
sudo dscl . -delete /Users/nixbld9
sudo dscl . -delete /Groups/nixbld
```

I'll write more about my experiences with Nix in the future. Stay
tuned.
