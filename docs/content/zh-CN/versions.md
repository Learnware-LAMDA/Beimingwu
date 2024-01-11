# 版本公告

## 北冥坞 v1.0 版本 (2024.01)

北冥坞学件基座系统 v1.0 版本是学件范式的首次系统级实现，旨在帮助用户有效查搜和复用学件，而无需从零开始构建机器学习模型。

### v1.0 系统特点

1. **学件规约生成**：北冥坞系统在 `learnware` Python 包中提供规约生成接口，支持多种数据类型（表格、图像和文本），可以在本地高效生成。
2. **学件质量检测**：北冥坞系统内置了多重检测机制，以确保系统中每个学件的质量。
3. **学件多样查搜**：北冥坞系统同时支持语义规约和统计规约的查搜，覆盖的数据类型包括表格、图像、文本。另外，对于表格型任务，系统额外支持异构表格学件的查搜。
4. **学件本地部署**：北冥坞系统在 `learnware` Python 包中同时提供学件部署与学件复用的接口，帮助用户便捷、安全的部署与复用学件。
5. **数据隐私保护**：北冥坞系统所涉及的学件上传、查搜、部署均无需用户上传本地数据，所有涉及的统计规约均由用户本地生成，确保用户数据隐私。
6. **系统完全开源**：北冥坞系统所有的源码全部开源，包括 `learnware` Python 包与前后端代码。

### v1.0 研发团队

- 系统总负责：<a href="http://cs.nju.edu.cn/zhouzh" style="text-decoration: none; color: inherit;">周志华</a>、<a href="http://www.lamda.nju.edu.cn/yuy" style="text-decoration: none; color: inherit;">俞扬</a>
- 系统研发总负责：<a href="http://www.lamda.nju.edu.cn/tanzh/" style="text-decoration: none; color: inherit;">谭志豪</a>
- 系统总架构与开发：<a href="http://www.lamda.nju.edu.cn/liujd/" style="text-decoration: none; color: inherit;">刘建东</a>
- 引擎架构与开发：<a href="http://www.lamda.nju.edu.cn/bixd/" style="text-decoration: none; color: inherit;">毕晓栋</a>
- 引擎算法研发：<a href="http://www.lamda.nju.edu.cn/tanp/" style="text-decoration: none; color: inherit;">谭鹏</a>
- 前端设计与开发：<a href="http://www.lamda.nju.edu.cn/zhengqc/" style="text-decoration: none; color: inherit;">郑钦城</a>
- 后端架构与开发：邹晓川
- 算法开发与开源学件准备：<a href="http://www.lamda.nju.edu.cn/xiey/" style="text-decoration: none; color: inherit;">谢逸</a>、刘海天、史浩宇、张鑫宇