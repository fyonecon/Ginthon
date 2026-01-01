
class request_data:

    # 获取完整的请求链接
    @staticmethod
    def full_href(request):
        return request.url

    # flask万能api取值方法
    @staticmethod
    def input(request, key: str = ""):
        default = None  # 值不存在时的默认值

        if not key:
            # 如果没有指定key，返回整个参数字典
            return request_data.all_params(request)

        # 统一转换key为字符串（避免数字key问题）
        key = str(key)

        # 根据请求方法获取参数
        if request.method == "GET":
            return request.args.get(key, default)

        elif request.method == "POST":
            # 尝试从JSON获取
            if request.is_json:
                try:
                    data = request.get_json(silent=True, force=False)
                    if data and key in data:
                        return data[key]
                except:
                    pass

            # 尝试从form-data获取
            if request.form and key in request.form:
                return request.form[key]

            # 尝试从files获取
            if request.files and key in request.files:
                return request.files[key]

            # 尝试从args获取（POST请求也可能有查询参数）
            if request.args and key in request.args:
                return request.args.get(key, default)

            return default

        # 支持PUT、PATCH、DELETE等其他方法
        elif request.method in ["PUT", "PATCH", "DELETE"]:
            # 尝试从JSON获取
            if request.is_json:
                try:
                    data = request.get_json(silent=True, force=False)
                    if data and key in data:
                        return data[key]
                except:
                    pass

            # 尝试从form-data获取
            if request.form and key in request.form:
                return request.form[key]

            # 尝试从args获取
            if request.args and key in request.args:
                return request.args.get(key, default)

            return default

        return default

    # 获取所有请求参数
    @staticmethod
    def all_params(request):
        """获取所有请求参数"""
        params = {}

        # 获取查询参数
        params.update(request.args.to_dict())

        # 获取表单参数
        params.update(request.form.to_dict())

        # 获取JSON参数
        if request.is_json:
            try:
                data = request.get_json(silent=True, force=False)
                if data:
                    params.update(data)
            except:
                pass

        # 获取文件参数（只记录文件名）
        if request.files:
            for file_key, file_obj in request.files.items():
                params[file_key] = file_obj.filename

        return params

    #
    pass
