# SearchEngine-demo

## 基于倒排索引的网络搜索引擎（精简版）
+ 通过爬虫程序爬取人民网英文版（http://en.people.cn）上的新闻，获取包括新闻链接（URL）、新闻标题和新闻正文等内容
+ 对爬取的新闻语料进行清洗，包括分词，去停用词等，并保存新闻链接到新闻语料的映射；在搭建好的Hadoop集群上实现基于MapReduce计算模型的倒排索引构造；将倒排索引存储在Mysql数据库并创建基于term列（即单词）的索引，以加快检索效率
+ 实现一个简易的新闻搜索Web应用，后端基于Django框架开发，主要实现对前端请求的响应，通过前端发送的query检索倒排索引并返回对应的新闻链接和内容；前端基于Vue框架开发，内容比较简洁

