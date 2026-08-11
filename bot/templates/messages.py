"""errors"""
def temp_error_data(e):
    return f"❌ Ошибка при формировании данных: {str(e)}"

def temp_error_find(cardname):
    return f"❌ Товар '{cardname}' не найден"

def temp_view_error(cardname):
    return f"⚠️ Ошибка отображения товара '{cardname}'"

def temp_take_data_error():
    return "❌ Ошибка при получении данных о товарах"

def temp_data_format_error():
    return "⚠️ Неверный формат данных в кнопке"

def temp_request_processing_error():
    return "⚠️ Произошла ошибка при обработке запроса"


"""info"""
def goods_doesnt_exists():
    return "⚠️ У Вас нет добавленных товаров"


"""hello"""
def welcome_message():
    return f"Привет. Мы PROSklad.\n\n  Это ИИ-помощник для продавцов на маркетплейсах, который автоматически повышает продажи за счет использования нейронных сетей, которые позволяют:\n◦  ⭐ Оптимизировать рейтинг товаров.\n◦  📦 Прогнозировать остатки товаров.\nПример:\nБот предупредил, что кроссовки закончатся через неделю, и посоветовал улучшить фото. После заказа новой партии и правок рейтинг вырос с 4.3 → 4.7, продажи +35%» 📈\nСуть: AI-аналитика, которая раньше была доступна только крупным компаниям, теперь для малого бизнеса. 🏦"

reg_url = ""
def hello_create(username):
    return f"Привет, {username}! Вам надо пройти регистрацию: {reg_url}."

def create_user_error():
    return "❌ Ошибка при создании пользователя"