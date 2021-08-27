"""
- fileを別に分ける理由: こちらはOrangeCanvasに組み込む必要はありません。PyCharmのrunコマンドで実行され、コードを確認できます。OrangeCanvasに組み込まない事で開発効率を上げています。
"""
from pathlib import Path
from typing import List, TypeVar

from Orange.data import Table
from janome.tokenizer import Tokenizer
from loguru import logger
from orangecontrib.text.corpus import Corpus

if __name__ == "__main__":  # FIXME: to be removed
    from module.comp import comp
else:
    from .module.comp import comp

t = Tokenizer()

T = TypeVar('T', Corpus, Table)


def parser(a_sent: str) -> str:
    """
    一文を形態素解析した結果(形態素を半角空白で結ぶ)を返す
    :param a_sent:
    :return:
    """
    if not isinstance(a_sent, str):
        logger.debug(f"文字列以外が渡された:{a_sent} Type:{type(a_sent)}")
    logger.debug(f"Inputted: {a_sent}")
    res2 = " ".join(r.surface for r in t.tokenize(a_sent) if comp(contains, r.part_of_speech.split(',')))
    logger.debug(f"Res: {res2}")
    return res2


# FIXME: print(str(token).decode('utf8'))がwindowsには必要かも
def morphological_analysis8(src: T, contains: List[List[str]]) -> T:
    """
    pd.DFを用いて、src corpusへ連結する
    :param src:
    :param contains: 抽出したい品詞(POS)が書かれたlist
    :return:
    """
    out = src.copy()
    if len(out.metas) == 0:
        raise Exception("文字の列がありません")
        return

    logger.debug(f"shape:{src.metas.shape}")
    logger.debug(f"meta:{src.metas}")

    for i_r in range(src.metas.shape[0]):  ## Row
        n_c = src.metas.shape[1]  ## Col

        if n_c == 1:
            """Usually, this scope will be performed"""
            # out.metas[i_r] = [" ".join(r.surface for r in t.tokenize(c) if r.part_of_speech in contains) for c in out.metas[i_r]]
            # res = [r.surface for r in t.tokenize(src.metas[i_r][0]) if comp(contains, r.part_of_speech.split(','))]
            out.metas[i_r][0] = " ".join(r.surface for r in t.tokenize(src.metas[i_r][0]) if comp(contains, r.part_of_speech.split(',')))
        else:
            for i_c in range(n_c):  ## Col
                # in_corpus.metas[i_r, i_c] = [" ".join(r.surface for r in t.tokenize(c) if r.part_of_speech.split(',')[0] in contains) for c in in_corpus.metas[i_r, i_c]]
                out.metas[i_r, i_c] = parser(src.metas[i_r, i_c])
    return out


def test_from_corpus(contains):
    # widgetsフォルダに居る事前提
    # in_table = Table.from_file("../tutorials/date_time_sample.xlsx")
    p = Path(__file__).parent.parent.joinpath("tutorials").joinpath("src.csv")
    in_corpus = Corpus.from_file(p.as_posix())

    # in_table = Table.from_file("date_time_sample.xlsx")
    # TODO: in_tableの
    logger.debug("Tableクラスの解析")
    logger.debug("Domain:", in_corpus.domain)
    # >> [Date, Time, DateTime, Value1, Class]と表示されます。
    # TODO: 1列目は年月日、2列目は時間のみ、3列目は1列目+2列目の各行の合算です。これを読み込み、変換する事
    # result = convert(source=in_corpus)  # FIXME: 手動で変換しているので直すべし
    result = morphological_analysis8(src=in_corpus, contains=contains)  # FIXME: 手動で変換しているので直すべし
    if result is None:
        raise Exception("result is None")
    logger.info("Result in main:\n", result)


if __name__ == '__main__':
    """Below is trial. If you check validation, make sure 'tests' dir for unit test"""
    # 日付が入ったExcelロード
    # import sys, os

    try:
        # a_path = Path(__file__).parent.joinpath("module")
        # print("inc?:", a_path)
        # sys.path.append(a_path)
        #
        ###########
        # test_from_corpus
        #
        contains = [["名詞"], ["形容詞"]]
        ret = test_from_corpus(contains=contains)
        print("Result(Corpus):", ret)

        p = Path(__file__).parent.parent.joinpath("tutorials").joinpath("src.csv")
        in_txt = Table.from_file(p.as_posix())
        logger.debug("Domain:", in_txt.domain)
        result = morphological_analysis8(src=in_txt, contains=[["名詞"], ["形容詞"]])
        if result is None:
            raise Exception("result is None")
        logger.info(f"Result in main:\n{result}")
    except OSError as e:
        import os

        logger.debug(f"PWD:{os.getcwd()}, ERROR:{e}")
        import sys

        for p in sys.path:
            logger.debug(p)
