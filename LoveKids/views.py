from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Product, Cart, Order, User, InquiryForm
from datetime import datetime
from .forms import GuestCheckoutForm, UserInquiryForm, LoginForm, SignupForm
from . import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/productlist/')
def productlist():
    products = Product.query.order_by(Product.name).all()
    return render_template('productlist.html', productlist=products)

@bp.route('/product-list-by-gender/<string:gender>')
def productlistbygender(gender):
    # creating list of products when user selects product by gender
    products = Product.query.filter(Product.gender == gender)
    return render_template('productlist.html', productlist = products, 
                           isBoy = gender == 'boy', isGirl = gender == 'girl')

@bp.route('/product-list-by-sizerange/<string:sizerange>')
def productlistbysizerange(sizerange):
    # creating list of products when user selects product by size ranges
    products = Product.query.filter(Product.sizerange == sizerange)
    return render_template('productlist.html', productlist = products, 
                           isUnder1 = sizerange == 'under1', is1To5 = sizerange == '1-5', is6To12 = sizerange == '6-12') 

@bp.route('/product-list-by-category/<string:category>')
def productlistbycategory(category):
    # creating list of products when user selects product by product categories
    products = Product.query.filter(Product.category == category)
    return render_template('productlist.html', productlist = products, 
                           isTop = category == 'top', isBottom = category == 'bottom', isJacket = category == 'jacket',
                           isSwimwear = category == 'swimwear', isDress = category == 'dress', isOnesie = category == 'onesie') 

@bp.route('/productdetails/<int:productid>')       
def getproduct(productid):
    product = Product.query.get(productid)
    return render_template('productdetails.html', product = product)

@bp.route('/shoppingcart/', methods=['POST', 'GET'])
def cart():
    # retrieving cart obejct if there is one
    if 'cart_id' in session.keys():
        cart = Cart.query.get(session['cart_id'])
    else:
        #when there is no cart object found
        cart = None
    
    #Only creating a cart if there is any product added to the cart
    product_id = request.args.get('product_id')
    if product_id is not None:
        if cart is None:
            cart = Cart()
            db.session.add(cart)
        product = Product.query.get(product_id)
        if product not in cart.products:
            try:
                cart.products.append(product)
                db.session.commit()
                session['cart_id'] = cart.id
            except:
                print('There was an issue adding the item to your cart')
            return redirect(url_for('main.cart'))
        else:
            flash('Item already in cart.')
            return redirect(url_for('main.cart'))
    
    #calculating the total price for products in the cart object
    totalprice = 0
    if cart is not None:
        for product in cart.products:
            totalprice = totalprice + product.cost 
    else:
        flash('There is no product in cart!')
 
    #checking if cart object is created by a member user or guest user and 
    # displaying membercheckout or guestcheckout page accordingly using a boolean called isGuest
    if 'user_id' in session.keys():
        isGuest = User.query.get(session['user_id']).isGuest
    else:
        isGuest = True
        
    return render_template('shoppingcart.html', cart = cart, totalprice = totalprice, isGuest = isGuest)

@bp.route('/deletecart/')
def deletecart():
    if 'cart_id' not in session:
        return redirect(url_for('main.cart'))
    else:
        cart = Cart.query.get(session['cart_id'])
        #deleting cart from both session on server side and in database    
        del session['cart_id']
        db.session.delete(cart)
        db.session.commit()
        flash('All items deleted.')
    return redirect(url_for('main.cart'))


@bp.route('/deletecartitem/', methods=['POST'])
def deletecartitem():
    id = request.form['id']
    cart = Cart.query.get_or_404(session['cart_id'])
    product_to_delete = Product.query.get(id)
    try:
        cart.products.remove(product_to_delete)
        db.session.commit()
        #deleting cart if the item being deleted is the last in cart
        if len(cart.products) == 0:
            db.session.delete(cart)
            del session['cart_id']
            db.session.commit()
        return redirect(url_for('main.cart'))
    except:
        print('There was an issue deleting the item from your cart')
    return redirect(url_for('main.cart'))

@bp.route('/guestcheckout/', methods=['POST','GET'])
def guestcheckout():
    #checking if cart is empty when user hits check out
    if 'cart_id' not in session:
        return redirect(url_for('main.cart'))
    
    cart = Cart.query.get(session['cart_id'])
    guestcheckoutform = GuestCheckoutForm()
    if guestcheckoutform.validate_on_submit():
        #creating a new user and order instance on validation
        user = User(username = None, password = None, isGuest = True, firstname='', surname='', email='', phone='', address='')
        order = Order(date=datetime.now(), total_cost=0, user_id='')
        user.firstname = guestcheckoutform.firstname.data
        user.surname = guestcheckoutform.surname.data
        user.email = guestcheckoutform.email.data
        user.phone = guestcheckoutform.phone.data
        user.address = guestcheckoutform.address.data
        order.products = cart.products

        order.total_cost = 0
        for product in order.products:
            order.total_cost = order.total_cost + product.cost 
        
        #adding both the new user and order to the database session and server session
        try:
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            order.user_id = user.id
            db.session.add(order)
            #cart will be deleted once order is created
            db.session.delete(cart)
            db.session.commit()
            del session['cart_id']
            session['order_id'] = order.id
        except:
            print('there was an issue checking out')
        return redirect('/orderconfirmation')
      
    return render_template('guestcheckout.html', form = guestcheckoutform)

