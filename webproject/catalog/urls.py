from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('PositiveMovies', views.getPositive, name='Positive'),
    path('NeutralMovies', views.getNeutral, name='Neutral'),
    path('NegativeMovies', views.getNegative, name='Negative'),
    path('AngryMovies', views.getAnger, name='Angry'),
    path('FearMovies', views.getFear, name='Fear'),
    path('AnticipationMovies', views.getAnticipation, name='Anticipation'),
    path('SurprisedMovies', views.getSurprise, name='Surprise'),
    path('JoyfullMovies', views.getJoy, name='Joy'),
    path('SadMovies', views.getSadness, name='Sadness'),
    path('TrustedMovies', views.getTrust, name='Trust'),
    path('DisgustingMovies', views.getDisgust, name='Disgust'),
    path('About', views.getAbout, name='About'),
    path('SearchResults', views.searchAction, name='SearchBar')
]