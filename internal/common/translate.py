import locale

# 获取翻译
def get_translate(key="-null-", lang=""):
    # 将语言转换成可用的数组索引标记
    def make_lang_index(language):
        _language = language.lower()
        if "zh" in _language:  # 简体中文（包含繁体）
            return "zh",
        elif "en" in _language:  # 英文
            return "en"
        elif "jp" in _language:  # 日文
            return "jp"
        elif "fr" in _language:  # 法语
            return "fr"
        elif "de" in _language:  # 德语
            return "de"
        elif "ru" in _language:  # 俄语或乌克兰语
            return "ru"
        elif "es" in _language:  # 西班牙语
            return "es"
        elif "vi" in _language:  # 越语
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
    has_key = lang_dict.get(key)
    has_lang = lang_dict.get(key).get(lang_index)
    #
    if has_key and has_lang:
        txt = lang_dict[key][lang_index]
        if len(txt)>0:
            return lang_dict[key][lang_index]
        else: # 为空就默认显示英文
            return " -" + key + "📍" + lang_index + "- "
    else: # 还没有定义key
        return lang_dict["-null-"]["en"]

# 翻译表
lang_dict = {
"test": {
    "zh": "测试",
    "en": "Test",
    "jp": "",
    "fr": "",
    "de": "",
    "ru": "",
    "es": "",
    "vi": "",
},
"-null-":{
    "zh": " -空- ",
    "en": " -Null- ",
    "jp": " -Null- ",
    "fr": " -Null- ",
    "de": " -Null- ",
    "ru": " -Null- ",
    "es": " -Null- ",
    "vi": " -Null- ",
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