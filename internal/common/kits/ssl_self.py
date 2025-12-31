# ssl证书
import os
import ssl

from OpenSSL import crypto
from internal.common.func import data_path
from internal.config import get_config

# 证书保存地址
_data_dirpath = data_path() + "/" + get_config("sys", "data_path_main_dir") # 结尾无/

# 生成新的ssl
def create_self_signed_cert(host="0.0.0.0", cert_file=_data_dirpath + "/flask_ssl" + "/cert.pem", key_file=_data_dirpath + "/flask_ssl" +"/key.pem"):
    """创建自签名证书"""
    # 创建密钥对
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)

    # 创建证书
    cert = crypto.X509()
    cert.get_subject().C = "CN"
    cert.get_subject().ST = "Piking"
    cert.get_subject().L = "Piking"
    cert.get_subject().O = "Gthon Open Source"
    cert.get_subject().emailAddress = "https://github.com/fyonecon/Ginthon"
    cert.get_subject().CN = host  # 使用 localhost、127.0.0.1、0.0.0.0、www.xxx.com
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(9 * 365 * 24 * 60 * 60)  # 9年有效期
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')

    # 保存证书和密钥
    with open(cert_file, "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    with open(key_file, "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

    print(f"证书已生成: {cert_file}, {key_file}")
    return cert_file, key_file

# 读取ssl上下文
def read_ssl_context(host="0.0.0.0"):
    # 检查证书文件是否存在
    ssl_cert = _data_dirpath + "/flask_ssl" + "/cert.pem"
    ssl_key = _data_dirpath + "/flask_ssl" + "/key.pem"
    if not os.path.exists(ssl_cert) or not os.path.exists(ssl_key):
        cert, key = create_self_signed_cert(host, ssl_cert, ssl_key)
        pass
    else:
        cert = ssl_cert
        key = ssl_key
        pass
    # 验证证书文件
    try:
        # 尝试加载证书和密钥
        with open(ssl_cert, 'r') as f:
            cert_content = f.read()
            pass
        with open(ssl_key, 'r') as f:
            key_content = f.read()
            pass
        # 验证格式
        if "-----BEGIN CERTIFICATE-----" not in cert_content:
            cert, key = create_self_signed_cert(host, ssl_cert, ssl_key)
            pass
        if "-----BEGIN PRIVATE KEY-----" not in key_content:
            cert, key = create_self_signed_cert(host, ssl_cert, ssl_key)
            pass
    except Exception as e:
        print(f"读取证书文件时出错: {e}")
        cert, key = create_self_signed_cert(host, ssl_cert, ssl_key)

    # 使用 SSL 上下文
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert, key)

    return context