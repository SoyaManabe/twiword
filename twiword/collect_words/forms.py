from django import forms
from .models import Words

class QuizForm(forms.Form):
    class Meta:
        model = Words
        fields = ("user",
                  "tweet",
                  "word",
                  "trans",
                  "category",
                  "quiz",
                  "owner")
