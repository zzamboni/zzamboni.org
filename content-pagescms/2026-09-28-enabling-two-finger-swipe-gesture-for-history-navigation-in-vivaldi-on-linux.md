+++
title = 'Enabling two-finger swipe gesture for history navigation in Vivaldi on Linux'
summary = 'How to enable this useful gesture in Vivaldi running on Linux.'
date = '2026-09-28T13:16:00.000'
tags = [
	'howto',
	'vivaldi',
	'linux',
	'troubleshooting',
	'tips',
]
draft = true
toc = false
featureimage = "img/generated/2026-09-28-enabling-two-finger-swipe-gesture-for-history-navigation-in-vivaldi-on-linux.webp"
+++
Using a two-finger swipe on the trackpad to move forward/back in history was not working for me, despite the option being enabled in the Vivaldi settings. I found the answer in [this Vivaldi forum post](https://forum.vivaldi.net/post/867957):

> Create a file `~/.var/app/com.vivaldi.Vivaldi/config/vivaldi-flags.conf` and put that line
>
> ```
> --enable-features=TouchpadOverscrollHistoryNavigation
> ```
>
> into it.  
> Restart Vivaldi.

Now it works!
