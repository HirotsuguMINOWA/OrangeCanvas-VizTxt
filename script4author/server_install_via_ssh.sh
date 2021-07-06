p='/usr/local/orange/bin/python'
$p -m pip uninstall NLP4OC
$p -m pip install -e git+ssh://git@github.com/HirotsuguMINOWA/OC-NLP.git#egg=nlp4oc
$p -m Orange.canvas --clear-widget-settings &