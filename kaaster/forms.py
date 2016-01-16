from django.forms import Form, CharField, Textarea, PasswordInput, ImageField,\
            EmailField

class UserLoginForm(Form):
    username = CharField(max_length=30)
    password = CharField(widget=PasswordInput)


class UserRegisterForm(Form):
    username = CharField(max_length=30)
    password = CharField(widget=PasswordInput)
    email = EmailField()