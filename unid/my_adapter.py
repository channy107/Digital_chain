from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import myPageInfomation
from django.urls import reverse


# social 회원가입시 Profile 인스턴스를 함께 생성하도록 오버라이딩
class MyAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super(MyAdapter, self).save_user(request, sociallogin)
        # br = myPageInfomation (
        #                         user=user,
        #                         email=user.email,
        #                         name=user.first_name + user.last_name,
        # )
        myPageInfomation.objects.create(
            user=user,
            email=user.email,
            name=user.last_name + user.first_name)
        print("저장")
        user.save()

    # def get_connect_redirect_url(self, request, socialaccount):
    #     super(MyAdapter, self).get_connect_redirect_url(request, socialaccount)
    #     """
    #     Returns the default URL to redirect to after successfully
    #     connecting a social account.
    #     """
    #     member = myPageInfomation.objects.get(user=request.user)
    #     print(request.user)
    #     request.session['user_email'] = member.email
    #     request.session['user_name'] = member.name
    #     print(request.session['user_email'])
    #     assert request.user.is_authenticated
    #     url = reverse('socialaccount_connections')
    #     return url