from orangecontrib.examples.widgets.mywidget import MyWidget

class TestMyWidget(WidgetTest):
    def setUp(self):
        self.widget = self.create_widget(MyWidget)

    def test_addition(self):
        self.assertEqual(1 + 1, 2)
