from django.urls import path

from api.views import UploadUserData, COVIDTest, BotApi

urlpatterns = [
    path('uploaddata/', UploadUserData.as_view()),
    path('test/', COVIDTest.as_view()),
    path('bot/', BotApi.as_view())

]