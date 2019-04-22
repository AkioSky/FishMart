import unicodedata
from captcha.fields import ReCaptchaField
from django import forms
from django.conf import settings
from django.contrib.auth import forms as django_forms, update_session_auth_hash, password_validation
from django.utils.translation import pgettext, pgettext_lazy
from django.contrib.auth.forms import UserCreationForm
from phonenumbers.phonenumberutil import country_code_for_region
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django.utils.translation import gettext, gettext_lazy as _

from . import emails
from ..account.models import User
from .i18n import AddressMetaForm, get_address_form_class


class FormWithReCaptcha(forms.BaseForm):
    def __new__(cls, *args, **kwargs):
        if settings.RECAPTCHA_PUBLIC_KEY and settings.RECAPTCHA_PRIVATE_KEY:
            # insert a Google reCaptcha field inside the form
            # note: label is empty, the reCaptcha is self-explanatory making
            #       the form simpler for the user.
            cls.base_fields['_captcha'] = ReCaptchaField(label='')
        return super(FormWithReCaptcha, cls).__new__(cls)


def get_address_form(
        data, country_code, initial=None, instance=None, **kwargs):
    country_form = AddressMetaForm(data, initial=initial)
    preview = False
    if country_form.is_valid():
        country_code = country_form.cleaned_data['country']
        preview = country_form.cleaned_data['preview']

    if initial is None and country_code:
        initial = {}
    if country_code:
        initial['phone'] = '+{}'.format(country_code_for_region(country_code))

    address_form_class = get_address_form_class(country_code)

    if not preview and instance is not None:
        address_form_class = get_address_form_class(instance.country.code)
        address_form = address_form_class(data, instance=instance, **kwargs)
    else:
        initial_address = (
            initial if not preview
            else data.dict() if data is not None else data)
        address_form = address_form_class(
            not preview and data or None,
            initial=initial_address,
            **kwargs)
    return address_form, preview


class ChangePasswordForm(django_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].user = self.user
        self.fields['old_password'].widget.attrs['placeholder'] = ''
        self.fields['new_password1'].widget.attrs['placeholder'] = ''
        del self.fields['new_password2']


def logout_on_password_change(request, user):
    if (update_session_auth_hash is not None and
            not settings.LOGOUT_ON_PASSWORD_CHANGE):
        update_session_auth_hash(request, user)


class LoginForm(django_forms.AuthenticationForm, FormWithReCaptcha):
    username = forms.EmailField(
        label=pgettext('Form field', 'Email'), max_length=75)

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        if request:
            email = request.GET.get('email')
            if email:
                self.fields['username'].initial = email


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))


class PopupLoginForm(django_forms.AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}),
                             label=pgettext('Alamat Email', 'Alamat Email'))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label=pgettext('Kata Sandi', 'Kata Sandi'), required=True)

    class Meta:
        model = User
        fields = ('email', 'password')


class SignupForm(forms.ModelForm, FormWithReCaptcha):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label=pgettext('Password', 'Password'))
    confirm_password = forms.CharField(widget=forms.PasswordInput(),
                                       label=pgettext('Confirm Password',
                                                      'Confirm Password'))
    email = forms.EmailField(
        label=pgettext('Email', 'Email'),
        error_messages={
            'unique': pgettext_lazy(
                'Registration error',
                'This email has already been registered.')})
    full_name = forms.CharField(widget=forms.TextInput,
                                label=pgettext('Full name', 'Full name'))
    birthday = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'),
                               label=pgettext('Date of birth', 'Date of birth'),
                               input_formats=('%Y-%m-%d',))
    phone = forms.CharField(widget=forms.TextInput,
                            label=pgettext('Phone Number', 'Phone Number'))
    address = forms.CharField(widget=forms.TextInput,
                              label=pgettext('Address', 'Address'))
    billing_address = forms.CharField(widget=forms.TextInput,
                                      label=pgettext('Billing Address',
                                                     'Billing Address'))
    SEX_CHOICES = (('man', 'Man'), ('woman', 'Woman'))
    sex = forms.TypedChoiceField(choices=SEX_CHOICES, widget=forms.RadioSelect)
    COMPANY_CHOICES = (('individual', 'Individual'), ('industry', 'Industry'))
    company = forms.TypedChoiceField(choices=COMPANY_CHOICES, widget=forms.RadioSelect)

    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }

    class Meta:
        model = User
        fields = ('email', 'full_name', 'birthday', 'phone', 'address',
                  'billing_address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update(
                {'autofocus': ''})

    def save(self, request=None, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password']
        user.set_password(password)
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return self.cleaned_data


class PopupSignUp(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    password1 = forms.CharField(
        label=_("Kata Sandi"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Konfirmasi Kata Sandi"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Alamat Email',
        error_messages={
            'unique': pgettext_lazy(
                'Registration error',
                'This email has already been registered.')},
        required=True)
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                label='Nama Lengkap',
                                required=True)
    birthday = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d',
                                                      attrs={'class': 'form-control'}),
                               label='Tanggal lahir',
                               input_formats=('%Y-%m-%d',),
                               required=True)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label='Nomer Telpon',
                            required=True)
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                              label='Alamat',
                              required=True)
    billing_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                      label='Alamat Penagihan',
                                      required=True)
    GENDER_CHOICES = (('man', 'Pria'), ('woman', 'Wanita'))
    gender = forms.ChoiceField(choices=GENDER_CHOICES,
                                    widget=forms.RadioSelect,
                                    required=True)
    COMPANY_CHOICES = (('individual', 'Individu'), ('industry', 'Industri'))
    user_type = forms.ChoiceField(choices=COMPANY_CHOICES,
                                       widget=forms.RadioSelect,
                                       required=True)

    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }

    class Meta:
        model = User
        fields = ('email', 'full_name', 'birthday', 'phone', 'address',
                  'billing_address', 'password1', 'password2', 'gender', 'user_type')

    def clean(self):
        cleaned_data = super(PopupSignUp, self).clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return self.cleaned_data


class PasswordResetForm(django_forms.PasswordResetForm, FormWithReCaptcha):
    """Allow resetting passwords.

    This subclass overrides sending emails to use templated email.
    """

    def get_users(self, email):
        active_users = User.objects.filter(email__iexact=email, is_active=True)
        return active_users

    def send_mail(
            self, subject_template_name, email_template_name, context,
            from_email, to_email, html_email_template_name=None):
        # Passing the user object to the Celery task throws an
        # error "'User' is not JSON serializable". Since it's not used in our
        # template, we remove it from the context.
        del context['user']
        emails.send_password_reset_email.delay(context, to_email)


class NameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        labels = {
            'first_name': pgettext_lazy(
                'Customer form: Given name field', 'Given name'),
            'last_name': pgettext_lazy(
                'Customer form: Family name field', 'Family name')}
