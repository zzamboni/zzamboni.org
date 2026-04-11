+++
title = "Vivaldi browser configuration in Linux"
author = ["Diego Zamboni"]
summary = "I switched from Zen to Vivaldi on my Linux machine, I'm documenting here some of the configuration tips I have discovered."
draft = true
creator = "Emacs 30.2 (Org mode 9.7.39 + ox-hugo)"
featured_image = "/images/tram-zurich.jpg"
toc = false
+++

## Enabling two-finger swipe gesture for history navigation {#enabling-two-finger-swipe-gesture-for-history-navigation}

Using a two-finger swipe on the trackpad to move forward/back in history was not working for me, despite the option being enabled in the Vivaldi settings. I found the answer [in this Vivaldi forum post](https://forum.vivaldi.net/post/867957):

> Create a file `~/.var/app/com.vivaldi.Vivaldi/config/vivaldi-flags.conf`
> and put that line
>
> ```sh
> --enable-features=TouchpadOverscrollHistoryNavigation
> ```
>
> into it.

Now it works!
