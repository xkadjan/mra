@echo off
title RTK serial ports logging script
echo RTK serial ports logging script run
echo ___________________
start putty -load log_mega
echo session log_mega started
start putty -load log_due
echo session log_due started
echo ___________________
pause
