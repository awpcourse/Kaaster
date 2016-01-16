from django.forms import Form, CharField, Textarea, PasswordInput, ImageField,\
            EmailField, ValidationError, ChoiceField, DateField, SelectDateWidget
from django.contrib.auth.models import User


class UserLoginForm(Form):
    username = CharField(max_length=30)
    password = CharField(widget=PasswordInput)


class UserRegisterForm(Form):
    username = CharField(max_length=30)
    password = CharField(widget=PasswordInput)
    email = EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count():
            raise ValidationError('Email already in use!')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).count():
            raise ValidationError('Username taken, pick another one!')
        return username


class CreatePostForm(Form):
    message = CharField(widget=Textarea(attrs={'rows': 20, 'cols': 50, 'placeholder': 'Your post'}), label='')
    link = CharField(max_length=100)


class EditProfileForm(Form):
    first_name = CharField(max_length=50, required=False)
    last_name = CharField(max_length=50, required=False)
    email = EmailField(required=False)
    birthday = DateField(widget=SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
        ), required=False)
    gender = ChoiceField(choices=(('M', 'Male'), ('F', 'Female')), required=False)
    avatar = ImageField(required=False)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count():
            raise ValidationError('Email already in use!')
        return email


class CreatePostReplyForm(Form):
    message = CharField(widget=Textarea(attrs={'rows': 5, 'cols': 50, 'placeholder': 'Your comment'}), label='')
    link = CharField(max_length=100, required=False)
