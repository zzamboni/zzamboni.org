#!/bin/bash
hugo
git add docs
git ci -m 'Regen'
git push
