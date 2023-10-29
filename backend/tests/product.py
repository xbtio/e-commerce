import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from repository.product import ProductRepo
from model.data.product import Product


class TestProductRepo(unittest.IsolatedAsyncioTestCase):
    async def test_insert_product(self):
        mock_db = MagicMock(spec=AsyncSession)
        product_repo = ProductRepo(mock_db)
        product = Product(name="Test Product", price=10.99)
        mock_db.execute.return_value = None
        mock_db.commit.return_value = None

        result = await product_repo.insert_product(product)

        self.assertTrue(result)
        mock_db.execute.assert_called_once()
        mock_db.commit.assert_called_once()

    async def test_update_product(self):
        mock_db = MagicMock(spec=AsyncSession)
        product_repo = ProductRepo(mock_db)
        product_id = 1
        details = {"name": "Updated Product", "price": 20.99}
        mock_db.execute.return_value = None
        mock_db.commit.return_value = None

        result = await product_repo.update_product(product_id, details)

        self.assertTrue(result)
        mock_db.execute.assert_called_once()
        mock_db.commit.assert_called_once()

    async def test_delete_product(self):
        mock_db = MagicMock(spec=AsyncSession)
        product_repo = ProductRepo(mock_db)
        product_id = 1
        mock_db.execute.return_value = None
        mock_db.commit.return_value = None

        result = await product_repo.delete_product(product_id)

        self.assertTrue(result)
        mock_db.execute.assert_called_once()
        mock_db.commit.assert_called_once()

    async def test_get_all_products(self):
        mock_db = MagicMock(spec=AsyncSession)
        product_repo = ProductRepo(mock_db)
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [
            Product(id=1, name="Product 1", price=10.99),
            Product(id=2, name="Product 2", price=20.99),
        ]
        mock_db.execute.return_value = mock_result

        result = await product_repo.get_all_products()

        self.assertEqual(len(result), 2)
        mock_db.execute.assert_called_once()
        mock_result.scalars.assert_called_once()
        mock_result.scalars.return_value.all.assert_called_once()

    async def test_get_product_by_id(self):
        mock_db = MagicMock(spec=AsyncSession)
        product_repo = ProductRepo(mock_db)
        product_id = 1
        mock_result = MagicMock()
        mock_result.scalars.return_value.one_or_none.return_value = Product(
            id=1, name="Product 1", price=10.99
        )
        mock_db.execute.return_value = mock_result

        result = await product_repo.get_product_by_id(product_id)

        self.assertIsNotNone(result)
        mock_db.execute.assert_called_once()
        mock_result.scalars.assert_called_once()
        mock_result.scalars.return_value.one_or_none.assert_called_once()