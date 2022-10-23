from django.urls import path

from goals import views

urlpatterns = [
    path('goal_category/create', views.GoalCategoryCreateView.as_view()),
    path('goal_category/list', views.GoalCategoryCreateView.as_view()),
    path('goal_category/<pk>', views.GoalCategoryView.as_view()),

    path('goal/create', views.GoalCreateView.as_view()),
    path('goal/list', views.GoalCreateView.as_view()),
    path('goal/<pk>', views.GoalView.as_view()),
]
