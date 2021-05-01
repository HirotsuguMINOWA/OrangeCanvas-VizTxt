"""
【失敗】
既存Corpusクラスに列追加: .extend_attributes/.extend_corpusメソッドによる追加
- sharpが合わないやら、色々エラーがでてくる。
- pd.df経由が素直で楽そう。
"""
# widgetsフォルダに居る事前提
# in_table = Table.from_file("../tutorials/date_time_sample.xlsx")
from pathlib import Path

import numpy as np
from orangecontrib.text import Corpus

p = Path(__file__).parent.parent.joinpath("tutorials").joinpath("src.csv")
in_corpus = Corpus.from_file("../orangecontrib/example/tutorials/src.csv")
# in_table = Table.from_file("date_time_sample.xlsx")
# TODO: in_tableの
print("[Debug] Domain:", in_corpus.domain)
# >> [Date, Time, DateTime, Value1, Class]と表示されます。
# TODO: 1列目は年月日、2列目は時間のみ、3列目は1列目+2列目の各行の合算です。これを読み込み、変換する事
# result = convert(source=in_corpus)  # FIXME: 手動で変換しているので直すべし
res = in_corpus.extend_attributes(X=np.ndarray([["test"], ["test"], ["test"], ["test"]]), feature_names=["test1"])
if res is None:
    raise Exception("result is None")
print("[Info] Result in main:\n", res)
# ret = in_table + result
# print("Result:",ret)
