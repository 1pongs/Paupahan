from django.test import SimpleTestCase

from paupahan.tenants.templatetags.formatters import format_amount


class FormatAmountFilterTests(SimpleTestCase):
    def test_format_amount_default(self):
        self.assertEqual(format_amount(1234.56), "1,234.56")

    def test_format_amount_zero_decimals(self):
        # decimals may come as a string from template usage
        self.assertEqual(format_amount("1234.00", "0"), "1,234")

    def test_format_amount_none(self):
        self.assertEqual(format_amount(None), "")

    def test_format_amount_non_numeric(self):
        self.assertEqual(format_amount("not-a-number"), "not-a-number")
