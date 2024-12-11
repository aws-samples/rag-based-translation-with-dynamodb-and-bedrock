# 词库支持多版本设计概述
在词库不支持版本之前，词库更新的时间段内，会导致当前词库不可用。
为了提高可用性，词库支持多版本设计。

## 设计考量
词库支持多版本设计，需要做到：
1. 导入时支持多版本
  - 导入时，WebUI上支持多版本
  - 涉及到S3 和 DynamoDB 存储结构支持多版本
2. 在WebUI上，可以指定词库使用哪个版本
3. 调用时支持多版本

如果在#2指定了某个词库对应的版本，那么在#3调用时，则使用#2指定的版本，这样可以对#3调用方透明。


### 导入时支持多版本
S3 当前的目录结构时
```
s3://user-bucket/user-prefix/aaa/
s3://user-bucket/user-prefix/bbb/
s3://user-bucket/user-prefix/ccc/
```

为了支持多版本，需要将S3的目录结构改为：
```
s3://user-bucket/user-prefix/aaa/
s3://user-bucket/user-prefix/aaa_v1/
s3://user-bucket/user-prefix/aaa_v2/
s3://user-bucket/user-prefix/bbb/
s3://user-bucket/user-prefix/bbb_v1/
s3://user-bucket/user-prefix/bbb_v2/
s3://user-bucket/user-prefix/ccc/
s3://user-bucket/user-prefix/ccc_v1/
s3://user-bucket/user-prefix/ccc_v2/
```

dynamodb 当前的表结构是：
```
translate_mapping_aaa
translate_mapping_bbb
translate_mapping_ccc
```

为了支持多版本，需要将dynamodb的表结构改为：
```
translate_mapping_aaa
translate_mapping_aaa_v1
translate_mapping_aaa_v2
translate_mapping_bbb
translate_mapping_bbb_v1
translate_mapping_bbb_v2
translate_mapping_ccc
translate_mapping_ccc_v1
translate_mapping_ccc_v2
```

为了记录当前词表的活跃版本，需要增加一个表：tranlate_meta
key: dict_name
value: default, v1, v2

如何创建新版本？
如果 dict_name 不存在，则创建新版本 v1
如果 dict_name 存在，则创建新版本 v(x+1)

如何判断当前使用的版本？
1. 如果translate_meta表中存在dict_name，则使用该表中的version作为当前活跃版本
2. 如果translate_meta表中不存在dict_name，则使用default作为当前活跃版本




# 测试用例
1. 创建新词库 （✅）
2. 更新词库
  - 2.1 aa --> aa_v1（✅）
  - 2.2 aa_v1 --> aa_v2（✅）
3. 修改活跃版本
   - 3.1 修改活跃版本为v1 （✅）
   - 3.2 修改活跃版本为default（✅）
4. 查询词库
   - 4.1 查询只有Default版本的词库 （✅）
   - 4.2 查询有多个版本的词库 （✅）
5. 推理
    - 5.1 推理时DynamoDB中没有词库信息
    - 5.2 推理时DynamoDB中有词库信息，v1，v2
    - 5.3 推理时DynamoDB中有词库信息，default