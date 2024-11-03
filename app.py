from operator import and_
from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cost_price = db.Column(db.Integer, nullable=False)
    selling_price = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return 'Product ' + str(self.id)

@app.route('/List')
def List():
    all_prod = Product.query.order_by(Product.id).all()
    return render_template("prod_list.html", all_prod=all_prod)

@app.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'POST':
        prod_name = request.form['name']
        prod_category = request.form['category']
        prod_quantity = int(request.form['quantity'])  # Ensure it's an integer
        prod_cost = int(request.form['cost_price'])    # Ensure it's an integer
        prod_sell = int(request.form['selling_price']) # Ensure it's an integer
        
        # Create new Product instance
        add_prod = Product(name=prod_name, category=prod_category, quantity=prod_quantity, 
                           cost_price=prod_cost, selling_price=prod_sell)
        db.session.add(add_prod)
        db.session.commit()
        return redirect('/product')
    else:
        all_prod = Product.query.order_by(Product.id).all()
        return render_template("product.html", all_prod=all_prod)

@app.route('/List/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect('/List')

@app.route('/List/edit/<int:id>', methods=['GET', 'POST'])
def edit(id): 
    prod = Product.query.get_or_404(id)  # Retrieve product outside the if block
    if request.method == 'POST':
        prod.name = request.form['name']
        prod.category = request.form['category']
        prod.quantity = int(request.form['quantity'])  # Ensure it's an integer
        prod.cost_price = int(request.form['cost_price'])   # Corrected attribute name
        prod.selling_price = int(request.form['selling_price'])  # Corrected attribute name
        
        db.session.commit()
        return redirect('/List')
    else:
        return render_template("prod_edit.html", prod=prod)  # Render edit page with product details
    
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    incharge = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.Unicode(255), nullable=False)
    
    def __repr__(self):
        return 'Location ' + str(self.id)

@app.route('/location', methods=['GET', 'POST'])
def location():
    if request.method == 'POST':
        loc_name = request.form['name']
        loc_address = request.form['address']
        loc_incharge = request.form['incharge'] 
        phone = int(request.form['phone'])    
        
        # Create new Product instance
        add_loc = Location(name=loc_name , address=loc_address , incharge=loc_incharge, phone=phone)
        db.session.add(add_loc)
        db.session.commit()
        return redirect('/location')
    else:
        all_loc = Location.query.order_by(Location.id).all()
        return render_template("location.html", all_loc=all_loc)
    

@app.route('/loclist')
def l_List():
    all_loc = Location.query.order_by(Location.id).all()
    return render_template("loc_list.html", all_loc=all_loc)

@app.route('/loclist/delete/<int:id>', methods=['GET', 'POST'])
def l_delete(id):
    location = Location.query.get_or_404(id)
    db.session.delete(location)
    db.session.commit()
    return redirect('/loclist')

@app.route('/loclist/edit/<int:id>', methods=['GET', 'POST'])
def l_edit(id): 
    loc = Location.query.get_or_404(id)  # Retrieve product outside the if block
    if request.method == 'POST':
        loc.name = request.form['name']
        loc.address = request.form['address']
        loc.incharge = request.form['incharge']  # Ensure it's an integer
        loc.phone = int(request.form['phone'])   # Corrected attribute name
        
        db.session.commit()
        return redirect('/loclist')
    else:
        return render_template("loc_edit.html", loc=loc)  # Render edit page with product details
    
class Move(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    quantity = db.Column(db.Integer, nullable=False)
    fromloc = db.Column(db.String, nullable=True)
    toloc = db.Column(db.String, nullable=True)
    
    def __repr__(self):
        return 'Move ' + str(self.id)

@app.route('/move', methods=['GET', 'POST'])
def move():
    if request.method == 'POST':
        pid  = int(request.form['pid'])
        
        # Convert timestamp from form if needed, or use current time
        timestamp_str = request.form.get('timestamp', None)
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else datetime.utcnow()
        
        quantity = int(request.form['quantity'])
        fromloc = request.form['fromloc']
        toloc = request.form['toloc']
        
        # Create new Move instance
        add_move = Move(pid=pid, timestamp=timestamp, quantity=quantity, fromloc=fromloc, toloc=toloc)
        db.session.add(add_move)
        db.session.commit()
        change(pid,fromloc,toloc,quantity)
        return redirect('/move')
    else:
        all_loc = Location.query.order_by(Location.id).all()
        all_prod = Product.query.order_by(Product.id).all()
        all_move = Move.query.order_by(Move.id).all()
        return render_template("move.html", all_move=all_move,all_prod=all_prod,all_loc=all_loc)
    

@app.route('/movelist')
def m_List():
    all_move = Move.query.order_by(Move.id).all()
    return render_template("move_list.html", all_move=all_move)

@app.route('/movelist/delete/<int:id>', methods=['GET', 'POST'])
def m_delete(id):
    move = Move.query.get_or_404(id)
    db.session.delete(move)
    db.session.commit()
    return redirect('/movelist')

class ProductLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    product_id = db.Column(db.Integer,db.ForeignKey('product.id'),  nullable=False)
    available_quantity = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return  str(self.available_quantity)

def change(pid, fromloc, toloc, quantity):
    
    product_locations = ProductLocation.query.filter(and_(ProductLocation.location_id==1,ProductLocation.product_id==1)).all()
 
    
    

@app.route('/quantity')
def quantity():
    product_locations = ProductLocation.query.order_by(ProductLocation.location_id).all()
    return render_template("quantity.html", product_locations=product_locations) 



if __name__ == "__main__":
    app.run(debug=True)