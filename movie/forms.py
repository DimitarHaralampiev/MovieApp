from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

from movie.models import Movie, Comment, Rating


class MovieForm(forms.ModelForm):
    """Form for adding and updating Movie objects."""

    release_date = forms.DateField(
        label='RELEASE DATE',
        required=True,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )

    def __init__(self, *args, **kwargs):
        """Initialize MovieForm with crispy-forms layout."""
        super(MovieForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'description',
            'release_date',
            'director',
            'genre',
            'cover_image',
            Submit('submit', 'Add Movie')
        )

    class Meta:
        model = Movie
        fields = ('title', 'description', 'release_date', 'director', 'genre', 'cover_image')


class CommentForm(forms.ModelForm):
    """Form for adding comments to Movie objects."""

    class Meta:
        model = Comment
        fields = ['text']


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']




