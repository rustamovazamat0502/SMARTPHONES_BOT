import sqlite3

database = sqlite3.connect('smartphones.db')
cursor = database.cursor()


def create_users_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name VARCHAR(50) NOT NULL,
        telegram_id INTEGER NOT NULL,
        phone_number VARCHAR(20),
        
        UNIQUE(telegram_id, phone_number)
    )
    ''')


def create_categories_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories(
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name VARCHAR(20) NOT NULL UNIQUE
    )
    ''')


def create_products_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products(
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        product_name VARCHAR(20) NOT NULL UNIQUE,
        price DECIMAL(12, 2) NOT NULL,
        product_characteristics VARCHAR(150),
        image TEXT,

        FOREIGN KEY(category_id) REFERENCES categories(category_id) 
    )
    ''')


def create_cart_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carts(
        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(user_id) UNIQUE,
        total_products INTEGER DEFAULT 0,
        total_price DECIMAL(12, 2) DEFAULT 0
    )
    ''')


def create_cart_products_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart_products(
        cart_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id INTEGER REFERENCES carts(cart_id),
        user_id INTEGER REFERENCES users(user_id),
        product_name VARCHAR(20) NOT NULL,
        quantity INTEGER NOT NULL,
        final_price DECIMAL(12, 2) NOT NULL,

        UNIQUE(cart_id, product_name)
    )
    ''')


def create_orders_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders(
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(user_id) UNIQUE,
        time_create DATETIME,
        total_products INTEGER DEFAULT 0,
        total_price DECIMAL(12, 2) DEFAULT 0
    )
    ''')


