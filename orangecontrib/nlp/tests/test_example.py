import unittest

from Orange.data import Domain, StringVariable, ContinuousVariable, Table
from loguru import logger
from orangecontrib.text import Corpus

from orangecontrib.nlp.widgets.module.comp import comp
# from ..widgets.module.comp import comp
from orangecontrib.nlp.widgets.morphologicalizer import morphological_analysis8


# from Orange.widgets.tests.base import WidgetTest

class ExampleTests(unittest.TestCase):
    def setUp(self):
        """ Here is called first """
        self.general_rule = [
            [["名詞"], ["形容詞"]]
        ]

    def test_addition(self):
        self.assertEqual(1 + 1, 2)

    def test_comp_func(self):
        tlist = [
            # User want extraction, gotten pos, compared Result(bool)
            [[["名詞"], ["形容詞"]], ["名詞", "ほげほげ"], True],  # ルールの深さ<比較対象の深さ、の場合
            [[["名詞"]], ["名詞", "ほげほげ"], True],  # ルールの深さ<比較対象の深さ、の場合
            [
                [["名詞"], ["形容詞", "ほげほげ"]],
                ["形容詞"],
                False
            ]  # ルールの深さ>比較対象の深さ、の場合
        ]
        for a_pair in tlist:
            self.assertEqual(comp(a_pair[0], a_pair[1]), a_pair[2])

    def test_morphological_parser_func(self):
        # p = Path(__file__).parent.parent.joinpath("tutorials").joinpath("src.csv")
        # in_corpus = Corpus.from_file(p.as_posix())
        in_corpus = Corpus.from_list(
            domain=Domain(attributes=[ContinuousVariable('No')], metas=[StringVariable.make(name='test_col')]),
            rows=[[1, "太郎と花子は学校へ行った"], [3, "すもももももももものうち"]])
        print("Corpus", in_corpus)
        #
        # Apply
        res = morphological_analysis8(in_corpus, contains=self.general_rule[0])
        print("res:", res.metas)
        for x, y in zip(res.metas, [['太郎 花子 学校'], ['すもも もも もも うち']]):
            self.assertEqual(x, y)

    def test_morphological_parser_func2(self):
        in_corpus = Corpus.from_list(
            domain=Domain(attributes=[ContinuousVariable('No')], metas=[StringVariable.make(name='test_col')]),
            rows=[[1, "太郎と花子は学校へ行った"], [3, "すもももももももものうち"]])
        res = morphological_analysis8(in_corpus, contains=[["助詞", "連体化"]])
        print("res:", res.metas)
        for x, y in zip(res.metas, [[''], ['の']]):
            self.assertEqual(x, y)

    def test_morph_parse_from_table(self):
        logger.info("Test morphological parse to data stored into Table class")
        in_table = Table.from_list(
            domain=Domain(attributes=[ContinuousVariable('No')], metas=[StringVariable.make(name='test_col')]),
            rows=[[1, "太郎と花子は学校へ行った"], [3, "すもももももももものうち"]])
        print("src:", in_table)
        #
        # Apply
        res = morphological_analysis8(in_table, contains=self.general_rule[0])
        print("res:", res.metas)
        for x, y in zip(res.metas, [['太郎 花子 学校'], ['すもも もも もも うち']]):
            self.assertEqual(x, y)
