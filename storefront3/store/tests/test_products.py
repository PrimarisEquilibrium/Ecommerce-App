from rest_framework import status
from model_bakery import baker
import pytest

from store.models import Collection, Product


@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post("/store/products/", product)
    return do_create_product


@pytest.fixture
def create_valid_product(api_client):
    def do_create_valid_product():
        collection = baker.make(Collection)
        return api_client.post("/store/products/", {
            "title": "a",
            "description": "a",
            "slug": "a",
            "inventory": 1,
            "unit_price": 1,
            "collection": collection.id
        })
    return do_create_valid_product


@pytest.mark.django_db
class TestCreateProduct:

    def test_if_user_is_anonymous_return_401(self, create_valid_product):
        response = create_valid_product()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_valid_return_201(self, authenticate, create_valid_product):
        authenticate(is_staff=True)

        response = create_valid_product()

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0

    def test_if_data_is_invalid_return_400(self, authenticate, create_product):
        authenticate(is_staff=True)

        response = create_product({"title": ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["title"] is not None

    def test_if_user_is_not_admin_return_403(self, authenticate, create_valid_product):
        authenticate()

        response = create_valid_product()

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestRetrieveProduct:

    def test_if_product_exists_return_200(self, api_client):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)

        print(product.__dict__)

        response = api_client.get(f"/store/products/{product.id}/")
        response.data.pop("price_with_tax") # Value is dynamically created when retrieved

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "slug": product.slug,
            "inventory": product.inventory,
            "unit_price": product.unit_price,
            "collection": collection.id,
            "images": []
        }

    def test_if_product_does_not_exist_return_404(self, api_client):
        response = api_client.get("/store/collections/a/")

        assert response.status_code == status.HTTP_404_NOT_FOUND
