---
title: "Fixing the Outlook-to-OmniFocus Script"
date: 2017-09-11T21:11:29+02:00
tags:
- hammerspoon
- howto
- mac
- outlook
- applescript
featured_image: '/images/hammerspoon.png'
slug: fixing-outlook-to-omnifocus-script
---

Here's how to fix the breakage caused by one of the recent updates to
Microsoft Outlook in the Outlook-to-OmniFocus AppleScript included
with my SendToOmniFocus spoon.

<!--more-->

One of the recent updates to Microsoft Outlook broke the
Outlook-to-OmniFocus AppleScript (courtesy of
[Veritrope](http://veritrope.com/code/outlook-2011-to-evernote/))
included with my [SendToOmniFocus
spoon](http://www.hammerspoon.org/Spoons/SendToOmniFocus.html). I’m
not sure which precise version introduced the breaking change, I’m
currently at version “15.39 (170905)”, and the breakage started one or
two updates ago.  After some investigation, I found the cause — it
seems Outlook AppleScript objects no longer have a “properties” field
which contains things like “subject”, “content”, etc., rather their
properties can be accessed directly on the object.

I have submitted a [pull-request for the
fix](https://github.com/Hammerspoon/Spoons/pull/49), but if you want
to apply it right away, just change the following line in
`~/.hammerspoon/Spoons/SendToOmniFocus.spoon/scripts/outlook-to-omnifocus.applescript`:

```applescript
set theProps to (properties of selectedItem)
```

to the following:

```applescript
try
        set theProps to (properties of selectedItem)
on error
        set theProps to selectedItem
end try
```

This tries the old behavior, and upon failure uses the new one.
