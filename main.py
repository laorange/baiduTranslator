from baiduTranslator import rewrite

if __name__ == '__main__':
    with open('text.txt', encoding='utf-8') as file:
        text = file.read()
    result = rewrite(text)
    print("原文:", text, sep='\n')
    print("-" * 10)
    print("处理后:", result, sep="\n")
