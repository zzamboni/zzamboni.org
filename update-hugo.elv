#!/usr/bin/env elvish
use re
var hugo-ver = (put (re:find 'v([\d.]+)' (hugo version))[groups][1][text])
sed -i'' 's/HUGO_VERSION = .*$/HUGO_VERSION ="'$hugo-ver'"/' netlify.toml 
git add netlify.toml
git ci -m 'Updated Hugo version to '$hugo-ver
git push

