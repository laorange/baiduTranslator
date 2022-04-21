# 调用百度翻译来粗暴降重

参考项目：https://github.com/QiYuTechOrg/baidu-translate-py

参考文档：https://api.fanyi.baidu.com/doc/21

## 使用方法：

```python
# 翻译
from baiduTranslator import Translator
text = "需要翻译的文本"
Translator(to_lang='en', from_lang='zh').translate(text)
```



```python
# 降重
from baiduTranslator import rewrite
text = "需要降重的文本"
rewrite(text)
```

