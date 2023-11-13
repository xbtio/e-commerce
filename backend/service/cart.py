from httpx import delete
from sqlalchemy.ext.asyncio import AsyncSession
from model.data.blog import Blog, ReviewBlog
from repository.cart import ShoppingCartRepo, ShoppingCartItemRepo
from fastapi import HTTPException, status

class ShoppingCartItemService:
    def __init__(self, db: AsyncSession):
        self.cart_repo = ShoppingCartRepo(db)
        self.cart_item_repo = ShoppingCartItemRepo(db)
    
    async def create_cart_item(self, cart_item, user_id: int):
        try:
            cart = await self.cart_repo.get_or_create_cart(user_id)
            cart_item['shopping_cart_id'] = cart.id
            await self.cart_item_repo.insert_cart_item(cart_item)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return True
    
    async def delete_cart_item(self, id: int):
        try:
            cart_item = await self.cart_item_repo.delete_cart_item(id)
            if cart_item is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return True

class ShoppingCartService:
    def __init__(self, db: AsyncSession):
        self.cart_repo = ShoppingCartRepo(db)
    
    async def get_all_carts(self):
        try:
            result = await self.cart_repo.get_all_carts()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return result
    
    async def get_cart_info_by_user_id(self, user_id):
        try:
            cart = await self.cart_repo.get_cart_info_by_user_id(user_id)
            if cart is None:
                print(cart)
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
            if cart:
                cart_price = 0
                cart_info = {
                    "cart_id": cart.id,
                    "user_id": cart.user_id,
                    "items": []
                }
                for item in cart.items:
                    product = item.product
                    cart_price += product.price * item.quantity
                    # Check if product already exists in the cart
                    existing_item = next((i for i in cart_info["items"] if i["product_id"] == product.id), None)
                    if existing_item:
                        # Update quantity if product exists
                        existing_item["quantity"] += item.quantity
                    else:
                        # Add new item to cart if it doesn't exist
                        cart_info["items"].append({
                            "item_id": item.id,
                            "product_id": product.id,
                            "product_name": product.name,
                            "product_description": product.description,
                            "product_price": product.price,
                            "product_image": product.image,
                            "product_rating": product.rating,
                            "product_number_of_ratings": product.number_of_ratings,
                            "product_weight": product.weigth,
                            "quantity": item.quantity
                        })
                cart_info["total_price"] = cart_price
                return cart_info
            else:
                # If no cart is found, handle accordingly, perhaps by returning an empty cart structure or raising an exception
                return {
                    "cart_id": None,
                    "user_id": user_id,
                    "items": []
                }
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
