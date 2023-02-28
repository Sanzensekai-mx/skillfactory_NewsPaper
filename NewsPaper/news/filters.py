from django import forms
from django_filters import FilterSet, DateTimeFilter, DateFilter

from .models import Post


class PostFilter(FilterSet):
    create_time = DateFilter(field_name='create_time', lookup_expr='gte',
                             widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
        }