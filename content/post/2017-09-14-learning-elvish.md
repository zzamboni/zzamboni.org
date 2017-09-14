---
title: "Elvish, an awesome Unix shell"
date: 2017-09-14T17:09:38
tags:
- elvish
- shell
- tips
- unix
featured_image: /images/elvish-logo.svg
summary: "I'm always on the lookout for new toys, particularly if they make my work more productive or enjoyable.  For a couple of months now I have been using a little-known Unix shell called Elvish as my default login shell on macOS, and I love it."
---

I'm always on the lookout for new toys, particularly if they make my
work more productive or enjoyable.  For a couple of months now I have
been using a new Unix shell called [Elvish](http://elvish.io) as my default login shell on
macOS, and I love it. It’s a young project but very usable and with
some very nice features.

Here are a few of the things I like about it:

- The [Elvish language](https://elvish.io/ref/language.html) is clean
  and powerful, with clear syntax. It supports name spaces, exception
  handling and proper data structures, including lists and maps.
- It has a rich [built-in library of
  functions](https://elvish.io/ref/builtin.html), including string
  manipulation, regex matching, JSON parsing, etc.
- Commands and functions can output two types of streams: bytes (what
  we usually see as standard output/error) and data (data values,
  potentially containing structured data), which makes it very
  flexible.
- It has very nice interactive features, including as-you-type syntax
  checking and highlighting, support for custom completions, a
  built-in command-line file browser, prompt hooks, configurable
  keybindings, and many others.
- Exceptions! In Elvish, if a command exits with a non-zero code, it
  generates an exception that stops the execution of the current
  script or function. This breaks completely with the Unix-shell
  tradition of silently setting return codes, and it takes a while to
  get used to it, but once you do it’s a very powerful idea, as it
  forces you to think about failures and to plan for them in your
  code.
- It is extensively documented. Take a look at https://elvish.io/ and
  you will see.

Elvish is very powerful, but it's different enough from other shells
that it's worth your time to read through some of the documentation
when you start. I would recommend the [Some Unique
Semantics](https://elvish.io/learn/unique-semantics.html) page, which
assumes you know other shells already. From there you can move to some
of the other tutorials and reference documentation.

Of course, Elvish is not without its quirks and drawbacks. None of
these has been a deal-breaker for me, but just for completeness:

- It’s very young. Occasionally I still encounter crashes, but they
  are few and far between, and the developer is always very
  responsive. Also, the language is still subject to change and there
  are still backwards-incompatible changes with relative frequency. If
  you are looking for absolute stability, it’s not yet ready.
- Its language syntax is still a bit quirky. Spacing is sometimes
  important. For example, in the `if`/`else` construct, the "`} else
  {`" has to be just like that---with spaces, and in a single line,
  for it to be recognized by the parser.
- The data/byte separation is not fully clear (at least to me)
  yet. Sometimes the data stream can be interpreted as bytes as well,
  sometimes it does not. The language is still evolving, so I am sure
  this will become clearer in the future.
- There is not yet a large body of code/scripts you can use. This is
  very noticeable in completions---while Elvish supports completions,
  there are very few implementations. Coming from
  [Fish](https://fishshell.com/), which has an [impressive library of
  custom
  completions](https://github.com/fish-shell/fish-shell/tree/master/share/completions)
  out-of-the-box, this lack is very noticeable, particularly with
  complex commands like `git`.

I am very happy with Elvish, and if you are interested in this sort of
thing, I encourage you to take a look. If you need a starting point,
you can use [my configuration
files](https://github.com/zzamboni/vcsh_elvish/tree/master/.elvish/)
at as an example of the kind of things you can do with it.

I will post more Elvish tips and tricks over time.
