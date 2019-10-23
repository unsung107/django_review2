from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model # 현재활성화된 user model을 return한다

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name']

# 커스터마이지한 유저모델을 인식하지못해서 직접 get_user_model 함수로
# 유저정보를 넣어줌

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields