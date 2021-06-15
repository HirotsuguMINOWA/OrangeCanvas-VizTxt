"""
【失敗】
既存Corpusクラス内のデータ入れ替え。OK!!
ただし、行のりサイズはまだできていない
"""
# widgetsフォルダに居る事前提
# in_table = Table.from_file("../tutorials/date_time_sample.xlsx")
from pathlib import Path

from orangecontrib.text import Corpus

p = Path(__file__).parent.parent.joinpath("tutorials").joinpath("src.csv")
in_corpus = Corpus.from_file("../orangecontrib/nlp/tutorials/src.csv")
# in_table = Table.from_file("date_time_sample.xlsx")
# TODO: in_tableの
print("[Debug] Domain:", in_corpus.domain)
print("Meta部のshape:", in_corpus.metas.shape)
print("Meta部の「最初のcell」[0,0]の抽出", in_corpus.metas[0, 0])
for i_r in range(in_corpus.metas.shape[0]):  ## Row
    for i_c in range(in_corpus.metas.shape[1]):  ## Col
        in_corpus.metas[i_r, i_c] = in_corpus.metas[i_r, i_c] + "あほ"
print("[Info] Result in main:\n", in_corpus)
