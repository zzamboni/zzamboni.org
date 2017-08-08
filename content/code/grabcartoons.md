---
title: "Grabcartoons"
date: 2017-08-03T17:25:50+02:00
description: "Grab your fix of the funnies"
---

GrabCartoons is a comic-summarizing utility. It is modular, and it is
very easy to write modules for new comics.

<!--more-->

[(ChangeLog)](http://github.com/zzamboni/grabcartoons/raw/master/ChangeLog)

You can see a sample of grabcartoons output
[here](../../cartoons-sample.html).

Installation
--------

You can download the latest source code for this project in either
[zip](http://github.com/zzamboni/grabcartoons/zipball/master) or
[tar](http://github.com/zzamboni/grabcartoons/tarball/master) formats.

You can also clone the project with [Git](http://git-scm.com) by
running:

    $ git clone git://github.com/zzamboni/grabcartoons

From within the source directory, run `make install`.

Available comics
----------------

Here's the list of comics for which we currently have modules:

{{< readfile file="/layouts/partials/grabcartoons/lom.txt" >}}

Grabcartoons also includes *templates* that allow you to fetch any comic
from a given site. At the moment we have the following templates:

{{< highlight console >}}
{{< readfile file="/layouts/partials/grabcartoons/templates.txt" >}}
{{< /highlight >}}

To fetch a comic using a module, simply use *template:comic* as the
specification in the command line. *name* can be any unique part of the
title of the comic you want.

Usage
-----

Basic usage example:

    $ grabcartoons.pl sinfest xkcd savage_chickens gocomics.com:gasoline > output.html

And then open `output.html` in your web browser.

Full set of options:

{{< highlight console >}}
{{< readfile file="/layouts/partials/grabcartoons/usage.txt" >}}
{{< /highlight >}}

Contributions
-------------

If you write any new modules, or have any suggestions, please share them
with us! You can post them at the [issue
tracker](http://github.com/zzamboni/grabcartoons/issues), and we will
add them to a future release. Or just fork the code in
[github](http://github.com/zzamboni/grabcartoons/) and then send a pull
request.

Authors
-------

[Diego Zamboni](http://github.com/zzamboni/)\
[Benjamin Kuperman](http://github.com/kuperman/)\

