#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <org_or_repo> <label>"
  exit 1
fi

target="$1"
label="$2"

if ! command -v gh &> /dev/null; then
  echo "Error: GitHub CLI (gh) is not installed." >&2
  exit 1
fi
if [[ "$target" == *"/"* ]]; then
  endpoint="repos/$target/actions/runners"
else
  endpoint="orgs/$target/actions/runners"
fi
response=$(gh api "$endpoint" 2>/dev/null)
if [ $? -ne 0 ]; then
  echo "Error: API call failed at $endpoint" >&2
  exit 1
fi
available=$(echo "$response" | jq -r --arg label "$label" '
  .runners[] | select(.status == "online" and (.labels[].name == $label))')
if [ -n "$available" ]; then
  echo "true"
else
  echo "false"
fi