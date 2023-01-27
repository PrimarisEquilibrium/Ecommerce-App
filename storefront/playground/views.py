from django.shortcuts import render
from django.db import connection
from django.db.models import Sum, Avg, Max, Min

from store.models import Product, Order, OrderItem, Collection

def say_hello(request):
    context = {"name": "Mosh"}
    return render(request, 'hello.html', context)


def test_area(request):
    queryset = Order.objects.select_related("customer"
    ).prefetch_related("orderitem_set__product"
    ).annotate(total_spent=Sum("orderitem__product__unit_price")
    ).order_by("-placed_at")

    product_price = "orderitem__product__unit_price"
    statistics = Order.objects.prefetch_related(product_price
    ).order_by("-placed_at").aggregate(
        total_sales=Sum(product_price), 
        avg_sales=Avg(product_price),
        max_sales=Max(product_price),
        min_sales=Min(product_price),
    )

    context = {'orders': list(queryset), 'statistics': statistics}
    return render(request, 'hello.html', context)