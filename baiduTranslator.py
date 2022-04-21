import time
import random
from hashlib import md5
from pprint import pprint
from typing import List, Optional
import json

import pydantic
from pydantic import BaseModel, Field
import requests
from tqdm import tqdm

# 在 secret.json 修改隐私信息
with open('secret.json', encoding='utf-8') as file:
    secret_info = json.load(file)
    APP_ID = secret_info["APP_ID"]
    APP_KEY = secret_info["APP_KEY"]

# ↓ 自定义设置
MAX_RETRY_TIMES = 5  # 如果请求错误的重试次数
# 翻译的任务序列
SEQUENCE = ['fra', 'spa', 'en', 'jp', 'spa', 'jp', 'fra', 'jp', 'de', 'jp', 'fra', 'jp', 'zh']


class BaiduTranslateItem(BaseModel):
    src: str = Field(..., title="源文本")
    dst: str = Field(..., title="翻译之后的文本")


class BaiduTranslateResult(BaseModel):
    from_: str = Field(..., title="源语言", alias="from")
    to: str = Field(..., title="目标语言")
    trans_result: Optional[List[BaiduTranslateItem]] = Field(None, title="翻译结果")


class Translator:
    def __init__(self, to_lang='zh', from_lang='auto', sleep_time=1):
        # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`

        self.appId = APP_ID
        self.appKey = APP_KEY

        self.from_lang = from_lang
        self.to_lang = to_lang

        self.sleep_time = sleep_time

    def translate(self, input_text: str, retry_times=0):
        time.sleep(self.sleep_time)

        input_text = input_text.strip()
        salt = random.randint(32768, 65536)
        sign = self.make_md5(self.appId + input_text + str(salt) + self.appKey)

        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': self.appId, 'q': input_text,
                   'from': self.from_lang, 'to': self.to_lang, 'salt': salt, 'sign': sign}

        # Send request
        response = requests.post(self.getUrl(), params=payload, headers=headers, timeout=60)
        try:
            return self.getJoinedTranslation(BaiduTranslateResult(**response.json()))
        except pydantic.error_wrappers.ValidationError:
            pprint(response.json())
            if retry_times < MAX_RETRY_TIMES:
                return self.translate(input_text, retry_times + 1)

    @staticmethod
    def getUrl():
        return 'http://api.fanyi.baidu.com/api/trans/vip/translate'

    @staticmethod
    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    @staticmethod
    def getJoinedTranslation(item: BaiduTranslateResult) -> str:
        output = ""
        for result in item.trans_result:
            output += result.dst + "\n"
        return output


def rewrite(input_text):
    if not len(input_text):
        return ""

    last_language = 'auto'
    for language in tqdm(SEQUENCE):
        input_text = Translator(to_lang=language, from_lang=last_language).translate(input_text)
        last_language = language
    return input_text


if __name__ == '__main__':
    text = "《自然辩证法》是恩格斯的自然哲学研究的重要成果，构建了马克思主义的辩证唯物自然观。"

    Translator(to_lang='en', from_lang='zh').translate(text)
