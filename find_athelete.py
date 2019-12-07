# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()



class Athelete(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'athelete'
    id = sa.Column(sa.Integer, primary_key=True,)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Float)
    gold_medals = sa.Column(sa.Float)
    silver_medals = sa.Column(sa.Float)
    bronze_medals = sa.Column(sa.Float)
    total_medals = sa.Column(sa.Float)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True,)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()


def findUser(id_user, session):
    """
    Производит поиск пользователя в таблице user по заданному идентификатору id_user
    """
    # нахдим пользователя в таблице User, у которых поле User.id совпадает с парарметром id_user
    user = session.query(User).filter(User.id == id_user).first()
    #переводим дату рождения пользователя в формат datetime
    user_birthdate = datetime.datetime.strptime(user.birthdate, "%Y-%m-%d")
    user_height = user.height
    return user_birthdate, user_height

def nearest_by_bd(user_birthdate, session):
    """
    Ищет ближайшего по дате рождения атлета к пользователю user
    """
    athletes = session.query(Athelete).all()
    athlete_id_bd = {}
    for athlete in athletes:
        athlete_birthdate = datetime.datetime.strptime(athlete.birthdate, "%Y-%m-%d")
        athlete_id_bd[athlete.id] = athlete_birthdate
    min_delta = None
    athlete_id = None
    athlete_bd = None

    for id_key, bd in athlete_id_bd.items():
        delta = abs(user_birthdate - bd)
        if not min_delta or delta < min_delta:
            min_delta = delta
            athlete_id = id_key
            athlete_bd = bd
    return athlete_id, athlete_bd


def nearest_by_height(user_heigh, session):
    """
    Ищет ближайшего по росту атлета к пользователю
    """
    athletes = session.query(Athelete).filter(Athelete.height != None).all()
    atlhete_id_height={}
    for athlete in athletes:
        #athlete_heigh = athlete.height
        atlhete_id_height[athlete.id] = athlete.height
    
    min_delta = None
    athlete_id = None
    athlete_height = None

    for id_key, athl_h in atlhete_id_height.items():
        delta = abs(user_heigh - athl_h)
        if not min_delta or delta < min_delta:
            min_delta = delta
            athlete_id = id_key
            athlete_height = athl_h
    return athlete_id, athlete_height

def main ():
    session = connect_db()
    # просим пользователя выбрать режим
    mode = input("Выбери режим.\n1 - найти пользователя по идентификатору\n2 - посмотреть идентификаторы пользователей\n")
    # проверяем режим
    if mode == "1":
        id_user = int(input("Введи индентификатор пользователя для поиска: "))
        user = session.query(User).filter(User.id == id_user).first()
        if not user:
            print("Пользователя с таким id не существует")
        else:
            #определяем день рождения и рост пользователя
            user_birthdate, user_heigh = findUser(id_user, session)
            # получаем ближайшего к пользователю атлета по дате рождения
            athlete_id, athlete_bd = nearest_by_bd(user_birthdate, session)
            # получаем ближайшего к пользователю атлета по росту
            athlete_id_height, athlete_height = nearest_by_height(user_heigh, session)
            print("Ближайший по дате рождения атлет: {}, его дата рождения: {}".format(athlete_id, athlete_bd))
            print("Ближайший по росту атлет: {}, его рост: {}".format(athlete_id_height, athlete_height))
    elif mode == "2":
        users = session.query(User).all()
        id_users = [user.id for user in users]
        print("список идентификаторов: " + str(id_users))
    else:
        print("Неверный режим")


if __name__ == "__main__":
    main()
