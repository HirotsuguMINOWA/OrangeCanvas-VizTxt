# from orangewidget import gui
import re
import typing as ty

import numpy as np
from AnyQt.QtWidgets import QGridLayout, QLabel
from Orange.data import Table
from Orange.widgets.utils.signals import Input, Output
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
    if len(in_corpus.metas) == 0:
        raise Exception("文字の列がありません")
        return
    #
    in_corpus = in_corpus.copy()
    del_candidates = []
    for i_r in range(in_corpus.metas.shape[0]):  ## Row
        for i_c in range(in_corpus.metas.shape[1]):  ## Col
            try:
                sent = in_corpus.metas[i_r, i_c]
                res = re.sub(pattern, "", sent)
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
        tmp_metas = in_corpus.metas
        tmp_X = in_corpus.X
        tmp_Y = in_corpus.Y
        tmp_W = in_corpus.W
        for i in del_candidates:
            tmp_metas = np.delete(tmp_metas, i, 0)
            tmp_X = np.delete(tmp_X, i, 0)
            tmp_Y = np.delete(tmp_Y, i, 0)
            tmp_W = np.delete(tmp_W, i, 0)
        ret_corpus = Corpus(domain=in_corpus.domain, X=tmp_X, Y=tmp_Y, metas=tmp_metas)
    else:
        ret_corpus = in_corpus
    return ret_corpus


class FilterWidget(OWWidget):
    # Widget needs a name, or it is considered an abstract widget
    # and not shown in the menu.
    name = "Filter"
    icon = "icons/mywidget.svg"  # FIXME: 要修正
    want_main_area = False
    extract_pos_str: str = "《.*》|［.*］|[「」、。]"  # lineEditと合わせて要修正

    def __init__(self):  # , parent):
        """
        :param parent: orange3-textに倣う
        ■ 失敗
        - controlArea.SetLayout()しても、生成したLayoutに置換されない
        """
        super().__init__()
        self.A: Table = None
        self._setup_gui()

    def _setup_gui(self):
        form_main = gui.QtWidgets.QFormLayout()
        form_main.setContentsMargins(5, 5, 5, 5)
        grid = QGridLayout()
        #
        ext_pos01 = QLabel("除去する正規表現パタン: \"")
        grid.addWidget(ext_pos01, 0, 0)
        ext_pos02 = gui.lineEdit(
            self, self, "extract_pos_str", controlWidth=400
        )
        grid.addWidget(ext_pos02, 0, 1)
        ext_pos02 = QLabel("\"")
        grid.addWidget(ext_pos02, 0, 2)
        form_main.addRow(grid)
        #
        self.controlArea.layout().addLayout(form_main)  # Set as MainForm
        #
        self.submit_button = gui.button(
            self.controlArea, self, "OK", self.accept
        )

    def load_ui_values(self):
        self.key_edit.setText(self.cm_key)
        self.secret_edit.setText(self.cm_secret)

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
        self.A: ty.Optional[Table, Corpus] = a

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
            tmp_table = filter_regexp(
                self.A, self.extract_pos_str
            )  # type: orangecontrib.text.Corpus # FIXME: 最初のテキストを解析
            self.Outputs.out_mine.send(tmp_table)


if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0

    WidgetPreview(FilterWidget).run()
