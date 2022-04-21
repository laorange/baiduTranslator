from baiduTranslator import rewrite

if __name__ == '__main__':
    with open('text.txt', encoding='utf-8') as file:
        text = file.read()
    result = rewrite(text)
    print(result)
