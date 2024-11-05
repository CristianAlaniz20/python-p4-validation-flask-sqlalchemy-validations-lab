from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 

    @validates("name", "phone_number")
    def validate_author_input(self, key, value):
        if key == "name":
            author_with_duplicate_name = Author.query.filter(Author.name == value).first()
            if not value or author_with_duplicate_name:
                raise ValueError("Author field must not be empty and cannot have a duplicate name.")
        elif key == "phone_number":
            if not len(value) == 10 or not value.isdigit():
                raise ValueError("Phone number must be only 10 characters long and all must be numbers.")
        return value


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates("title", "content", "category", "summary")
    def validates_post_input(self, key, value):
        if key == "title":
            title_keywords_list = ["Won't Believe", "Secret", "Top", "Guess"]
            title_includes_keyword = [True for keyword in title_keywords_list if keyword in value]
            if not value or not title_includes_keyword:
                raise ValueError("Title cannot be empty and must contain a keyword.")

        if key == "content":
            if len(value) < 250:
                raise ValueError("Content needs to be at least 250 characters long.")
        
        if key == "summary":
            if len(value) > 250:
                raise ValueError("Summary needs to be a maximum of 250 characters.")

        if key == "category":
            if not value == "Fiction" and not value == "Non-Fiction":
                raise ValueError("Category can only be Fiction or Non-Fiction.")

        return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
