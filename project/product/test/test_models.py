
import pytest
from django.db.utils import IntegrityError

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_output(self, category_factory):
        category = category_factory(name='test_category')

        assert category.__str__() == 'test_category'


class TestProductModel:
    def test_str_name_product(self, product_factory):
        product = product_factory(name='product1')

        assert product.__str__() == 'product1'


class TestProductlineModel:
    def test_str_sku_output_(self, productline_factory):
        productline = productline_factory(sku='test_SKU_0')

        assert productline.__str__() == 'test_SKU_0'

    def test_unique_order_productline_per_product(
            self,
            product_factory,
            productline_factory
    ):
        product = product_factory()
        productline_factory(product=product, order=1)

        with pytest.raises(IntegrityError):
            productline_factory(product=product, order=1)
