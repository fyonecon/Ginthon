
// POST请求专用
const FetchPOST = function (api_url, body_dict) {
    let state = 0;
    let msg = "";
    let content = {};
    return new Promise(async (resolve) => {
        try {
            const response = await fetch(api_url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: typeof body_dict === 'string' ? body_dict :JSON.stringify(body_dict),
                mode: 'cors', // cors, no-cors, same-origin
                cache: 'no-cache', // default, no-cache, reload, force-cache, only-if-cached
                timeout: 12, // 自定义超时 s
            });
            if (!response.ok) {
                state = 0;
                msg = "API Status Error.";
                content = {
                    "api_url": api_url,
                    "status": response.status,
                    "error": "接口返回状态错误"
                };
                //
                resolve({
                    state: state,
                    msg: msg,
                    content: content,
                });
            } else {
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
                //
                resolve(result);
            }
        } catch (error) {
            // console.error('接口不通:', error);
            state = 0;
            msg = "API filed.";
            content = {
                "api_url": api_url,
                "error": error
            };
            //
            resolve({
                state: state,
                msg: msg,
                content: content,
            });
        }
    });
}

export default FetchPOST;