from django import forms
from .models import Movie, Genre
from django.core.exceptions import ValidationError
from datetime import date
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import PrependedText
from .models import Comment


class MovieForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Géneros (Selecciona de 1 a 3)",
        required=True
    )

    class Meta:
        model = Movie
        fields = [
            'title', 'description', 'release_date', 'rating', 
            'duration', 'language', 'director', 'cast', 
            'tmdb_url', 'poster_image', 'drive_url', 'genres'
        ]

    def clean_genres(self):
        genres = self.cleaned_data.get('genres')
        if len(genres) < 1:
            raise forms.ValidationError("Debes seleccionar al menos 1 género.")
        if len(genres) > 3:
            raise forms.ValidationError("No puedes seleccionar más de 3 géneros.")
        return genres
    
'''Este formulario incluye:
- Campos para los datos básicos de la película.
- Un selector múltiple para los géneros (`genres`).'''


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['nick', 'email', 'text']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        # Personaliza las etiquetas y los placeholders
        self.fields['nick'].label = "Tu Nick"
        self.fields['nick'].widget.attrs.update({'placeholder': 'Escribe tu nombre aquí...'})

        self.fields['email'].label = "Correo Electrónico (opcional)"
        self.fields['email'].widget.attrs.update({'placeholder': 'comecerebros@gmail.com.'})

        self.fields['text'].label = "Texto"
        self.fields['text'].widget.attrs.update({
            'placeholder': 'Escribe tu comentario...',
            'maxlength': '400'  # Límite visual en el campo
        })

        # Configuración de Crispy Forms
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            PrependedText('nick', '@'),  # Prefijo "@" para el campo Nick
            PrependedText('email', '✉'),  # Prefijo "✉" para el campo Email
            'text',  # Campo Texto
            Submit('submit', 'Enviar', css_class='btn btn-success btn-lg mt-3')  # Botón verde "Enviar"
        )

    # Validación del campo "text" para un límite de 300 caracteres
    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) > 400:
            raise ValidationError("El comentario no puede tener más de 400 caracteres.")
        return text
