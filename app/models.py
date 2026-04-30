from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional
from app import db

class User(db.Model):
  __tablename__ = 'users'

  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
  password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))

  recipes: so.WriteOnlyMapped['Recipe'] = so.relationship(
        back_populates='creator')

  def __repr__(self):
    return '<User {}>'.format(self.username)
  
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  def to_json(self):
    return {
      'id': self.id,
      'username': self.username
    }
  
class Recipe(db.Model):
  __tablename__ = 'recipes'

  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  title: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
  long_desc: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
  short_desc: so.Mapped[str] = so.mapped_column(sa.String(512))

  categories: so.Mapped[Optional[dict]] = so.mapped_column(sa.JSON)
  tags: so.Mapped[Optional[dict]] = so.mapped_column(sa.JSON)
  ingredients: so.Mapped[dict] = so.mapped_column(sa.JSON)
  instructions: so.Mapped[dict] = so.mapped_column(sa.JSON)

  timestamp: so.Mapped[datetime] = so.mapped_column(
    index=True, default=lambda: datetime.now(timezone.utc))
  updated: so.Mapped[datetime] = so.mapped_column(
    default=lambda: datetime.now(timezone.utc))
  user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

  creator: so.Mapped[User] = so.relationship(back_populates='recipes')

  def __repr__(self):
    return '<Recipe {}'.format(self.title)
  
  # serialize the data for frontend
  def to_json(self):
    json_recipe = {
      'id': self.id,
      'title': self.title,
      'long_desc': self.long_desc,
      'short_desc': self.short_desc,
      'categories': self.categories,
      'tags': self.tags,
      'ingredients': self.ingredients,
      'instructions': self.instructions,
      'timestamp': self.timestamp.isoformat(),
      'updated': self.updated.isoformat() if self.updated else None,
      'user_id': self.user_id,
      'creator': self.creator.username
    }
    return json_recipe