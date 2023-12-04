from itertools import product
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sdek.sdek import SdekService
from repository.order import OrderRepo

from auth.manager import get_user_manager
from auth.auth import auth_backend
from model.data.model import User
from fastapi_users import FastAPIUsers

from db_config.session import get_async_session
from service.address import AddressService
from service.cart import ShoppingCartService
from repository.order_request import OrderRequestRepo
from repository.product_for_order import ProductForOrderRepo
from fastapi import HTTPException
from repository.product import ProductRepo

from model.request.order_request import OrderRequestCreate

from sdek.schema import Phone

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

router = APIRouter()

@router.get("/callback")
async def callback(cdek_number):
    sdek_service = SdekService()
    result = await sdek_service.get_status_about_order(cdek_number)
    if result is not None:
        return JSONResponse({"message": "order info received successfully", "data": result})
    return JSONResponse({"message": "order info receiving failed"})


@router.post("/order")
async def create_order_request(order_req: OrderRequestCreate, user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    address_service = AddressService(db)
    cart_service = ShoppingCartService(db)

    order_request_repo = OrderRequestRepo(db)
    product_for_order_repo = ProductForOrderRepo(db)

    cart_info = await cart_service.get_cart_info_by_user_id(user.id)
    address_of_user = await address_service.get_address_by_user_id(user.id)

    product_repo = ProductRepo(db)

    if cart_info is not None:
        cart_info = cart_info['items']
        weight = 0
        for item in cart_info:
            weight += item['product_weight'] * item['quantity']

    order_request_id = await order_request_repo.insert_order_request({'user_email': user.email, 'name_of_recipient': order_req.name, 'phone_of_recipient': order_req.phone, 'additional_num': order_req.additional_num, 'address_id': address_of_user.id, 'order_weigth': weight, 'passport_series': order_req.passport_series, 'passport_number': order_req.passport_number, 'passport_date_of_issue': order_req.passport_date_of_issue, 'passport_organization': order_req.passport_organization, 'tin': order_req.tin})
    if order_request_id is not None:
        for item in cart_info:
            await product_for_order_repo.insert_product_for_order({'order_request_id': order_request_id, 'product_id': item['product_id'], 'quantity': item['quantity']})
            product = await product_repo.get_product_by_id(item['product_id'])
            if product is not None:
                await product_repo.update_product(item['product_id'], {'quantity': product.quantity - item['quantity']})
            else:
                return JSONResponse({"message": "order request creation failed"})
        return JSONResponse({"message": "order request created successfully"})
    return JSONResponse({"message": "order request creation failed"})

@router.get("/admin/orders", dependencies=[Depends(current_superuser)])
async def get_order_requests(db: AsyncSession = Depends(get_async_session)):
    order_request_repo = OrderRequestRepo(db)
    product_for_order_repo = ProductForOrderRepo(db)

    def to_dict(obj):
        if obj is None:
            return None
        # If the object has a method to return a dict, use it
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        # Otherwise, manually construct a dictionary
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


    try:
        order_requests = await order_request_repo.get_all_order_requests()
        if not order_requests:
            return JSONResponse({"message": "No order requests found"}, status_code=404)

        orders_with_products = []
        for order_request in order_requests:
            # Fetch products for each order
            products = await product_for_order_repo.get_product_for_order_by_order_id(order_request.id)
            
            # Construct the order information with nested products
            order_data = {
                'order_request': to_dict(order_request),  # Assuming this is a serializable dict or ORM model instance
                'products': [to_dict(product) for product in products]  # Assuming this is a list of product data
            }
            orders_with_products.append(order_data)

        return JSONResponse({"message": "Order requests received successfully", "data": orders_with_products})

    except Exception as e:
        print(f"Error retrieving order requests: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving order requests")

@router.put("/admin/orders/{order_request_id}/approve", dependencies=[Depends(current_superuser)])
async def approve_order_request(order_request_id: int, length: int, heigth: int, width: int,db: AsyncSession = Depends(get_async_session)):
    order_request_repo = OrderRequestRepo(db)
    sdek_service = SdekService()
    address_service = AddressService(db)

    order_request = await order_request_repo.get_order_request_by_id(order_request_id)
    if order_request is not None:
        address = await address_service.get_address_by_id(order_request.address_id)
        if address is not None:
            result = await sdek_service.create_order(name_of_recepient=order_request.name_of_recipient, user_email=order_request.user_email, phone_of_recepient=order_request.phone_of_recipient, additional_num=order_request.additional_num, address_of_recepient=address, length=length, heigth=heigth, width=width, weigth=order_request.order_weigth, passport_series=order_request.passport_series, passport_number=order_request.passport_number, passport_date_of_issue=order_request.passport_date_of_issue, passport_organization=order_request.passport_organization, tin=order_request.tin)
            if result is not None:

                await order_request_repo.update_order_request(order_request_id, {'order_status': 'approved'})
                return JSONResponse({"message": "order approved successfully", "data": result})

            return JSONResponse({"message": "order approving failed"})

    return JSONResponse({"message": "order approving failed"})


@router.post("/order/refusal")
async def create_order_refusal(user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    sdek_service = SdekService()
    order_repo = OrderRepo(db)
    order_of_user = await order_repo.get_order_by_user_id(user.id)
    if order_of_user is not None:
        result = await sdek_service.refuse_order(order_of_user.sdek_order_uuid)
        if result is not None:
            return JSONResponse({"message": "order refused successfully", "data": result})
        return JSONResponse({"message": "order refusing failed"})
    return JSONResponse({"message": "order refusing failed"})
    