@bp.route('/membercheckout/', methods=['POST','GET'])
def membercheckout():
    #checking if cart is empty when user hits check out
    if 'cart_id' not in session:
        return redirect(url_for('main.cart'))
    
    cart = Cart.query.get(session['cart_id'])
    #creating order for user
    order = Order(date=datetime.now(), total_cost=0, user_id='')
    order.products = cart.products
    order.total_cost = 0
    for product in order.products:
        order.total_cost = order.total_cost + product.cost 
    order.user_id = session['user_id']

    #adding order and deleting cart in both server and database session
    try:
        db.session.add(order)
        db.session.delete(cart)
        db.session.commit()
        del session['cart_id']
        session['order_id'] = order.id
    except:
        print('there was an issue checking out')
    return redirect('/orderconfirmation')
              
@bp.route('/orderconfirmation/')
def orderconfirmation():
    flash('Your order is successfully checked out and will be processed soon!')
    return render_template('orderconfirmation.html')
    
@bp.route('/inquiryform/', methods=['POST','GET'])
def inquiryform():
    inquiryform = UserInquiryForm()
    if inquiryform.validate_on_submit():
        inquiry_form = InquiryForm(firstname="", surname="", email="", phone="", message="")
        inquiry_form.firstname = inquiryform.firstname.data
        inquiry_form.surname = inquiryform.surname.data
        inquiry_form.email = inquiryform.email.data
        inquiry_form.phone = inquiryform.phone.data
        inquiry_form.message = inquiryform.message.data
    
        try:
            db.session.add(inquiry_form)
            db.session.commit()
            flash('Thanks for your inquiry. We will get back to you soon...')
            return redirect(url_for('main.index'))
        except:
            return 'There was an issue submitting your inquiry'
    return render_template('inquiryform.html', form = inquiryform)

@bp.route('/login/', methods=['POST','GET'])
def login():
    #checking if member has already logged in
    if 'user_id' in session.keys():
        isGuest = User.query.get(session['user_id']).isGuest
        #redirecting member to account page if he has already logged in
        if isGuest == False:
            return redirect(url_for('main.account'))
    
    loginform = LoginForm()
    if loginform.validate_on_submit():
        #checking if correct username and password are entered
        user = User.query.filter(User.username == loginform.username.data, User.password == loginform.password.data).first()
        if user is not None:
            flash('You have successfully logged in!')
            session['user_id'] = user.id
            return redirect(url_for('main.account'))
        #re-promoting user to re-enter log in details
        else:
            loginform = LoginForm()
            flash ('Invalid username or password. Please retry!')
            return redirect(url_for('main.login'))
    return render_template('login.html', form = loginform)

@bp.route('/signup/', methods=['POST','GET'])
def signup():
    signupform = SignupForm()
    #checking if username is in use
    if signupform.validate_on_submit():
        user = User.query.filter(User.username == signupform.username.data).first()
        if user is not None:
            flash ('Username is already in use. Please retry!')
            signupform = SignupForm()
            return redirect(url_for('main.signup'))
        #creating a new user instance which will be assigned values from the signupform 
        user = User(username = None, password = None, isGuest = False, firstname='', surname='', email='', phone='', address='')
        user.username = signupform.username.data
        user.password = signupform.password.data
        user.firstname = signupform.firstname.data
        user.surname = signupform.surname.data
        user.email = signupform.email.data
        user.phone = signupform.phone.data
        user.address = signupform.address.data
        db.session.add(user)
        db.session.commit()
        flash ('You are now a member with us. Please use your login details to log in!')
        return redirect(url_for('main.login'))
    return render_template('signup.html', form = signupform)

@bp.route('/account/', methods=['POST','GET'])
def account():
    #showing user details and order information
    user = User.query.get(session['user_id'])
    orders = Order.query.filter(Order.user_id == user.id).all()
    #using a boolean variable to conditionally displaying message when there is no order
    hasNoOrder = len(orders) == 0
    return render_template('account.html', user = user, orders = orders, hasNoOrder = hasNoOrder)

@bp.route('/logout/')
def logout():
    flash ('You are successfully logged out')
    del session['user_id']
    return redirect (url_for('main.index'))