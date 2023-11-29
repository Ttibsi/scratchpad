#!/usr/bin/env bash
read -sdR -p $'\E[6n' CURPOS
CURPOS=${CURPOS#*[} # Strip decoration characters <ESC>[
echo "${CURPOS}"    # Return position in "row;col" format
