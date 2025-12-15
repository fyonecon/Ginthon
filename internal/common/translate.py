# -*- coding: utf-8 -*-

import locale

# 获取翻译
def get_translate(key="-null-", lang=""):
    # 将语言转换成可用的数组索引标记
    def make_lang_index(language):
        if language is not None:
            _language = language.lower()
            pass
        else:
            print("locale.getlocale() = ", locale.getlocale())
            _language = ""
            pass
        #
        if _language.find("zh", 0)==0 or _language.find("chinese", 0)==0:  # 简体中文（包含繁体）
            return "zh"
        elif _language.find("en", 0)==0 or _language.find("english", 0)==0:  # 英文
            return "en"
        elif _language.find("jp", 0)==0:  # 日文
            return "jp"
        elif _language.find("fr", 0)==0:  # 法语
            return "fr"
        elif _language.find("de", 0)==0:  # 德语
            return "de"
        elif _language.find("ru", 0)==0:  # 俄语或乌克兰语
            return "ru"
        elif _language.find("es", 0)==0:  # 西班牙语
            return "es"
        elif _language.find("vi", 0)==0:  # 越语
            return "vi"
        else:  # 默认英文
            return "en"
    # 系统语言
    def sys_language(_lang=""):
        if len(_lang) >= 2:
            return _lang
        else:
            return locale.getlocale()[0]
    #
    lang_index = make_lang_index(sys_language(lang))
    #
    if lang_dict.get(key):
        if lang_dict[key].get(lang_index):
            return lang_dict[key][lang_index]
        else:
            if len(lang_dict[key]["en"])>=1:
                return lang_dict[key]["en"]
            else:
                return lang_dict["-null-"]["en1"]
    else:
        if lang_dict["-null-"].get(lang_index):
            return lang_dict["-null-"][lang_index]
        else:
            return lang_dict["-null-"]["en2"]

# 翻译表
lang_dict = {
"test": { # 示例
    "zh": "测试",
    "en": "Test",
    "jp": "",
    "fr": "",
    "de": "",
    "ru": "",
    "es": "",
    "vi": "",
},
"-null-":{ # 必须
    "zh": " -空- ",
    "en": " -Null- ",
    "en1": " -Null-1- ",
    "en2": " -Null-2- ",
},
#
"show_window": {
    "zh": "显示视窗",
    "en": "Show Window",
},
"exit_app": {
    "zh": "退出程序",
    "en": "Exit App",
},
"about_app": {
    "zh": "关于程序",
    "en": "About App",
},

#
}