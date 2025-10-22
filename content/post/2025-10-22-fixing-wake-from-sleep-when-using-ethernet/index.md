+++
title = "Fixing wake-from-sleep in Linux on a Mac when using Ethernet"
author = ["Diego Zamboni"]
date = 2025-10-22T23:28:00+02:00
tags = ["linux", "howto", "mac", "networking", "troubleshooting"]
draft = false
creator = "Emacs 29.3 (Org mode 9.7.34 + ox-hugo)"
featured_image = "/images/tram-zurich.jpg"
toc = false
+++

I noticed that after being asleep, my [2015 MBP running Linux]({{< relref "2025-10-01-reviving-an-old-mac-with-linux-part-1" >}}) would not wake up if it had an Ethernet cable connected when it went to sleep. With some help from ChatGPT I learned that this seems to be a known problem on some Macs in which the Thunderbolt controller doesn’t resume cleanly, leaving the system stuck in a low-level power state — which effectively hangs the resume process.

The fix is to disable the offending drivers **before** going to sleep, and reenabling them after. Fortunately, this was easy to automate with `systemd`. The Thunderbolt Ethernet device on my machine is at `/sys/bus/thunderbolt/devices/0-3/` on my machine, and the `/sys/bus/thunderbolt/devices/0-3/authorized` file can be used to enable/disable the device (by writing a 1 or 0 to it). This can be automated by using a system-hook script. Here's the script, which should be stored at `/lib/systemd/system-sleep/thunderbolt-auto-rebind.sh` and made executable. The script automatically detects all the Thunderbolt devices that can be disabled (works for me, but you may have to change it):

```bash
#!/bin/sh
# thunderbolt-auto-rebind.sh
# Auto-detect Thunderbolt endpoint devices and deauthorize/reauthorize them
# around suspend/resume to avoid resume-hangs when TB devices (eg TB->Ethernet)
# are attached.

LOGTAG="tb-auto-rebind"

# Find TB devices under /sys/bus/thunderbolt/devices/
find_tb_devices() {
  for devpath in /sys/bus/thunderbolt/devices/*; do
    [ -d "$devpath" ] || continue
    devname="$(basename "$devpath")"
    # Skip the host controller or special entries if desired (commonly 0-0)
    # Only include endpoints that have an "authorized" control file
    if [ -w "$devpath/authorized" ]; then
      echo "$devname"
    fi
  done
}

case "$1" in
  pre)
    # Before suspend: deauthorize all TB endpoint devices found
    for dev in $(find_tb_devices); do
      devpath="/sys/bus/thunderbolt/devices/$dev"
      echo 0 > "$devpath/authorized" 2>/dev/null && \
        systemd-cat -t "$LOGTAG" echo "pre-suspend: deauthorized $dev"
    done
    ;;
  post)
    # After resume: small wait then re-authorize
    sleep 2
    for dev in $(find_tb_devices); do
      devpath="/sys/bus/thunderbolt/devices/$dev"
      echo 1 > "$devpath/authorized" 2>/dev/null && \
        systemd-cat -t "$LOGTAG" echo "post-resume: reauthorized $dev"
    done
    ;;
esac
```

(by the way, this script was also written by ChatGPT. I have found it's quite good at debugging issues like this. It doesn't normally get there at the first try, but with a bit of back and forth and giving it additional information its very useful)

That's it! Now my machine sleeps and wakes up correctly regardless of how it's connected to the network!
