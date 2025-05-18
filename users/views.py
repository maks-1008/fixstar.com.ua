from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from .forms import CustomUserCreationForm, ProfileForm
from typing import Any


def login_signup_view(request) -> HttpResponse:
    """Обрабатывает и вход, и регистрацию на одной странице"""
    
    print(f"--- Request START: {request.path}, Method: {request.method} ---")
    print(f"--- Cookies: {request.COOKIES}")
    print(f"--- Session: {request.session.items()}")
    print(f"--- User authenticated: {request.user.is_authenticated}")
    
    if request.user.is_authenticated:
        print(f"--- Авторизован как: {request.user.username}, is_staff={request.user.is_staff}, is_superuser={request.user.is_superuser}")
        return redirect('main:index') 

    force_login_form = request.GET.get('login') == 'true'
    print(f"[GET] force_login_form={force_login_form}")
    
    active_form = 'login'  # По умолчанию
    
    login_form = AuthenticationForm()
    signup_form = CustomUserCreationForm()
    
    if request.method == 'POST':
        action = request.POST.get('action', '[НЕ УКАЗАН]') # Получаем action, отмечаем если его нет
        print(f"[POST] Received action: '{action}'") 
        
        if action == 'login':
            print("[POST] Processing LOGIN action")
            active_form = 'login' # Устанавливаем явно при обработке логина
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                print(f"[DEBUG] Пытаемся авторизовать пользователя с логином: {username}")
                
                user = authenticate(request, username=username, password=password)
                print(f"[DEBUG] Результат аутентификации для '{username}': {'УСПЕШНО' if user else 'ОШИБКА'}")
                
                if user is not None:
                    print(f"[DEBUG] Пользователь найден: {user}, is_active={user.is_active}, is_staff={user.is_staff}, is_superuser={user.is_superuser}")
                    print(f"[DEBUG] Вызываем auth_login с бэкендом 'django.contrib.auth.backends.ModelBackend'")
                    
                    # Очищаем сессию перед входом
                    if '_auth_user_id' in request.session:
                        request.session.flush()
                        print("[DEBUG] Предыдущая сессия очищена")
                    
                    auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    
                    print(f"[DEBUG] Сессия после логина: {request.session.items()}")
                    print(f"[DEBUG] Авторизованный пользователь: {request.user.is_authenticated}")
                    
                    user.last_login = now()
                    user.save(update_fields=['last_login'])
                    messages.success(request, f'Вітаємо, {user.username}!')
                    
                    # Проверка, был ли указан next в запросе
                    redirect_to = request.GET.get('next', 'main:index')
                    print(f"[DEBUG] Перенаправление на: {redirect_to}")
                    
                    return redirect(redirect_to)
                else:
                    messages.error(request, 'Невірний логін або пароль.')
                    active_form = 'login' # Повторно явно устанавливаем активную форму
                    print(f"[LOGIN ERROR] При ошибке входа: active_form = {active_form}")
            else:
                print(f"[POST Login] Login form invalid: {login_form.errors.as_data()}")
                print(f"[POST Login] Login form data: {request.POST}")
                messages.error(request, 'Невірний логін або пароль (форма невалідна).')
                active_form = 'login' # Повторно явно устанавливаем активную форму
                print(f"[LOGIN ERROR] При ошибке валидации: active_form = {active_form}")

        elif action == 'signup':
            print("[POST] Processing SIGNUP action")
            active_form = 'signup' # Устанавливаем явно при обработке регистрации
            # Копируем POST данные для обработки
            post_data = request.POST.copy()
            
            # Автоматически копируем password1 в password2
            if 'password1' in post_data:
                post_data['password2'] = post_data.get('password1')
            
            signup_form = CustomUserCreationForm(post_data)
            
            if signup_form.is_valid():
                try:
                    user = signup_form.save()
                    # Используем конкретный бэкенд аутентификации
                    auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    messages.success(request, f'Вітаємо, {user.username}! Ваш акаунт успішно створено.')
                    return redirect('main:index')
                except Exception as e:
                    messages.error(request, f'Помилка реєстрації: {str(e)}')
                    active_form = 'signup'
            else:
                print(f"[POST Signup] Signup form invalid: {signup_form.errors.as_json()}")
                # active_form уже 'signup'
                # Собираем ошибки для отдельного отображения в шаблоне
                password_errors = []
                has_common_password_error = False
                
                # Проверяем ошибки password2 и связанные с общими паролями
                common_password_errors = ['распространён', 'common password', 'слишком просто', 'too common', 'поширен']
                short_password_errors = ['коротк', 'минимум', 'minimum', 'at least', 'короткий']
                numeric_password_errors = ['числов', 'numeric', 'цифр', 'digit']
                similar_password_errors = ['похож', 'similar']
                
                # Определяем типы ошибок пароля
                password_too_common = False
                password_too_short = False
                password_only_numbers = False
                password_too_similar = False
                
                
        else:
            print(f"[POST] UNKNOWN action: '{action}'. Defaulting to LOGIN form.")
            active_form = 'login' # Если action не login и не signup, показываем вход

    # Принудительно показываем форму входа если нужно (переопределяет ошибки)
    if force_login_form:
        print("[GET] Forcing login form due to ?login=true")
        active_form = 'login'
    
    # ДОПОЛНИТЕЛЬНАЯ ЗАЩИТА: Если действие было login, устанавливаем активную форму 'login'
    if request.method == 'POST' and request.POST.get('action') == 'login':
        print("[ДОПОЛНИТЕЛЬНАЯ ЗАЩИТА] Пост-запрос с action=login, устанавливаем активную форму 'login'")
        active_form = 'login'
    
    print(f"--- Request END: Rendering template with active_form = '{active_form}' ---")
    
    context = {
        'title': 'Вхід / Реєстрація',
        'login_form': login_form,
        'signup_form': signup_form,
        'active_form': active_form,
        'messages': messages.get_messages(request),
        'password_errors': password_errors if 'password_errors' in locals() else [], # Передаем ошибки пароля отдельно
        'has_common_password_error': password_too_common if 'password_too_common' in locals() else False,
        'has_short_password_error': password_too_short if 'password_too_short' in locals() else False,
        'has_numeric_password_error': password_only_numbers if 'password_only_numbers' in locals() else False,
        'has_similar_password_error': password_too_similar if 'password_too_similar' in locals() else False,
        'force_login': force_login_form
    }
    return render(request, 'users/login_signup.html', context)


