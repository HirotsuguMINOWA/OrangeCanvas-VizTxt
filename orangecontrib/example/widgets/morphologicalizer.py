"""
- 概略: DataFrame(Table)の日付を経過時間に変換する関数
- TODO: 上記を作成しましょう、大倉君。
- fileを別に分ける理由: こちらはOrangeCanvasに組み込む必要はありません。PyCharmのrunコマンドで実行され、コードを確認できます。OrangeCanvasに組み込まない事で開発効率を上げています。

"""
# from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple  # wappingするdatetimeの後におくべき

from Orange.data import (
    ContinuousVariable,
    Domain,
    Table,
    StringVariable, RowInstance,
)
from janome.tokenizer import Tokenizer
from orangecontrib.text.corpus import Corpus

t = Tokenizer()


def morphological_analysis(col_ja: Domain) -> Domain:
    name_col_out = "tokenized"
    n_row = len(col_ja)
    tmp_domain = Domain([ContinuousVariable.make(name_col_out)])
    ret = Table.from_domain(tmp_domain, n_rows=n_row)
    for i, row in enumerate(col_ja):
        # for token in t.tokenize(row):
        #     tmp_domain[i]=token
        tmp_domain[i] = " ".join([r.surface.decode('utf8') for r in t.tokenize(row)])  # Win用にutf8化している
    return tmp_domain


def morphological_analysis2(col_ja: list) -> Tuple[list, Domain]:
    name_col_out = "tokenized"
    # n_row = len(col_ja)
    tmp_domain = Domain([StringVariable.make(name_col_out)])
    # ret = Table.from_domain(tmp_domain, n_rows=n_row)
    ret = list()
    for i, row in enumerate(col_ja):
        # for token in t.tokenize(row):
        #     tmp_domain[i]=token
        # ret.append(" ".join([r.surface.decode('utf8') for r in t.tokenize(row)]))  # Win用にutf8化している
        ret.append(" ".join([r.surface for r in t.tokenize(row)]))  # Win用にutf8化している
    return ret, tmp_domain


def morphological_analysis3(col_ja: list) -> Table:
    """1つめのrowの解析しかできず"""
    name_col_out = "tokenized"
    n_row = len(col_ja)
    tmp_domain = Domain([], metas=[StringVariable(name_col_out)])
    # ret = Table.from_domain(tmp_domain, n_rows=n_row)
    ret = list()
    for i, row in enumerate(col_ja):
        # for token in t.tokenize(row):
        #     tmp_domain[i]=token
        # ret.append(" ".join([r.surface.decode('utf8') for r in t.tokenize(row)]))  # Win用にutf8化している
        # ret.append(" ".join([r.surface for r in t.tokenize(row)]))  # Win用にutf8化している
        # ret[i] = " ".join([r.surface for r in t.tokenize(row)])  # Win用にutf8化している
        ret.append(" ".join([r.surface for r in t.tokenize(row)]))
    data = Table.from_list(tmp_domain, [
        ret
    ])
    return data, tmp_domain


def morphological_analysis4(col_ja: Corpus) -> Table:
    """
    - Tableに結果格納して、上位の関数で元のCorpusへマージする？
    - このメソッドのver.5で既に各cellの解析ができている。そちらを参照し、こちらは見る必要ない。
    :param col_ja:
    :return:
    """
    name_col_out = "tokenized"
    n_row = len(col_ja)
    tmp_domain = Domain([], metas=[StringVariable(name_col_out)])
    tmp_table = Table.from_domain(tmp_domain, n_rows=n_row)
    ret = list()
    n_str_len = col_ja.metas.shape[1]  # 文字列colの数
    for i in range(n_str_len):
        ret.append(list())
    for i_r, row in enumerate(col_ja):  # type: int,RowInstance
        for i_c, cell in enumerate(row.list):  # type: int,str
            if isinstance(cell, str):
                for token in t.tokenize(cell):
                    ret[i_c][i_r].append(token)
                # ret.append(" ".join([r.surface.decode('utf8') for r in t.tokenize(row)]))  # Win用にutf8化している
                # ret.append(" ".join([r.surface for r in t.tokenize(row)]))  # Win用にutf8化している
                # ret[i] = " ".join([r.surface for r in t.tokenize(row)])  # Win用にutf8化している
                ret.append([" ".join([r.surface for r in t.tokenize(row)])])
                tmp_table[i_r] = " ".join([r.surface for r in t.tokenize(row)])
    t2 = Table.from_table(domain=tmp_domain, source=tmp_table)
    t3 = Table.from_list(domain=tmp_domain, rows=ret)
    Corpus.add
    return t3, tmp_domain


