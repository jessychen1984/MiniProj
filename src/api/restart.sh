##########################################################################
# File Name: restart.sh
# Author: amoscykl
# mail: amoscykl980629@163.com
# Created Time: Sun Apr  5 16:06:59 2020
#########################################################################
#!/bin/zsh
uwsgi --stop api.pid
sleep 1
uwsgi --ini conf.ini
