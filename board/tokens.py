# 만들어준 AccountActivationTokenGenerator 는 PasswordResetTokenGenerator 를 상속
# PasswordResetTokenGenerator 는 장고에서 제공해주는 class 로서 비밀번호를 리셋할 떄 token을 발급해주고 해당 기능을 처리
# 이 방법으로 token 받음 
# text_type 은 유니코드 정수로부터 유니코드 문자열을 가져옴
# user의 pk, 현재시간, user의 활성화를 가지고 합쳐 tokens 을 생성

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)) +  six.text_type(user.is_active)

account_activation_token = AccountActivationTokenGenerator()