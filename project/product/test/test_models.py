import pytest
import uuid
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError, DataError
from decimal import Decimal
from product.models import Category, Product, ProductLine

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_output(self, category_factory):
        category = category_factory(name='test_category')

        assert category.__str__() == 'test_category'

    def test_category_max_length_name(self, category_factory):
        name = "x" * 236
        with pytest.raises(DataError):
            category_factory(name=name)

    def test_category_name_unique_field(self, category_factory):
        category_factory(name="name_unique")
        with pytest.raises(IntegrityError):
            category_factory(name="name_unique")

    def test_category_slug_max_length(self, category_factory):
        slug = "x" * 256
        with pytest.raises(DataError):
            category_factory(slug=slug)

    def test_category_slug_unique_field(self, category_factory):
        category_factory(slug="slug_unique")
        with pytest.raises(IntegrityError):
            category_factory(slug="slug_unique")

    def test_category_is_active_true_default(self, category_factory):
        category = category_factory()
        assert category.is_active is True

    def test_parent_category_on_delete_protect(self, category_factory):
        category1 = category_factory()
        category_factory(parent=category1)
        with pytest.raises(IntegrityError):
            category1.delete()

    def test_category_parent_field_null(self, category_factory):
        category1 = category_factory()
        assert category1.parent is None

    def test_category_return_category_active_only_true(self, category_factory):
        category_factory(is_active=True)
        category_factory(is_active=False)
        qs = Category.objects.active().count()
        assert qs == 1

    def test_category_return_category_active_only_false(self, category_factory):
        category_factory(is_active=True)
        category_factory(is_active=False)
        qs = Category.objects.count()
        assert qs == 2


class TestProductModel:
    def test_product_str_name_product(self, product_factory):
        product = product_factory(name='product1')
        assert product.__str__() == 'product1'

    def test_product_max_length_name(self, product_factory):
        name = "x" * 101
        with pytest.raises(DataError):
            product_factory(name=name)

    def test_product_slug_max_length(self, product_factory):
        slug = "x" * 256
        with pytest.raises(DataError):
            product_factory(slug=slug)

    def test_product_slug_unique_field(self, product_factory):
        product_factory(slug="slug_unique")
        with pytest.raises(IntegrityError):
            product_factory(slug="slug_unique")

    def test_product_pid_unique_field(self, product_factory):
        product_factory(pid="u4s5d6f")
        with pytest.raises(IntegrityError):
            product_factory(pid="u4s5d6f")

    def test_product_is_digital_false_default(self, product_factory):
        obj = product_factory(is_digital=False)
        assert obj.is_digital is False

    def test_product_is_active_default_true(self, product_factory):
        obj = product_factory(is_digital=True)
        assert obj.is_active is True

    def test_product_fk_category_on_delete_protect(self, category_factory, product_factory):
        obj1 = category_factory()
        product_factory(category=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    def test_product_return_product_active_only_true(self, product_factory):
        product_factory(is_active=True)
        product_factory(is_active=False)
        qs = Product.objects.active().count()
        assert qs == 1

    def test_product_return_active_only_false(self, product_factory):
        product_factory(is_active=True)
        product_factory(is_active=False)
        qs = Product.objects.count()
        assert qs == 2


class TestProductlineModel:
    def test_str_sku_output_(self, productline_factory):
        productline = productline_factory(sku='test_SKU_0')

        assert productline.__str__() == 'test_SKU_0'

    def test_productline_max_5_digits_price(self, productline_factory):
        price = 123456
        with pytest.raises(DataError):
            productline_factory(price=price)

    def test_productline_price_decimal(self, productline_factory):
        price = Decimal("1.010")
        productline = productline_factory(price=price)

        with pytest.raises(ValidationError):
            productline.full_clean()

    def test_productline_str_sku_max_length(self, productline_factory):
        sku = 'x' * 11

        with pytest.raises(DataError):
            productline_factory(sku=sku)

    def test_unique_order_productline_per_product(
            self,
            product_factory,
            productline_factory,
    ):
        product = product_factory()
        productline_factory(product=product, order=1)

        with pytest.raises(IntegrityError):
            productline_factory(product=product, order=1)

    def test_productline_fk_product_on_delete_protect(self, product_factory, productline_factory):
        product1 = product_factory()
        productline_factory(product=product1)
        with pytest.raises(IntegrityError):
            product1.delete()

    def test_productline_return_active_only_true(self, productline_factory):
        productline_factory(is_active=True)
        productline_factory(is_active=False)
        qs = ProductLine.objects.active().count()
        assert qs == 1

    def test_productline_return_active_only_false(self, productline_factory):
        productline_factory(is_active=True)
        productline_factory(is_active=False)
        qs = ProductLine.objects.count()
        assert qs == 2


class TestProductImageModel:
    def test_str_image_productline(
        self,
        product_image_factory,
        productline_factory,
    ):

        productline = productline_factory()
        image = product_image_factory(
            product_line=productline,
            alt_text="alt_img_test"
        )

        assert image.__str__() == 'alt_img_test'

    def test_uuid_url_image_productline(
        self,
        product_image_factory,
        productline_factory,
    ):

        productline = productline_factory()
        ext = '.png'
        uuidtest = f'{uuid.uuid4()}{ext}'
        image = product_image_factory.create(
            product_line=productline,
            url=uuidtest
        )
        image.save()
        filename = image.url

        assert filename == uuidtest

    def test_productimage_delete_cascade_productline(
        self,
        product_image_factory,
        productline_factory
    ):
        productline = productline_factory()
        product_image_factory(
            product_line=productline)
        productline.delete()
        qs = ProductImage.objects.count()
        assert qs == 0

    def test_unique_order_productline_per_order(
            self,
            product_image_factory,
            productline_factory
    ):

        productline = productline_factory()

        product_image_factory(product_line=productline, order=1)

        with pytest.raises(IntegrityError):
            product_image_factory(product_line=productline, order=1)

    def test_alt_text_max_length(self, product_image_factory):
        alt_text = "x" * 111
        with pytest.raises(DataError):
            product_image_factory(alt_text=alt_text)

    def test_alt_text_cannot_be_null_if_image_exist(
        self,
        product_image_factory,
    ):
        with pytest.raises(IntegrityError):
            product_image_factory(alt_text=False)

    def test_order_cannot_be_null_if_image_exist(self, product_image_factory):

        with pytest.raises(IntegrityError):
            product_image_factory(order=False)


class TestProductTypeModel:
    def test_str_method_producttype(self, product_type_factory):
        obj = product_type_factory.create(name="test_type_product")

        assert obj.__str__() == "test_type_product"

    def test_producttype_name_max_length(self, product_type_factory):
        name = "x" * 101
        with pytest.raises(DataError):
            product_type_factory(name=name)

    def test_producttype_name_unique_field(self, product_type_factory):
        product_type_factory(name="name_unique")
        with pytest.raises(IntegrityError):
            product_type_factory(name="name_unique")


class TestAttributeModel:
    def test_str_method_attr_type(self, attribute_factory):
        obj = attribute_factory(attribute_name="TestAttributeName")
        assert obj.__str__() == "TestAttributeName"

    def test_attribute_name_max_length(self, attribute_factory):
        name = "x" * 101
        with pytest.raises(DataError):
            attribute_factory(attribute_name=name)

    def test_attribute_on_delete_cascade_producttype(
        self,
        attribute_factory,
        product_type_factory
    ):
        producttype = product_type_factory()
        attribute_factory(
            product_type=producttype)
        producttype.delete()
        qs = Attribute.objects.count()
        assert qs == 0


class TestProductlineAttributeValueModel:
    def test_productline_attributes_unique_together(
            self,
            product_type_factory,
            product_factory,
            attribute_factory,
            productline_factory,
            productline_attribute_value_factory,
    ):

        # Create instances of ProductType, Attribute, Product and ProductLine
        product_type = product_type_factory()
        attr_type = attribute_factory(attribute_name="test_attribute", product_type=product_type)
        product = product_factory()
        productline = productline_factory(product=product, sku="123")

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
