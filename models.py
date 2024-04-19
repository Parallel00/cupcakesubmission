from flask_sqlalchemy import SQLAlchemy

databs = SQLAlchemy()

DEFAULT_IMG = "https://tinyurl.com/demo-cupcake"

class Cupcake(databs.Model):
	__tablename__ = "cupcake"
	
	id = databs.Column(databs.Integer, primary_key=True, autoincrement=True)
	flavor = databs.Column(db.Text, nullable=False)
	size = databs.Column(db.Float, nullable=False)
	rating = db.Column(db.Float, nullable=False)
	image = db.Column(db.Text, nullable=False, default=DEFAULT_IMG)
	
	def ser_to_dict(slf):
	
		return{
			"id": slf.id,
			"flavor": slf.flavor,
			"size": slf.size,
			"rating": slf.rating,
			"image": slf.image,
		}
	def connect_to_databs(app):
		databs.app = app
		databs.init_app(app_