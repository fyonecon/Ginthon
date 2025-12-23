from internal.common.func import cache_path
from internal.common.kits.local_database import local_database_get_data


#
def get_play_audio_list():
    state = 1
    msg = "完成"

    list = [
        {
            "filename": "青花瓷",
            "href": "http://192.168.101.198:9550/read_file?show_path=%E9%9F%B3%E4%B9%90%E7%A6%BB%E7%BA%BF4%2F%E5%91%A8%E6%9D%B0%E4%BC%A6%20-%20%E9%9D%92%E8%8A%B1%E7%93%B7.flac&token=4c30f4f1a3f23745bca4e053ec8384c6&url_timeout=8L6F4ORBc3j6fsaRhs9t47ZDPYJxC_@-V_@-1ediHGGBNOFbjPdQqCjunBvlG3Td6eh1sC1OLwq_@-FdUvU0bq9dPBLNU7jhKWEOW9JizupJI9nAj2YqCtEo9ICSbeYXpSiTb/7ia2qqq9jlg_@_&ap=preview ",
            "cover": "",
        },
        {
            "filename": "断了的弦",
            "href": "http://192.168.101.198:9550/read_file?show_path=%E9%9F%B3%E4%B9%90%E7%A6%BB%E7%BA%BF4%2F%E6%96%AD%E4%BA%86%E7%9A%84%E5%BC%A6.flac&token=4c30f4f1a3f23745bca4e053ec8384c6&url_timeout=8L6F4ORBc3j6fsaRhs9t47ZDPYJxC_@-V_@-1ediHGGBNOFbjPdQqCjunBvlG3Td6eh1sC1OLwq_@-FdUvU0bq9dPBLNU7jhKWEOW9JizupJI9nAj2YqCtEo9ICSbeYXpSiTb/7ia2qqq9jlg_@_&ap=preview  ",
            "cover": "",
        },
        {
            "filename": "此生不换DJ",
            "href": "http://192.168.101.198:9550/read_file?show_path=%E9%9F%B3%E4%B9%90%E7%A6%BB%E7%BA%BF4%2F%E6%AD%A4%E7%94%9F%E4%B8%8D%E6%8D%A2(DJ%E7%89%88).m4a&token=4c30f4f1a3f23745bca4e053ec8384c6&url_timeout=8L6F4ORBc3j6fsaRhs9t47ZDPYJxC_@-V_@-1ediHGGBNOFbjPdQqCjunBvlG3Td6eh1sC1OLwq_@-FdUvU0bq9dPBLNU7jhKWEOW9JizupJI9nAj2YqCtEo9ICSbeYXpSiTb/7ia2qqq9jlg_@_&ap=preview  ",
            "cover": "",
        },
        {
            "filename": "花海",
            "href": "http://192.168.101.198:9550/read_file?show_path=%E9%9F%B3%E4%B9%90%E7%A6%BB%E7%BA%BF4%2F%E8%8A%B1%E6%B5%B7.flac&token=4c30f4f1a3f23745bca4e053ec8384c6&url_timeout=8L6F4ORBc3j6fsaRhs9t47ZDPYJxC_@-V_@-1ediHGGBNOFbjPdQqCjunBvlG3Td6eh1sC1OLwq_@-FdUvU0bq9dPBLNU7jhKWEOW9JizupJI9nAj2YqCtEo9ICSbeYXpSiTb/7ia2qqq9jlg_@_&ap=preview  ",
            "cover": "",
        },
    ]

    dir_key = "play_audio_dir-1"
    _value, _state = local_database_get_data(dir_key)

    #
    return {
        "state": state,
        "msg": msg,
        "content": {
            "list_name": "歌单",
            "count": len(list),
            "list": [],
            "dir": _value,
            "_state": _state,
        },
    }