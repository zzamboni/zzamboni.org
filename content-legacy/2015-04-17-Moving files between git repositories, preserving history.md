---
tags:
- howto
- tips
- git
date: '2015-04-17'
description: ''
keywords: []
title: Moving files between git repositories, preserving history
aliases:
- /new/blog/moving-files-between-git-repositories-preserving-history
slug: moving-files-between-git-repositories-preserving-history
---


I needed to copy a directory between two `git` repositories while preserving its history. I found some good instructions at <a href='http://gbayer.com/development/moving-files-from-one-git-repository-to-another-preserving-history/'>http://gbayer.com/development/moving-files-from-one-git-repository-to-another-preserving-history/</a>, which got me started, but I figured out a way to avoid having to move all the files into their directory again (lines 5-6 in Greg's instructions) by reversing the filter to remove everything I don't want instead of only including the directory I want. Here are the steps (the idea is the same as in Greg's post, so please read that to get the explanation, I'm only listing the commands here for reference):


## Get files ready for the move


(`directory1` is the one you want to preserve)
```
git clone git-repository-A-url repo-A-tmp-dir
cd repo-A-tmp
git remote rm origin   # for safety
git filter-branch --tree-filter 'rm -rf $(git ls-files | egrep -v directory1)' -- --all
```


(2016-06-08: update thanks to Pawel Veselov, using `git ls-files` instead of `ls` in the last command)


The last line replaces lines 4-8 in the original instructions.


At this point you should verify that only `directory1` remains in the repository, with the correct history. I used the following command to verify that only commits related to my desired directory remained:
```
git log -p | grep '^diff ' | grep -v directory1
```


## Merge files into the new repository


These steps are identical from Greg's instructions.
```
git clone git-repository-B-url
cd git-repository-B-dir
git remote add repo-A-branch repo-A-tmp-dir
git pull repo-A-branch master
git remote rm repo-A-branch
```


