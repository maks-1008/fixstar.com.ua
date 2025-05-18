from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, 
        required=False, 
        help_text='Необов\'язково.',
        widget=forms.TextInput(attrs={'placeholder': "Ім'я", 'class': 'form-input'})
    )
    last_name = forms.CharField(
        max_length=150, 
        required=False, 
        help_text='Необов\'язково.',
        widget=forms.TextInput(attrs={'placeholder': 'Прізвище', 'class': 'form-input'})
    )
    email = forms.EmailField(
        max_length=254, 
        help_text='Обов\'язково. Введіть дійсну адресу електронної пошти.',
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'autocomplete': 'email', 'class': 'form-input'})
    )
    phone_number = forms.CharField(
        required=True,
        help_text='Обов\'язково для зв\'язку.',
        widget=forms.TextInput(attrs={
            'id': 'id_phone', 
            'type': 'tel', 
            'placeholder': 'Номер телефону', 
            'class': 'form-input'
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "phone_number")
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': "Логін", 'autocomplete': 'username', 'class': 'form-input'}),
        }
        help_texts = {
            'username': None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = ''
        
        # Установка плейсхолдеров для полей паролей
        self.fields['password1'].widget.attrs.update({'placeholder': 'Пароль', 'class': 'form-input'})
        
        # Делаем поле password2 скрытым и автоматически заполняемым
        if 'password2' in self.fields:
            self.fields['password2'].widget = forms.HiddenInput()
            self.fields['password2'].required = False

class ProfileForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть номер телефону'})
    )
    
    old_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть поточний пароль'}),
        label='Старий пароль'
    )
    
    password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть новий пароль'}),
        label='Новий пароль'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['email'].required = True
    
    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        password1 = cleaned_data.get('password1')
        
        # Если пользователь хочет изменить пароль, старый пароль должен быть указан
        if password1 and not old_password:
            self.add_error('old_password', 'Для зміни пароля потрібно ввести старий пароль')
        
        # Проверка правильности старого пароля
        if old_password and not self.instance.check_password(old_password):
            self.add_error('old_password', 'Невірний пароль')
            
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Если указан новый пароль и старый пароль проверен, меняем пароль
        password1 = self.cleaned_data.get('password1')
        old_password = self.cleaned_data.get('old_password')
        
        if password1 and old_password and self.instance.check_password(old_password):
            user.set_password(password1)
            
        if commit:
            user.save()
            
        return user