def create_order_products_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_products(
        order_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER REFERENCES orders(order_id),
        product_name VARCHAR(20) NOT NULL,
        final_price DECIMAL(12, 2) NOT NULL,

        UNIQUE(order_id, product_name)
    )
    ''')


# create_users_table()
# create_cart_table()
# create_cart_products_table()
# create_categories_table()
# create_products_table()
# create_orders_table()
# create_order_products_table()


def insert_categories():
    cursor.execute("""
    INSERT INTO categories(category_name) VALUES
    ('Smartphones'), ('Vivo'), ('OPPO'), ('Apple smartphones'), ('Samsung smartphones'), ('Honor'), ('Xiaomi'),
     ('Huawei'), ('TECNO'), ('Realme'), ('Gaming'), ('Flagships'), ('Optimal'), ('Radiotelephones'), ('push-button')
    """)


# insert_categories()


def insert_products():
    cursor.execute("""
    INSERT INTO products(category_id, product_name, price, product_characteristics, image) VALUES
    (1, 'Galaxy A52 4/128Gb Black',
    3252000, 
    'Brand:  Samsung,
    OS Version:  Android 11,
    Screen type:  Color Super AMOLED,touch,
    Diagonal:  6.5",
    Camera:  64 MP, 12 MP, 5 MP, 5 MP,
    Front-camera:  32 MP,
    Built-in memory (ROM):  128 GB,
    Random Access Memory (RAM):  4 GB,
    Battery capacity:  4500 mAh',
    'media/smartphone.png'),


    (2, 'Smartphone Vivo x60 Pro 12/256Gb Blue',
    8245000,
    'Brand:  Vivo,
    OS Version:  Android 11,
    Screen type:  AMOLED,
    Diagonal:  6.56",
    Camera:  MP 48,13 MP, 13 MP,
    Front-camera:  32 MP,
    video processor:  Adreno 650, 
    Random Access Memory (RAM):  12 GB,
    Built-in memory (ROM):  256 GB,
    Battery capacity:  4200 mAh',
    'media/vivo.jpg'),
    
    (3, 'Smartphone OPPO A74 4/128GB KORA',
    3000000, 
    'Brand: OPPO,
    OS Tour: Android 11,
    Tour screen: AMOLED COLOR, SENSORLY,
    Diagonal: 6,43",
    Camera: 48 MP, 2 MP, 2 MP,
    Old camera: 16 MP,
    CPU: Qualcomm Snapdragon 662,
    video processor: Adreno 610,
    Ichki Hotira (ROM): 128 GB,
    Random access memory (RAM): 4GB,
    Battery Click: 5000 mA / h',
    'media/oppo.jpg'),
    
    (4, 'Apple iPhone 12 Pro 128GB Pacific Blue',
    12826000,
    'Brand: Apple,
    OS Tour: iOS 14,
    Tour screen: Rangley OLED, sensorli,
    Diagonal: 6,1",
    Camera: 12 MP, 12 MP, 12 MP,
    Old camera: 12 MP,
    CPU: Apple A14 Bionic,
    Ichki Hotira (ROM): 128 GB,
    Random access memory (RAM): 6 GB',
    'media/apple.jpg'),
    
    (5, 'Samsung Galaxy A32 4 / 64Gb Black smartphone',
    2884000,
    'Brand: Samsung,
    OS Tour: Android 11,
    Tour screen: Super AMOLED ranges, sensors,
    Diagonal: 6.4",
    Camera: 64 MP, 8 MP, 5 MP, 5 MP,
    Old camera: 20 MP,
    CPU: MediaTek Helio G80,
    video processor: Mali-G52 MC2,
    Ichki Hotira (ROM): 64 GB,
    Random access memory (RAM): 4GB,
    Battery Click: 5000 mA / h',
    'media/samsung.jpg'),
    
    (6, 'Honor 8S Prime 3/64 black',
    1280000,
    'Brand: Honor,
    Camera: 13 MP,
    Old camera: 5 MP,
    OS Tour: Android 10,
    Battery Click: 3020 mA / h,
    Diagonal: 5.7",
    Tour screen: Rangley IPS, 16.78 million ranglar, sensorli,
    CPU: MediaTek Helio A22 (MT6761),
    Random access memory (RAM): 3 GB,
    Ichki Hotira (ROM): 64 GB,
    video processor: PowerVR',
    'media/honor.jpg'),
    
    (7, 'Xiaomi Mi 11 Lite 5G 8/128 Gb Blue',
    4235000,
    'Brand: Xiaomi,
    OS Tour: Android 11,
    Tour screen: AMOLED ranks, sensors,
    Diagonal: 6,55",
    Camera: 64 MP, 8 MP, 5 MP,
    Old camera: 16 MP,
    CPU: Qualcomm Snapdragon 732G,
    video processor: Adreno 618,
    Ichki Hotira (ROM): 128 GB,
    Random access memory (RAM): 8 GB,
    Battery Click: 4250 mA / h',
    'media/mi.jpg'),
    
    (8, 'Huawei P Smart 3/32GB 2019 Blue',
    2063000,
    'Brand: Huawei,
    Camera: 13 MP, 2 MP,
    Old camera: 16 MP,
    OS Tour: Android 9',
    'media/huawei.jpg'),
    
    (9, 'Smartphone TECNO Spark 5 Air 2/32GB Misty Gray KD6',
    319000,
    'Brand: TECNO,
    OS Tour: Android 10,
    Tour screen: ranges, sensors,
    Diagonal: 7",
    Camera: 13 MP, 2 MP,
    Old camera: 8 MP,
    CPU: MediaTek Helio A22 (MT6761),
    video processor: PowerVR,
    Ichki Hotira (ROM): 32 GB,
    Random access memory (RAM): 2 GB,
    Battery Click: 5000 mA / h',
    'media/tecno.jpg'),
    
    (10, 'Galaxy S21 Ultra 12/256Gb Black',
    13673000,
    'Brand: Samsung,
    OS Tour: Android 11,
    Tour screen: Rangley Dynamic AMOLED 2X, sensors,
    Diagonal: 6,8",
    Camera: 108 MP, 12 MP, 10 MP, 10 MP,
    Old camera: 40 MP,
    CPU: Exynos 2100,
    video processor: Mali-G78,
    Random access memory (RAM): 12 GB,
    Ichki Hotira (ROM): 256 GB,
    Battery Click: 5000 mA / h',
    'media/game_smartphones.jpg'),

    (11, 'Samsung Galaxy S21 Ultra 8 / 256Gb silver',
    13673000,
    'Brand: Samsung,
    OS Tour: Android 11,
    Tour screen: Rangli Speaker AMOLED 2X, sensory,
    Diagonal: 6,8"M,
    Camera: 108 MP, 12 MP, 10 MP, 10 MPM,
    Old camera: 40 MP,
    CPU: Exynos 2100,
    video processor: Mali-G78,
    Random access memory (RAM): 12 GB,
    Ichki Hotira (ROM): 256 GB,
    Battery Click: 5000 mA / h',
    'media/flag.jpg'),
    
    (12, 'Samsung Galaxy A02s 3 / 32GB Black',
    1788000,
    'Brand: Samsung,
    OS Tour: Android 10,
    Tour screen: Rangli, iltimos, sensorli,
    Diagonal: 6,5",
    Camera: 13 MP, 2 MP, 2 MP,
    Old camera: 5 MP,
    CPU: Qualcomm Snapdragon 450,
    video processor: Adreno 506,
    Ichki Hotira (ROM): 32 GB,
    Random access memory (RAM): 3 GB,
    Battery Click: 5000 mA / h',
    'media/optimal.jpg'),
    
    (13, 'Panasonic KX-TG2511UAN cordless telephone',
    367000,
    'Brand: Available,
    Collection: Base, handset phone,
    Operating speed: 1880-1900 MHz,
    Indoor / outdoor activity: 50 / 300 m,
    Integrated telephone book: 50 numbers,
    Save dialed numbers: 5,
    Active working time: 18 hours,
    Waiting time: 170 hours,
    sony battery: 2 ,
    Format: AAA,
    Turi accumulator: Ni-MH,
    Battery Click: 550 mA / h,
    Display: Monochrome, 2 rows,
    Number privacy: Available,
    Caller ID: Available,
    Call list: 50 numbers,
    Bell music: ten,
    Respond when you pick up the phone: Available',
    'media/radio.jpg'),
    
    (14, 'Tugmali phone Nokia 230 Dual Sim black',
    879000,
    'Brand: Nokia,
    Camera: 2 Mpix,
    Old camera: 2 Mpix,
    Ichki Hotira (ROM): 32 MB',
    'media/buttons.jpg')
    """)


# insert_products()

database.commit()
database.close()
