cd ~/OC-NLP
git pull
p='/usr/local/orange/bin/python'
$p -m pip  uninstall NLP4OC
$p setup.py install
$p -m  Orange.canvas --clear-widget-settings &