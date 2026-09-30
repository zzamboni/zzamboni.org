#!/bin/bash

#read -r -s -p "Linkblog secret: " LINKBLOG_SECRET; echo
STAGING_URL="https://staging--zzamboni.netlify.app"

jq -n \
  --arg photo "$(base64 < ./test-photoupload.jpg | tr -d '\n')" \
  '{
    title: "Photo upload test",
    commentary: "Testing from curl",
    draft: false,
    photos: [$photo]
  }' |
curl -i -sS --fail-with-body \
  -X POST "$STAGING_URL/api/photoblog" \
  -H "Authorization: Bearer $LINKBLOG_SECRET" \
  -H "Content-Type: application/json" \
  --data-binary @-
