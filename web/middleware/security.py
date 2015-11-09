# -*- coding:utf-8 -*-

import time, base64
from Crypto.PublicKey import RSA

from django.http import HttpResponse, HttpResponseForbidden


PRI = RSA.importKey('-----BEGIN KEY-----\nMIICXAIBAAKBgQCXceM9hdJM7LL7TnrmwX7HCMqVKvSaKHRwuFGDG2yFBfceJ92P\nWfKisn7l1QrtjHEXLvht1AlLi8q+keZSxGmsrlUMz7NlwhtBuwT+EjGZJ0+c8zra\nwHFbmcfMcAhVEKrQwecTU11Y9L7Xm1sB+OnfAVOt+jItBVlUIJif6llCjwIDAQAB\nAoGAaEpCTZy5LMYXnx31XrFDJ7czIrQZC4vuW61iXKHnAlgQTBDx74TmpQm8f3NN\nejarrmZnJ+LLn92decypSrf9eJ///aT+HCEcKow+evufBSS3y3XooKbVo5FRgdK1\n3aQOfSWZ7/oE4Y9bF61rrKDvWpnL4bhZUMAncfDzZgPwQpECQQC2fmDZf3gF9bvr\nzn37JoxXEQGURPeHX/6SM1qWoGT/mj1RjligYvKv6isZ+x7wA5MWp9il2oyhCeoa\ndQmuWICJAkEA1HHzCWTVzsAS/hbY4oLi0RFBWKnlsvoU6UiE6D20dja9D+7IdeeK\njcBJghZYHtibJzuBiSs+y8MLhRuIQuv0VwJBAIhIjK8ggFODFdmdlXtvaDLFInbF\nokzYpVYtP6NpGMPBPbWgJhNwkWhJ6fI3FP2MzdWHd0U0lvzUWJ11dctbkHECQFIX\n+m+d3JU5Wd2AHK1jIJzjixnlBVMlGmGPWXSZK5wmyOZYQnR1VfAy5vTzB3hcAZCm\niQblhC2fIFt+aShbH58CQBfRkmXCIwY525HX+LT31E97CAT5WT5l5sMM2fQrY9F1\n7iI+O2e5nuEwN32M1KrVYXDilkK7+xc8apfcguGzyM8=\n-----END KEY-----')

HEADER_KEY = "HTTP_KEY"

class Security(object):

    accept_name = ("myopen", "appstore", "zeus")
    accept_time_offset = 60 * 3

    def process_request(self, request):
        if request.META.get('PATH_INFO') == u"/admin/" or request.META.get('REMOTE_ADDR') == u"127.0.0.1" or request.user.is_authenticated():
            return None

        co = request.META.get(HEADER_KEY)
        if not co:
            return HttpResponseForbidden()

        try:
            name, send_time = self.pkcs1_unpad(PRI.decrypt(base64.b64decode(co))).split(" : ")
        except Exception, e:
            print "exception:", e
            return HttpResponseForbidden()

        if name not in self.accept_name:
            return HttpResponseForbidden()

        offset = int(time.time()) - int(send_time)
        if offset > self.accept_time_offset and offset < 0:
            return HttpResponseForbidden()


    def pkcs1_unpad(self, text):
        if len(text) > 0 and text[0] == '\x02':
            # Find end of padding marked by nul
            pos = text.find('\x00')
            if pos > 0:
                return text[pos+1:]
        return text

