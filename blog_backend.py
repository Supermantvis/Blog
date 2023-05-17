# Komandinė užduotis (BLOG'as):
# Reikalavimai:
# - SQLAlchemy
# - Duomenų modelio sąsajos: išnaudotas many-to-one ryšys, many-to-many būtų pliusas
# - PySimpleGUI pagrindu įgyvendinta vartotojo sąsaja
# - Išskirtas backend (modelis ir bazės sukūrimas) ir frontend (vartotojo sąsaja)
# Objektiškai realizuota vartotojo sąsaja yra didelis pliusas 

from sqlalchemy import create_engine, Integer, String, ForeignKey, Column
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_name = Column(String(50))
    email = Column(String(50))
    f_name = Column(String(50))
    l_name = Column(String(50))
    # Relationships:
    posts_by_user = relationship("Posts", back_populates="user_post")
    liked_by_user = relationship("Likes", back_populates="user_like")
    commented_by_user = relationship("Comments", back_populates="user_comments")

    def __repr__(self):
        return f"({self.id}, {self.user_name})"


class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_name = Column(String(50))
    content = Column(String(300))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    # Relationships:
    user_post = relationship("Users", back_populates="posts_by_user")
    posts_in_topic = relationship("Topics", back_populates="topic_with_posts")
    all_likes = relationship("Likes", back_populates="post_like")
    all_comments = relationship("Comments", back_populates="post_comments")

    def __repr__(self):
        return f"({self.id}, {self.user_id}, {self.topic_id})"


class Topics(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True)
    topic_name = Column(String(50))
    # Relationships:
    topic_with_posts = relationship("Posts", back_populates="posts_in_topic")

    def __repr__(self):
        return f"({self.id}, {self.topic_name})"


class Likes(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    # Relationships:
    user_like = relationship("Users", back_populates="liked_by_user")
    post_like = relationship("Posts", back_populates="all_likes")

    def __repr__(self):
        return f"({self.user_id}, {self.post_id})"
    

class Comments(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    comment = Column(String(250))
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    # Relationships:
    user_comments = relationship("Users", back_populates="commented_by_user")
    post_comments = relationship("Posts", back_populates="all_comments")

    def __repr__(self):
        return f"({self.comment}, {self.user_id}, {self.post_id})"


engine = create_engine('sqlite:///blog.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def add_user(user_name, email, f_name, l_name, ):
    user = Users(user_name=user_name, email=email, f_name=f_name, l_name=l_name)
    session.add(user)
    session.commit()

add_user('Kielele', 'kiele@gmail.com','Leta', 'Kiele')
add_user('Mojo', 'linge@gmail.com', 'Marius', 'Linge')
add_user('Nemunas', 'karietaite@gmail.com', 'Gile', 'Karietaite')
add_user('Lololo', 'alka@gmail.com', 'Lina', 'Alka')
add_user('Klaja', 'bukutis@gmail.com', 'Martynas', 'Bukutis')


def get_users():
    users = session.query(Users).all()
    return users

def get_user_by_id(user_id):
    user = session.get(Users, user_id)
    return user

def view_posts():
    posts = session.query(Posts).all()
    for post in posts:
        print(post)
    return posts

def add_posts(user_id, post_name, content, topic_id):
    posts = Posts(user_id=user_id, post_name=post_name, content=content, topic_id=topic_id)
    session.add(posts)
    session.commit()

def add_topic(topic_name):
    topic = Topics(topic_name=topic_name)
    session.add(topic)
    session.commit()

def view_topic():
    all_topics = session.query(Topics).all()
    for topic in all_topics:
        print(topic)
    return all_topics