def morphological_analysis5(col_ja: Corpus) -> Corpus:
    """
    - 参考に残す。
    - Copus内のTableに該当する箇所へ、形態素解析の結果を格納しようと試みるコード
    - tryフォルダの中のサンプルを使え、そちらの方がシンプルで理解しやすい
    :param col_ja:
    :return:
    """
    name_col_out = "tokenized"
    n_row = len(col_ja)
    tmp_domain = Domain([], metas=[[StringVariable(name_col_out)] * len(col_ja.metas)])
    tmp_table = Table.from_domain(tmp_domain, n_rows=n_row)
    ret = list()
    for i_r, row in enumerate(col_ja.metas):
        for i_c, col in enumerate(row):
            if i_c == 0:
                ret.append([None] * len(col))
            # for token in t.tokenize(row):
            #     tmp_domain[i]=token
            # ret.append(" ".join([r.surface.decode('utf8') for r in t.tokenize(row)]))  # Win用にutf8化している
            # ret.append(" ".join([r.surface for r in t.tokenize(row)]))  # Win用にutf8化している
            # ret[i] = " ".join([r.surface for r in t.tokenize(row)])  # Win用にutf8化している
            # ret.append([" ".join([r.surface for r in t.tokenize(row)])])
            # ret.append(" ".join([r.surface for r in t.tokenize(col)]))
            ret[i_c+1][i_r] = " ".join(r.surface for r in t.tokenize(col))
            # tmp_table[i_c, i_r] = " ".join([r.surface for r in t.tokenize(row)])
    return col_ja

def morphological_analysis6(col_ja: Corpus) -> Table:
    """
    【廃棄】 gensimのDictionaryを使って、Corpusへのマージを試みた結果。
    - tryフォルダにsimpleなコードが入っているのでそちらを参考にすべき
    - .extend_corpus(document)を使って、拡張を試みようとしている。

    :param col_ja:
    :return:
    """
    name_col_out = "tokenized"
    for i, col in enumerate(range(2)):
        # col_ja = col_ja..add_column(variable=StringVariable(name_col_out + str(i)), data=["a", "a", "a", "a"], to_metas=True)
        # col_ja = col_ja.extend_corpus(metadata=["a", "a", "a", "a"], Y=StringVariable(name_col_out + str(i))) # ValueError: Extending corpus only works when X is emptywhile the shape of X is (4, 1)
        # col_ja = col_ja.set_text_features(["a", "a", "a", "a"])
        # col_ja=col_ja.extend_attributes(X=[["a"], ["a"], ["a"], ["a"]],feature_names=[StringVariable(name_col_out + str(i))])
        col_ja = col_ja.extend_attributes(X=[["a"], ["a"], ["a"], ["a"]], feature_names=[name_col_out + str(i)])
        from gensim import matutils
        words = ['アナタ', 'ブラウザ', 'ブック', 'マーク', 'ブック', 'マーク', '管理', 'ライフ', 'リスト', 'オススメ', '最近', 'ネット', 'サーフィン', '際', '利用', 'の', 'ライフ', 'リスト', 'サイト', 'ライフ', 'リスト',
                 'ひとこと', '自分', '専用', 'ブックマークサイト', 'ブラウザ', 'スタート', 'ページ', 'ブラウザ', 'ブック', 'マーク', '管理', '不要', '便利', 'サイト', 'の']
        dictionary = Corpus.from_list()
        dictionary.filter_extremes(no_below=20, no_above=0.3)
        tmp = dictionary.doc2bow(words)
        dense = list(matutils.corpus2dense([tmp], num_terms=len(dictionary)).T[0])
        col_ja = col_ja.extend_attributes(X=dense, feature_names=[name_col_out + str(i), "d"])
        # col_ja = col_ja.extend_attributes(X=[["a"], ["a"], ["a"], ["a"]], feature_names=[name_col_out + str(i)])
        # t2 = Table.from_table(domain=tmp_domain, source=tmp_table)
        # t3 = Table.from_list(domain=tmp_domain, rows=ret)
        # return t3, tmp_domain
        col_ja.metas

    return col_ja

