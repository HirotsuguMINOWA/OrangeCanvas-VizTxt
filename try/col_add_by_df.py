"""
Corpusに列追加 : DF経由で列追加編
"""
# widgetsフォルダに居る事前提
# in_table = Table.from_file("../tutorials/date_time_sample.xlsx")
from pathlib import Path

import numpy as np
import pandas as pd
from Orange.data.pandas_compat import OrangeDataFrame
from Orange.data import pandas_compat
from orangecontrib.text import Corpus

p = Path(__file__).parent.parent.joinpath("tutorials").joinpath("src.csv")
in_corpus = Corpus.from_file("../orangecontrib/example/tutorials/src.csv")
# in_table = Table.from_file("date_time_sample.xlsx")
# TODO: in_tableの
print("[Debug] Domain:", in_corpus.domain)
print("[Debug] Attributes:", in_corpus.attributes)
# >> [Date, Time, DateTime, Value1, Class]と表示されます。
# TODO: 1列目は年月日、2列目は時間のみ、3列目は1列目+2列目の各行の合算です。これを読み込み、変換する事
# result = convert(source=in_corpus)  # FIXME: 手動で変換しているので直すべし
p: OrangeDataFrame = in_corpus.metas_df
print("Pandoas", p)
df2 = pd.DataFrame({'A': ['A4', 'A5', 'A6', 'A6'],
                    'C': ['C4', 'C5', 'C6', 'C6']},
                   # index=["_o4","_o5","_o6","_o7"]) # row名を指定するのが期待どおりcombineされるコツ。
                   index=[f"_o{x}" for x in in_corpus.ids]) # row名を指定するのが期待どおりcombineされるコツ。
# res = pd.concat(p, df2)
# res=p.(other=df2)
res=p.combine_first(df2)
print(res)
if res is None:
    raise Exception("result is None")
print("[Info] Result in main:\n", res)
# ret = in_table + result
# print("Result:",ret)
