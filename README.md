# 要整理

# 実現したい事
1. 開発中のWidgetにはinput, outputの2つがある。
2. inputから入力されたdataframeの内のdatetime型の1列から、経過時間(秒、分、時間か選択可能にする)に変換した新しい1列を追加したdataframeをoutputから返す役割をする。
3. ~~入力した列をoutputされるdataframeから削除/残す、の選択がGUI上でできると良い?~~

# ToDo
1. inputから入ったデータを上記の通り加工してoutputからでるように枠を作る

# 追記
## 注意
1. 使用するPythonバージョン<3.9でなければなりません。
   1. Python>=3.9は`orange3`のインストールに失敗する(2021.1.6現在)

## 本アドオンの動作確認の手順
1. orange3を事前にインストール
   1. `pip install -U orange3`
2. Orange3に本addonを組み込む
   1. `python setup.py install`
3. Orangeを起動してインストールされている事を確認する
   1. `python -m Orange.canvas`

# Requirement - 必要要件
1. Python>=3.7.
   - `datetime`にて`fromisoformat` method is available from py3.7.

# How to install via https
`pip install -e git+https://github.com/HirotsuguMINOWA/OC-NLP.git#egg=nlp4oc`

# How to install via ssh
`pip install -e git+ssh://git@github.com/HirotsuguMINOWA/OC-NLP.git#egg=nlp4oc`

Orange3 Example Add-on
======================

This is an example add-on for [Orange3](http://orange.biolab.si). Add-on can extend Orange either 
in scripting or GUI part, or in both. We here focus on the GUI part and implement a simple (empty) widget,
register it with Orange and add a new workflow with this widget to example tutorials.

Installation
------------

To install the add-on, run

    pip install .

To register this add-on with Orange, but keep the code in the development directory (do not copy it to 
Python's site-packages directory), run

    pip install -e .

Documentation / widget help can be built by running

    make html htmlhelp

from the doc directory.

Usage
-----

After the installation, the widget from this add-on is registered with Orange. To run Orange from the terminal,
use

    python -m Orange.canvas

The new widget appears in the toolbox bar under the section Example.

![screenshot](https://github.com/biolab/orange3-example-addon/blob/master/screenshot.png)
