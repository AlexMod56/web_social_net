from django import forms
from .models import Chat, Message
from django.contrib.auth.models import User

class ChatForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_superuser=False),
        widget=forms.CheckboxSelectMultiple,  # Отображаем список пользователей в виде чекбоксов
        required=True
    )

    class Meta:
        model = Chat
        fields = ['name', 'participants']  # Добавляем возможность выбирать участников

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # Получаем текущего пользователя из параметров
        super(ChatForm, self).__init__(*args, **kwargs)
        self.fields['participants'].queryset = User.objects.filter(is_superuser=False).exclude(id=self.user.id)  # Исключаем текущего пользователя из списка возможных участников

class MessageForm(forms.ModelForm):
    is_anonymous = forms.BooleanField(required=False, label='Send anonymously')  # Поле для выбора анонимности

    class Meta:
        model = Message
        fields = ['content', 'is_anonymous']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message here...'}),
        }
