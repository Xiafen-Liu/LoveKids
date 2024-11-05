from flask import Blueprint
from . import db
from .models import Product, Cart, Order, User, InquiryForm
import datetime

bp = Blueprint('admin', __name__, url_prefix='/admin/')

@bp.route('/dbseed/')
def dbseed():
    product1 = Product (name='baby sleepbag olive spot', title='Baby sleepbag olive spot', sizerange='under1', \
                        size='6 months', gender='boy', category='sleepbag', color='grey', \
                        description='Soft and stratchable sleepbag made of organic cotton and featuring a bell-shaped bottom to promote healthy hip joint development', \
                        image='baby sleepbag olive spot.jpg', cost=50.00)
    product2 = Product (name='blue boys sweatshirt', title='Blue boys sweatshirt', sizerange='6-12', \
                        size='7', gender='boy', category='top', color='blue', \
                        description='Crewneck boys sweatshirt made from cotton for a comfortable feel, perfect either as a single piece or for laying up', \
                        image='blue boys sweatshirt.jpg', cost=35.00)
    product3 = Product (name='floral girls dress', title='Floral girls dress', sizerange='1-5', \
                        size='5', gender='girl', category='dress', color='pearl blue', \
                        description='Long sleeve girls dress made from cotton, with floral print all over it, designed with a wide neckline and a button at the back for easy dressing', \
                        image='floral girls dress.jpg', cost=55.00)
    product4 = Product (name='floral girls swimwear', title='Floral girls swimwear', sizerange='1-5', \
                        size='4', gender='girl', category='swimwear', color='pink', \
                        description='Long sleeve onepiece girls swimwear made from a stretchable and sun protectice material, with a UPF level of 50+, perfect outfit for a day out at the beach', \
                        image='floral girls swimwear.jpg', cost=55.00)
    product5 = Product (name='green kids rainjacket', title='Green kids rainjacket', sizerange='6-12', \
                        size='7', gender='girl', category='jacket', color='green', \
                        description='The perfect addition to your kids wardrobe to accompany them for every one of their water adventures, with a fun pop of colour and stylish design', \
                        image='green kids rainjacket.jpg', cost=100.00)
    product6 = Product (name='green stripe boys polo shirt', title='Green stripe boys polo shirt', sizerange='1-5', \
                        size='3', gender='boy', category='top', color='green', \
                        description='Short sleeve boys polo shirt, designed with white stripes for styling, made with cotton for softness and comfort', \
                        image='green stripe boys polo shirt.jpg', cost=35.00)
    product7 = Product (name='grey baby onesie', title='Grey baby onesie', sizerange='under1', \
                        size='3 months', gender='boy', category='onesie', color='grey', \
                        description='Soft baby onesie made from organic cotton, designed with buttons instead of zip to protect babys delicate skin and for ultimate comfort', \
                        image='grey baby onesie.jpg', cost=45.00)
    product8 = Product (name='jeans girls jacket', title='Jeans girls jacket', sizerange='1-5', \
                        size='3', gender='girl', category='jacket', color='blue', \
                        description='Cotton denim gils jacket with a classic dark wash finish, with dual falp chest pockets and button-up fastening for a stylish look', \
                        image='jeans girls jacket.jpg', cost=55.00)
    product9 = Product (name='polo boys shorts', title='Polo boys shorts', sizerange='6-12', \
                        size='10', gender='boy', category='bottom', color='grey', \
                        description='Boys shorts made from a super soft cotton blend, comes with a matching polo shirt that will keep your boy looking smart, stylish and sporty', \
                        image='polo boys shorts.jpg', cost=55.00)

    try:
        db.session.add(product1)
        db.session.add(product2)
        db.session.add(product3)
        db.session.add(product4)
        db.session.add(product5)
        db.session.add(product6)
        db.session.add(product7)
        db.session.add(product8)
        db.session.add(product9)
        db.session.commit()
    except:
        return 'There was an issue adding the products in dbseed function'
    
    return 'DATA LOADED'