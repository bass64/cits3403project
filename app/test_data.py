from app import db
from app.models import User

def add_test_users_to_db():

    Sibi = User(username="Sibi")
    Sibi.set_password("SafePassword123")
    Sibi.following_articles = []

    Cooper = User(username="Cooper")
    Cooper.set_password("SafePassword123")
    Cooper.following_articles = []

    Alex = User(username="Alex")
    Alex.set_password("SafePassword123")
    Alex.following_articles = []

    Daniel = User(username="Daniel")
    Daniel.set_password("SafePassword123")
    Daniel.following_articles = []

    users = [Sibi, Cooper, Alex, Daniel]

    for user in users:
        db.session.add(user)
        db.session.commit()