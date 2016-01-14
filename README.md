# symget

## General description
A script written in Python for a Linux command line tool.
Purpose of the tool: Allow user to add and quickly retrieve symbols or phrases via command line.

For example, the keyword "dash" is paired with the symbol "–". Typing "symget dash" in the command line, the symbol "–" will be returned and put to clipboard.

The script allows the user to retrieve symbols, add keyword-symbol pairs, subsitute multiple keyword in a phrase with symbols in a phrase, remove keywords and display contents of the symbol map.

## Logs

Each keyword call is logged to a "call_log" file.
A timestampted copy of the symbol map is saved whenever contents of the symbol map are changed.

## Structure of the script
The code of the scripts is split to two files for easier reading. symget_basefunctions.py contains the more basic functions.

