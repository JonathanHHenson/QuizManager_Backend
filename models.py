import sqlalchemy as sa
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

db = SQLAlchemy()


class Quiz(db.Model):
    __tablename__ = 'Quiz'
    id = sa.Column('ID', sa.Integer, primary_key=True)
    title = sa.Column('Title', sa.String(50), nullable=False)
    questions = relationship("Question", backref="Quiz.ID", cascade="all, delete")

    def __repr__(self):
        return f'<Quiz(id={self.id}, title={self.title})>'


class Question(db.Model):
    __tablename__ = 'Question'
    id = sa.Column('ID', sa.Integer, primary_key=True)
    quiz_id = sa.Column('QuizID', sa.Integer, sa.ForeignKey('Quiz.ID'))
    question_text = sa.Column('QuestionText', sa.String(200), nullable=False)
    question_order = sa.Column('QuestionOrder', sa.Integer, nullable=False)
    answer_a = sa.Column('AnswerA', sa.String(200), nullable=False)
    answer_b = sa.Column('AnswerB', sa.String(200), nullable=False)
    answer_c = sa.Column('AnswerC', sa.String(200), nullable=False)
    answer_d = sa.Column('AnswerD', sa.String(200))
    answer_e = sa.Column('AnswerE', sa.String(200))

    def __repr__(self):
        return f'<Question(id={self.id}, question_text={self.question_text})>'


class Authentication(db.Model):
    __tablename__ = 'Authentication'
    id = sa.Column('ID', sa.Integer, primary_key=True)
    permission_id = sa.Column('PermissionID', sa.Integer, sa.ForeignKey('Permission.ID'))
    username = sa.Column('Username', sa.String(20), nullable=False, unique=True)
    password = sa.Column('Password', sa.String(256), nullable=False)

    def __repr__(self):
        return f'<Authentication(id={self.id}, username={self.username})>'


class Permission(db.Model):
    __tablename__ = 'Permission'
    id = sa.Column('ID', sa.Integer, primary_key=True)
    label = sa.Column('Label', sa.String(20), nullable=False, unique=True)

    def __repr__(self):
        return f'<Permission(id={self.id}, label={self.label})>'


class QuizSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Quiz
        include_relationships = True
        load_instance = True


class QuestionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Question
        include_fk = True
        load_instance = True


class AuthenticationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Authentication
        include_fk = True
        load_instance = True


class PermissionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Permission
        load_instance = True
