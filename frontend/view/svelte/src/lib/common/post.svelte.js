
let formData = {
    username: '',
    email: '',
    password: ''
};

let responseMessage = '';
let isLoading = false;

// 基本POST请求
async function handleSubmit() {
    isLoading = true;
    responseMessage = '';

    try {
        const response = await fetch('https://api.example.com/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // 如果需要认证
                // 'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        responseMessage = `注册成功！用户ID: ${data.userId}`;

        // 重置表单
        formData = { username: '', email: '', password: '' };

    } catch (error) {
        console.error('Error:', error);
        responseMessage = `错误: ${error.message}`;
    } finally {
        isLoading = false;
    }
}

//
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
                // throw new Error(`HTTP error! status: ${response.status}`);
                state = 0;
                msg = "接口错误";
                content = {
                    "error": response.status
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
            state = 0;
            msg = "接口错误";
            content = {
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