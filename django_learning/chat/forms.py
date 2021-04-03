from django import forms
from .models import Message
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        # 这里面有的参数必须包含在models
        fields = [
            'title',
            'content',
            'asker',
        ]

# class MessageForm(forms.Form):
#     title = forms.CharField()
#     content = forms.CharField()