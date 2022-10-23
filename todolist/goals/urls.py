from django.urls import path

from goals import views

urlpatterns = [
    path('goal_category/create', views.GoalCategoryCreateView.as_view()),
    path('goal_category/list', views.GoalCategoryCreateView.as_view()),
    path('goal_category/<pk>', views.GoalCategoryView.as_view()),
]
