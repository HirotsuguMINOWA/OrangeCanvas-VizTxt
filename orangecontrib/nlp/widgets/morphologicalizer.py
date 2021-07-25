"""
- 概略: DataFrame(Table)の日付を経過時間に変換する関数
- TODO: 上記を作成しましょう、大倉君。
- fileを別に分ける理由: こちらはOrangeCanvasに組み込む必要はありません。PyCharmのrunコマンドで実行され、コードを確認できます。OrangeCanvasに組み込まない事で開発効率を上げています。

"""
# from strenum import StrEnum
from enum import Enum
from logging import getLogger
# from datetime import datetime
from pathlib import Path
from typing import List, TypeVar, Generic

from Orange.data import Table
from janome.tokenizer import Tokenizer
from orangecontrib.text.corpus import Corpus

t = Tokenizer()

logger = getLogger(__file__)


class POS(str, Enum):
    # class POS(StrEnum):
    noun = "名詞"
    verb = "動詞"
    adverb = "形容詞"


from .module.comp import comp

T = TypeVar('T', Corpus, Table)


# TODO: logger置き換えろ
# FIXME: print(str(token).decode('utf8'))がwindowsには必要かも
def morphological_analysis8(a_corpus: Generic[T], contains: List[List[str]] = []) -> T:
    """
    pd.DFを用いて、src corpusへ連結する
    :param a_corpus:
    :param contains:
    :return:
    """
    out = a_corpus.copy()
    if len(out.metas) == 0:
        raise Exception("文字の列がありません")
        return

    def parser(a_sent: str) -> str:
        """
        一文を形態素解析した結果(形態素を半角空白で結ぶ)を返す
        :param a_sent:
        :return:
        """
        if not isinstance(a_sent, str):
            print("[Debug] 文字列以外が渡された:", a_sent, "Type:", type(a_sent))
        # return [" ".join(r.surface for r in t.tokenize(c) if r.part_of_speech.split(',')[0] in contains) for c in a_sent]
        print("[Debug] Inputted: ", a_sent)
        # res = [(r.surface, r.part_of_speech) for r in t.tokenize(a_sent) if r.part_of_speech.split(',')[0] in comp(contains, r.part_of_speech.split(','))]
        res = [(r.surface, r.part_of_speech) for r in t.tokenize(a_sent) if comp(contains, r.part_of_speech.split(','))]
        print("[Debug] Row:", res)
        res2 = " ".join(r.surface for r in t.tokenize(a_sent) if comp(contains, r.part_of_speech.split(',')))
        print("[Debug] Res2:", res2)
        return res2

    print("[Debug] shape:", a_corpus.metas.shape)
    print("[Debug] meta:", a_corpus.metas)

    for i_r in range(a_corpus.metas.shape[0]):  ## Row
        n_c = a_corpus.metas.shape[1]  ## Col
        # print(f"[Debug] n_c:{n_c}")

        if n_c == 1:
            """Usually, this scope will be performed"""
            # out.metas[i_r] = [" ".join(r.surface for r in t.tokenize(c) if r.part_of_speech in contains) for c in out.metas[i_r]]
            # TODO: Word(もとの言葉)を返しているが、GUIで選べれるように変更する事
            res = [r.surface for r in t.tokenize(a_corpus.metas[i_r][0]) if comp(contains, r.part_of_speech.split(','))]
            out.metas[i_r][0] = " ".join(res)
        else:
            for i_c in range(n_c):  ## Col
                # in_corpus.metas[i_r, i_c] = [" ".join(r.surface for r in t.tokenize(c) if r.part_of_speech.split(',')[0] in contains) for c in in_corpus.metas[i_r, i_c]]
                out.metas[i_r, i_c] = parser(a_corpus.metas[i_r, i_c])

    #
    # print("[Info] Result in main:\n", ret_corpus)
    return out


if __name__ == '__main__':
    # 日付が入ったExcelロード
    try:
        # widgetsフォルダに居る事前提
        # in_table = Table.from_file("../tutorials/date_time_sample.xlsx")
        p = Path(__file__).parent.parent.joinpath("tutorials").joinpath("src.csv")
        in_corpus = Corpus.from_file(p.as_posix())
        # in_table = Table.from_file("date_time_sample.xlsx")
        # TODO: in_tableの
        print("[Debug] Domain:", in_corpus.domain)
        # >> [Date, Time, DateTime, Value1, Class]と表示されます。
        # TODO: 1列目は年月日、2列目は時間のみ、3列目は1列目+2列目の各行の合算です。これを読み込み、変換する事
        # result = convert(source=in_corpus)  # FIXME: 手動で変換しているので直すべし
        result = morphological_analysis8(source=in_corpus)  # FIXME: 手動で変換しているので直すべし
        if result is None:
            raise Exception("result is None")
        print("[Info] Result in main:\n", result)
        # ret = in_table + result
        # print("Result:",ret)
    except OSError as e:
        import os

        print(f"PWD:{os.getcwd()},ERROR:{e}")
        import sys

        for p in sys.path:
            print(p)
