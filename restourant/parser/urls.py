from django.urls import path

from .views import BurgerKingView, KFCView, McDonaldsView

urlpatterns = [
    path("v1/parser/kfc", KFCView.as_view()),
    path("v1/parser/burger_king", BurgerKingView.as_view()),
    path("v1/parser/mcdonalds", McDonaldsView.as_view()),
]
