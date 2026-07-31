#!/usr/bin/env bash


yes_no(){
  declare desc="Prompt for conformation. \$\"\{1\}\":  conformation message."

  local arg1="${1}"

  local response

  read -r -p "${arg1} {y/[n]}" response

  if [[ "${response}" =~ ^[Yy]$  ]]

  then
    return 0
  else
    return 1

  fi
}