[TOC]

## 摘要说明

**修订记录** 

| 日期 | 版本 | 说明 | 作者 |
| :---: | :---: | :---: | :----: |
| 2020-02-24 | 1.0.0 | 1.Fast-Auto接口文档建立 | 麦锦培 |
**工作方式** 

- 双方通过HTTP方式交互数据。即通过HTTP的POST/ GET方式交互
- 双方需要保证数据传输的完整和安全性，每次请求都必须有响应（响应返回格式为json纯文本或者get方式提交数据供返回）

**返回值说明**

- status是返回状态标示符，0是成功，其他是错误。
- msg是返回状态说明。
- result是返回数据，如果没有返回数据，result字段内容为空。

**错误码对应表**

| status | 含义 | 说明 |
| :---: | :---: | :---: |
|  0   | 请求成功，没有错误 | 表示接口返回正确值 |
|  >0  | 请求失败，请求参数异常 | 表示接口请求参数错误,其他错误 |



## 通用接口说明

**简要描述** 

- 接口的加密解密描述，请求连接的格式：` http://xxx.xxx.xxx/?ct=xxx&ac=xxx&p={密文}&ts={原始raw_key} `

**请求方式** 

- p和ts用post方式请求

**加解密流程说明** 

- 加密流程：
	1）当前时间戳+10位长度Digits(0-9)随机数进行32位小写的md5加密得到原始秘钥raw_key
	2）把原始秘钥raw_key正序和倒序拼接成64位长度字符串进行16位小写的md5加密得到AES秘钥aes_key
	3）使用AES秘钥aes_key对数据进行AES/CBC/PKCS5Padding加密得到数据密文p
	
- 解密流程：
	1）把原始秘钥raw_key正序和倒序拼接成64位长度字符串进行16位小写的md5加密得到AES秘钥aes_key
	2）使用秘钥aes_key对加密的数据进行解密。得到数据原文

