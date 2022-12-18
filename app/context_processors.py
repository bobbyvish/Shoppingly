from app.views import cart
from .models import Category, Cart


def category(request):
    cat_list = Category.objects.all()
    context = {'categorys': cat_list}
    return context


def CartTotal(request):
    if request.user.is_authenticated:
        cart_total = Cart.objects.filter(user=request.user).count()
    else:
        cart_total = 0
    context = {'cart_total': cart_total}
    return context
