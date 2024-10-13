from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, OrderItem
from django.contrib.auth.decorators import login_required

def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'product_list.html', {'categories': categories, 'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order, created = Order.objects.get_or_create(customer=request.user.customer, paid=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if not created:
        order_item.quantity += 1
        order_item.save()
    return redirect('cart')

def cart(request):
    order = Order.objects.filter(customer=request.user.customer, paid=False).first()
    return render(request, 'cart.html', {'order': order})

@login_required
def checkout(request):
    order = Order.objects.filter(customer=request.user.customer, paid=False).first()
    if request.method == 'POST':
        # Implement payment processing logic here
        order.paid = True
        order.save()
        return redirect('product_list')
    return render(request, 'checkout.html', {'order': order})
