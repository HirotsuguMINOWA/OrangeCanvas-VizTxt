"""
【失敗】
既存Corpusクラス内のデータ入れ替え。OK!!
ただし、行のりサイズはまだできていない
"""
# widgetsフォルダに居る事前提
# in_table = Table.from_file("../tutorials/date_time_sample.xlsx")
from pathlib import Path

from Orange.data import Table

from orangecontrib.nlp.widgets.morphologicalizer import morphological_analysis8

p = Path(__file__).parent.parent.joinpath("tutorials").joinpath("src.csv")
# in_corpus = Corpus.from_file("../orangecontrib/nlp/tutorials/src.csv")
loaded_dat = Table.from_file("../tutorials/src.csv")
# in_table = Table.from_file("date_time_sample.xlsx")
# TODO: in_tableの
print("[Debug] Input:", loaded_dat)
print("[Debug] Domain:", loaded_dat.domain)
print("Meta部のshape:", loaded_dat.metas.shape)
print("Meta部の「最初のcell」[0,0]の抽出", loaded_dat.metas[0, 0])
# out_corpus = morphological_analysis8(a_corpus=loaded_dat, contains=[POS.noun, POS.verb])
out_corpus = morphological_analysis8(a_corpus=loaded_dat, contains=[['名詞'], ['形容詞']])
print("[Info] Result in main:\n", out_corpus)
print("Type of output:", type(out_corpus))
