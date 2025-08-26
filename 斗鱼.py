import re
import requests
import json
import time
import os
from tqdm import tqdm
from multiprocessing import Pool, Manager
import os
import re
import time
import requests
import execjs
import m3u8
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from tqdm import tqdm
# 初始化锁
lock = threading.Lock()
jsonl_lock = threading.Lock()


headers = {
    'cookie': 'dy_did=7e150955b060f8744973ca9f00071701; _ga=GA1.1.1471502649.1721787407; _ga_5JKQ7DTEXC=GS1.1.1721821049.2.0.1721821049.60.0.1716336261; _clck=4ponib%7C2%7Cfnx%7C0%7C1666; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1721787406,1722424045; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1722424045; HMACCOUNT=EAD429051243B61E; post-csrfToken=dcf8132ebc744a36566ecf; msg_auth=e69827f6763d32238827791dfd081104572e50f8; msg_uid=Mn7MEz2pQX7j; acf_jwt_token=eyJhbGciOiJtZDUiLCJ0eXAiOiJKV1QifQ.eyJjdCI6MCwiaWF0IjoxNzIyNDI0MDgwLCJhdWQiOlsiZHkiXSwibHRraWQiOjc0NDk4NjUzLCJiaXoiOjkzLCJ1aWQiOjUwMDc2NzQyNCwiZXhwIjoxNzIzMDI4ODgwLCJzdWIiOiJzdCIsImtleSI6ImR5LWp3dC1tZDUiLCJzdGsiOiI5MWI2ZjZhOTAzYTg1NmI0In0.NDYyNTU4M2NiZTkxOGYwZTMzZjlhYTc5NTIwYmFjOTM; acf_dmjwt_token=eyJhbGciOiJtZDUiLCJ0eXAiOiJKV1QifQ.eyJjdCI6MCwiaWF0IjoxNzIyNDI0MDgwLCJhdWQiOlsiZG0iXSwibHRraWQiOjc0NDk4NjUzLCJiaXoiOjkzLCJ1aWQiOjUwMDc2NzQyNCwiZXhwIjoxNzIzMDI4ODgwLCJzdWIiOiJzdCIsImtleSI6ImR5LWp3dC1tZDUiLCJzdGsiOiI5MWI2ZjZhOTAzYTg1NmI0In0.Nzc4MTlkZWJmN2Y4ODE1MWVlMDAyNzA4YzAyYjEzNTM; _ga_7RMFJRR7D2=GS1.1.1722421526.5.1.1722424121.26.0.1014220467; _clsk=1w4eh5s%7C1722424122325%7C13%7C1%7Cv.clarity.ms%2Fcollect; msgUnread=waiting',
    'origin': 'https://v.douyu.com',
    'referer': f'https://yuba.douyu.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}


def extract_vid_and_seo_title(script_text):
    """
    从 script_text 中提取 vid 和 seo_title
    """
    vid_pattern = r'"vid":"(.*?)"'
    seo_title_pattern = r'seo_title:"(.*?)"'
    print(script_text)
    vid_match = re.search(vid_pattern, script_text)
    seo_title_match = re.search(seo_title_pattern, script_text)

    vid = vid_match.group(1) if vid_match else None
    seo_title = seo_title_match.group(1) if seo_title_match else None
    print(vid, seo_title)
    return vid, seo_title

def get_point_id(vid):
    point_url = f"https://v.douyu.com/wgapi/vod/front/video/secondary/info?hid={vid}"
    response = requests.get(point_url, headers=headers)
    point_id = response.json()['data']['vid']
    print(point_id)
    return point_id

def get_sign(vid, point_id, did, tt):
    main_url = f'https://v.douyu.com/show/{vid}'
    html_data = requests.get(main_url, headers=headers).text
    title = re.findall('<title>(.*?)</title>', html_data)[0]
    script_data = re.findall(r'<script>(.*?)</script>', html_data, re.DOTALL)
    relevant_script = None
    for script in script_data:
        if "var vdwdae325w_64we" in script:
            relevant_script = script
            break

    if relevant_script is None:
        raise ValueError("未找到包含 var vdwdae325w_64we 的脚本")
    js_code = f"""
const CryptoJS = require('crypto-js');

{relevant_script}

console.log(ub98484234('{point_id}', '{did}', '{tt}'));
"""
    js_filename = f'D:\\2024work\\zhou\\1\\{point_id}.js'
    with open(js_filename, 'w') as file:
        file.write(js_code)
    node_script_path = f'D:\\2024work\\zhou\\1\\{point_id}.js'
    run_command = [r'C:\Program Files\nodejs\node.exe', node_script_path]
    result = subprocess.run(run_command, capture_output=True, text=True)
    # Node.js结果
    if result.returncode == 0:
        print("Node.js script executed successfully.")
        print(result.stdout)
    else:
        print("Error executing Node.js script:")
        print(result.stderr)
    # const CryptoJS = require('crypto-js');
    # var vdwdae325w_64we = "220320240801";var i075b25e2d6ea3c70f8a=[0x9aeace88,0x76a33721,0xb2e4c727,0xdb1d094b,0x2ac44f9,0x6a1c7934,0xf2f684bc,0xcb6fc256,0xd6c3b6e7,0x537330c7,0x40e8b854,0xe1772d92,0x2f18fb36,0xa8cf960f,0x7a18da7d,0x3bd6090b,0x76e5ffc7,0xd60e2c1b,0x21c2d0a5,0xb79a011e,0xfa9c76bf,0x7a153440,0xfd1e9182,0xf50036a3,0x831db5ac,0xfcbfde1b,0xbd7af11a,0xe366d2d4,0x87a96546,0x395cac0a,0x46344985,0xadb91dca,0x9b856800,0xbe4b9515,0x3444aeb7,0xf87cb89c,0xa5a37399,0xfb66d716,0xbcef2736,0x2ad2e85,0xa27f3068,0xd3017620,0xd7476240,0xb99eaf0c,0x33fc2c75,0x51b1f41a,0xfe482fb4,0x31bc4897,0xe9a10b29,0xb10f1b78,0xd818e334,0x5241f3fe,0xd34da9d3,0x6c7b55c9,0x3626d82c,0xd2e219b5,0x4a9de55c,0x76f435af,0x8865cb73,0xe96399a7,0x6ee9b3f9,0x98d017d4,0x62a85a72,0xbec85801,0xb670d7bd,0x5d1d4f81,0x6b7aea12,0x7839d230,0xc5444c47,0xcc9eab8,0x364de543,0xa1ccff81,0x1855a3dc,0x94269dd0,0x2f9f8b3d,0x5b29a4a3,0x4580ef60,0xef2c00b3,0x5d151f77,0xa375e6ff,0xf54c58a2,0x2cbc5b08,0xb88a98fd,0xe00da25,0x73b41fc6,0x1a9b1f5e,0x42d3ccdb,0xb127a2ea,0xc7faf76,0x2331ed25,0xceb376bf,0x187d9973,0x4f80739e,0x18c237a0,0xcc0f7c68,0x1c61af5c,0xbf22753f,0x64abba93,0x696cb136,0x2874b119,0x54ba314,0x14709321,0xbce0f476,0x6b8dc262,0xea2f1fed,0xa1cff02b,0x328d2ec2,0x347f786,0xb417b9cc,0x174b6034,0x722c6d1f,0x9579c810,0x258a322b,0xfaaab99f,0xda5b3cab,0xbd1005b8,0x1d381171,0xb9af4ffc,0xace47114,0x1ddf9841,0x40b0de45,0x98ed454b,0x79c75a29,0xc6754d5e,0x46197ef7,0x577cc276,0x1add07cc,0x584241f,0x928e2510,0xeada7b82,0xb54cf185,0x6e90472,0x9ccf19b5,0xd3d54deb,0xba1f6991,0x94d9c5f4,0x630dd2ac,0xa53fada9,0xcf56b03f,0x6512da08,0x634093e3,0x9582cb04,0xfaa00c8f,0x87463129,0xb4898926,0xbc4f00e4,0x12378d50,0xf130de88,0x1e4f63b0,0x3c64b01,0xb9edd3f7,0x74a92696,0x67616298,0xd979125,0x41944b34,0x71dfd434,0xb90eac3d,0x2f97f2ef,0xcbb6c918,0xad37b8ac,0x643d96d4,0xf59095c7,0x3e6ec4d9,0xb28a088a,0xd46ea471,0x439a2435,0x2e331156,0xe92b067b,0x3d65d482,0x9a7139cc,0x8ca462c4,0xccf1b36c,0x718370e,0xce9d163c,0xa9098077,0x4ac5f12d,0xe68c848b,0x8e755f93,0x9a002964,0x9c5edc3c,0xc7e7e3af,0xeafdbc6d,0xf87e392e,0x641d650a,0x35e4c5a6,0xe005ad57,0xa21ac0d2,0xb5acb267,0x53d967c4,0x6dcb28d8,0xf52a0909,0x6ef67bbc,0x74e0a40d,0xc61c07de,0x8bb216a8,0x3f7598f1,0x479182c9,0x7b929742,0xfdf32057,0x5d26a5ea,0xd1643437,0x6dcc4640,0x8301b2ea,0xdf4b6b02,0x184b1816,0xc4c2d588,0x9374c691,0xa853649,0x86aa9f02,0x482676f6,0x944e764f,0x7436c116,0xa1b94ae9,0x523d89b8,0x6c1e0b79,0xd79e94b6,0x46a31a01,0x84da2d5d,0xeb023865,0xf9924414,0xf513f2a4,0x2666bf7,0x60eb8a78,0xefc0b5c,0xdacfe175,0xaaa88238,0x18de1605,0x6a751ce,0xdb4784bb,0x84f59dc8,0xcc9a2b31,0xc51b2666,0xd32274c0,0xf81f230d,0x73d13684,0xc63d6fd3,0xc8a9ba63,0x257f4f90,0xc60a0b9c,0x7ac60401,0x1e879141,0x571df16a,0x113a0362,0x739b1342,0x6e854c14,0x1506a6,0x3a55d17d,0xe14e2cfe,0x6942f70c,0x69551d74,0x41fd877,0x27267271,0xabfb781c,0x76d4a821,0x662bb790,0xa33b9b72,0x7e4cb426,0x1df3d7fc,0xf5208bbf,0x91cd76c9,0xb75e487,0xf65db3fd,0x6dbd01c0,0xb13e94d,0xf4409f7,0xe3c14ed9,0x2ecca9ff,0xa2490666,0x7f420518,0x8ec2858,0xd8d084a0,0xdfe6f78,0x75e97ef3,0x870a27b5,0x3ec37fdc,0x5ab7c369,0x897e4c4,0x18c2c643,0x6a7db0d0,0xb398561d,0x3269da2f,0x540e30a1,0x725773a6,0x7a4f2217,0x2b016604,0x3d8a2e0d,0x69872cfd,0xc7c6fa1a,0x767f6994,0xb9f3d038,0x8995b3a1,0x79288815,0x7b1fa06c,0x520504d6,0xd62e6f36,0x888e5fa2,0xc7782c50,0xb8bc065a,0x5f4266b9,0x11926e67,0x4ef30653,0xc3c49dec,0x7c66a161,0x68e3d5d,0x85c3c194,0x37a32430,0x1739290d,0x5c0acc7b,0xc21694e2,0x4a0b2233,0xa05f6106,0x8b2f09ce,0x4a5f7276,0xab5c700b,0x3af16857,0x43c49b98,0xd8412b70,0x7a1d7da7,0x6d6c08b1,0x1711ff18,0x369359e8,0xaadf6965,0x2ef69cf2,0x24595332,0x12b7606d,0x7de3bce4,0x93aaf24e,0x9ac6fd0e,0xc1919831,0xd431eb57,0x5cb338d3,0x55d26375,0xc34f7dfa,0x9d7551b4,0x491dc9ff,0x979360d6,0xbf703925,0xaa458ba1,0x9ee764ed,0x1134921a,0x2d273c57,0xb47d9032,0x2be58c77,0x6fd3ad74,0x77fe6318,0xabbae905,0x7d7b3085,0x6cd698ef,0x75848cc6,0x38d1a23b,0x6b4fb64b,0xb1e96944,0xd112c742,0x35ec33e0,0xaff77785,0xca0b1ead,0x81fc9bca,0x20b4761d,0x39c4e5d7,0x3200af8a,0x63f70a27,0xbfb8c22d,0xe634a885,0x459b273f,0x779b8595,0x6a8007ff,0x510ef8be,0x1fda9659,0x9630ce79,0xe0861ea1,0x142c950f,0xd13e0d8d,0xb2f4426f,0xd3219d30,0x86cb5850,0x5f54f5d8,0x2d398d32,0x640f2e9e,0xe738e2cd,0xc8835712,0x9a40c53e,0x56241a13,0x887f3348,0xc8b964c,0xb972b878,0xb370566b,0xdf9fe262,0xc239a673,0x9b2f3a5b,0x1ea9d39b,0xf98d630,0xeb59398,0x2278fe91,0x114f35b9];function ub98484234(i075b25e2d6ea3c70f8a0,i075b25e2d6ea3c70f8a1,i075b25e2d6ea3c70f8a2){var rk=[16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12,10,16,18,33,24,41,17,14,12];var k2=[0x5a6ceb35,0x6ff85cf9];var lk=[0x5a6ceb35,0x6ff85cf9];var v = i075b25e2d6ea3c70f8a.slice(0);var k=[0xbd7375f8,0xdfcfb71b,0x3f7fed8e,0xf7bb9631];for(var O=0;O<394;O++){v[O]^=0x74c037e;}v[1]=(v[1]>>>(lk[1]%16))|(v[1]<<(32-(lk[1]%16)));v[0]=(v[0]<<(lk[0]%16))|(v[0]>>>(32-(lk[0]%16)));v[3]=(v[3]>>>(lk[1]%16))|(v[3]<<(32-(lk[1]%16)));v[2]^=lk[0];v[5]-=lk[1];v[4]+=lk[0];v[7]=(v[7]>>>(lk[1]%16))|(v[7]<<(32-(lk[1]%16)));v[6]=(v[6]>>>(lk[0]%16))|(v[6]<<(32-(lk[0]%16)));v[9]-=lk[1];v[8]+=lk[0];v[11]^=lk[1];v[10]-=lk[0];v[13]=(v[13]>>>(lk[1]%16))|(v[13]<<(32-(lk[1]%16)));v[12]-=lk[0];v[15]+=lk[1];v[14]=(v[14]>>>(lk[0]%16))|(v[14]<<(32-(lk[0]%16)));v[17]-=lk[1];v[16]-=lk[0];v[19]=(v[19]>>>(lk[1]%16))|(v[19]<<(32-(lk[1]%16)));v[18]=(v[18]<<(lk[0]%16))|(v[18]>>>(32-(lk[0]%16)));v[21]=(v[21]>>>(lk[1]%16))|(v[21]<<(32-(lk[1]%16)));v[20]^=lk[0];v[23]-=lk[1];v[22]+=lk[0];v[25]=(v[25]>>>(lk[1]%16))|(v[25]<<(32-(lk[1]%16)));v[24]=(v[24]>>>(lk[0]%16))|(v[24]<<(32-(lk[0]%16)));v[27]-=lk[1];v[26]+=lk[0];v[29]^=lk[1];v[28]-=lk[0];v[31]=(v[31]>>>(lk[1]%16))|(v[31]<<(32-(lk[1]%16)));v[30]-=lk[0];v[33]+=lk[1];v[32]=(v[32]>>>(lk[0]%16))|(v[32]<<(32-(lk[0]%16)));v[35]-=lk[1];v[34]-=lk[0];v[37]=(v[37]>>>(lk[1]%16))|(v[37]<<(32-(lk[1]%16)));v[36]=(v[36]<<(lk[0]%16))|(v[36]>>>(32-(lk[0]%16)));v[39]=(v[39]>>>(lk[1]%16))|(v[39]<<(32-(lk[1]%16)));v[38]^=lk[0];v[41]-=lk[1];v[40]+=lk[0];v[43]=(v[43]>>>(lk[1]%16))|(v[43]<<(32-(lk[1]%16)));v[42]=(v[42]>>>(lk[0]%16))|(v[42]<<(32-(lk[0]%16)));v[45]-=lk[1];v[44]+=lk[0];v[47]^=lk[1];v[46]-=lk[0];v[49]=(v[49]>>>(lk[1]%16))|(v[49]<<(32-(lk[1]%16)));v[48]-=lk[0];v[51]+=lk[1];v[50]=(v[50]>>>(lk[0]%16))|(v[50]<<(32-(lk[0]%16)));v[53]-=lk[1];v[52]-=lk[0];v[55]=(v[55]>>>(lk[1]%16))|(v[55]<<(32-(lk[1]%16)));v[54]=(v[54]<<(lk[0]%16))|(v[54]>>>(32-(lk[0]%16)));v[57]=(v[57]>>>(lk[1]%16))|(v[57]<<(32-(lk[1]%16)));v[56]^=lk[0];v[59]-=lk[1];v[58]+=lk[0];v[61]=(v[61]>>>(lk[1]%16))|(v[61]<<(32-(lk[1]%16)));v[60]=(v[60]>>>(lk[0]%16))|(v[60]<<(32-(lk[0]%16)));v[63]-=lk[1];v[62]+=lk[0];v[65]^=lk[1];v[64]-=lk[0];v[67]=(v[67]>>>(lk[1]%16))|(v[67]<<(32-(lk[1]%16)));v[66]-=lk[0];v[69]+=lk[1];v[68]=(v[68]>>>(lk[0]%16))|(v[68]<<(32-(lk[0]%16)));v[71]-=lk[1];v[70]-=lk[0];v[73]=(v[73]>>>(lk[1]%16))|(v[73]<<(32-(lk[1]%16)));v[72]=(v[72]<<(lk[0]%16))|(v[72]>>>(32-(lk[0]%16)));v[75]=(v[75]>>>(lk[1]%16))|(v[75]<<(32-(lk[1]%16)));v[74]^=lk[0];v[77]-=lk[1];v[76]+=lk[0];v[79]=(v[79]>>>(lk[1]%16))|(v[79]<<(32-(lk[1]%16)));v[78]=(v[78]>>>(lk[0]%16))|(v[78]<<(32-(lk[0]%16)));v[81]-=lk[1];v[80]+=lk[0];v[83]^=lk[1];v[82]-=lk[0];v[85]=(v[85]>>>(lk[1]%16))|(v[85]<<(32-(lk[1]%16)));v[84]-=lk[0];v[87]+=lk[1];v[86]=(v[86]>>>(lk[0]%16))|(v[86]<<(32-(lk[0]%16)));v[89]-=lk[1];v[88]-=lk[0];v[91]=(v[91]>>>(lk[1]%16))|(v[91]<<(32-(lk[1]%16)));v[90]=(v[90]<<(lk[0]%16))|(v[90]>>>(32-(lk[0]%16)));v[93]=(v[93]>>>(lk[1]%16))|(v[93]<<(32-(lk[1]%16)));v[92]^=lk[0];v[95]-=lk[1];v[94]+=lk[0];v[97]=(v[97]>>>(lk[1]%16))|(v[97]<<(32-(lk[1]%16)));v[96]=(v[96]>>>(lk[0]%16))|(v[96]<<(32-(lk[0]%16)));v[99]-=lk[1];v[98]+=lk[0];v[101]^=lk[1];v[100]-=lk[0];v[103]=(v[103]>>>(lk[1]%16))|(v[103]<<(32-(lk[1]%16)));v[102]-=lk[0];v[105]+=lk[1];v[104]=(v[104]>>>(lk[0]%16))|(v[104]<<(32-(lk[0]%16)));v[107]-=lk[1];v[106]-=lk[0];v[109]=(v[109]>>>(lk[1]%16))|(v[109]<<(32-(lk[1]%16)));v[108]=(v[108]<<(lk[0]%16))|(v[108]>>>(32-(lk[0]%16)));v[111]=(v[111]>>>(lk[1]%16))|(v[111]<<(32-(lk[1]%16)));v[110]^=lk[0];v[113]-=lk[1];v[112]+=lk[0];v[115]=(v[115]>>>(lk[1]%16))|(v[115]<<(32-(lk[1]%16)));v[114]=(v[114]>>>(lk[0]%16))|(v[114]<<(32-(lk[0]%16)));v[117]-=lk[1];v[116]+=lk[0];v[119]^=lk[1];v[118]-=lk[0];v[121]=(v[121]>>>(lk[1]%16))|(v[121]<<(32-(lk[1]%16)));v[120]-=lk[0];v[123]+=lk[1];v[122]=(v[122]>>>(lk[0]%16))|(v[122]<<(32-(lk[0]%16)));v[125]-=lk[1];v[124]-=lk[0];v[127]=(v[127]>>>(lk[1]%16))|(v[127]<<(32-(lk[1]%16)));v[126]=(v[126]<<(lk[0]%16))|(v[126]>>>(32-(lk[0]%16)));v[129]=(v[129]>>>(lk[1]%16))|(v[129]<<(32-(lk[1]%16)));v[128]^=lk[0];v[131]-=lk[1];v[130]+=lk[0];v[133]=(v[133]>>>(lk[1]%16))|(v[133]<<(32-(lk[1]%16)));v[132]=(v[132]>>>(lk[0]%16))|(v[132]<<(32-(lk[0]%16)));v[135]-=lk[1];v[134]+=lk[0];v[137]^=lk[1];v[136]-=lk[0];v[139]=(v[139]>>>(lk[1]%16))|(v[139]<<(32-(lk[1]%16)));v[138]-=lk[0];v[141]+=lk[1];v[140]=(v[140]>>>(lk[0]%16))|(v[140]<<(32-(lk[0]%16)));v[143]-=lk[1];v[142]-=lk[0];v[145]=(v[145]>>>(lk[1]%16))|(v[145]<<(32-(lk[1]%16)));v[144]=(v[144]<<(lk[0]%16))|(v[144]>>>(32-(lk[0]%16)));v[147]=(v[147]>>>(lk[1]%16))|(v[147]<<(32-(lk[1]%16)));v[146]^=lk[0];v[149]-=lk[1];v[148]+=lk[0];v[151]=(v[151]>>>(lk[1]%16))|(v[151]<<(32-(lk[1]%16)));v[150]=(v[150]>>>(lk[0]%16))|(v[150]<<(32-(lk[0]%16)));v[153]-=lk[1];v[152]+=lk[0];v[155]^=lk[1];v[154]-=lk[0];v[157]=(v[157]>>>(lk[1]%16))|(v[157]<<(32-(lk[1]%16)));v[156]-=lk[0];v[159]+=lk[1];v[158]=(v[158]>>>(lk[0]%16))|(v[158]<<(32-(lk[0]%16)));v[161]-=lk[1];v[160]-=lk[0];v[163]=(v[163]>>>(lk[1]%16))|(v[163]<<(32-(lk[1]%16)));v[162]=(v[162]<<(lk[0]%16))|(v[162]>>>(32-(lk[0]%16)));v[165]=(v[165]>>>(lk[1]%16))|(v[165]<<(32-(lk[1]%16)));v[164]^=lk[0];v[167]-=lk[1];v[166]+=lk[0];v[169]=(v[169]>>>(lk[1]%16))|(v[169]<<(32-(lk[1]%16)));v[168]=(v[168]>>>(lk[0]%16))|(v[168]<<(32-(lk[0]%16)));v[171]-=lk[1];v[170]+=lk[0];v[173]^=lk[1];v[172]-=lk[0];v[175]=(v[175]>>>(lk[1]%16))|(v[175]<<(32-(lk[1]%16)));v[174]-=lk[0];v[177]+=lk[1];v[176]=(v[176]>>>(lk[0]%16))|(v[176]<<(32-(lk[0]%16)));v[179]-=lk[1];v[178]-=lk[0];v[181]=(v[181]>>>(lk[1]%16))|(v[181]<<(32-(lk[1]%16)));v[180]=(v[180]<<(lk[0]%16))|(v[180]>>>(32-(lk[0]%16)));v[183]=(v[183]>>>(lk[1]%16))|(v[183]<<(32-(lk[1]%16)));v[182]^=lk[0];v[185]-=lk[1];v[184]+=lk[0];v[187]=(v[187]>>>(lk[1]%16))|(v[187]<<(32-(lk[1]%16)));v[186]=(v[186]>>>(lk[0]%16))|(v[186]<<(32-(lk[0]%16)));v[189]-=lk[1];v[188]+=lk[0];v[191]^=lk[1];v[190]-=lk[0];v[193]=(v[193]>>>(lk[1]%16))|(v[193]<<(32-(lk[1]%16)));v[192]-=lk[0];v[195]+=lk[1];v[194]=(v[194]>>>(lk[0]%16))|(v[194]<<(32-(lk[0]%16)));v[197]-=lk[1];v[196]-=lk[0];v[199]=(v[199]>>>(lk[1]%16))|(v[199]<<(32-(lk[1]%16)));v[198]=(v[198]<<(lk[0]%16))|(v[198]>>>(32-(lk[0]%16)));v[201]=(v[201]>>>(lk[1]%16))|(v[201]<<(32-(lk[1]%16)));v[200]^=lk[0];v[203]-=lk[1];v[202]+=lk[0];v[205]=(v[205]>>>(lk[1]%16))|(v[205]<<(32-(lk[1]%16)));v[204]=(v[204]>>>(lk[0]%16))|(v[204]<<(32-(lk[0]%16)));v[207]-=lk[1];v[206]+=lk[0];v[209]^=lk[1];v[208]-=lk[0];v[211]=(v[211]>>>(lk[1]%16))|(v[211]<<(32-(lk[1]%16)));v[210]-=lk[0];v[213]+=lk[1];v[212]=(v[212]>>>(lk[0]%16))|(v[212]<<(32-(lk[0]%16)));v[215]-=lk[1];v[214]-=lk[0];v[217]=(v[217]>>>(lk[1]%16))|(v[217]<<(32-(lk[1]%16)));v[216]=(v[216]<<(lk[0]%16))|(v[216]>>>(32-(lk[0]%16)));v[219]=(v[219]>>>(lk[1]%16))|(v[219]<<(32-(lk[1]%16)));v[218]^=lk[0];v[221]-=lk[1];v[220]+=lk[0];v[223]=(v[223]>>>(lk[1]%16))|(v[223]<<(32-(lk[1]%16)));v[222]=(v[222]>>>(lk[0]%16))|(v[222]<<(32-(lk[0]%16)));v[225]-=lk[1];v[224]+=lk[0];v[227]^=lk[1];v[226]-=lk[0];v[229]=(v[229]>>>(lk[1]%16))|(v[229]<<(32-(lk[1]%16)));v[228]-=lk[0];v[231]+=lk[1];v[230]=(v[230]>>>(lk[0]%16))|(v[230]<<(32-(lk[0]%16)));v[233]-=lk[1];v[232]-=lk[0];v[235]=(v[235]>>>(lk[1]%16))|(v[235]<<(32-(lk[1]%16)));v[234]=(v[234]<<(lk[0]%16))|(v[234]>>>(32-(lk[0]%16)));v[237]=(v[237]>>>(lk[1]%16))|(v[237]<<(32-(lk[1]%16)));v[236]^=lk[0];v[239]-=lk[1];v[238]+=lk[0];v[241]=(v[241]>>>(lk[1]%16))|(v[241]<<(32-(lk[1]%16)));v[240]=(v[240]>>>(lk[0]%16))|(v[240]<<(32-(lk[0]%16)));v[243]-=lk[1];v[242]+=lk[0];v[245]^=lk[1];v[244]-=lk[0];v[247]=(v[247]>>>(lk[1]%16))|(v[247]<<(32-(lk[1]%16)));v[246]-=lk[0];v[249]+=lk[1];v[248]=(v[248]>>>(lk[0]%16))|(v[248]<<(32-(lk[0]%16)));v[251]-=lk[1];v[250]-=lk[0];v[253]=(v[253]>>>(lk[1]%16))|(v[253]<<(32-(lk[1]%16)));v[252]=(v[252]<<(lk[0]%16))|(v[252]>>>(32-(lk[0]%16)));v[255]=(v[255]>>>(lk[1]%16))|(v[255]<<(32-(lk[1]%16)));v[254]^=lk[0];v[257]-=lk[1];v[256]+=lk[0];v[259]=(v[259]>>>(lk[1]%16))|(v[259]<<(32-(lk[1]%16)));v[258]=(v[258]>>>(lk[0]%16))|(v[258]<<(32-(lk[0]%16)));v[261]-=lk[1];v[260]+=lk[0];v[263]^=lk[1];v[262]-=lk[0];v[265]=(v[265]>>>(lk[1]%16))|(v[265]<<(32-(lk[1]%16)));v[264]-=lk[0];v[267]+=lk[1];v[266]=(v[266]>>>(lk[0]%16))|(v[266]<<(32-(lk[0]%16)));v[269]-=lk[1];v[268]-=lk[0];v[271]=(v[271]>>>(lk[1]%16))|(v[271]<<(32-(lk[1]%16)));v[270]=(v[270]<<(lk[0]%16))|(v[270]>>>(32-(lk[0]%16)));v[273]=(v[273]>>>(lk[1]%16))|(v[273]<<(32-(lk[1]%16)));v[272]^=lk[0];v[275]-=lk[1];v[274]+=lk[0];v[277]=(v[277]>>>(lk[1]%16))|(v[277]<<(32-(lk[1]%16)));v[276]=(v[276]>>>(lk[0]%16))|(v[276]<<(32-(lk[0]%16)));v[279]-=lk[1];v[278]+=lk[0];v[281]^=lk[1];v[280]-=lk[0];v[283]=(v[283]>>>(lk[1]%16))|(v[283]<<(32-(lk[1]%16)));v[282]-=lk[0];v[285]+=lk[1];v[284]=(v[284]>>>(lk[0]%16))|(v[284]<<(32-(lk[0]%16)));v[287]-=lk[1];v[286]-=lk[0];v[289]=(v[289]>>>(lk[1]%16))|(v[289]<<(32-(lk[1]%16)));v[288]=(v[288]<<(lk[0]%16))|(v[288]>>>(32-(lk[0]%16)));v[291]=(v[291]>>>(lk[1]%16))|(v[291]<<(32-(lk[1]%16)));v[290]^=lk[0];v[293]-=lk[1];v[292]+=lk[0];v[295]=(v[295]>>>(lk[1]%16))|(v[295]<<(32-(lk[1]%16)));v[294]=(v[294]>>>(lk[0]%16))|(v[294]<<(32-(lk[0]%16)));v[297]-=lk[1];v[296]+=lk[0];v[299]^=lk[1];v[298]-=lk[0];v[301]=(v[301]>>>(lk[1]%16))|(v[301]<<(32-(lk[1]%16)));v[300]-=lk[0];v[303]+=lk[1];v[302]=(v[302]>>>(lk[0]%16))|(v[302]<<(32-(lk[0]%16)));v[305]-=lk[1];v[304]-=lk[0];v[307]=(v[307]>>>(lk[1]%16))|(v[307]<<(32-(lk[1]%16)));v[306]=(v[306]<<(lk[0]%16))|(v[306]>>>(32-(lk[0]%16)));v[309]=(v[309]>>>(lk[1]%16))|(v[309]<<(32-(lk[1]%16)));v[308]^=lk[0];v[311]-=lk[1];v[310]+=lk[0];v[313]=(v[313]>>>(lk[1]%16))|(v[313]<<(32-(lk[1]%16)));v[312]=(v[312]>>>(lk[0]%16))|(v[312]<<(32-(lk[0]%16)));v[315]-=lk[1];v[314]+=lk[0];v[317]^=lk[1];v[316]-=lk[0];v[319]=(v[319]>>>(lk[1]%16))|(v[319]<<(32-(lk[1]%16)));v[318]-=lk[0];v[321]+=lk[1];v[320]=(v[320]>>>(lk[0]%16))|(v[320]<<(32-(lk[0]%16)));v[323]-=lk[1];v[322]-=lk[0];v[325]=(v[325]>>>(lk[1]%16))|(v[325]<<(32-(lk[1]%16)));v[324]=(v[324]<<(lk[0]%16))|(v[324]>>>(32-(lk[0]%16)));v[327]=(v[327]>>>(lk[1]%16))|(v[327]<<(32-(lk[1]%16)));v[326]^=lk[0];v[329]-=lk[1];v[328]+=lk[0];v[331]=(v[331]>>>(lk[1]%16))|(v[331]<<(32-(lk[1]%16)));v[330]=(v[330]>>>(lk[0]%16))|(v[330]<<(32-(lk[0]%16)));v[333]-=lk[1];v[332]+=lk[0];v[335]^=lk[1];v[334]-=lk[0];v[337]=(v[337]>>>(lk[1]%16))|(v[337]<<(32-(lk[1]%16)));v[336]-=lk[0];v[339]+=lk[1];v[338]=(v[338]>>>(lk[0]%16))|(v[338]<<(32-(lk[0]%16)));v[341]-=lk[1];v[340]-=lk[0];v[343]=(v[343]>>>(lk[1]%16))|(v[343]<<(32-(lk[1]%16)));v[342]=(v[342]<<(lk[0]%16))|(v[342]>>>(32-(lk[0]%16)));v[345]=(v[345]>>>(lk[1]%16))|(v[345]<<(32-(lk[1]%16)));v[344]^=lk[0];v[347]-=lk[1];v[346]+=lk[0];v[349]=(v[349]>>>(lk[1]%16))|(v[349]<<(32-(lk[1]%16)));v[348]=(v[348]>>>(lk[0]%16))|(v[348]<<(32-(lk[0]%16)));v[351]-=lk[1];v[350]+=lk[0];v[353]^=lk[1];v[352]-=lk[0];v[355]=(v[355]>>>(lk[1]%16))|(v[355]<<(32-(lk[1]%16)));v[354]-=lk[0];v[357]+=lk[1];v[356]=(v[356]>>>(lk[0]%16))|(v[356]<<(32-(lk[0]%16)));v[359]-=lk[1];v[358]-=lk[0];v[361]=(v[361]>>>(lk[1]%16))|(v[361]<<(32-(lk[1]%16)));v[360]=(v[360]<<(lk[0]%16))|(v[360]>>>(32-(lk[0]%16)));v[363]=(v[363]>>>(lk[1]%16))|(v[363]<<(32-(lk[1]%16)));v[362]^=lk[0];v[365]-=lk[1];v[364]+=lk[0];v[367]=(v[367]>>>(lk[1]%16))|(v[367]<<(32-(lk[1]%16)));v[366]=(v[366]>>>(lk[0]%16))|(v[366]<<(32-(lk[0]%16)));v[369]-=lk[1];v[368]+=lk[0];v[371]^=lk[1];v[370]-=lk[0];v[373]=(v[373]>>>(lk[1]%16))|(v[373]<<(32-(lk[1]%16)));v[372]-=lk[0];v[375]+=lk[1];v[374]=(v[374]>>>(lk[0]%16))|(v[374]<<(32-(lk[0]%16)));v[377]-=lk[1];v[376]-=lk[0];v[379]=(v[379]>>>(lk[1]%16))|(v[379]<<(32-(lk[1]%16)));v[378]=(v[378]<<(lk[0]%16))|(v[378]>>>(32-(lk[0]%16)));v[381]=(v[381]>>>(lk[1]%16))|(v[381]<<(32-(lk[1]%16)));v[380]^=lk[0];v[383]-=lk[1];v[382]+=lk[0];v[385]=(v[385]>>>(lk[1]%16))|(v[385]<<(32-(lk[1]%16)));v[384]=(v[384]>>>(lk[0]%16))|(v[384]<<(32-(lk[0]%16)));v[387]-=lk[1];v[386]+=lk[0];v[389]^=lk[1];v[388]-=lk[0];v[391]=(v[391]>>>(lk[1]%16))|(v[391]<<(32-(lk[1]%16)));v[390]-=lk[0];v[393]+=lk[1];v[392]=(v[392]>>>(lk[0]%16))|(v[392]<<(32-(lk[0]%16)));for(var I=0;I<394;I+=2){var i,v0=v[I]^k2[0],v1=v[I+1]^k2[1],d=0x9E3779B9,sum=d*rk[I/2];for(i=0;i<rk[I/2];i++){v1-=(((v0<<4)^(v0>>>5))+v0)^(sum+k[(sum>>>11)&3]);sum-=d;v0-=(((v1<<4)^(v1>>>5))+v1)^(sum+k[sum&3]);}v[I]=v0^k2[1];v[I+1]=v1^k2[0];}for(var O=393;O>0;O--){v[O]^=v[O-1];}v[0]^=0x74c037e;var strc="";for(var i=0;i<v.length;i++) {strc+=String.fromCharCode(v[i]&0xff,v[i]>>>8&0xff,v[i]>>>16&0xff,v[i]>>>24&0xff);}return eval(strc)(i075b25e2d6ea3c70f8a0,i075b25e2d6ea3c70f8a1,i075b25e2d6ea3c70f8a2);} ;
    result_stdout = result.stdout.strip()
    # 提取sign签名值
    pairs = result_stdout.split('&')
    result_dict = {}
    for pair in pairs:
        key, value = pair.split('=')
        result_dict[key] = value
    print(result_dict)
    sign = result_dict['sign']
    v=result_dict['v']
    os.remove(js_filename)
    return v,sign, title
def get_stream_url(v, did, tt, sign, vid):
    data = {
        'v': v,
        'did': did,
        'tt': str(tt),
        'sign': sign,
        'vid': vid
    }
    url = 'https://v.douyu.com/api/stream/getStreamUrl'
    response = requests.post(url=url, headers=headers, data=data)
    m3u8_url = response.json()['data']['thumb_video']['high']['url']
    print(m3u8_url)
    return m3u8_url

def download_m3u8(m3u8_url, title):
    sub_ts = m3u8_url.split('playlist')[0]
    m3u8_text = requests.get(m3u8_url).text
    ts_list = re.sub('#E.*', '', m3u8_text).split()
    for ts in tqdm(ts_list):
        ts_url = sub_ts + ts
        ts_data = requests.get(ts_url).content
        with open(f'D:\\2024work\\zhou\\斗鱼\\{title}.mp4', mode='ab') as f:
            f.write(ts_data)

from urllib.parse import urlparse, parse_qs

def extract_anchor_id(url):
    """从给定的URL中提取anchorId"""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get('anchorId', [None])[0]

def process_url(url, output_file):
    # anchor_id_match = re.search(r'anchorId=([^&]+)', url)

    # if not anchor_id_match:
    #     print(f"Failed to extract anchorId from {url}")
    #     return
    anchor_id = extract_anchor_id(url)
    # print(anchor_id)
    # anchor_id = anchor_id_match.group(1)

    new_url = f'https://v.douyu.com/show/{anchor_id}'

    try:
        response = requests.get(new_url, headers=headers)
        script_texts = re.findall(r'<script[^>]*>(.*?)</script>', response.text, re.DOTALL)
        print(new_url,script_texts[1])
        if len(script_texts) > 1:
            script_text = script_texts[1]
            vid, seo_title = extract_vid_and_seo_title(script_text)
            print(vid, seo_title)
            if vid:
                point_id = get_point_id(vid)
                did = "10000000000000000000000000001501"
                tt = int(time.time())

                v, sign, title = get_sign(vid, point_id, did, tt)
                m3u8_url = get_stream_url(v, did, tt, sign, vid)
                download_m3u8(m3u8_url, title)
                print(m3u8_url)
                audio_name = f'{title}.mp4'
                data={
                    'url': url,
                    'title': title,
                    'title_tags': '',
                    'time': '',
                    'audio_path': audio_name,
                    'tag': 'gemini人设'
                }
                # 使用锁来确保线程安全地写入文件
                with jsonl_lock:
                    with open(output_file, 'a+', encoding='utf-8') as jsonl_file:
                        jsonl_file.write(json.dumps(data, ensure_ascii=False) + '\n')

            else:
                print(f"Failed to extract vid from {new_url}")
        else:
            print(f"Failed to find script text in {new_url}")
    except Exception as e:
        print(f"Error processing {new_url}: {e}")


def main():
    input_file = 'D:\\2024work\\zhou\\douyu.txt'
    output_file = 'D:\\2024work\\zhou\\斗鱼.jsonl'

    with open(input_file, 'r') as f:
        urls = [line.strip() for line in f.readlines()]


    # manager = Manager()
    # results = manager.list()

    with Pool(1) as pool:
        pool.starmap(process_url, [(url, output_file) for url in urls])

    # with open(output_file, 'w') as f:
    #     for result in results:
    #         f.write(json.dumps(result, ensure_ascii=False) + '\n')


if __name__ == "__main__":
    main()


