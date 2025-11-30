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
    view_html = view_url + "/" + filename
    file_path = mian_virtual_dirpath("frontend") + "/view/"+filename
    #
    html = read_html(file_path)
    js = f'''
    <script>const view_url = "{view_url}";const view_html="{view_html}"; const view_filename = "{filename}";</script>
    '''
    if len(html)==0:
        html = '''
        <html lang="zh">
        <head>
            <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=0" />
            <title>Default Window</title>
            <style>
                .hide{
                    display: none !important;
                }
                .click{
                    cursor: pointer;
                }
                .click:active{
                    opacity: 0.6;
                }
                .select-none{
                    -moz-user-select: none;-webkit-user-select: none;-ms-user-select: none;
                    user-select: none;
                }
                .break{
                    overflow: hidden;
                    word-wrap: break-word;
                    overflow-wrap: break-word;
                }
            </style>
        </head>
        <body style="background-color: transparent;">
            <br/>
            <h2 style="text-align: center; " class="select-none">当前使用了空模板。</h2>
            <div style="text-align: center;">
                <p id="info" class="break"></p>
                <p class="select-none"><img src="http://127.0.0.1:9100/file/test.png" width="192" alt=""/></p>
            </div>
            <script>
            function show_info(_view_html) {
                let info = [
                    window.location.host, 
                    !!window.localStorage, 
                    !!window.indexedDB, 
                    navigator.webdriver, 
                    navigator.languages, 
                    window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light", "✅", 
                    window.navigator.userAgent,
                    view_url,
                    view_html,
                ]; 
                console.log(info);
                document.getElementById("info").innerHTML = view_filename+" 文件不存在。"; 
            }
            show_info(view_html);
            </script>
        </body>
        </html>
        '''
        pass

    return js+html