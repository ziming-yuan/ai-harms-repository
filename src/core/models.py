from src import db

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    url = db.Column(db.String(300), unique=True, nullable=False)
    publisher = db.Column(db.String(100), nullable=False, default='Unknown')
    publisher_url =  db.Column(db.String(300))
    created_utc = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    other = db.Column(db.String(100))
    status = db.Column(db.Enum('Unread', 'Filtered', 'Not relevant', 'Relevant'), default='Unread')
    notes = db.Column(db.String(1000))

    def __init__(self, title, url, publisher, created_utc, category, other=None, publisher_url=None, notes=None, status='Unread'):
        self.title = title
        self.url = url
        self.publisher = publisher
        self.publisher_url = publisher_url
        self.created_utc = created_utc
        self.category = category
        self.other = other
        self.status = status
        self.notes = notes
