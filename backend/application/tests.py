import os
import sys
from django.test import TestCase
from django.test.client import Client
from django.contrib import auth
import hashlib
from dvadmin.system.models import Users
from django.contrib.auth import get_user_model


class LoginTest(TestCase):
    def test_check_passwd(self):
        self.setup()
        # username = "deep-voxel"
        # password = "admin123456"
        # password = "a66abb5684c45962d887564f08346e8d"
        # # user_obj = auth.authenticate(
        # #     username=username,
        # #     password=hashlib.md5(password.encode(encoding="UTF-8")).hexdigest(),
        # # )
        c = self.client
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
        data = {"username":"sty","password":"123456","captcha":"8","captchaKey":108}
        response = c.post("/api/login/", data=data, content_type='application/json', HTTP_USER_AGENT=user_agent)   
        # print(response.status_code)
        print(response.json())
        # print(user_obj)
        # if user_obj:
        #     print("查找到")
        # else:
        #     print("用户/密码错误")
    
    def setup(self):
        self.user = Users(username="sty") # NB: You could also use a factory for this
        password = '123456'
        self.user.set_password(password)
        self.user.save()
        self.client = Client()
        self.client.login(username="sty", password=password)
# c = Client()
# # response = c.get("/api/init/settings/")
# data = {"username":"deep-voxel","password":"a66abb5684c45962d887564f08346e8d","captcha":"8","captchaKey":108}
# response = c.post("/api/login", data)
# print(response)
username = "deep-voxel"
UserModel = get_user_model()
user = UserModel._default_manager.get_by_natural_key(username)
user.set_password("123456")
user.save()
print(type(user))
# password = "a66abb5684c45962d887564f08346e8d"
# check_password = user.check_password(password)
# print(check_password)