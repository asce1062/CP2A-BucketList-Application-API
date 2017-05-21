#!/bin/bash
# Specify colors utilized in the terminal
normal='tput sgr0'              # White
red='tput setaf 1'              # Red
green='tput setaf 2'            # Green
yellow='tput setaf 3'           # Yellow
blue='tput setaf 4'             # Blue
violet='tput setaf 5'           # Violet
cyan='tput setaf 6'             # Cyan
white='tput setaf 7'            # White
txtbld=$(tput bold)             # Bold
bldred=${txtbld}$(tput setaf 1) # Bold Red
bldgrn=${txtbld}$(tput setaf 2) # Bold Green
bldblu=${txtbld}$(tput setaf 4) # Bold Blue
bldylw=$(txtbld)$(tput setaf 3) # Bold Yellow
bldvlt=${txtbld}$(tput setaf 5) # Bold Violet
bldcya=${txtbld}$(tput setaf 6) # Bold Cyan
bldwht=${txtbld}$(tput setaf 7) # Bold White

clear
        echo "${bldred}██████╗ ██╗   ██╗ ██████╗██╗  ██╗███████╗████████╗██╗     ██╗███████╗████████╗     █████╗ ██████╗ ██╗"
        echo "${bldred}██╔══██╗██║   ██║██╔════╝██║ ██╔╝██╔════╝╚══██╔══╝██║     ██║██╔════╝╚══██╔══╝    ██╔══██╗██╔══██╗██║"
        echo "${bldred}██████╔╝██║   ██║██║     █████╔╝ █████╗     ██║   ██║     ██║███████╗   ██║       ███████║██████╔╝██║"
        echo "${bldred}██╔══██╗██║   ██║██║     ██╔═██╗ ██╔══╝     ██║   ██║     ██║╚════██║   ██║       ██╔══██║██╔═══╝ ██║"
        echo "${bldred}██████╔╝╚██████╔╝╚██████╗██║  ██╗███████╗   ██║   ███████╗██║███████║   ██║       ██║  ██║██║     ██║"
        echo "${bldred}╚═════╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝╚══════╝   ╚═╝       ╚═╝  ╚═╝╚═╝     ╚═╝"
        echo "${bldred}                                                                                                     "
        echo "${bldred}                             CP2A - BucketList Application API                                       "
        echo "${bldred}                                                                                                     "
        echo "${bldred}                                    R E S T f u l A P I                                              "
        echo "${bldred}                                                                                                     "
        echo "${bldcya}                                 Setting up your computer!                                           "

tput setaf 3
	sleep 1
	echo  
	echo Setting up environmental variables...
	echo  
	sleep 3

tput setaf 2
	time source .env