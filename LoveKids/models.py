from . import db

class Product(db.Model):
    __tablename__='products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    title = db.Column(db.String(128), unique=True)
    sizerange = db.Column(db.String(64))
    size = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    category = db.Column(db.String(64))
    color = db.Column(db.String(64))
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False, default='defaultproduct.jpg')
    cost = db.Column(db.Float, nullable=False)
           
    def __repr__(self):
        str = "Id: {}, Name: {}, Title: {}, Sizerange: {}, Size: {}, Gender: {}, Category: {}, "
        "Color: {}, Description: {}, Image: {}, Cost: {}\n" 
        str =str.format( self.id, self.name, self.title, self.sizerange, self.size, self.gender, 
                        self.category, self.color, self.description, self.image, self.cost)
        return str
  
cartdetails = db.Table('cartdetails',
    db.Column('cart_id', db.Integer, db.ForeignKey('carts.id'), nullable=False),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), nullable=False),
    db.PrimaryKeyConstraint('cart_id', 'product_id'))

class Cart(db.Model):
    __tablename__='carts'
    id = db.Column(db.Integer, primary_key=True)
    products = db.relationship("Product", secondary=cartdetails, backref="carts")
    
    def get_order_details(self):
        return str(self)

    def __repr__(self):
        str = "Id: {}, Products: {}\n" 
        str =str.format( self.id, self.products)
        return str
    
orderdetails = db.Table('orderdetails',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), nullable=False),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), nullable=False),
    db.PrimaryKeyConstraint('order_id', 'product_id'))

class Order(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime)
    total_cost = db.Column(db.Float)
    products = db.relationship("Product", secondary=orderdetails, backref="orders")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  
         
    def __repr__(self):
        str = "Id: {}, Status: {}, Date: {}, Products: {}, Total Cost: {}, User: {}\n" 
        str =str.format( self.id, self.status, self.date, self.products, self.total_cost, self.user_id)
        return str

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    isGuest = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    address = db.Column(db.String(256), nullable=False)
    orders = db.relationship('Order', backref="User", cascade="all, delete-orphan")

    def _repr_(self):
        str = "Id: {}, Username: {}, Password: {}, IsGuest: {},  Firsname: {}, Surname: {}, Email: {}, Phone: {}, Address: {}\n"
        str = str.format(self.id, self.username, self.password, self.isGuest, self.firstname, self.surname, self.email, self.phone, self.address)

class InquiryForm(db.Model):
    __tablename__ ='inquiryforms'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    message = db.Column(db.String(1000))
    
    def _repr_(self):
        str = "Id: {}, Firstname: {}, Surname: {}, Email: {}, Phone: {}, message: {}\n"
        str = str.format( self.id, self.firstname, self.surname, self.email, self.phone, self.message)