from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Item, CartItem

def home(request):
    # Display all the categories and items on the home page
    categories = Category.objects.all()
    items = Item.objects.all()
    context = {
        'categories': categories,
        'items': items,
    }
    return render(request, 'Home.html', context)

def category(request, category_id):
    # Display the items belonging to a specific category
    category = get_object_or_404(Category, id=category_id)
    items = Item.objects.filter(category=category)
    context = {
        'category': category,
        'items': items,
    }
    return render(request, 'Category.html', context)

def single_item(request, item_id):
    # Display the details of a single item
    item = get_object_or_404(Item, id=item_id)
    context = {
        'item': item,
    }
    return render(request, 'Single item.html', context)

@login_required
def add_item_for_sale(request):
    # Allow a logged in user to add an item for sale
    if request.method == 'POST':
        # Process the form data and save the item
        name = request.POST.get('name')
        price = request.POST.get('price')
        category = request.POST.get('category')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        item = Item(name=name, price=price, category=category, description=description, image=image)
        item.save()
        messages.success(request, 'Your item has been added successfully.')
        return redirect('home')
    else:
        # Display the form to add an item
        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'Add item for sale.html', context)

@login_required
def add_to_cart(request, item_id):
    # Allow a logged in user to add an item to their shopping cart
    item = get_object_or_404(Item, id=item_id)
    user = request.user
    # Check if the user already has the item in their cart
    cart_item = CartItem.objects.filter(user=user, item=item).first()
    if cart_item:
        # Increase the quantity of the existing cart item
        cart_item.quantity += 1
        cart_item.save()
    else:
        # Create a new cart item with quantity 1
        cart_item = CartItem(user=user, item=item, quantity=1)
        cart_item.save()
    messages.success(request, f'You have added {item.name} to your cart.')
    return redirect('home')

@login_required
def remove_from_cart(request, cart_item_id):
    # Allow a logged in user to remove an item from their shopping cart
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    user = request.user
    # Check if the user owns the cart item
    if cart_item.user == user:
        # Delete the cart item from the database
        cart_item.delete()
        messages.success(request, f'You have removed {cart_item.item.name} from your cart.')
    else:
        # Display an error message
        messages.error(request, 'You cannot remove this item from your cart.')
    return redirect('shopping_cart')

@login_required
def shopping_cart(request):
    # Display the items in the user's shopping cart and the total price
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    total_price = 0
    for cart_item in cart_items:
        total_price += cart_item.item.price * cart_item.quantity
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'Shopping cart.html', context)

@login_required
def checkout(request):
    # Allow a logged in user to proceed to payment for their shopping cart items
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    total_price = 0
    for cart_item in cart_items:
        total_price += cart_item.item.price * cart_item.quantity
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
