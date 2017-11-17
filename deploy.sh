#!/bin/bash
export HUGO_ENV=production
hugo
git add docs
git ci -m 'Regen'
git push
