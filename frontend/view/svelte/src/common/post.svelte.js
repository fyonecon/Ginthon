// POST请求专用
// state=404代表接口无效，0代表接口有效但无数据。

/**
 * POST
 * @param {string} api_url 接口
 * @param {object} body_dict 数据data字典
 * @param {number} timeout_s 超时
 * @returns {Promise<object>} 返回固定格式
 */
const FetchPOST = function (api_url, body_dict = {}, timeout_s = 20) {
    let state = 0;
    let msg = "";
    let content = {};

    return new Promise(async (resolve) => {
        // 创建 AbortController 用于超时控制
        const controller = new AbortController();

        // 设置超时（秒转换为毫秒）
        const timeoutMs = (timeout_s <= 0 ? 20 : timeout_s) * 1000;
        const timeoutId = setTimeout(() => {
            controller.abort();
            console.warn(`FetchPOST请求超时: ${api_url}, 超时时间: ${timeout_s}秒`);
        }, timeoutMs);

        try {
            // 准备请求体
            let requestBody;
            if (typeof body_dict === 'string') {
                requestBody = body_dict;
            } else if (body_dict instanceof FormData) {
                // 如果是 FormData，不要设置 Content-Type，浏览器会自动设置
                requestBody = body_dict;
            } else {
                requestBody = JSON.stringify(body_dict);
            }

            // 准备 headers
            const headers = {};
            if (!(body_dict instanceof FormData)) {
                headers['Content-Type'] = 'application/json';
            }
            headers['Accept'] = 'application/json, text/plain, */*';

            const response = await fetch(api_url, {
                method: 'POST',
                headers: headers,
                body: requestBody,
                mode: 'cors', // cors, no-cors, same-origin。GET请使用no-cors，POST请使用cors。
                cache: 'no-cache', // default, no-cache, reload, force-cache, only-if-cached
                credentials: 'omit', // 控制是否发送 cookies
                signal: controller.signal, // 关键：绑定中断信号
            });

            // 清除超时定时器
            clearTimeout(timeoutId);

            if (!response.ok) {
                console.warn("response.ok=", response, response.ok);

                state = 0;
                msg = `POST Status Error.`;
                content = {
                    "api_url": api_url,
                    "status": response.status,
                    "statusText": response.statusText,
                    "error": "POST接口访问成功，但接口返回状态错误"
                };

                resolve({
                    state: state,
                    msg: msg,
                    content: content,
                });
            }else{
                // 根据 Content-Type 解析响应
                const contentType = response.headers.get('content-type') || '';
                let result;

                try {
                    if (contentType.includes('application/json')) {
                        result = await response.json();
                    } else if (contentType.includes('text/')) {
                        result = await response.text();
                    } else if (contentType.includes('form-data')) {
                        result = await response.formData();
                    } else if (contentType.includes('image/') || contentType.includes('application/octet-stream')) {
                        result = await response.blob();
                    } else {
                        result = await response.text();
                    }
                } catch (parseError) {
                    resolve({
                        state: 0,
                        msg: "POST Parse Error.",
                        content: {
                            "api_url": api_url,
                            "error": "响应解析失败",
                            "parseError": parseError.message
                        }
                    });
                    return;
                }

                // 成功返回数据
                resolve(result);
            }
        } catch (error) {
            // 清除超时定时器
            clearTimeout(timeoutId);

            // 判断错误类型
            if (error.name === 'AbortError') {
                state = 404;
                msg = "POST Timeout.";
                content = {
                    "api_url": api_url,
                    "error": `请求超时（${timeout_s}秒）`,
                    "error_type": "AbortError"
                };
            } else {
                state = 404;
                msg = "POST Broken.";
                content = {
                    "api_url": api_url,
                    "error": error.message || "未知错误",
                    "error_type": error.name || "UnknownError"
                };
            }

            resolve({
                state: state,
                msg: msg,
                content: content,
            });
        }
    });
}

export default FetchPOST;