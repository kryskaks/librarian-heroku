# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, SelectMultipleField, BooleanField, PasswordField
from wtforms.validators import Required, Length, EqualTo
from config import USERS
from constants import ERROR_LOGIN_INVALID, ERROR_PASSWORD_INVALID
from app.models import User


class SearchForm(Form):    
  text = TextField('', [Required(), Length(max=150)])
  by_author = BooleanField(u'По автору', default = True)
  by_title = BooleanField(u'По названию', default = True)

  def set_defaults(self):
  	self.by_author.data = True
  	self.by_title.data = True

  	return self  

class AddEntityForm(Form):
  text = TextField('', [Required(), Length(max=150)])

class UpdateAuthorForm(Form):  
  text = TextField('', [Required(), Length(max=150)])  

class UpdateBookForm(Form):
  text = TextField('', [Required(), Length(max=150)])	
  authors = SelectMultipleField('')

  def validate(self):
  	return self.text.validate({})

class LoginForm(Form):
  login = TextField('', [Required(), Length(max=150)])
  password = PasswordField('', [Required(), Length(max=150)])

  def validate(self):
    if not self.login.validate({}) or not self.password.validate({}):
      return False

    login = self.login.data
    password = self.password.data

    user = User.query.filter_by(login = login).first()

    if not user:
      self.login.errors.append(ERROR_LOGIN_INVALID.format(user = login))
      return False
    
    if password != user.password:
      self.password.errors.append(ERROR_PASSWORD_INVALID.format(user = login))
      return False

    return True

class RegistrationForm(Form):
  login = TextField('', [Required(), Length(max=150)])
  password = PasswordField('', [Required(), EqualTo('confirm', message = u'Пароли должны совпадать'), Length(max=150)])
  confirm = PasswordField('')