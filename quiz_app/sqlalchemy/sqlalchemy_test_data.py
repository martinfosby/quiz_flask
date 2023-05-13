from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Administrator, User, Quiz, Answer, UserHasQuiz

engine = create_engine('sqlite:///quiz.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Insert administrators
admins = [
    Administrator(username='johndoe', password_hash='abcd', first_name='John', last_name='Doe'),
    Administrator(username='janedoe', password_hash='efgh', first_name='Jane', last_name='Doe'),
    Administrator(username='bobsmith', password_hash='ijkl', first_name='Bob', last_name='Smith'),
    Administrator(username='sarajones', password_hash='mnop', first_name='Sara', last_name='Jones'),
    Administrator(username='davidbrown', password_hash='qrst', first_name='David', last_name='Brown')
]
session.add_all(admins)
session.commit()

# Insert users
users = [
    User(username='amandasmith', password_hash='password678', answer='B'),
    User(username='michaeljones', password_hash='password901', answer='C'),
    User(username='sophiawilliams', password_hash='password234', answer='A'),
    User(username='samuelbrown', password_hash='password567', answer='D'),
    User(username='oliviawilson', password_hash='password890', answer='B')
]
session.add_all(users)
session.commit()

# Insert quizzes
quizzes = [
    Quiz(title='Science Quiz', question='What is the chemical symbol for gold?', active=1, category='Chemistry', administrator_id=1),
    Quiz(title='History Quiz', question='Who was the first president of the United States?', active=1, category='History', administrator_id=1),
    Quiz(title='Geography Quiz', question='What is the capital city of Australia?', active=0, category='Geography', administrator_id=2),
    Quiz(title='Literature Quiz', question='Who wrote the novel "To Kill a Mockingbird"?', active=1, category='Literature', administrator_id=1),
    Quiz(title='Math Quiz', question='What is the value of pi?', active=1, category='Mathematics', administrator_id=3),
    Quiz(title='Music Quiz', question='Who composed the opera "The Barber of Seville"?', active=0, category='Music', administrator_id=4),
    Quiz(title='Sports Quiz', question='Which country won the FIFA World Cup in 2018?', active=1, category='Sports', administrator_id=2),
    Quiz(title='Technology Quiz', question='What is the name of Apple\'s virtual assistant?', active=1, category='Technology', administrator_id=4),
    Quiz(title='Animal Quiz', question='What is the largest mammal in the world?', active=1, category='Science', administrator_id=3),
    Quiz(title='Food Quiz', question='What is the national dish of Italy?', active=0, category='Cuisine', administrator_id=1),
    Quiz(title='Movie Quiz', question='Who directed the movie "Pulp Fiction"?', active=1, category='Movies', administrator_id=2)
]
session.add_all(quizzes)
session.commit()