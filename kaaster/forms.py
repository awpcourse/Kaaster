from django.forms import Form, CharField, Textarea, PasswordInput, ImageField

class UserLoginForm(Form):
    username = CharField(max_length=30)
    password = CharField(widget=PasswordInput)