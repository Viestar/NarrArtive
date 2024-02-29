from captcha.fields import ReCaptchaField
from django import forms


class SupportForm(forms.Form):
    """ Class with the form to use in asking for support """
    email = forms.EmailField(
        max_length=256,
        required=True
    )
    subject = forms.CharField(
        max_length=256
    )
    message = forms.CharField(
        max_length=65536
    )
    captcha = ReCaptchaField()
