- 代码介绍

  ```python
  .
  ├── offline_process
  │   ├── aos_write_job.py                 # 离线数据注入Glue python脚本，从s3写入到opensearch中的index
  │   ├── rag_based_translate.py           # 离线翻译的Glue python脚本，会根据关键词召回对应的term和映射关系
  │   └── batch_upload_docs.py             # 批量数据注入脚本，可以指定S3的路径，路径下的所有json文件都会摄入，可以控制并发
  ```