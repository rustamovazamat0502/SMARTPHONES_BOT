from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery, LabeledPrice

from configs import TOKEN
from keyboards import *

bot = Bot(TOKEN, parse_mode="HTML")

dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Thi is a test bot for delivery !")
    await register_user(message)
    await show_direction(message)


async def register_user(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name

    database = sqlite3.connect("smartphones.db")
    cursor = database.cursor()

    try:
        cursor.execute("""
        INSERT INTO users(full_name, telegram_id) VALUES(?, ?);
        """, (full_name, chat_id))
        database.commit()
        await bot.send_message(chat_id, "Registration is successful !")
    except:
        await bot.send_message(chat_id, f"Authorization is successful !")

    database.close()

    await create_cart(message)


async def show_direction(message: Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Choose what you want: ", reply_markup=generate_direction())


async def create_cart(message: Message):
    chat_id = message.chat.id

    database = sqlite3.connect("smartphones.db")
    cursor = database.cursor()

    try:
        cursor.execute("""
            INSERT INTO carts(user_id) VALUES
            (
            (SELECT user_id FROM users WHERE telegram_id = ?)
            )
        """, (chat_id,))
        database.commit()
    except:
        pass
    database.close()


@dp.callback_query_handler(lambda call: "category" in call.data)
async def show_products(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    _, category_id = call.data.split("_")

    category_id = int(category_id)

    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Please choose from the products: ",
                                reply_markup=generate_products_menu(category_id))


@dp.callback_query_handler(lambda call: "product" in call.data)
async def show_detail_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    _, product_id = call.data.split("_")
    database = sqlite3.connect("smartphones.db")
    cursor = database.cursor()

    cursor.execute("""
    SELECT product_id, product_name, price, product_characteristics, category_id, image FROM products
    WHERE product_id = ?;
    """, (product_id,))

    product = cursor.fetchone()
    print(product)
    database.close()

    await bot.delete_message(chat_id, message_id)

    with open(product[5], mode="rb") as img:
        await bot.send_photo(chat_id,
                             photo=img,
                             caption=f"""<strong>{product[1]}</strong>
<strong>Characteristics: </strong>{product[3]}
<strong>Price: </strong>{product[2]}""",
                             reply_markup=generate_product_detail_menu(product_id=product_id, category_id=product[4]))


@dp.callback_query_handler(lambda call: call.data.startswith("cart"))
async def add_product_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, product_id, quantity = call.data.split("_")

    product_id, quantity = int(product_id), int(quantity)

    database = sqlite3.connect("smartphones.db")
    cursor = database.cursor()

    cursor.execute("""
    SELECT cart_id FROM carts WHERE user_id =
    (SELECT user_id FROM users WHERE telegram_id = ?)
    """, (chat_id,))

    cart_id = cursor.fetchone()[0]

    cursor.execute("""
    SELECT product_name, price FROM products
    WHERE product_id = ?;
    """, (product_id,))

    product_name, price = cursor.fetchone()
    final_price = quantity * price

    try:
        cursor.execute("""
        INSERT INTO cart_products(cart_id, product_name, quantity, final_price)
        VALUES (?, ?, ?, ?)
        """, (cart_id, product_name, quantity, final_price))
        database.commit()
        await bot.answer_callback_query(call.id, text="Product Added Successfully !")
    except:
        cursor.execute("""
        UPDATE cart_products SET quantity = ?,final_price = ? WHERE product_name = ? AND cart_id = ?
        """, (quantity, final_price, product_name, cart_id))
        database.commit()
        await bot.answer_callback_query(call.id, text="Quantity updated successfully !")
    finally:
        database.close()


@dp.callback_query_handler(lambda call: "back" in call.data)
async def return_to_category(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _, category_id = call.data.split("_")
    await bot.delete_message(chat_id, message_id=message_id)
    await bot.send_message(chat_id=chat_id, text="Choose from the products: ",
                           reply_markup=generate_products_menu(category_id))


@dp.callback_query_handler(lambda call: "main_menu" in call.data)
async def back_to_categories(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Choose from the categories: ",
                                reply_markup=generate_category_menu())


@dp.message_handler(lambda message: "Cart 🛒" in message.text)
async def show_cart(message: Message, edit_message: bool = False):
    chat_id = message.chat.id

    database = sqlite3.connect("smartphones.db")
    cursor = database.cursor()

    cursor.execute("""
    SELECT cart_id FROM carts WHERE user_id =
    (
    SELECT user_id FROM users WHERE telegram_id = ?
    )
    """, (chat_id,))
    cart_id = cursor.fetchone()[0]

    try:
        cursor.execute("""
        UPDATE carts SET total_products = (
            SELECT SUM(quantity) FROM cart_products
            WHERE cart_id = :cart_id
        ),
        total_price = (
        SELECT SUM(final_price) FROM cart_products

        WHERE cart_id = :cart_id
        )
        WHERE cart_id = :cart_id
        """, {"cart_id": cart_id})
        database.commit()
    except:
        await bot.send_message(chat_id, "Cart is Unavailable !")
        database.close()
        return

    cursor.execute("""
    SELECT total_products, total_price FROM carts
    WHERE user_id = (
    SELECT user_id FROM users WHERE telegram_id = ?
    )
    """, (chat_id,))
    total_products, total_price = cursor.fetchone()

    cursor.execute("""
    SELECT product_name, quantity, final_price FROM cart_products
    WHERE cart_id = ?
    """, (cart_id,))

    text = "Your Cart: \n\n"
    i = 0
    cart_products = cursor.fetchall()

    for product_name, quantity, final_price in cart_products:
        i += 1
        text += f"""{i}. {product_name}
Quantity: {quantity}
Final Price: {final_price} \n\n"""

    text += f"""Total Products: {0 if total_products is None else total_products}
Total Price of cart: {0 if total_price is None else total_price}"""
    if edit_message:
        await bot.edit_message_text(text, chat_id, message.message_id,
                                    reply_markup=generate_cart_menu(cart_id))
    else:
        await bot.send_message(chat_id, text, reply_markup=generate_cart_menu(cart_id))


@dp.callback_query_handler(lambda call: "delete" in call.data)
async def delete_product_cart(call: CallbackQuery):
    message = call.message
    chat_id = call.message.chat.id
    _, cart_product_id = call.data.split("_")
    cart_product_id = int(cart_product_id)

    database = sqlite3.connect("smartphones.db")
    cursor = database.cursor()

    cursor.execute("""
DELETE FROM cart_products WHERE cart_product_id = ?
""", (cart_product_id,))
    database.commit()
    database.close()
    await bot.answer_callback_query(call.id, "Product deleted successfully !")
    await show_cart(message, edit_message=True)


@dp.callback_query_handler(lambda call: 'click' in call.data)
async def create_order(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, cart_id = call.data.split('_')
    cart_id = int(cart_id)

    database = sqlite3.connect('smartphones.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_name, quantity, final_price
    FROM cart_products
    WHERE cart_id = ?
    ''', (cart_id,))
    cart_products = cursor.fetchall()
    cursor.execute('''
        SELECT total_products, total_price FROM carts
        WHERE user_id = (
            SELECT user_id FROM users
            WHERE telegram_id = ?    
        )
    ''', (chat_id,))
    total_products, total_price = cursor.fetchone()

    text = 'Your check: \n\n'
    i = 0

    for product_name, quantity, final_price in cart_products:
        i += 1
        text += f'''{i}. {product_name}
    Quantity: {quantity},
    Total price: {final_price}\n\n'''
    text += f'''Total phones: {0 if total_products is None else total_products}
    Total price of the check: {0 if total_price is None else total_price}'''

    await bot.send_invoice(
        chat_id=chat_id,
        title=f'Check №{cart_id}',
        description=text,
        payload='bot-defined invoice payload',
        provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
        currency='UZS',
        prices=[
            LabeledPrice(label='Total price', amount=int(str(total_price) + '00')),
            LabeledPrice(label='Delivery', amount=900000)
        ]
    )

    await bot.send_message(chat_id, 'Order has been paid !')


@dp.callback_query_handler(lambda call: 'payme' in call.data)
async def create_order(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, cart_id = call.data.split('_')
    cart_id = int(cart_id)

    database = sqlite3.connect('smartphones.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_name, quantity, final_price
    FROM cart_products
    WHERE cart_id = ?
    ''', (cart_id,))
    cart_products = cursor.fetchall()
    cursor.execute('''
        SELECT total_products, total_price FROM carts
        WHERE user_id = (
            SELECT user_id FROM users
            WHERE telegram_id = ?    
        )
    ''', (chat_id,))
    total_products, total_price = cursor.fetchone()

    text = 'Your check: \n\n'
    i = 0

    for product_name, quantity, final_price in cart_products:
        i += 1
        text += f'''{i}. {product_name}
    Quantity: {quantity},
    Total price: {final_price}\n\n'''
    text += f'''Total phones: {0 if total_products is None else total_products}
    Total price of the check: {0 if total_price is None else total_price}'''

    await bot.send_invoice(
        chat_id=chat_id,
        title=f'Check №{cart_id}',
        description=text,
        payload='bot-defined invoice payload',
        provider_token='371317599:TEST:1654789179633',
        currency='UZS',
        prices=[
            LabeledPrice(label='Total price', amount=int(str(total_price) + '00')),
            LabeledPrice(label='Delivery', amount=700000)
        ]
    )

    await bot.send_message(chat_id, 'Order has been paid !')


@dp.callback_query_handler(lambda call: 'master' in call.data)
async def create_order(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, cart_id = call.data.split('_')
    cart_id = int(cart_id)

    database = sqlite3.connect('smartphones.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_name, quantity, final_price
    FROM cart_products
    WHERE cart_id = ?
    ''', (cart_id,))
    cart_products = cursor.fetchall()
    cursor.execute('''
        SELECT total_products, total_price FROM carts
        WHERE user_id = (
            SELECT user_id FROM users
            WHERE telegram_id = ?    
        )
    ''', (chat_id,))
    total_products, total_price = cursor.fetchone()

    text = 'Your check: \n\n'
    i = 0

    for product_name, quantity, final_price in cart_products:
        i += 1
        text += f'''{i}. {product_name}
    Quantity: {quantity},
    Total price: {final_price}\n\n'''
    text += f'''Total products: {0 if total_products is None else total_products}
    Total price of the check: {0 if total_price is None else total_price}'''

    await bot.send_invoice(
        chat_id=chat_id,
        title=f'Check №{cart_id}',
        description=text,
        payload='bot-defined invoice payload',
        provider_token='1650291590:TEST:1654789205268_DoCg56hSs2Dp296Z',
        currency='UZS',
        prices=[
            LabeledPrice(label='Total price', amount=int(str(total_price) + '00')),
            LabeledPrice(label='Delivery', amount=500000)
        ]
    )

    await bot.send_message(chat_id, 'Order has been paid !')


# MAKE ORDER
@dp.message_handler(lambda message: "SmartPhones 📱" in message.text)
async def make_order(message: Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Please choose from the categories: ", reply_markup=generate_category_menu())


executor.start_polling(dp, skip_updates=True)
