import sqlite3

from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from utils import build_inline_menu


def generate_direction():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text="SmartPhones 📱"), KeyboardButton(text="🚀 Checkout")],
        [KeyboardButton(text="History of orders🗒️"), KeyboardButton(text="Cart 🛒")],
        [KeyboardButton(text="Help 🆘"), KeyboardButton(text="About Us 🧑🏿‍💻")]
    ], resize_keyboard=True, one_time_keyboard=True)


def generate_category_menu():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text="All Menu 📜", url='https://telegra.ph/All-menu-of-our-Fast-Food-05-22'))
    database = sqlite3.connect("smartphones.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT category_id, category_name FROM categories;
    """)
    categories = cursor.fetchall()
    database.close()
    build_inline_menu(markup, categories, "category")
    return markup


def generate_products_menu(category_id: int):
    markup = InlineKeyboardMarkup()
    database = sqlite3.connect("smartphones.db")
    cursor = database.cursor()
    cursor.execute("""
    SELECT product_id, product_name FROM products WHERE category_id = ?
    """, (category_id,))
    products = cursor.fetchall()
    database.close()
    build_inline_menu(markup, products, "product")
    return markup


def generate_product_detail_menu(product_id: int, category_id: int):
    markup = InlineKeyboardMarkup()
    numbers_list = [i for i in range(1, 9 + 1)]

    in_row = 3
    rows = len(numbers_list) // in_row
    if len(numbers_list) % in_row != 0:
        rows += 1

    start = 0
    end = in_row
    for i in range(rows):
        new_lst = []
        for number in numbers_list[start:end]:
            new_lst.append(
                InlineKeyboardButton(text=str(number), callback_data=f"cart_{product_id}_{number}")
            )

        markup.row(*new_lst)
        start = end
        end += in_row
    markup.row(
        InlineKeyboardButton(text="Back", callback_data=f"back_{category_id}")
    )
    return markup


def generate_cart_menu(cart_id: int):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Click ✅", callback_data=f"click_{cart_id}")],
            [InlineKeyboardButton(text="Payme 🪙", callback_data=f"payme_{cart_id}")],
            [InlineKeyboardButton(text="Master/Visa Card 💳", callback_data=f"master_{cart_id}")]
        ]
    )
    database = sqlite3.connect("smartphones.db")
    cursor = database.cursor()

    cursor.execute("""
    SELECT cart_product_id, product_name FROM cart_products
    WHERE cart_id = ? 
    """, (cart_id,))

    cart_products = cursor.fetchall()

    database.close()

    for product_id, product_name in cart_products:
        markup.row(
            InlineKeyboardButton(text=f"❌ {product_name}", callback_data=f"delete_{product_id}")
        )

    return markup
