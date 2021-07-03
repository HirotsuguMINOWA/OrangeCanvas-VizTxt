# from orangewidget import gui
from AnyQt.QtWidgets import QGridLayout, QLabel
from Orange.data import Table
from Orange.widgets import gui  # Prent Widget?
from Orange.widgets.utils.signals import Input, Output
# from Orange.widgets.widget import OWWidget
from Orange.widgets.widget import OWWidget
# TODO:
# TODO: Orange3-Textのインストールされてないときのチェックするようにしよう
# TODO: GUI部でoutputのCorpusへ残すPOSを指定できるようにしよう
# from conv2elapsed_time import convert  # not found
# from orangecontrib.example.widgets.conv2elapsed_time import convert
from orangecontrib.text import Corpus

# from orangecontrib.example.widgets.morphologicalizer import convert
try:
    from .morphologicalizer import morphological_analysis8, POS
except:
    from orangecontrib.nlp.widgets.morphologicalizer import morphological_analysis8, POS

# TODO: logger置き換えろ
class MorphParser(OWWidget):
    # Widget needs a name, or it is considered an abstract widget
    # and not shown in the menu.
    name = "JA Morphological Parser"  # FIXME: 名前修正しよう
    icon = "icons/mywidget.svg"  # FIXME: 要修正, 著作権問題が気になるため
    want_main_area = False
    cm_key = ""  # CredentialManager("Twitter API Key")
    cm_secret = ""  # CredentialManager("Twitter API Secret")
    extract_pos_str = '["名詞"]["名詞","サ変接続"]'
    secret_input = ""

    def __init__(self):
        """

        ■ 失敗
        - controlArea.SetLayout()しても、生成したLayoutに置換されない
        """
        super().__init__()
        self.A: Table = None
        # self.extract_pos_str = ""
        self._setup_gui()
        # # GUIパネルの構築
        # label = QLabel("【未だ有効じゃない】Column of DateTime Converted")
        # self.col = QComboBox()
        # self.col.addItem("Test_columnt")
        # # TODO: 変換対象の列を選択するPullDownmenuを要追加
        # # TODO: 単位を決めるラジオボンタンを要追加
        # # lay=QGraphicsGridLayout()
        # col2 = QComboBox()
        # col2.addItem("Second")
        # col2.addItem("Minutes")
        # col2.addItem("Hours")
        # col2.addItem("Day")
        # # TODO: week居る？

    def _setup_gui(self):
        # grid = QGridLayout()
        # box = gui.widgetBox(self.controlArea, "Scoring Methods", grid)
        # grid = QGridLayout()
        # grid.setContentsMargins(0, 0, 0, 0)
        # # col2 = QComboBox()
        # label = QLabel("【未だ有効じゃない】Column of DateTime Converted")
        # grid.addItem(label, 1, 1)
        # # box.layout().addItem(label)
        # box.layout().addLayout(grid)
        form_main = gui.QtWidgets.QFormLayout()
        form_main.setContentsMargins(5, 5, 5, 5)
        grid = QGridLayout()
        #

        ext_pos01 = QLabel("抽出する品詞: [")
        grid.addWidget(ext_pos01, 0, 0)
        ext_pos02 = gui.lineEdit(
            self, self, "extract_pos_str", controlWidth=400
        )
        grid.addWidget(ext_pos02, 0, 1)
        ext_pos02 = QLabel("]")
        grid.addWidget(ext_pos02, 0, 2)
        # self.setLayout(grid)
        form_main.addRow(grid)

        tmp = QLabel('["名詞"],["助詞","サ変名詞"]')
        # self.setLayout(form_main)
        # self.key_edit = gui.lineEdit(
        #     self, self, "key_input", controlWidth=400
        # )
        # form_main.addRow("Key:", self.key_edit)
        # self.secret_edit = gui.lineEdit(
        #     self, self, "secret_input", controlWidth=400
        # )
        # form_main.addRow("Secret:", self.secret_edit)
        self.controlArea.layout().addLayout(form_main)  # Set as MainForm
        #
        self.submit_button = gui.button(
            self.controlArea, self, "OK", self.accept
        )
        # self.load_ui_values()

    def load_ui_values(self):
        self.key_edit.setText(self.cm_key)
        self.secret_edit.setText(self.cm_secret)

    class Inputs:
        """
        get Inputs
        """
        input_data = Input("Data", Corpus, default=True)

    class Outputs:
        # out_mine = Output("Data", Table)
        out_mine = Output("Data", Corpus)

    @Inputs.input_data
    def set_A(self, a):
        """Set input_data value into this instance(self) variable"""
        self.A: Table = a

    def handleNewSignals(self):
        """Coalescing update."""
        self.commit()

    def commit(self):
        """Commit/send the outputs"""
        print("Entered commit method")
        if self.A is None:
            # Clear the channel by sending `None`
            self.Outputs.out_mine.send(None)
        else:
            """Input is exists, so try conversion"""
            # TODO: 入力されたPOSリストが有効(eg. 2重リストか否か)をチェックする事
            # print("domain", self.A.domain)
            # names = self.A.domain[:2]
            # print("names:", repr(names[0]), names[1].name)
            # # tmp_domain = Domain(["sepal length", "petal length", DiscreteVariable.make("color")], iris.domain.class_var, source=self.A.domain)
            # print("ContinuousVariable.make(names[1].name):", ContinuousVariable.make(names[1].name))
            # # tmp_domain = Domain([ContinuousVariable.make(names[0].name), ContinuousVariable.make(names[1].name)],
            # #                     class_vars=ContinuousVariable.make(names[1].name), metas=None, source=self.A.domain)
            #
            # """
            # Inputデータと同じ行数を持つTableクラスを生成。
            # - 列名はcol_out変数値
            # - 列数は1
            # """
            # col_out = "sum"
            # tmp_domain = Domain([ContinuousVariable.make(col_out)])
            # n_row = len(self.A)
            # print("tmp_domain:", tmp_domain)
            # print("len of row:", n_row)
            #
            # tmp_table = Table.from_domain(tmp_domain, n_rows=n_row)
            # print("tmp_tableの確認:", tmp_table)
            #
            # """
            # 以下はInputから入力された1,2番目の列の同行の値を加算して、上記で生成した同行の変数に代入している。
            # これで2列の値が加算された1列が生成される。
            # #TODO: 確認後消してOK.
            # #TODO: ここに経過時間へ変換する関数を呼び出し、変換結果を利用できるようにしましょう。
            # """
            # for i in range(n_row):
            #     print(f"i:{i}, name:{names[0].name}")
            #     print(f"res:{self.A[i, names[0].name]}")
            #     tmp_table[i, col_out] = self.A[i, names[0].name] + self.A[i, names[1].name]
            extract_pos = eval(self.extract_pos_str)
            # FIXME: DateTime型がなければエラーとなるかも、要修正。
            if len(self.A) == 0:
                raise Exception("文字の列がありません")
                return
            tmp_table = morphological_analysis8(self.A, contains=extract_pos)  # type: orangecontrib.text.Corpus # FIXME: 最初のテキストを解析
            # 出力に接続されたWidgetへ結果を送信するため、Outputへ上記生成したTableを転送する
            self.Outputs.out_mine.send(tmp_table)


if __name__ == "__main__":
    """ This code can attempt action of this widget"""
    from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0

    WidgetPreview(MorphParser).run()
