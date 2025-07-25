import uuid

from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .models import Product, Cart, CartItem, Transaction
from .serializers import ProductSerializer, DetailedProductSerializer, CartItemSerializer, SimpleCartSerializer, \
    CartSerializer, UserSerializer, UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
from django.conf import settings
import requests
import paypalrestsdk



BASE_URL = settings.REACT_BASE_URL

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

@api_view(["POST"])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    serializer = DetailedProductSerializer(product)
    return Response(serializer.data)

@api_view(["POST"])
def add_item(request):
    try:
        cart_code = request.data.get("cart_code")
        product_id = request.data.get("product_id")
        cart, created = Cart.objects.get_or_create(cart_code=cart_code)
        product = Product.objects.get(id=product_id)
        cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cartitem.quantity += 1
        else:
            cartitem.quantity = 1
        cartitem.save()
        serializer = CartItemSerializer(cartitem)
        return Response({"data": serializer.data, "message": "CartItem created/updated successfully"}, status=201)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(["GET"])
def product_in_cart(request):
    cart_code = request.query_params.get("cart_code")
    product_id = request.query_params.get("product_id")

    cart = Cart.objects.get(cart_code=cart_code)
    product = Product.objects.get(id=product_id)

    product_exists_in_cart = CartItem.objects.filter(cart=cart, product=product).exists()

    return Response({"product_in_cart" : product_exists_in_cart})

@api_view(["GET"])
def get_cart_stat(request):
    cart_code = request.query_params.get("cart_code")
    cart = Cart.objects.get(cart_code=cart_code, paid=False)
    serializer = SimpleCartSerializer(cart)
    return Response(serializer.data)

@api_view(["GET"])
def get_cart(request):
    cart_code = request.query_params.get("cart_code")
    cart = Cart.objects.get(cart_code=cart_code, paid=False)
    serializer = CartSerializer(cart)
    return Response(serializer.data)

@api_view(["PATCH"])
def update_quantity(request):
    try:
        cartitem_id = request.data.get("item_id")
        quantity = request.data.get("quantity")
        quantity = int(quantity)
        cartitem = CartItem.objects.get(id=cartitem_id)
        cartitem.quantity = quantity
        cartitem.save()
        serializer = CartItemSerializer(cartitem)
        return Response({ "data":serializer.data, "message": "CartItem updated successfully!" })

    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(["POST"])
