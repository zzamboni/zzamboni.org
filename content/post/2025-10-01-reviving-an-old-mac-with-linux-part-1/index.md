+++
title = "Reviving an old Mac with Linux (part 1 - installing Linux)"
author = ["Diego Zamboni"]
summary = "I recently learned how to extend the life of an old Mac by installing Linux on it. It's like having a new machine!"
date = 2025-10-14T22:23:00+02:00
tags = ["howto", "mac", "linux", "opencore", "oclp"]
draft = false
creator = "Emacs 29.3 (Org mode 9.7.34 + ox-hugo)"
featured_image = "/images/20251013-223325_eOS-default-OpenCore-boot.png"
toc = false
+++

I've been a Mac user and fan for many years. However, my current work machine is a Windows laptop (to which, reluctantly, I've gotten used by now), and my personal machine is a 13" 2015 Macbook Pro which was pretty beefed up at the time (16GB, 500GB SSD), but which has felt slower as macOS has progressed. Officially it can only run up to Monterey (macOS 12), and even then it felt quite slow. Some time ago I installed [OpenCore Legacy Patcher](https://dortania.github.io/OpenCore-Legacy-Patcher/) so I could use it with newer versions of macOS. Most recently I had updated it to Sequoia (macOS 15), and by this time the machine felt almost unusable. So I decided to bring it back to life by installing Linux on it. In this and following posts I will write about this process, including some tips and problems I've encountered along the way.

Let me start by saying I'm extremely happy with the result! My old Mac feels like a new machine again - it's fast and responsive. It's also been great to catch up with the Linux desktop universe. The last time I had regularly used a Linux machine as my desktop was back in 2007 or so, when I had Gentoo Linux installed on my laptop at work. I've been pleasantly surprised by  the evolution of Linux desktop environments since then!

The road hasn't been a straight line. I started with [Ubuntu](https://ubuntu.com/) 25.04, which I thought was the safest way to go given its popularity. I used it with [Omakub](https://omakub.org/), which provides a great starting point. However I decided to keep experimenting. I briefly tried [Pop!_OS](https://system76.com/pop/), which is very nice, but eventually landed on [elementary OS](https://elementary.io/), which feels highly polished, works great, and reminds me a lot of macOS. It's also based on Ubuntu, so most packages work. I kept my machine as dual-boot with macOS in case I ever need it, but so far I've remained firmly on the Linux side and don't regret it.

Here are some screenshots to wet your appetite: my current dual-boot OpenCore boot screen and my custom [mac-like](https://github.com/zzamboni/mac-like) boot theme for Elementary.

{{< figure src="images/20251001-230259_OC-dual-boot-screen.png" link="images/20251001-230259_OC-dual-boot-screen.png" >}}

{{< figure src="images/20251001-231342_eOS-mac-like-boot.png" link="images/20251001-231342_eOS-mac-like-boot.png" >}}

Anyhow, how did we get here?

{{% note %}}
Please note that I had already installed OpenCore Legacy Patcher on my Mac, which influences some of the following steps. Adjust as needed.

****In fact****, if you are not already using OCLP, most likely makes no sense to use it unless you want to tinker - most Linux distros will auto-detect macOS and give you a choice in the Grub boot loader (I think, I'm not sure). OC makes for some very nice boot screens, as seen above.

Please note also that the following assumes some understanding of Linux/macOS internals, and fluency with the command line. Also: **backup your system** before you try any of this.
{{% /note %}}


## Step 1: Back up, clean up and repartition macOS {#step-1-back-up-clean-up-and-repartition-macos}

{{% warning %}}
Again, before getting started: **make a backup of your system!** I can't stress this enough. Although tools have evolved a lot (for example, you can now easily repartition disks without data loss), there's always a chance things will go wrong. Make a full backup of your disk, or at least of your valuable data.
{{% /warning %}}

After this, the first step was to free enough space on macOS so I could resize its disk and leave a chunk of disk empty for my Linux partition. I used the excellent [DaisyDisk](https://daisydiskapp.com/) for this, but there are a number of other utilities that can help you identify where the space is going. Fire at will. In my 500GB disk, I managed to reduce my usage to below 300GB on macOS, which allowed me to create a 200GB partition for Linux.

{{% tip %}}
When I first tried to resize my disk, Disk Utility kept refusing due to snapshots taking up the space. With some help from ChatGPT I figured out how to identify and delete them:

1.  Check existing snapshots:
    ```bash
       tmutil listlocalsnapshots /
    ```
2.  Delete them:
    ```bash
       sudo tmutil deletelocalsnapshots <snapshot-date>
    ```
3.  Repeat until they are all gone.
{{% /tip %}}

Once you've freed up the space, you can resize the macOS partition to leave unused space in the disk. This can be done graphically using Disk Utility or from the command line with `diskutil`. For example:

```bash
diskutil apfs resizeContainer disk0s2 300g
```

Make sure you are using the right partition, you can view them with `diskutil list`.

Make sure you can still reboot into macOS and that everything works OK.

If you had [disabled the boot picker in OCLP](https://dortania.github.io/OpenCore-Legacy-Patcher/POST-INSTALL.html#booting-seamlessly-without-boot-picker), make sure to reenable it again, it will make it easier to see what's happening when you dual-boot the machine through OpenCore.


## Step 2: Install Linux {#step-2-install-linux}

Finally! We can install Linux. Download the installer for your chosen distro and store it in a USB stick (make sure you keep it around, it will be useful if the machine cannot boot after installation). I first installed Ubuntu and fine-tuned my OpenCore boot process with it, but you can also try going directly with something else. Let me give you a few general tips:

-   In most Linux installers, you will need to identify the EFI partition where the boot components will be stored. Ubuntu allows you to use the existing macOS/OpenCore boot partition, which is 200MB in size. Elementary OS however, requires its EFI partition to be at least 1GB in size, and will not let you choose a smaller partition. Fortunately, OpenCore automatically knows how to handle multiple EFI partitions, so you can just create an extra 1GB EFI partition in your free space, use it for Elementary, and leave the rest for the main Linux partition. It looks like this in GParted (`dev/sda1` was the preexisting EFI partition, `dev/sda3` is the one I created for installing Elementary):

    {{< figure src="images/20251005-000848_eOS-Gparted-extra-EFI-partition.png" link="images/20251005-000848_eOS-Gparted-extra-EFI-partition.png" >}}

-   After the Linux installation finishes, try rebooting. In principle, you should see the OpenCore boot screen. However, in my case OpenCore refused to identify the Linux partitions. After **a lot** of head banging I figured out the solution: The trick was to manually install the latest [OpenCore release](https://github.com/acidanthera/OpenCorePkg/releases/) into the EFI partition, overwriting the existing BOOT and OC directories (make sure you back them up first!). You can do this either from macOS if it boots, or from the Linux USB installer. Then OpenCore automatically detected and correctly booted both Linux and macOS. Once everything works, you should see something like this:

    {{< figure src="images/20251013-223325_eOS-default-OpenCore-boot.png" link="images/20251013-223325_eOS-default-OpenCore-boot.png" >}}

This is good! You can select macOS or Linux. Give them a try. You can set your default boot entry by choosing it with the arrow keys and pressing `Ctrl-Enter`.

In the [next post]({{< relref "2025-10-14-reviving-an-old-mac-with-linux-part-2-prettifying-the-boot-screens" >}}) in this series we will look into making the boot screen prettier.
