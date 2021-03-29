import os
import subprocess
import socket

from typing import List  # noqa: F401
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import fontawesome as fa
import nerdfonts as nf 

mod = "mod4"
# terminal = guess_terminal()
terminal = "alacritty"
file_manager = "nautilus"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

@lazy.function
def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

@lazy.function
def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

@lazy.function
def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)


keys = [

# SUPER + FUNCTION KEYS

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "v", lazy.spawn('pavucontrol')),
    Key([mod], "x", lazy.spawn('oblogout')),
    Key([mod], "Escape", lazy.spawn('xkill')),
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "KP_Enter", lazy.spawn(terminal)),
    Key([mod], "F11", lazy.spawn('rofi -show drun -fullscreen -show-icons')),
    Key([mod], "F12", lazy.spawn('rofi -show drun -show-icons')),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "control"], "Return", lazy.spawn("rofi -show window -show-icons"), desc="Display running task"),
# SUPER + SHIFT KEYS
    Key([mod, "shift"], "Return", lazy.spawn("rofi -combi-modi window,drun,ssh -show combi -show-icons"), desc='Run Launcher'),
    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "control"], "r", lazy.restart()),
     Key([mod, "shift"], "x", lazy.shutdown()),

# CONTROL + ALT KEYS

    Key(["mod1", "control"], "a", lazy.spawn('xfce4-appfinder')),
    Key(["mod1", "control"], "b", lazy.spawn(file_manager)),
    Key(["mod1", "control"], "c", lazy.spawn('catfish')),
    Key(["mod1", "control"], "f", lazy.spawn('firefox')),
    Key(["mod1", "control"], "g", lazy.spawn('chromium -no-default-browser-check')),
    Key(["mod1", "control"], "m", lazy.spawn('xfce4-settings-manager')),
    Key(["mod1", "control"], "p", lazy.spawn('pamac-manager')),
    Key(["mod1", "control"], "r", lazy.spawn('rofi-theme-selector')),
    Key(["mod1", "control"], "s", lazy.spawn('spotify')),
    Key(["mod1", "control"], "t", lazy.spawn(terminal)),
    Key(["mod1", "control"], "v", lazy.spawn('pavucontrol')),
    Key(["mod1", "control"], "Return", lazy.spawn(terminal)),

# ALT + ... KEYS

    Key(["mod1"], "F3", lazy.spawn('xfce4-appfinder')),

### Switch focus to specific monitor (out of three)
    Key([mod], "w",
        lazy.to_screen(0),
        desc='Keyboard focus to monitor 1'
        ),
    Key([mod], "e",
        lazy.to_screen(1),
        desc='Keyboard focus to monitor 2'
        ),
    ### Switch focus of monitors
    Key([mod], "period",
        lazy.next_screen(),
        desc='Move focus to next monitor'
        ),
    Key([mod], "comma",
        lazy.prev_screen(),
        desc='Move focus to prev monitor'
        ),
# CONTROL + SHIFT KEYS

    Key([mod2, "shift"], "Escape", lazy.spawn('xfce4-taskmanager')),

# SCREENSHOTS

    Key([], "Print", lazy.spawn('xfce4-screenshooter')),
    Key([mod2, "shift"], "Print", lazy.spawn('gnome-screenshot -i')),

# MULTIMEDIA KEYS

# INCREASE/DECREASE BRIGHTNESS
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 5")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 5")),

# INCREASE/DECREASE/MUTE VOLUME
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),

    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),

    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
    Key([], "XF86AudioNext", lazy.spawn("mpc next")),
    Key([], "XF86AudioPrev", lazy.spawn("mpc prev")),
    Key([], "XF86AudioStop", lazy.spawn("mpc stop")),

# QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "Tab", lazy.next_layout()),

# CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),

# RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

# FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

# MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

# TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
# ---------- LAUNCH PROGRAMS ----------
    KeyChord(
        [mod],
        "d",
        [
            Key([], "space", lazy.spawn(terminal), desc="Launch terminal"),
            Key([], "b", lazy.spawn("brave"), desc="Launch Browser"),
            Key(
                [],
                "s",
                lazy.spawn("spotify"),
                desc="Launch Spotify",
            ),
            Key(
                [],
                "m",
                lazy.spawn("element-desktop"),
                desc="Launch Matrix client Element",
            ),
            Key(
                [],
                "t",
                lazy.spawn("telegram-desktop"),
                desc="Launch Telegram",
            ),
            Key(
                [],
                "k",
                lazy.spawn("keepassxc"),
                desc="Launch KeepAssXC",
            ),
            Key([], "d", lazy.spawn("dolphin"), desc="Launch Dolphin"),
            Key([], "f", lazy.spawn("firefox"), desc="Launch Firefox"),
        ],
    ),
# ---------- ROFI ----------
    KeyChord(
        [mod],
        "space",
        [
            Key(
                [],
                "space",
                lazy.spawn("rofi -show drun"),
                desc="Spawn a command using a prompt widget",
            ),
            Key(
                [],
                "w",
                lazy.spawn("rofi -show window -show-icons"),
                desc="Spawn a command using a prompt widget",
            ),
            Key(
                [],
                "n",
                lazy.spawn("rofi-wifi-menu -config ~/dotfiles/rofi/monokai.rasi"),
                desc="Spawn wifi menu",
            ),
            Key(
                [],
                "b",
                lazy.spawn("rofi-bluetooth"),
                desc="Spawn bluetooth menu",
            ),
        ],
    ),
]



group_labels = ["", "", "", "", "", "", "", "", "", "",]

# Groups
def my_groups():
    return [
         {"name": "1", "layout": "max", "label": nf.icons["fa_firefox"]},
         {"name": "2", "layout": "monadtall", "label": group_labels[1]},
         {"name": "3", "layout": "monadtall", "label": group_labels[2]},
         {"name": "4", "layout": "monadtall", "label": group_labels[3]},
         {"name": "5", "layout": "monadtall", "label": group_labels[4]},
         {"name": "6", "layout": "monadtall", "label": nf.icons["fa_book"]},
         {"name": "7", "layout": "monadtall", "label": nf.icons["fa_bar_chart_o"]},
         {"name": "8", "layout": "monadtall", "label": nf.icons["fa_file_text"]},
         {"name": "9", "layout": "monadtall", "label": group_labels[8]},
         {"name": "0", "layout": "monadtall", "label": nf.icons["fa_headphones"]},
    ]

group_names = my_groups()
groups = [Group(**kwargs) for kwargs in group_names]



for i in groups:
    keys.extend([
#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True)),
    ])

@hook.subscribe.client_new
def programs_to_group_startup(window):
    if "Teams" in window.name:
        window.togroup("9", switch_group=False)
    elif "spotify" in window.name:
        window.togroup("0", switch_group=False)
    elif "Firefox" in window.name:
        window.togroup("1", switch_group=False)




def init_layout_theme():
    return {"margin":5,
            "border_width":2,
            "border_focus": "#6272a4",
            "border_normal": "#44475a"
            }

layout_theme = init_layout_theme()


layouts = [
    layout.MonadTall(margin=8, border_width=2, border_focus="#6272a4", border_normal="#44475a"),
    layout.MonadWide(margin=8, border_width=2, border_focus="#6272a4", border_normal="#44475a"),
    layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Floating(margin=5, border_width=2, border_focus="#bd93f9", border_normal="#44475a"),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme)
]

# COLORS FOR THE BAR



# Colorpalet - Dracula Theme
def my_colors():
    return {
        "background": "282a36",
        "foreground": "f8f8f2",
        "grey": "#44475a", 
        "blue": "#6272a4", 
        "black": "#575b70",
        "red": "#ff5555",
        "green": "#50fa7b",
        "yellow": "#f1fa8c",
        "orange": "#ffb86c",
        "pink": "#ff79c6",
        "cyan": "#8be9fd",
        "white": "#bfbfbf",
        "purple": "#bd93f9",
    }


colors = my_colors()


def init_colors():
    return [["#282a36", "#282a36"], # Background 0
            ["#44475a", "#44475a"], # "Current Line" 1
            ["#f8f8f2", "#f8f8f2"], # Foreground 2
            ["#6272a4", "#6272a4"], # Comment 3 
            ["#8be9fd", "#8be9fd"], # Cyan 4
            ["#50fa7b", "#50fa7b"], # Green 5
            ["#ffb86c", "#ffb86c"], # Organge 6
            ["#ff79c6", "#ff79c6"], # Pink 7
            ["#bd93f9", "#bd93f9"], # Purple 8
            ["#ff5555", "#ff5555"], # Red 9
            ["#f1fa8c", "#f1fa8c"]] # Yellow 10


