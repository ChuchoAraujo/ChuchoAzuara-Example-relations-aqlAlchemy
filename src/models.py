from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    favorites = db.relationship('Favorite', backref='user')

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": [fav.serialize() for fav in self.favorites]
        }


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    climate = db.Column(db.String(80))
    terrain = db.Column(db.String(80))

    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'climate': self.climate,
            'terrain': self.terrain
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(280))
    titulo = db.Column(db.String(280))

    def __repr__(self):
        return f'<People {self.name}>'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)

    
    planet = db.relationship('Planet')
    people = db.relationship('People')

    def __repr__(self):
        return f'<Favorite {self.id}>'

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'planet': self.planet.serialize() if self.planet else None,
            'people': self.people.serialize() if self.people else None
        }


# Relación de 1 a 1
# Relación entre un usuario y su perfil de usuario. 
# Cada usuario solo tiene un perfil de usuario y cada perfil de usuario pertenece a un solo usuario.

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

   
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'profile': self.profile.serialize() if self.profile else None # se accede al objeto profile para confirmar si existe o se devuelve none
        }

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120))
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)

    member = db.relationship('Member', uselist=False) #useList se usa para establecer una relacion uno a uno


    def serialize(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'member_id': self.member_id,
        }


##---------------------------------------------------------------------------------------------------------

# Relación de 1 a muchos // Modelo de tablas // Logica aplicacion
# Relación entre una tienda y sus productos. 
# Una tienda tiene muchos productos, que estan relacionados a una tienda

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    store = db.relationship('Store')


    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'store_id': self.store_id,
            'store_name': self.store.name
        }



##---------------------------------------------------------------------------------------------------------

# Relación de muchos a 1
# Relación entre un pedido y un cliente. 
# Muchos pedidos pueden pertenecer a un solo cliente.

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    orders = db.relationship('Order', backref='customer')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'orders': [o.serialize() for o in self.orders]
        }


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'product': self.product,
            'quantity': self.quantity,
            'customer_id': self.customer_id
        }


##---------------------------------------------------------------------------------------------------------

# Relación de muchos a muchos
# Relación entre los estudiantes y los cursos. 
# Muchos estudiantes pueden estar inscritos en muchos cursos.


# Tabla intermedia
inscription = db.Table('inscription',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

# Clases de modelo
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    courses = db.relationship('Course', secondary=inscription, backref='students')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'courses': [c.name for c in self.courses]
        }

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'students': [s.name for s in self.students]
        }