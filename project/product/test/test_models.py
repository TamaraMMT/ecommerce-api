
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
            productline_factory,

    ):
        product = product_factory()
        productline_factory(product=product, order=1)

        # Trying to create another Productline instance with the same order, should raise IntegrityError
        with pytest.raises(IntegrityError):
            productline_factory(product=product, order=1)


class TestProductImageModel:
    def test_str_image_productline(
        self,
        productline_factory,
        product_image_factory,
    ):
        productline = productline_factory(sku="sku_test")
        image = product_image_factory(order=1, product_line=productline)

        assert image.__str__() == 'sku_test_img'


class TestProductTypeModel:
    def test_str_method_producttype(self, product_type_factory):
        obj = product_type_factory.create(name="test_type_product")

        assert obj.__str__() == "test_type_product"


class TestAttributeTypeModel:
    def test_str_method_attr_type(self, attribute_factory, product_type_factory):
        product_type = product_type_factory(name="TestProductType")
        obj = attribute_factory.create(attribute_name="TestAttributeName", product_type=product_type)
        assert obj.__str__() == "TestProductType-TestAttributeName"



class TestProductlineAttributeValueModel:
    def test_unique_together(
            self,
            product_type_factory,
            product_factory,
            attribute_factory,
            productline_factory,
            productline_attribute_value_factory,


    ):
        # Create instances of ProductType, AttributeType, AttributeValue, Product y ProductLine
        product_type = product_type_factory()
        attr_type = attribute_factory(attribute_name="test_attribute", product_type=product_type)
        product = product_factory()
        productline = productline_factory(product=product)

        # Create instances of ProductlineAttributeValue
        productline_attribute_value_factory(
            attribute_value="AttributeValue",
            attribute=attr_type,
            productline=productline
        )

        # Trying to create another ProductlineAttributeValue instance with the same values should raise IntegrityError
        with pytest.raises(IntegrityError):
            productline_attribute_value_factory(
                attribute_value="AttributeValue",
                attribute=attr_type,
                productline=productline
            )