colors_old = init_colors()


# WIDGETS FOR THE BAR


def get_line_sep():
    return widget.Sep(
        padding=10, linewidth=2, size_percentage=80, foreground=colors["grey"]
    )


def init_widgets_defaults():
    return dict(font="Ubuntu Nerd",
                fontsize = 12,
                padding = 2,
                foreground = colors["foreground"],
                background=colors["background"])

widget_defaults = init_widgets_defaults()



def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
               widget.GroupBox(font="UbuntuNerd",
                        fontsize = 18,
                        margin_y = 4,
                        margin_x = 0,
                        padding_y = 6,
                        padding_x = 5,
                        borderwidth = 2,
                        disable_drag = True,
                        active = colors["purple"],
                        inactive = colors["grey"],
                        urgent_border=colors["red"],
                        rounded = False,
                        highlight_method = "line",
                        highlight_color=colors["background"],
                        this_current_screen_border = colors["pink"],
                        ),
               get_line_sep(),
               widget.CurrentLayout(font="UbuntuNerd Bold"),
               get_line_sep(),
               widget.Prompt(),
              widget.TaskList(
                         border=colors["grey"],
                         borderwidth=0,
                         highlight_method="block",
                         padding = 2,
                         txt_floating=nf.icons["fa_window_restore"],
                         txt_minimized=nf.icons["fa_window_minimize"],
                         txt_maximized=nf.icons["fa_window_maximize"],
                         max_title_width=250,
                         title_width_method="uniform",
                        ),
               widget.TextBox(
                        # text="",
                        text=nf.icons["fa_arrow_down"]+nf.icons["fa_arrow_up"],
                        foreground=colors["green"],
                        fontsize=11
                        ),
                widget.NetGraph(
                         graph_color=colors["green"],
                         fill_color = colors["grey"],
                         border_color = colors["grey"],
                         margin_y=4,
                         ),
                get_line_sep(),
               widget.TextBox(
                        # text="  ",
                        text=nf.icons["fa_tachometer"],
                        foreground=colors["orange"],
                        fontsize=16
                        ),
               widget.CPUGraph(
                        graph_color=colors["orange"],
                        fill_color = colors["grey"],
                        border_color = colors["grey"],
                        margin_y=4,
                        ),
               get_line_sep(),
               widget.TextBox(
                        font="FontAwesome",
                        text="  ",
                        foreground=colors["purple"],
                        fontsize=16
                        ),
               widget.Memory(
                        format = '{MemUsed:.0f}M/{MemTotal:.0f}M',
                        update_interval = 1,
                       ),
               get_line_sep(),
               widget.TextBox(
                        font="FontAwesome",
                        text="  ",
                        foreground=colors["pink"],
                        fontsize=16
                        ),
               widget.Clock(
                        foreground = colors_old[2],
                        background = colors_old[0],
                        format="%Y-%m-%d %H:%M"
                        ),
               get_line_sep(),
               widget.Systray(
                        background=colors_old[0],
                        icon_size=20,
                        padding = 4
                        ),
              ]
    return widgets_list

# widgets_list = init_widgets_list() # is it useful?

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()[:-1] # just remove systray, buggy otherwise
    return widgets_screen2

widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26))]
screens = init_screens()


# MOUSE CONFIGURATION
# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]


dgroups_key_binder = None
dgroups_app_rules = []  # type: List


main = None  # WARNING: this is deprecated and will be removed soon

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]



@hook.subscribe.startup_once
def start_once():
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.screen_change
def restart_on_randr(qtile):
    qtile.cmd_restart()

follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'blueman-manager'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
    {'wmclass': 'nitrogen'},
    {'wmclass': 'pavucontrol'},
    {'wmclass': 'xfce4-power-manager-settings'},
    {'wmclass': 'xfce4-appfinder'},
    {'wmclass': 'galculator'},
    {'wmclass': 'skype'},
], **layout_theme)
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

