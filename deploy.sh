#!/bin/bash
# Regenerate with Hugo and upload
# Arguments (if any) are used as commit message, otherwise a generic one is used
if [ $# -gt 0 ]; then
  MSG="$@"
else
  MSG="Regen"
fi
export HUGO_ENV=production
hugo
git add docs
git ci -m "$MSG"
git push
