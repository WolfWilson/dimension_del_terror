from django import forms
from .models import Movie, Genre
from django.core.exceptions import ValidationError
from datetime import date
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import PrependedText
from .models import Comment
from .models import MovieRequest

from django import forms
from .models import Movie, Genre
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset
from django.core.exceptions import ValidationError
from urllib.parse import urlparse

from .models import Series, Genre, Season, Episode
from crispy_forms.layout import Layout, Submit, Fieldset, Row, Column

class MovieForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "custom-checkbox"}),
        label="Géneros (Selecciona de 1 a 3)",
        required=True
    )
    
    class Meta:
        model = Movie
        fields = [
            'title', 'description', 'release_date', 'rating', 'duration', 
            'language', 'director', 'cast', 'tmdb_url', 'poster_image', 
            'header_image', 'drive_url', 'trailer_url', 'genres', 'review'
        ]
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'review': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
            'poster_image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'header_image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'drive_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://drive.google.com/...'}),
            'trailer_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/...'}),
        }

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Fieldset(
                'Agregar Película',
                Row(
                    Column('title', css_class='form-group col-md-6 mb-0'),
                    Column('release_date', css_class='form-group col-md-6 mb-0'),
                ),
                'description',
                Row(
                    Column('rating', css_class='form-group col-md-4 mb-0'),
                    Column('duration', css_class='form-group col-md-4 mb-0'),
                    Column('language', css_class='form-group col-md-4 mb-0'),
                ),
                Row(
                    Column('director', css_class='form-group col-md-6 mb-0'),
                    Column('cast', css_class='form-group col-md-6 mb-0'),
                ),
                'tmdb_url',
                'drive_url',
                'trailer_url',
                Row(
                    Column('poster_image', css_class='form-group col-md-6 mb-0'),
                    Column('header_image', css_class='form-group col-md-6 mb-0'),
                ),
                'genres',
                'review'
            ),
            Submit('submit', 'Guardar Película', css_class='btn btn-success')
        )

    def clean_genres(self):
        """Validar que el usuario selecciona entre 1 y 3 géneros."""
        genres = self.cleaned_data.get('genres')
        if not genres or len(genres) < 1:
            raise ValidationError("Debes seleccionar al menos 1 género.")
        if len(genres) > 3:
            raise ValidationError("No puedes seleccionar más de 3 géneros.")
        return genres

    def clean_trailer_url(self):
        """Validar que la URL del tráiler sea de YouTube o válida."""
        url = self.cleaned_data.get('trailer_url')
        if url:
            parsed_url = urlparse(url)
            if "youtube.com" not in parsed_url.netloc and "youtu.be" not in parsed_url.netloc:
                raise ValidationError("La URL del tráiler debe ser un enlace de YouTube válido.")
        return url

    def clean_rating(self):
        """Validar que la calificación esté entre 0 y 10."""
        rating = self.cleaned_data.get('rating')
        if rating is not None and (rating < 0 or rating > 10):
            raise ValidationError("La calificación debe estar entre 0 y 10.")
        return rating

    
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


class MovieRequestForm(forms.ModelForm):
    class Meta:
        model = MovieRequest
        fields = ['name', 'email', 'message']

    def __init__(self, *args, **kwargs):
        super(MovieRequestForm, self).__init__(*args, **kwargs)

        # Personaliza las etiquetas y los placeholders
        self.fields['name'].label = "Nombre"
        self.fields['name'].widget.attrs.update({'placeholder': 'Tu nombre...'})

        self.fields['email'].label = "Correo Electrónico"
        self.fields['email'].widget.attrs.update({'placeholder': 'tuemail@ejemplo.com'})

        self.fields['message'].label = "Mensaje"
        self.fields['message'].widget.attrs.update({
            'placeholder': 'Escribe tu pedido (máximo 150 caracteres)...',
            'maxlength': '150'  # Límite visual en el input
        })

        # Configuración de Crispy Forms
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            PrependedText('name', '👤'),  # Prefijo para el campo Nombre
            PrependedText('email', '✉'),  # Prefijo para el campo Email
            'message',  # Campo Mensaje
            Submit('submit', 'Enviar Pedido', css_class='btn btn-success btn-lg mt-3')  # Botón verde
        )

    # Validación del campo "message" para un límite de 150 caracteres
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) > 150:
            raise forms.ValidationError("El mensaje no puede tener más de 150 caracteres.")
        return message
    


#:::::::::::::::::::::::: formularuio para el fornted simpificado::::::::::::::::::::::::::::::

from urllib.parse import urlparse

class MovieFrontendForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all().order_by('name'),  # Ordenar alfabéticamente
        widget=forms.CheckboxSelectMultiple(attrs={"class": "custom-checkbox"}),
        label="Géneros (Selecciona de 1 a 3)",
        required=True
    )

    class Meta:
        model = Movie
        fields = ['title', 'tmdb_url', 'drive_url', 'genres']  # Cambiar 'trailer_url' por 'drive_url'
        widgets = {
            'tmdb_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.themoviedb.org/...'}),
            'drive_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://drive.google.com/...'}),  # Actualizar placeholder
        }

    def __init__(self, *args, **kwargs):
        super(MovieFrontendForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Agregar Película',
                'title',
                'tmdb_url',
                'drive_url',  # Cambiar 'trailer_url' por 'drive_url'
                'genres',
            ),
            Submit('submit', 'Guardar Película', css_class='btn btn-success')
        )

    def clean_genres(self):
        """Validar que el usuario seleccione entre 1 y 6 géneros."""
        genres = self.cleaned_data.get('genres')
        if not genres or len(genres) < 1:
            raise ValidationError("Debes seleccionar al menos 1 género.")
        if len(genres) > 6:  # Cambiado de 3 a 6
            raise ValidationError("No puedes seleccionar más de 6 géneros.")
        return genres

    def clean_drive_url(self):
        """Validar que la URL del enlace sea de Google Drive."""
        url = self.cleaned_data.get('drive_url')
        if url:
            parsed_url = urlparse(url)
            if "drive.google.com" not in parsed_url.netloc:
                raise ValidationError("La URL debe ser un enlace de Google Drive válido.")
        return url


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = [
            'title',
            'description',
            'release_date',
            'rating',
            'language',
            'tmdb_url',
            'poster_image',
            'header_image',
            'genres',
        ]


# forms.py
from django import forms
from .models import Episode
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Row, Column

class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = [
            'season',
            'episode_number',
            'title',
            'description',
            'air_date',
            'duration',
            'drive_url',
            'screenshot',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Información de episodio',
                Row(
                    Column('season', css_class='form-group col-md-4 mb-0'),
                    Column('episode_number', css_class='form-group col-md-4 mb-0'),
                    Column('duration', css_class='form-group col-md-4 mb-0'),
                ),
                Row(
                    Column('title', css_class='form-group col-md-6 mb-0'),
                    Column('air_date', css_class='form-group col-md-6 mb-0'),
                ),
                'description',
                'drive_url',
                'screenshot',
            ),
            Submit('submit', 'Guardar')
        )