# ##################### 以下は、不要
# class Unit(Enum):
#     second = auto()
#     minute = auto()
#     hour = auto()
#     day = auto()
#
#
# def get_elapsed_time(dt_in_1col: Table, unit: Unit = Unit.second) -> Tuple[int]:
#     """
#     datetime型値群から数値へ変換する
#     :param dt_in_1col: 経過時間を求めたい入力となるdatetime型の値群
#     :param unit: 変換単位. Unit.secondなら秒単位で経過時間を返却する
#     :return:
#     """
#     """
#     https://orange3.readthedocs.io/projects/orange-visual-programming/en/latest/loading-your-data/index.html
#     Datetime Format¶
#     To avoid ambiguity, Orange supports date and/or time formatted in one of the ISO 8601 formats. For example, the following values are all valid:
#
#     2016
#     2016-12-27
#     2016-12-27 14:20:51
#     16:20
#     """
#     # if len(dt_in_1col.domain) != 1 or dt_in_1col.domain[0].name != "DateTime":
#     if len(dt_in_1col.domain) != 1 or not dt_in_1col.domain[0].is_time:
#         raise Exception("[Bug] Please fix given value:(1)type Table,(2)len(column)==1,(3)Its domain is DateTime,(4) Input data was DateTime(Not Date or Time)")
#     # Prepare storage to return
#     col_out = "ElapseTime"
#     n_row = len(dt_in_1col)
#     tmp_domain = Domain([ContinuousVariable.make(col_out)])
#     ret = Table.from_domain(tmp_domain, n_rows=n_row)
#     # TODO: 1列Table作れ、それに経過時間を保存、returnしろ。
#     # FIXME: 特定セル(1行1列)の欠損値の処理
#     # for i, dat in enumerate(dt_in_1col[:, 0]):
#
#     # for i, dat in enumerate(dt_in_1col):
#     #     # ret[i, 0] = dt.datetime.fromisoformat(str(dat[0]))  # convert type Value to datetime. py>=3.7.
#     #     ret[i, 0] = ia
#     elapsed_time = None
#     for i, dat in enumerate(dt_in_1col):
#         dt_: dt.datetime = dt.datetime.fromisoformat(str(dat[0]))  # convert type Value to datetime. py>=3.7.
#         # t: time = list({row[1].value})[0]
#         if i == 0:
#             """基準の日付を作成"""
#             # dt_criteria = datetime.combine(dt.date(), t)
#             dt_criteria = dt_
#             # elapsed_time = dt_criteria
#             ret[i, 0] = 0
#             # ws.cell(i + start_row, out_col + 1).value = 0
#         else:
#             """上記以外の差分日を求める"""
#             # dt = datetime.combine(dt.date(), t)
#             diff: dt.timedelta = dt_ - dt_criteria
#             # res = datetime.strptime(f"{date_tmp.year}", "%Y/%m/%d %H:%M:%S")
#             # ws.cell(i + start_row, out_col).value = dt  # date+timeの書き込み
#             # ws.cell(i + start_row, out_col + 1).value = diff.total_seconds()  # 経過時間の書き込み
#             ret[i, 0] = diff.total_seconds()  # 経過時間の書き込み
#             if diff.total_seconds() == 0:
#                 raise Exception("差が0になるエラー")
#     return ret
#
#
# def detect_1st_datetime_col(source: Table) -> int:
#     """ Return index of first(most left) column(field) of datetime type
#     - Return minus value if not found a datetime type column.
#     :param source:
#     """
#     for i, a_domain in enumerate(source.domain):
#         # if a_domain.name == "DateTime":
#         if a_domain.is_time:  # Check whether var is TimeVar or not.
#             # col_idx_ = i
#             print(f"[Debug] DateTime col found at No.{i + 1}(idx:{i})")
#             return i
#     else:
#         return -100


def convert(source: Corpus, col_idx: Optional[int] = None) -> Optional[Table]:
    """
    - 日付(Data, Time, DateTime)を経過時間(日,時間、分、秒)などに直す関数
    :param source: 変換したいデータが入ったTableクラスのデータ
    :param col_idx: 変換したい日付データが入ったsourceの列番号。Noneなら最も若い番号のDateTimeを変換する
    :return:
    """
    if len(source.metas) == 0:
        raise Exception("文字の列がありません")
        return
    # for var_cls in source.text_features:
    # # Detect datetime col.
    # if col_idx is None:
    #     target: int = detect_1st_datetime_col(source)
    # Get output table
    # ret = None
    # if col_idx >= 0:
    #     # ret = Table.from_domain(morphological_analysis(source[:, col_idx]))
    #     # Tableは不可。内部で数値に変換してしまう？
    #     # result, tmp_domain = morphological_analysis2(source.documents)
    #     # ret = Corpus.from_documents(documents=result, name="morphologies", attributes=tmp_domain)
    #     tmp_table, tmp_domain = morphological_analysis5(source)
    #     ret = Corpus.from_table(domain=tmp_domain, source=tmp_table)
    # return ret
    # t_convd, tmp_domain = morphological_analysis5(source)
    # ret = Corpus.from_table(domain=tmp_domain, source=t_convd)
    # ret = Corpus.add_column()
    # return morphological_analysis5(source)
    return morphological_analysis4(source)


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
        result = convert(source=in_corpus)  # FIXME: 手動で変換しているので直すべし
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
