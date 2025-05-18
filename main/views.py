from django.http import HttpResponse
from django.shortcuts import render
from django.template import context



def index(request):
    
    context = {
        'title': 'FixStar',
        'content': "063-447-48-46",
        'additional_phone': "099-708-69-84",    
    }
    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'title': 'FixStar',  # Заголовок страницы
        'content': "",  # Контент страницы
         'text_on_page': (
              '<span class="fixstar">'
              '<span class="text-blue">Fix</span>'
              '<span class="text-orange">Star</span>'
              '</span> - інтернет-магазин кріпильних матеріалів, фарби та інструментів. '
              'Наші товари стануть у пригоді всім, хто пов\'язаний з будівництвом, ремонтом, монтажем обладнання та різних конструкцій.'
              ' У нас обслуговуються як фізичні так і юридичні осіби. Підтримується готівкова та безготівкова оплата. На більшість товарів надаються постійні накопичувальні знижки, деякі товари знижки від обсягу купівлі. У разі оптових замовлень можливі спеціальні договірні умови.'
        ),
        'main_values_title': "Головним для нас є:",  # Заголовок для списка ценностей
        'main_values': [
            "якість наших товарів",
            "високий рівень обслуговування клієнтів",
            "довгострокова співпраця з партнерами",
            "розвиток власного бренду",
        ],
        'cta': 'Якщо вам сподобався наш товар, натискайте на кнопку "Замовити" та оформлюйте заявку!',  # Призыв к действию
    }

    
    return render(request, 'main/about.html', context)

def deliverypayment(request):
    context = {
        'title': 'FixStar',
        'content': "Доставка і оплата",
        'text_on_page': "",
        'delivery_values_title': "Доставка:",  # Унікальний ключ
        'delivery_values': [  # Унікальний ключ
            "по Україні кур'єрами транспортних компаній. Доставку товару оплачує покупець згідно з тарифами перевізника;",
            "в Полтаві та Полтавській області можлива безкоштовна доставка власним транспортом компанії при сумі замовлення від 5000 грн;",
            "самовивіз зі складу в Полтаві, вул. Чумацький Шлях, 72, графік роботи складу 9:00-16:00 щодня.",
        ],
        'payment_values_title': "Способи оплати:",  # Унікальний ключ
        'payment_values': [  # Унікальний ключ
            "накладений платіж;",
            "оплата на сайті платіжною картою;",
            "безготівковий розрахунок;",
            "відстрочка платежу згідно з індивідуальним договором (для постійних клієнтів)."
        ],
        'cta': 'Відвантаження товару замовнику відбувається в день оплати або наступного робочого дня, якщо оплата надійшла після 14:00. Умови оплати та доставки узгоджуються під час остаточного оформлення замовлення.',
    }
    return render(request, 'main/deliverypayment.html', context)


def contacts(request):
    context = {
        'title': 'FixStar',
        'content': "Контактна інформація",
        'text_on_page': "",
        'cont_values_title': "",
        'cont_values': [
            {
                'icon': 'deps/images/location.png',  # Шлях до іконки для адреси
                'text': "Адреса: вул. Чумацький Шлях, 72, Полтава, Україна, 36000",
                "is_address": True,  # Флаг для адреса
                "maps_link":"https://surl.li/dtqmyl"
            },
            {
                'icon': 'deps/images/Lifecell.png',  # Шлях до іконки для телефону
                'text': "063-447-48-46"
            },
            {
                'icon': 'deps/images/Vodafone.png',  # Шлях до іконки для телефону
                'text': "099-708-69-84"
            },
            {
                'icon': 'deps/images/email.png',  # Шлях до іконки для email
                'text': '<a href="mailto:office@fixstar.com.ua">office@fixstar.com.ua</a>',
                "is_email": True  # Флаг для email

            }
        ],
        'cta': 'Зв’яжіться з нами сьогодні!'
    }
    return render(request, 'main/contacts.html', context)

