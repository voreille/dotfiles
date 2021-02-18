#!/bin/bash

function run {
  if ! pgrep $1 ;
  then
    $@&
  fi
}

#Set your native resolution IF it does not exist in xrandr
#More info in the script
#run $HOME/.config/qtile/scripts/set-screen-resolution-in-virtualbox.sh

#Find out your monitor name with xrandr or arandr (save and you get this line)
xrandr --output DP-2-1 --primary --mode 1920x1080 --rate 60.00*+ --pos 0x0 --rotate normal --output eDP-1 --mode 1920x1080 --rate 60.00*+  --right-of DP-2-1 &
#xrandr --output LVDS1 --mode 1366x768 --output DP3 --mode 1920x1080 --right-of LVDS1
#xrandr --output HDMI2 --mode 1920x1080 --pos 1920x0 --rotate normal --output HDMI1 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output VIRTUAL1 --off

#change your keyboard if you need it
#setxkbmap -layout be
setxkbmap -option caps:escape

# for the scrolling 
imwheel -kill

#Some ways to set your wallpaper besides variety or nitrogen
# feh --bg-fill $HOME/Pictures/wallpapers/zvzw74vx3we61.png &


#starting utility applications at boot time
run variety &
run nm-applet &
run blueman-applet &
run pamac-tray &
run xfce4-power-manager &
picom --config $HOME/.config/qtile/scripts/picom.conf &
#/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
/usr/lib/xfce4/notifyd/xfce4-notifyd &

#starting user applications at boot time
run volumeicon &
#run discord &
nitrogen --restore &
#run caffeine -a &
#run vivaldi-stable &
#run firefox &
#run thunar &
#run dropbox &
#run insync start &
#run spotify &
#run atom &
#run telegram-desktop &

