
import pytest

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_output(self, category_factory):
        category = category_factory(name='test_category')

        assert category.__str__() == 'test_category'


class TestProductlineModel:
    def test_str_sku_output_(self, productline_factory):
        productline = productline_factory()

        assert productline.__str__() == 'test_SKU_1'
