from datetime import datetime
from . import db

class Category(db.Model):
    __tablename__ = 'categories'

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    products    = db.relationship(
        'Product',
        back_populates='category',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Category {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'product_count': len(self.products)
        }


class Product(db.Model):
    __tablename__ = 'products'

    id          = db.Column(db.Integer, primary_key=True)
    sku         = db.Column(db.String(20), nullable=False, unique=True)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    price       = db.Column(db.Numeric(10,2), nullable=False)
    stock       = db.Column(db.Integer, default=0, nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # FK a categoría
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id'),
        nullable=False
    )
    category = db.relationship(
        'Category',
        back_populates='products'
    )

    def __repr__(self):
        return f'<Product {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'sku': self.sku,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'stock': self.stock,
            'category': {
                'id': self.category.id,
                'name': self.category.name
            },
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
