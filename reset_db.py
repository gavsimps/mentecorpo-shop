from datetime import datetime, date
from models import db, Merchandise
# import random

def reset_database():
    db.drop_all()

    db.create_all()

    shop_info = [
        {'name':'Mario skin suit', 'image':'images/newUS.png', 'product_tb':'m', 'product_type':'skin', 'size':'large', 'color':'italian', 'price': 4.99, 'in_stock': 1, 'amount_sold': 0, 'featured': 1}
    ]

    for i, data in enumerate(shop_info):
        merch = Merchandise(
            name = data['name'],
            image = data['image'],
            product_tb = data['product_tb'],
            product_type = data['product_type'],
            size = data['size'],
            color = data['color'],
            price = data['price'],
            in_stock = data['in_stock'],
            amount_sold = data['amount_sold'],
            featured = data['featured'],
            date_created = date.today()
        )
        db.session.add(merch)

    db.session.commit()
