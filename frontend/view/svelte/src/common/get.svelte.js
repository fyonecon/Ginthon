// GET方法
// 注意参数不要过长
// state=404代表接口无效，0代表接口有效但无数据。

/**
 * GET
 * @param {string} api_url 接口
 * @param {object} body_dict 数据data字典
 * @param {number} timeout_s 超时
 * @returns {Promise<object>} 返回固定格式
 */
const FetchGET = function (api_url, body_dict = {}, timeout_s = 10) {
    let state = 0;
    let msg = "";
    let content = {};

    // 构建查询参数
    const params = new URLSearchParams(body_dict);
    if (params.toString()) {
        api_url = api_url + "?" + params.toString();
    }

    return new Promise(async (resolve) => {
        // 创建 AbortController 用于超时控制
        const controller = new AbortController();

        // 设置超时（秒转换为毫秒）
        const timeoutMs = (timeout_s <= 0 ? 10 : timeout_s) * 1000;
        const timeoutId = setTimeout(() => {
            controller.abort();
        }, timeoutMs);

        try {
            const response = await fetch(api_url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                mode: 'no-cors', // cors, no-cors, same-origin。GET请使用no-cors，POST请使用cors。
                cache: 'no-cache', // default, no-cache, reload, force-cache, only-if-cached
                signal: controller.signal, // 关键：绑定中断信号
            });

            // 清除超时定时器
            clearTimeout(timeoutId);

            if (!response.ok) {
                console.warn("response.ok=", response, response.ok);

                state = 0;
                msg = "GET Status Error.";
                content = {
                    "api_url": api_url,
                    "status": response.status,
                    "statusText": response.statusText,
                    "error": "GET接口访问成功，但接口返回状态错误"
                };

                resolve({
                    state: state,
                    msg: msg,
                    content: content,
                });
            }else{
                // 根据 Content-Type 解析响应
                const contentType = response.headers.get('content-type');
                let result;

                if (contentType && contentType.includes('application/json')) {
                    result = await response.json();
                } else if (contentType && contentType.includes('text/')) {
                    result = await response.text();
                } else if (contentType && contentType.includes('form-data')) {
                    result = await response.formData();
                } else if (contentType && contentType.includes('blob')) {
                    result = await response.blob();
                } else {
                    result = await response.text();
                }

                // 成功返回数据
                resolve(result);
            }
        } catch (error) {
            // 清除超时定时器
            clearTimeout(timeoutId);

            // 判断是否是超时错误
            if (error.name === 'AbortError') {
                state = 404;
                msg = "GET Timeout Error.";
                content = {
                    "api_url": api_url,
                    "error": `请求超时（${timeout_s}秒）`,
                    "error_type": "AbortError"
                };
            } else {
                // 其他错误
                state = 404;
                msg = "GET Broken.";
                content = {
                    "api_url": api_url,
                    "error": error.message || error,
                    "error_type": error.name || "NetworkError"
                };
            }

            resolve({
                state: state,
                msg: msg,
                content: content,
            });
        }
    });
};

export default FetchGET;