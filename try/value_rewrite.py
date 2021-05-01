"""
Corpusクラス内の既存の文字列の置換 → 実現

"""
# widgetsフォルダに居る事前提
# in_table = Table.from_file("../tutorials/date_time_sample.xlsx")
from pathlib import Path

from orangecontrib.text import Corpus

p = Path(__file__).parent.parent.joinpath("tutorials").joinpath("src.csv")
in_corpus = Corpus.from_file("../orangecontrib/example/tutorials/src.csv")
print("[Debug] Domain:", in_corpus.domain)
print("[Debug] Attributes:", in_corpus.attributes)
for i, col in enumerate(in_corpus.metas):
    for i_r, row in enumerate(col):
        in_corpus.metas[i, i_r] = row + str("hoge")
        print(row)
print(in_corpus)