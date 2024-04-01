
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
    def test_str_sku_output_(self, productline_factory, attribute_value_factory):
        attr = attribute_value_factory(attribute_value="test")
        productline = productline_factory(sku='test_SKU_0', attribute_value=(attr,))
        print(productline, 'prdoductlineeeeeeee')

        assert productline.__str__() == 'test_SKU_0'

    def test_unique_order_productline_per_product(
            self,
            product_factory,
            productline_factory,
            attribute_value_factory,

    ):
        attr = attribute_value_factory(attribute_value="test")
        product = product_factory()
        productline_factory(product=product, order=1, attribute_value=(attr,))

        # Trying to create another Productline instance with the same order, should raise IntegrityError
        with pytest.raises(IntegrityError):
            productline_factory(product=product, order=1)


class TestProductImageModel:
    def test_str_image_productline(
        self,
        productline_factory,
        product_image_factory,
        attribute_value_factory
    ):
        attr = attribute_value_factory(attribute_value="test")
        productline = productline_factory(sku="sku_test", attribute_value=(attr,))
        image = product_image_factory(order=1, product_line=productline)

        assert image.__str__() == 'sku_test_img'


class TestProductTypeModel:
    def test_str_method_producttype(self, product_type_factory):
        obj = product_type_factory.create(name="test_type_product")

        assert obj.__str__() == "test_type_product"


class TestAttributeTypeModel:
    def test_str_method_attr_type(self, attribute_type_factory, product_type_factory):
        prducttype = product_type_factory.create(name="test_type_product")
        obj = attribute_type_factory(name="test_attributetype", product_type= prducttype)

        assert obj.__str__() == "test_attributetype"


class TestAttributeValueModel:
    def test_str_method_attr_value(self, attribute_value_factory, attribute_type_factory):
        obj_a = attribute_type_factory(name="test_attribute")
        obj_b = attribute_value_factory(attribute_value="test_value", attribute_type=obj_a)

        assert obj_b.__str__() == "test_attribute-test_value"


class TestProductlineAttributeValueModel:
    def test_unique_together(
            self,
            product_type_factory,
            product_factory,
            attribute_type_factory,
            attribute_value_factory,
            productline_factory,
            productline_attribute_value_factory,


    ):
        # Create instances of ProductType, AttributeType, AttributeValue, Product y ProductLine
        product_type = product_type_factory()
        attr_type = attribute_type_factory(name="test_attribute", product_type=product_type)
        attr_value = attribute_value_factory(attribute_value="test_value", attribute_type=attr_type)
        product = product_factory()
        productline = productline_factory(product=product, attribute_value=(attr_value,))

        # Create instances of ProductlineAttributeValue
        productline_attribute_value_factory(
            attribute_value=attr_value,
            productline=productline
        )

        # Trying to create another ProductlineAttributeValue instance with the same values should raise IntegrityError
        with pytest.raises(IntegrityError):
            productline_attribute_value_factory(
                attribute_value=attr_value,
                productline=productline
            )
