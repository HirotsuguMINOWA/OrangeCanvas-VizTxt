# from orangewidget import gui
import re

import numpy as np
from AnyQt.QtWidgets import QFormLayout
from Orange.data import Table
from Orange.widgets.utils.signals import Input, Output
# from Orange.widgets.widget import OWWidget
from Orange.widgets.widget import OWWidget
from orangecontrib.text import Corpus

try:
    from orangewidget import gui
except ImportError:
    from Orange.widgets import gui


def filter_regexp(in_corpus: Corpus, pattern: str) -> Corpus:
    """
    pd.DFを用いて、src corpusへ連結する
    :param pattern:
    :param in_corpus:
    :return:
    """
    # print("[Debug] Domain:", in_corpus.domain)
    # print("Meta部のshape:", in_corpus.metas.shape)
    # print("Meta部の「最初のcell」[0,0]の抽出", in_corpus.metas[0, 0])
    if len(in_corpus.metas) == 0:
        raise Exception("文字の列がありません")
        return
    #
    in_corpus=in_corpus.copy()
    del_candidates = []
    for i_r in range(in_corpus.metas.shape[0]):  ## Row
        for i_c in range(in_corpus.metas.shape[1]):  ## Col
            try:
                sent = in_corpus.metas[i_r, i_c]
                res = re.sub(pattern, '', sent)
                if res is None or res == "":
                    del_candidates.append(i_r)
                in_corpus.metas[i_r, i_c] = res
            except Exception as e:
                print(f"patn:{pattern},sent:{sent},i_r:{i_r}")
                return None


        # 不要
        # if i_r == 2 or i_r == 11:
        #     print(f"row:{i_r} was res:{res}")
    # Delete rows AND create new Corpus
    if len(del_candidates) > 0:
        del_candidates.sort(reverse=True)
        print(f"res_cand:{del_candidates}")
        tmp_metas = in_corpus.metas
        tmp_X = in_corpus.X
        tmp_Y = in_corpus.Y
        tmp_W = in_corpus.W
        for i in del_candidates:
            tmp_metas = np.delete(tmp_metas, i, 0)
            tmp_X = np.delete(tmp_X, i, 0)
            tmp_Y = np.delete(tmp_Y, i, 0)
            tmp_W = np.delete(tmp_W, i, 0)
        ret_corpus = Corpus(
            domain=in_corpus.domain,
            X=tmp_X,
            Y=tmp_Y,
            metas=tmp_metas)
    else:
        ret_corpus = in_corpus
    #
    # print("[Info] Result in main:\n", ret_corpus)
    return ret_corpus


class FilterWidget(OWWidget):
    # Widget needs a name, or it is considered an abstract widget
    # and not shown in the menu.
    name = "filter_widget"  # FIXME: 名前修正しよう
    icon = "icons/mywidget.svg"  # FIXME: 要修正, 著作権問題が気になるため
    want_main_area = False
    key_input: str = '《.*》|［.*］|[「」、。]'  # lineEditと合わせて要修正

    def __init__(self):  # , parent):
        """
        :param parent: orange3-textに倣う
        ■ 失敗
        - controlArea.SetLayout()しても、生成したLayoutに置換されない
        """
        super().__init__()
        self.A: Table = None
        # self.parent = parent

        # # GUIパネルの構築
        # label = QLabel("【未だ有効じゃない】Column of DateTime Converted")
        # self.setLayout(QGridLayout())
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
        form = QFormLayout()
        form.setContentsMargins(5, 5, 5, 5)
        self.key_edit = gui.lineEdit(self, self, 'key_input', controlWidth=400)
        form.addRow('Regexp for filtering:', self.key_edit)
        self.controlArea.layout().addLayout(form)
        self.submit_button = gui.button(self.controlArea, self, "OK", self.commit)

    class Inputs:
        """
        get Inputs
        """
        input_data = Input("Data", Corpus, default=True)

    class Outputs:
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
            tmp_table = filter_regexp(self.A, self.key_input)  # type: orangecontrib.text.Corpus # FIXME: 最初のテキストを解析
            # 出力に接続されたWidgetへ結果を送信するため、Outputへ上記生成したTableを転送する
            self.Outputs.out_mine.send(tmp_table)


if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0

    WidgetPreview(FilterWidget).run()
