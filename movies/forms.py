from django import forms
from .models import Movie, Genre
from datetime import date

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

