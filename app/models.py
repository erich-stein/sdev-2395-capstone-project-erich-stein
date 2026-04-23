from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
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
  
class Recipe(db.Model):
  __tablename__ = 'recipes'

  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  #title name of recipe
  #long_desc for recipe page
  #short_desc for recipe card
  #categories main, side, dessert, etc.
  #tags meat, vegetarian, vegan, pork, beef, lamb, etc. maybe a list of selectables
  #ingredients
  #instructions
  timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
  user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

  creator: so.Mapped[User] = so.relationship(back_populates='recipes')

  def __repr__(self):
    return '<Recipe {}'.format(self.title)