# --- Старые представления (можно удалить или оставить для других целей) ---

def login(request) -> HttpResponse:
    if request.user.is_authenticated:
        messages.info(request, 'Ви вже авторизовані в системі')
        return redirect('main:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            user.last_login = now()
            user.save(update_fields=['last_login'])
            messages.success(request, f'Вітаємо, {user.get_full_name() or user.username}! Ви успішно увійшли в систему.')
            
            if request.POST.get('next'):
                return HttpResponseRedirect(request.POST.get('next'))
            return redirect('main:index')
        
        messages.error(request, 'Помилка автентифікації. Будь ласка, перевірте правильність введених даних')
    
    context = {
        'title': 'Авторизація',
        'form': AuthenticationForm(),
        'messages': messages.get_messages(request)
    }
    return render(request, 'users/login.html', context)

def registration(request) -> HttpResponse:
    if request.user.is_authenticated:
        messages.info(request, 'Для реєстрації нового акаунту потрібно вийти з поточного')
        return redirect('main:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Вітаємо, {user.get_full_name()}! Ваш акаунт успішно створено та авторизовано.')
            return redirect('main:index')
        
        messages.error(request, 'Помилка реєстрації. Будь ласка, виправте наступні помилки:')
        # Отображение детальных ошибок
        for field, errors in form.errors.items():
            for error in errors:
                field_name = form.fields[field].label if form.fields[field].label else field
                if field == "password1":
                    field_name = "Пароль"
                # Обработка password2 удалена, так как не используется
                elif field == "__all__":
                    field_name = "Форма"
                
                messages.error(request, f'{field_name}: {error}')
    else:
        form = CustomUserCreationForm()

    context = {
        'title': 'Реєстрація',
        'form': form,
        'messages': messages.get_messages(request)
    }
    return render(request, 'users/registration.html', context)

@login_required(login_url='/user/signup/')
def profile(request) -> HttpResponseRedirect | HttpResponse:
    if request.method == 'POST':
        form = ProfileForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user
        )
        if form.is_valid():
            user = form.save(commit=False)
            
            # Проверка, указан ли новый пароль и валиден ли старый
            password1 = form.cleaned_data.get('password1')
            old_password = form.cleaned_data.get('old_password')
            
            if password1 and old_password and request.user.check_password(old_password):
                # Устанавливаем новый пароль через форму, которая обрабатывает это
                form.save()
                # После смены пароля, нужно повторно авторизовать пользователя
                update_session_auth_hash(request, user)
                messages.success(request, '✅ Ваш пароль успішно змінено!')
            else:
                # Если пароль не меняется или проверка старого пароля не прошла, просто сохраняем обычные поля
                user.save()
                
            messages.success(request, '✅ Ваш профіль успішно оновлено!')
            return HttpResponseRedirect(reverse('users:profile'))
        
        messages.error(request, '❌ Помилка оновлення профілю:')
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{form.fields[field].label if field != "__all__" else "Форма"}: {error}')
    else:
        form = ProfileForm(instance=request.user)

    # Получаем заказы пользователя
    from orders.models import Order
    user_orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    
    context: dict[str, Any] = {
        'title': 'Особистий кабінет',
        'form': form,
        'user': request.user,
        'messages': messages.get_messages(request),
        'user_orders': user_orders,
    }
    return render(request, 'users/profile.html', context)

def users_cart(request) -> HttpResponse:
    return render(request, 'users/users_cart.html')

@login_required
def logout(request) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    username = request.user.get_full_name() or request.user.username
    auth_logout(request)
    messages.success(request, f'До побачення, {username}! Ви успішно вийшли з системи. Заходьте знову!')
    return redirect(reverse('main:index'))