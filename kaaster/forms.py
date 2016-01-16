from django.forms import Form, CharField, Textarea, PasswordInput, ImageField

class UserLoginForm(Form):
    username = CharField(max_length=30)
    password = CharField(widget=PasswordInput)

class CreatePostForm(Form):
    message = CharField(widget=Textarea(attrs={'rows': 20, 'cols': 50, 'placeholder': 'Your post'}), label='')
    link = CharField(max_length=100)

class UserPostForm(Form):
    text = CharField(widget=Textarea(attrs={'cols': 100, 'rows': 5}), label='')