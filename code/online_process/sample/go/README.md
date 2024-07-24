## Go lang sample to call online translate
Go Version
``` shell
go version
go version go1.15.15 linux/amd64
```

How to run
``` shell
go get github.com/aws/aws-sdk-go
go run go_sample.go
```

Sample output
```
Original contents: [蚕食者之影在哪里能找到？ 蚕食者之影的弱点是什么？]
--------------------
Translated Text: Where can I find the Decaying Shadow?
Model: anthropic.claude-3-haiku-20240307-v1:0
Dict: {"glossary":"test_dict1"}
--------------------
Translated Text: What are the weaknesses of the Decaying Shadow?
Model: anthropic.claude-3-haiku-20240307-v1:0
Dict: {"glossary":"test_dict1"}
```