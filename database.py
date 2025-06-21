""" Database module for logging conversations in dicord bot applications """

from sqlalchemy import create_engine, Column, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, timezone
import logging

loggerDB = logging.getLogger('Database')

# DATABASE SETUP
database = declarative_base()
engine = create_engine('sqlite:///bot_data.db', echo=False)
Session = sessionmaker(bind=engine)

# Define Tables
class User(database):
    __tablename__ = 'users'
    user_id = Column(String, primary_key=True)
    username = Column(String)
    creation_time = Column(DateTime, default=datetime.now(timezone.utc))

    messages = relationship('Message', back_populates='user')

class Message(database):
    __tablename__ = 'messages'
    message_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.user_id'))
    command = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="messages")
    response = relationship("Response", uselist=False, back_populates="message")

class Response(database):
    __tablename__ = 'responses'
    response_id = Column(String, primary_key=True)
    message_id = Column(String, ForeignKey('messages.message_id'))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))

    message = relationship("Message", back_populates="response")

# Initialize database
def init_db():
    database.metadata.create_all(engine)
    loggerDB.info("Database tables created.")

# Function to log conversations
def log_conversation(user_id, username, message_id, command, user_message, response_id, bot_response):
    """ Log a conversation in the database.
    Args:
        user_id (str): Unique identifier for the user.
        username (str): Username of the user.
        message_id (str): Unique identifier for the message.
        command (str): Command used by the user.
        user_message (str): Content of the user's message.
        response_id (str): Unique identifier for the bot's response.
        bot_response (str): Content of the bot's response.
    """
    session = Session()

    user = session.get(User, user_id)
    # Creates new user if they are new
    if not user:
        user = User(user_id=user_id, username=username)
        session.add(user)
        loggerDB.info(f"New user added: {user_id} ({username})")
    
    message = Message(message_id=message_id, user=user, command=command, content=user_message)
    response = Response(response_id=response_id, message=message, content=bot_response)

    session.add_all([message, response])
    session.commit()
    loggerDB.info(f"Conversation logged: User {user_id}, Message {message_id}, Response {response_id}")
    session.close()
    
# Function to retrieve all users    
def get_all_users():
    """ Retrieve all users from the database."""
    session = Session()
    users = session.query(User).all()
    users = [{
        "user_id": user.user_id,
        "username": user.username,
        "creation_time": user.creation_time.isoformat(),
        "message_count": len(user.messages)
    } for user in users]
    session.close()
    loggerDB.info(f"Retrieved {len(users)} users from database.")
    return users

# Function to retrieve all messages for a user
def get_user_messages(user_id):
    """ Retrieve all messages and their responses for a given user ID."""
    session = Session()
    user = session.query(User).filter_by(user_id=user_id).first()
    conversations = []
    if user:
        for message in user.messages:
            conversations.append({
                "message_id": message.message_id,
                "command": message.command,
                "content": message.content,
                "timestamp": message.timestamp,
                "response_id": message.response.response_id if message.response else None,
                "response_content": message.response.content if message.response else None
            })
        loggerDB.info(f"Fetched {len(conversations)} conversations for user {user_id}.")
    else:
        loggerDB.warning(f"User ID {user_id} not found.")
    session.close()
    return conversations

# Function to retrieve a message by its ID
def get_message_by_id(message_id):
    """ Retrieve a message and its response by message ID."""
    session = Session()
    message = session.query(Message).filter_by(message_id=message_id).first()
    if message:
        response_content = message.response.content if message.response else None
        result = {
            "message_id": message.message_id,
            "user_id": message.user.user_id,
            "command": message.command,
            "content": message.content,
            "timestamp": message.timestamp,
            "response_id": message.response.response_id if message.response else None,
            "response_content": response_content
        }
        loggerDB.info(f"Message {message_id} retrieved successfully.")
    else:
        result = None
        loggerDB.warning(f"Message ID {message_id} not found.")
    session.close()
    return result

# Function to search users by username
def search_users_by_username(query):
    """ Search for users by username using a case-insensitive search."""
    session = Session()
    results = session.query(User).filter(User.username.ilike(f"%{query}%")).all()
    loggerDB.info(f"Found {len(results)} users matching query '{query}'.")
    session.close()
    return results

print(get_all_users())
# print(get_user_messages('596483438517682186'))