- 图示：
![QQ20200226-103002.png](https://i.loli.net/2020/02/26/nVCaSkcdyHsT3i2.png)

- AES加密配置：
	1）必须为秘钥长度16字节(128bit)或者32字节(256bit)
	2）初始向量IV的生成算法。对长度16字节(128bit)或者32字节(256bit)的秘钥进行倒序。例如：AES秘钥为 0123456789abcdef , 则IV为 fedcba9876543210
	3）加解密方法及PADDING为: AES/CBC/PKCS5Padding

**返回值示例**

```json
{
    "code":"0",
    "msg":"xxxx",
    "data":{
        "p":"{密文}",
        "ts":"{原始raw_key}"
    }
}
```
- code是返回状态标示符。0是成功，其他是错误。
- msg是返回状态说明。code为0的时候是空，code为其他的时候是错误信息。
- data是返回加密数据，如果没有返回数据，就没有data字段。
- ts是原始raw_key

**公共参数**

- 接口公共参数common：

| 参数名 | 必须 | 非空 |  类型 | 说明 |
| :---: | :---: | :---: | :---: | :---: |
| class_type | 是 | 是 | int | 业务类型：1.国内发行;2.海外发行;3.独立发行 |
| server_version | 是 | 是 | string | 服务端版本，v1 |
| client_version | 是 | 是 | string | 客户端版本 |
| ext | 是 | 否 | json | 扩展参数 |



## 任务请求接口

**简要描述** 

- 任务请求规则：
	1）上一条任务完成或中断时请求
	2）客户端空闲>=2min时开启定时轮询，以2min为一个执行单元

**请求Url** 

- `http://xxx.xxx.xxx/?ct=AutoPackage&ac=getTaskInfo&p={密文}&ts={原始raw_key}`

**请求参数**

| 参数名 | 必须 | 非空 |  类型 | 说明 |
| :---: | :---: | :---: | :---: | :---: |
| task_id | 是 | 否 | string | 上一次打包任务id |
| ext | 是 | 否 | json | 扩展参数 |

**请求示例**

```json
{
    "task_id": "1234",
    "ext": ""
}
```

**返回参数** 

- result

| 参数名 | 必须 | 非空 |  类型 | 说明 |
| :---: | :---: | :---: | :---: | :---: |
| task_info | 是 | 是 | json | 任务信息 |
|  - task_id | 是 | 是 | string | 任务id |
|  - is_majia | 是 | 是 | int | 是否打马甲包 |
|  - is_white_bag | 是 | 是 | int | 是否打白包 |
|  - is_debug_bag | 是 | 是 | int | 是否打debug包 |
|  - has_plugin_sdk | 是 | 是 | int | 是否打媒体包 |
| bag_info | 是 | 是 | json | 母包信息 |
| - group_id | 是 | 是 | json | 母包游戏组id |
| - group_name | 是 | 是 | json | 母包游戏组名 |
| - game_id | 是 | 是 | string | 母包游戏id |
| - version_code | 是 | 是 | string | 母包版本号 |
| - version_name | 是 | 是 | string | 母包游戏名 |
| - file_name | 是 | 是 | string | 母包文件名 |
| - file_url | 是 | 是 | string | 母包文件url |
| - file_md5 | 是 | 是 | string | 母包文件md5 |
| sdk_info | 是 | 是 | json | sdk信息 |
| - common_sdk | 是 | 是 | json | 融合sdk信息 |
| -- version | 是 | 是 | string | 融合sdk版本 |
| -- file_name | 是 | 是 | string | 融合sdk文件名 |
| -- file_url | 是 | 是 | string | 融合sdk文件url |
| -- file_md5 | 是 | 是 | string | 融合sdk文件md5 |
| - channel_sdk | 是 | 是 | json | 渠道sdk信息 |
| -- version | 是 | 是 | string | 渠道sdk版本 |
| -- file_name | 是 | 是 | string | 渠道sdk文件名 |
| -- file_url | 是 | 是 | string | 渠道sdk文件url |
| -- file_md5 | 是 | 是 | string | 渠道sdk文件MD5 |
| - plugin_sdk | 是 | 否 | json | 媒体插件sdk信息 |
| -- （plugin_interface_name） | 是 | 是 | json | 媒体插件sdk类型 |
| --- version | 是 | 是 | string | 媒体插件sdk版本 |
| --- file_name | 是 | 是 | string | 媒体插件sdk文件名 |
| --- file_url | 是 | 是 | string | 媒体插件sdk文件url |
| --- file_md5 | 是 | 是 | string | 媒体插件sdk文件md5 |
| keystore_info | 是 | 是 | json | 签名文件信息 |
| - keystore_name | 是 | 是 | string | 签名文件名 |
| - keystore_password | 是 | 是 | string | 签名文件密码 |
| - keystore_alias | 是 | 是 | string | 签名文件别名 |
| - keystore_alias_password | 是 | 是 | string | 签名文件别名密码 |
| - file_url | 是 | 是 | string | 签名文件url |
| - file_md | 是 | 是 | string | 签名文件md5 |
| script_info | 是 | 是 | json | 脚本文件信息 |
| - common_scirpt | 是 | 否 | json | 融合脚本文件信息 |
| -- file_name | 是 | 是 | string | 融合脚本文件名 |
| -- file_url | 是 | 是 | string | 融合脚本文件url |
| -- file_md5 | 是 | 是 | string | 融合脚本文件md5 |
| - game_scirpt | 是 | 否 | json | 游戏脚本文件信息 |
| -- file_name | 是 | 是 | string | 游戏脚本文件名 |
| -- file_url | 是 | 是 | string | 游戏脚本文件url |
| -- file_md5 | 是 | 是 | string | 游戏脚本文件md5 |
| params_info | 是 | 是 | json | 参数信息 |
| - common_params | 是 | 是 | json | 融合参数信息 |
| -- game_id | 是 | 是 | string | 游戏id |
| -- package-chanle | 是 | 是 | json | 拿包id-分发id |
| -- total | 是 | 是 | int | 子包个数 |
| -- channel_name | 是 | 是 | string | 渠道名 |
| -- channel_id | 是 | 是 | string | 渠道id |
| -- deploy_id | 是 | 是 | json | 渠道配置id |
| - channel_info | 是 | 是 | json | 渠道参数信息 |
| - plugin_params | 是 | 否 | json | 媒体插件参数信息 |
| - game_params | 是 | 是 | json | 游戏参数信息 |
| -- game_package_name | 是 | 是 | string | 游戏包名 |
| -- game_name | 是 | 是 | string | 游戏名 |
| -- game_version_code | 是 | 是 | string | 游戏版本号 |
| -- game_version_name | 是 | 是 | string | 游戏版本名 |
| -- game_orientation | 是 | 是 | int | 游戏横竖屏配置：0.横屏；1.竖屏 |
| -- game_icon_url | 是 | 否 | string | 游戏icon文件url |
| -- game_logo_url | 是 | 否 | string | 游戏logo文件url |
| -- game_splash_url | 是 | 否 | string | 游戏闪屏文件url |
| -- game_background_url | 是 | 否 | string | 游戏登录页背景文件url |
| -- game_loading_url | 是 | 否 | string | 游戏加载图文件url |
| -- game_resource_url | 是 | 否 | string | 游戏特殊资源文件url |
| ext | 是 | 否 | json | 扩展参数 |

**返回示例** 

```json
{
    "task_info": {
        "task_id": "1234",
        "is_majia": 0,
        "is_white_bag": 0,
        "is_debug_bag": 0,
        "has_plugin_sdk": 1
    },
    "bag_info": {
        "group_id": "7",
		"group_name":"星辰奇缘",
        "game_id": "92",
        "version_code": "100",//后端木有，暂时不传
        "version_name": "1.0.0",
        "file_name": "xcqy_100.apk",
        "file_url": "http://xcqy_100.apk",
        "file_md5": "aabbaabbaabbaabbaabbaabbaabbaabb"
    },
    "sdk_info": {
        "common_sdk": {
            "version": "6.0.3_media",
            "file_name": "6.0.3_media_1582689753.zip",
            "file_url": "http://6.0.3_media_1582689753.zip",
            "file_md5": "aabbaabbaabbaabbaabbaabbaabbaabb"
        },
        "channel_sdk": {
            "version": "4.7.0",
            "file_name": "3k_1582689753.zip",
            "file_url": "http://6.0.3_media_1582689753.zip",
            "file_md5": "aabbaabbaabbaabbaabbaabbaabbaabb"
        },
        "plugin_sdk": {
            "toutiao_plugin": {
                "version": "2.0.6",
                "file_name": "Toutiao_EventTracking_2.0.6_1579160694.zip",
                "file_md5": "d283a45f341a9d28421dedbf9f7a27ed",
                "file_url": "http://Toutiao_EventTracking_2.0.6_1579160694.zip"
            },
            "gdt_action_plugin": {
                "version": "1.5.0",
                "file_name": "GDT_Action_1.5.0_1578586437.zip",
                "file_md5": "e8dfb222de998671697be3896f71f569",
                "file_url": "http://20200116/GDT_Action_1.5.0_1578586437.zip.zip"
            }
        }
    },
    "keystore_info": {
        "keystore_name": "lzzdy_3k2018.keystore",
        "keystore_password": "lzzdyjkb_3k2018",
        "keystore_alias": "alias.lzzdy_3k2018",
        "keystore_alias_password ": "lzzdyjkb_3k2018",
        "file_url": "http: //1569296395/lzzdy_3k2018.keystore",
        "file_md5": "aabbaabbaabbaabbaabbaabbaabbaabb"
    },
    "script_info": {
        "common_script": {
            "file_name": "common_script.zip",
            "file_url": "http://xxx/common_script.zip",
            "file_md5": "e8dfb222de998671697be3896f71f569"
        },
        "game_script": {
            "file_name": "game_script.zip",
            "file_url": "http://xxx/game_script.zip",
            "file_md5": "e8dfb222de998671697be3896f71f569"
        }
    },
    "params_info": {
        "common_params": {
            "game_id": "123456",
            "package_chanle": {
                "30494": "30494",
                "30495": "30495",
                "30496": "30496",
                "30497": "30497",
                "30498": "30498"
            },
            "total": 5,
            "channel_name": "3k",
            "channel_id": "0",
            "deploy_id": ""
        },
        "channel_params": {},
        "plugin_params": {
                "FUSE_SS_ENABLE": "true",
                "FUSE_SS_APP_ID": "168277",
                "FUSE_SS_APP_NAME": "scbtb_xcqy12",
                "FUSE_SS_APP_CHANNEL": "scbtb_xcqy12"
                "FUSE_GDT_ACTION_ENABLE": "true",
                "FUSE_GDT_ACTION_SET_ID": "1109810298",
                "FUSE_GDT_ACTION_SECRET_KEY": "5964c391dcf1909db0afb7ed5f905089"
        },
        "game_params": {
            "game_package_name": "com.scbtb.kkkwan12",
            "game_name": "\u795e\u5ba0BT\u7248",
            "game_version_code": "340000",
            "game_version_name": "2.6.0",
            "game_orientation": "0",
            "game_icon_url": "http: //8cb96b124b033f68d9633934103992cb_1541400072.png",
            "game_logo_url": "https://upload_oeaclugrhh8fa3qjxv37rxk0e2gj4lhl.png",
            "game_splash_url": "",
            "game_background_url": "",
            "game_loading_url": "",
            "game_resource_url": ""
        },
		"ext": {}
    }
}
```



## 打包状态上报接口

**简要描述**

- 任务打包的状态上报，如果失败时会上传对应的log日志

**请求url**

- `http://xxx.xxx.xxx/?ct=AutoPackage&ac=getStatusReport&p={密文}&ts={原始raw_key}`

**请求参数**

| 参数名 | 必须 | 非空 |  类型 | 说明 |
| :---: | :---: | :---: | :---: | :---: |
| task_id | 是 | 是 | string | 任务id |
| package_id | 是 | 是 | string | 子包的包id |
| status_code | 是 | 是 | int | 状态码：1204.失败；1210.成功 |
| bag_url | 是 | 否 | string | 打包成功后生成的云链url |
| common_sdk_version | 是 | 否 | string | 融合SDK版本 |
| channel_sdk_version | 是 | 否 | string | 渠道SDK版本 |
| package_size | 是 | 否 | int | 分包体大小，单位：byte |
| ext | 是 | 否 | json | 扩展参数 |
| package_size | 是 | 否 | int | 母包体大小，单位：byte |
| rh_sdk_size | 是 | 否 | int | 融合sdk大小，单位：byte |
| channel_sdk_size | 是 | 否 | int | 渠道sdk大小，单位：byte |
| plugin_size | 是 | 否 | int | 插件sdk大小，单位：byte |
| rh_time | 是 | 否 | int | 融合时长，单位：秒 |
| from_time | 是 | 否 | int | 分发时长，单位：秒 |
| upload_time | 是 | 否 | int | 上传时长，单位：秒 |


**请求示例**

```json
{
    "task_id": "1234",
    "package_id":"2020",
    "status_code": 1210,
    "bag_url": "https://abc/xxx.apk",
    "common_sdk_version": "1.0.0",
    "channel_sdk_version": "1.0.0",
	"package_size":100,
    "ext": {
		"package_size":100,
		"rh_sdk_size":100,
		"channel_sdk_size":100,
		"plugin_size":100,
		"rh_time":100,
		"from_time": 100,
		"upload_time":100,
	}
}
```

**返回参数**

| 参数名 | 必须 | 非空 |  类型 | 说明 |
| :---: | :---: | :---: | :---: | :---: |
| status_code | 是 | 是 | int | 是否停止打包，0：是；1：否 |

**返回示例**

```json
{
    "status": 0,
    "msg": "",
    "result": {
        "is_stop":0,
    }
}
```

## 任务状态上报接口

**简要描述**

- 任务状态上报，

**请求url**

- `http://xxx.xxx.xxx/?ct=AutoPackage&ac=getTaskReport&p={密文}&ts={原始raw_key}`

**请求参数**

| 参数名 | 必须 | 非空 |  类型 | 说明 |
| :---: | :---: | :---: | :---: | :---: |
| task_id | 是 | 是 | string | 任务id |
| status_code | 是 | 是 | int | 状态码：1204.失败；1210.成功(成功的话，只有全部包上传完成后才上报) |

**请求示例**

```json
{
    "task_id": "1234",
    "status_code": 1210,
}
```

**返回参数**

| 参数名 | 必须 | 非空 |  类型 | 说明 |
| :---: | :---: | :---: | :---: | :---: |

**返回示例**

```json
{
    "status": 0,
    "msg": "",
    "result": {}
}
```