def delete_cartitem(request):
    cartitem_id = request.data.get("item_id")
    cartitem = CartItem.objects.get(id=cartitem_id)
    cartitem.delete()
    return Response({"message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_username(request):
    user = request.user
    return Response({"username": user.username})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    carts = Cart.objects.filter(user=user, paid=True)
    items = CartItem.objects.filter(cart__in=carts).select_related('product')
    serializer = CartItemSerializer(items, many=True, context={'request': request})
    return Response({
        'username': user.username,
        'email': user.email,
        'items': serializer.data
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        cart_code = request.data.get("cart_code")
        if not cart_code:
            return Response({"error": "cart_code is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(cart_code=cart_code)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        tx_ref = str(uuid.uuid4())

        amount = sum(item.quantity * item.product.price for item in cart.items.all())
        if amount <= 0:
            return Response({"error": "Cart total is invalid"}, status=status.HTTP_400_BAD_REQUEST)

        tax = Decimal("4.00")
        total_amount = amount + tax
        currency = "USD"
        redirect_url = f"{settings.BASE_URL}/payment-status/"

        transaction = Transaction.objects.create(
            ref=tx_ref,
            cart=cart,
            amount=total_amount,
            currency=currency,
            user=user,
            status="pending",
        )

        flutterwave_payload = {
            "tx_ref": tx_ref,
            "amount": str(total_amount),
            "currency": currency,
            "redirect_url": redirect_url,
            "customer": {
                "email": user.email or 'default@example.com',
                "name": user.username,
                "phonenumber": getattr(user, 'phone', '')  # Handle missing phone
            },
            "customizations": {
                "title": "Shoppit Payment"
            }
        }

        headers = {
            "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            'https://api.flutterwave.com/v3/payments',
            json=flutterwave_payload,
            headers=headers
        )

        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response({"error": response.json()}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({"error": f"Server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def payment_callback(request):
    status = request.GET.get('status')
    tx_ref = request.GET.get('tx_ref')
    transaction_id = request.GET.get('transaction_id')

    user = request.user

    if status == 'successful':
        # Verify the transaction using Flutterwave's API
        headers = {
            "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}"
        }

        response = requests.get(f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify", headers=headers)
        response_data = response.json()

        if response_data['status'] == 'success':
            transaction = Transaction.objects.get(ref=tx_ref)

            # Confirm the transaction details
            if (response_data['data']['status'] == "successful"
                    and float(response_data['data']['amount']) == float(transaction.amount)
                    and response_data['data']['currency'] == transaction.currency):
                # Update transaction and cart status to paid
                transaction.status = 'completed'
                transaction.save()

                cart = transaction.cart
                cart.paid = True
                cart.user = user
                cart.save()

                return Response({'message': 'Payment successful!',
                                 'subMessage': 'You have successfully made payment for the items you purchased 😍'})
            else:
                # Payment verification failed
                return Response({'message': 'Payment verification failed.',
                                 "subMessage": "Your payment verification failed, kindly try again. ✌️"}, status=400)
        else:
            return Response({'message': 'Failed to verify transaction with Flutterwave.',
                             "subMessgae": "We couldn't verify your payment, use a different payment method 👍"},
                            status=400)
    else:
        # Payment was not successful
        return Response({'message': 'Payment was not successful.'}, status=400)


@api_view(['POST'])
def initiate_paypal_payment(request):
    if request.method == 'POST' and request.user.is_authenticated:
        # Fetch the cart and calculate total amount
        tx_ref = str(uuid.uuid4())
        user = request.user
        cart_code = request.data.get("cart_code")
        cart = Cart.objects.get(cart_code=cart_code)
        amount = sum(item.product.price * item.quantity for item in cart.items.all())
        tax = Decimal("4.00")
        total_amount = amount + tax

        # Create a PayPal payment object
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                # Use a single redirect URL for both success and cancel
                "return_url": f"{BASE_URL}/payment-status?paymentStatus=success&ref={tx_ref}",
                "cancel_url": f"{BASE_URL}/payment-status?paymentStatus=cancel"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Cart Items",
                        "sku": "cart",
                        "price": str(total_amount),
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": str(total_amount),
                    "currency": "USD"
                },
                "description": "Payment for cart items."
            }]
        })

        transaction, created = Transaction.objects.get_or_create(
            ref=tx_ref,
            cart=cart,
            amount=total_amount,
            user=user,
            status='pending'
        )

        if payment.create():
            # Extract PayPal approval URL to redirect the user
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return Response({"approval_url": approval_url})
        else:
            return Response({"error": payment.error}, status=400)

    return Response({"error": "Invalid request"}, status=400)


@api_view(['POST'])
def paypal_payment_callback(request):
    payment_id = request.query_params.get('paymentId')
    payer_id = request.query_params.get('PayerID')
    ref = request.query_params.get('ref')

    user = request.user

    try:
        transaction = Transaction.objects.get(ref=ref)

        if payment_id and payer_id:
            # Fetch payment object using PayPal SDK
            payment = paypalrestsdk.Payment.find(payment_id)
            
            # Execute the payment
            if payment.execute({"payer_id": payer_id}):
                # Payment executed successfully
                transaction.status = 'completed'
                transaction.save()
                cart = transaction.cart
                cart.paid = True
                cart.user = user
                cart.save()

                return Response({
                    'message': 'Payment successful!',
                    'subMessage': 'You have successfully made payment for the items you purchased 😍'
                })
            else:
                # Payment execution failed
                return Response({
                    "error": "Payment execution failed: " + payment.error,
                    "details": payment.error
                }, status=400)
        else:
            return Response({"error": "Invalid payment details."}, status=400)
    
    except Transaction.DoesNotExist:
        return Response({"error": "Transaction not found."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)