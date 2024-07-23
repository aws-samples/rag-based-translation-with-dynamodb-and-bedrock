# DynamoDB-RAG

## 界面演示效果

![demo](./demo.gif) 

- 界面启动方式
```
# 如果没有安装pip
# sudo yum install pip -y

cd code/web_ui

# 拷贝之前部署时的环境变量
cp ../../deploy/.env ./utils/.env

pip install -r requirement.txt
nohup streamlit run home.py &
```

### 目标：

利用RAG召回的元数据，更好的支持翻译, VOC等任务。

### 适用场景：

存在大量的专有名词(无须翻译), 存在大量的不同语言之间的标准映射，不能够一次性把这些元信息添加到PE。

### 实现方式：

通过DynamoDB来存储大量专词的映射关系，元数据摄入部分通过Glue Job进行调度。 调用部分，可以采用离线(Glue job)或者在线(Lambda)的方式进行。

### 部署文档：

[飞书](https://amzn-chn.feishu.cn/docx/HxO8dK41UosPFvxAylScW6Xunah?from=from_copylink)

### 调用方式：

- 离线方式(仅翻译接口，按照文件级别进行并发推理)
    - 参见[飞书文档](https://amzn-chn.feishu.cn/docx/HxO8dK41UosPFvxAylScW6Xunah?from=from_copylink)的4.2小节

- 在线方式(三种请求类型，segment_only|term_mapping|translate)
    【注意】需要指定dictionary_id, 这个是对应专词映射词典的名称
    - 仅切词

        参考payload
        ```json
        {
            "src_content":"奇怪的渔人吐司可以达到下面效果，队伍中所有角色防御力提高88点，持续300秒。多人游戏时，仅对自己的角色生效。《原神手游》赤魔王图鉴，赤魔王能捉吗",
            "src_lang":"CHS",
            "dest_lang":"EN",
            "request_type":"segment_only",
            "dictionary_id": "dictionary_1",
            "model_id":"anthropic.claude-3-sonnet-20240229-v1:0"
        }
        ```
        参考response
        ```json
        {
          "words": [
            "赤魔王",
            "奇怪的渔人吐司"
          ]
        }
        ```
    - 获取专词映射

        参考payload
        ```json
		{
		    "src_content":"奇怪的渔人吐司可以达到下面效果，队伍中所有角色防御力提高88点，持续300秒。多人游戏时，仅对自己的角色生效。《原神手游》赤魔王图鉴，赤魔王能捉吗",
		    "src_lang":"CHS",
		    "dest_lang":"EN",
		    "request_type":"term_mapping",
        "dictionary_id": "dictionary_1",
		    "model_id":"anthropic.claude-3-sonnet-20240229-v1:0"
		}
        ```
        参考response
        ```json
        {
          "term_mapping": [
            [
              "赤魔王",
              "Akai Maou",
              "Serenitea Pot家园"
            ],
            [
              "奇怪的渔人吐司",
              "Suspicious Fisherman's Toast",
              "Material 材料"
            ]
          ]
        }
        ```
    - 翻译
        参考payload
        ```json
        #CHS => EN
        {
            "src_content":"奇怪的渔人吐司可以达到下面效果，队伍中所有角色防御力提高88点，持续300秒。多人游戏时，仅对自己的角色生效。《原神手游》赤魔王图鉴，赤魔王能捉吗",
            "src_lang":"CHS",
            "dest_lang":"EN",
            "request_type":"translate",
            "dictionary_id": "dictionary_1",
            "model_id":"anthropic.claude-3-sonnet-20240229-v1:0"
        }

        #EN => CHS
        {
            "src_content":"Suspicious Fisherman’s Toast can achieve the following effect: all characters in the team gain 88 points of DEF, lasting for 300 seconds. In multi-player mode, this effect only applies to your own characters. Akai Maou Handbook, can Akai Maou be caught?",
            "src_lang":"EN",
            "dest_lang":"CHS",
            "request_type":"translate",
            "dictionary_id": "dictionary_1",
            "model_id":"anthropic.claude-3-sonnet-20240229-v1:0"
        }

        #EN => VI
        {
            "src_content":"Suspicious Fisherman’s Toast can achieve the following effect: all characters in the team gain 88 points of DEF, lasting for 300 seconds. In multi-player mode, this effect only applies to your own characters. Akai Maou Handbook, can Akai Maou be caught?",
            "src_lang":"EN",
            "dest_lang":"VI",
            "request_type":"translate",
            "dictionary_id": "dictionary_1",
            "model_id":"anthropic.claude-3-sonnet-20240229-v1:0"
        }

        #VI => CHS
        {
            "src_content":"Bánh Người Cá Kỳ Lạ có thể đạt được hiệu quả sau: tất cả nhân vật trong đội nhận được 88 điểm DEF, kéo dài trong 300 giây. Trong chế độ đa người chơi, hiệu quả này chỉ áp dụng cho nhân vật của riêng bạn. Xích Ma Vương Handbook, có thể bắt được Xích Ma Vương không?",
            "src_lang":"VI",
            "dest_lang":"CHS",
            "request_type":"translate",
            "dictionary_id": "dictionary_1",
            "model_id":"anthropic.claude-3-sonnet-20240229-v1:0"
        }
        ```
        参考response
        ```json
        {
          "term_mapping": [
            [
              "赤魔王",
              "Akai Maou",
              "Serenitea Pot家园"
            ],
            [
              "奇怪的渔人吐司",
              "Suspicious Fisherman's Toast",
              "Material 材料"
            ]
          ],
          "result": "\nSuspicious Fisherman's Toast can achieve the following effect: All characters in the team gain 88 DEF for 300 seconds. In multi-player mode, this effect only applies to your own characters. Genshin Impact Akai Maou Codex, can Akai Maou be caught?\n"
        }
        ```