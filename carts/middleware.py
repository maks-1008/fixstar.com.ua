from django.core.exceptions import ImproperlyConfigured

class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Инициализация корзины в сессии, если ее нет
        if not request.session.get('cart'):
            request.session['cart'] = {}
        
        response = self.get_response(request)
        return response