# models.py

from src import db
from sqlalchemy import Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


from enum import Enum


def get_url(content):
    return f"https://{content.s3_bucket}.s3.amazonaws.com/{content.s3_id}"


class MediaType(Enum):
    Image = 1
    Text = 2
    Video = 3


class Content(db.Model):
    __tablename__ = "content"
    id = db.Column(db.Integer,
                   primary_key=True
    )  # primary keys are required by SQLAlchemy

    # relationships
    content_engagements = relationship("Engagement")  # one piece of content with many engagements
    generated_content_metadata = relationship('GeneratedContentMetadata', back_populates="content")
    non_generated_content_metadata = relationship('NonGeneratedContentMetadata', back_populates="content", uselist=False)

    # columns
    media_type = db.Column(SqlEnum(MediaType))
    s3_bucket = db.Column(db.String(200), nullable=True)
    s3_id = db.Column(db.String(200), nullable=True)  # might be only text, if media_type = Text
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    # Foreign Keys
    author_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)

class GeneratedType(Enum):
    HumanTxt2Img = 1
    GPT3Txt2Img = 2
    Img2Txt2Img = 3
    Img2Img = 4


class GeneratedContentMetadata(db.Model):
    __tablename__ = "generated_content_metadata"
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    content_id = db.Column(db.Integer, ForeignKey("content.id"))
    content = relationship("Content", back_populates="generated_content_metadata")

    seed = db.Column(db.Integer)
    num_inference_steps = db.Column(db.Integer)
    guidance_scale = db.Column(db.Integer)
    prompt = db.Column(db.String(1500))
    original_prompt = db.Column(db.String(1500))
    artist_style = db.Column(db.String(100))
    source = db.Column(db.String(100))
    source_img = db.Column(db.String(200), nullable=True)
    generated_type = db.Column(SqlEnum(GeneratedType))


class NonGeneratedContentMetadata(db.Model):
    __tablename__ = "non_generated_content_metadata"
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    content_id = db.Column(db.Integer, ForeignKey("content.id"))
    content = relationship("Content", back_populates="non_generated_content_metadata")

    source = db.Column(db.String(100))
    text = db.Column(db.String(1000), nullable=True)  # text on the post