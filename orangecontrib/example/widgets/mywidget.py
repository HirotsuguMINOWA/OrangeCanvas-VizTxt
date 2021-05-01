# from orangewidget import gui
from Orange.data import Table
from Orange.widgets.utils.signals import Input, Output
# from Orange.widgets.widget import OWWidget
from Orange.widgets.widget import OWWidget

# from conv2elapsed_time import convert  # not found
# from orangecontrib.example.widgets.conv2elapsed_time import convert
from orangecontrib.example.widgets.morphologicalizer import convert


class MyWidget(OWWidget):
    # Widget needs a name, or it is considered an abstract widget
    # and not shown in the menu.
    name = "MorphorerJPN"  # FIXME: 名前修正しよう
    icon = "icons/mywidget.svg"  # FIXME: 要修正, 著作権問題が気になるため
    want_main_area = False

    def __init__(self):
        """

        ■ 失敗
        - controlArea.SetLayout()しても、生成したLayoutに置換されない
        """
        super().__init__()
        self.A: Table = None

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

    class Inputs:
        """
        get Inputs
        """
        input_data = Input("Data", Table, default=True)

    class Outputs:
        out_mine = Output("Data", Table)

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
            # FIXME: DateTime型がなければエラーとなるかも、要修正。
            tmp_table = convert(self.A, col_idx=0)  # FIXME: 最初のテキストを解析
            # 出力に接続されたWidgetへ結果を送信するため、Outputへ上記生成したTableを転送する
            self.Outputs.out_mine.send(tmp_table)


if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0

    WidgetPreview(MyWidget).run()
