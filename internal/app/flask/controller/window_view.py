from internal.common.main_dirpath import mian_virtual_dirpath
import os

# 视图view
def window_view(rand_id, filename):
    #
    def read_html(the_file):
        content = ""
        if os.path.exists(the_file):  # 存在文件或文件夹
            if os.path.isfile(the_file):  # 是文件
                with open(the_file, "r", encoding="utf-8") as file:
                    content = file.read()
                    pass
        return content
    #
    view_url = "http://127.0.0.1:9100/view"
    file_path = mian_virtual_dirpath("frontend") + "/view/"+filename
    #
    html = read_html(file_path)
    js = f'''
    <script>const view_url = "{view_url}";</script>
    '''
    if len(html)==0:
        html = '''
        <html lang="zh">
        <head>
            <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0" />
            <title>Default Window</title>
        </head>
        <body style="background-color: transparent;">
            <h2>当前使用了空模板。</h2>
            <img src="http://127.0.0.1:9100/file/test.png" width="192" alt=""/>
        </body>
        </html>
        '''
        pass

    return js+html