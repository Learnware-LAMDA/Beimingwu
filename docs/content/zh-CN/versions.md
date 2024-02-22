# 版本公告

## 北冥坞 v1.0 版本 (2024.01)

北冥坞学件基座系统 v1.0 版本是学件的第一个系统性开源实现，为学件相关研究提供了一个初步科研平台。该系统旨在通过查搜和复用学件，帮助用户便捷解决机器学习任务，而无需从零开始构建机器学习模型。

### v1.0 系统特点

1. **学件规约生成**：北冥坞系统在 `learnware` Python 包中提供规约生成接口，支持多种数据类型（表格、图像和文本），可以在本地高效生成。
2. **学件质量检测**：北冥坞系统内置了多重检测机制，以确保系统中每个学件的质量。
3. **学件多样查搜**：北冥坞系统同时支持语义规约和统计规约的查搜，覆盖的数据类型包括表格、图像、文本。另外，对于表格型任务，系统额外支持初步的异构表格学件查搜。
4. **学件本地部署**：北冥坞系统在 `learnware` Python 包中提供统一的学件部署与复用的接口，帮助用户便捷的使用学件。
5. **保护原始数据**：北冥坞系统所涉及的学件上传、查搜、部署均无需用户上传本地数据，生成统计规约的过程在用户本地进行且代码公开。
6. **面向社区开源**：北冥坞系统面向社区开源，包括 `learnware` Python 包与前后端代码。

### v1.0 研发团队

北冥坞研发团队人员包括：<a href="http://cs.nju.edu.cn/zhouzh" style="text-decoration: none; color: inherit;" target="_blank">周志华</a>、<a href="http://www.lamda.nju.edu.cn/yuy" style="text-decoration: none; color: inherit;" target="_blank">俞扬</a>、<a href="http://www.lamda.nju.edu.cn/tanzh/" style="text-decoration: none; color: inherit;" target="_blank">谭志豪</a>、<a href="http://www.lamda.nju.edu.cn/liujd/" style="text-decoration: none; color: inherit;" target="_blank">刘建东</a>、<a href="http://www.lamda.nju.edu.cn/tanp/" style="text-decoration: none; color: inherit;" target="_blank">谭鹏</a>、<a href="http://www.lamda.nju.edu.cn/bixd/" style="text-decoration: none; color: inherit;" target="_blank">毕晓栋</a>、<a href="http://www.lamda.nju.edu.cn/zhengqc/" style="text-decoration: none; color: inherit;" target="_blank">郑钦城</a>、邹晓川、<a href="http://www.lamda.nju.edu.cn/xiey/" style="text-decoration: none; color: inherit;" target="_blank">谢逸</a>、刘海天、史浩宇、张鑫宇等人，此外，<a href="https://www.lamda.nju.edu.cn/guolz/" style="text-decoration: none; color: inherit;" target="_blank">郭兰哲</a>、<a href="http://www.lamda.nju.edu.cn/chenzx/" style="text-decoration: none; color: inherit;" target="_blank">陈梓轩</a>、<a href="http://www.lamda.nju.edu.cn/zhouz/" style="text-decoration: none; color: inherit;" target="_blank">周植</a>、<a href="http://www.lamda.nju.edu.cn/jinyx/" style="text-decoration: none; color: inherit;" target="_blank">金苡萱</a>等人也参与了早期的原型研发。

<!-- 系统总负责：<a href="http://cs.nju.edu.cn/zhouzh" style="text-decoration: none; color: inherit;" target="_blank">周志华</a>、<a href="http://www.lamda.nju.edu.cn/yuy" style="text-decoration: none; color: inherit;" target="_blank">俞扬</a>
- 系统研发负责：<a href="http://www.lamda.nju.edu.cn/tanzh/" style="text-decoration: none; color: inherit;" target="_blank">谭志豪</a>
- 系统架构与开发：<a href="http://www.lamda.nju.edu.cn/liujd/" style="text-decoration: none; color: inherit;" target="_blank">刘建东</a>
- 引擎架构与开发：<a href="http://www.lamda.nju.edu.cn/bixd/" style="text-decoration: none; color: inherit;" target="_blank">毕晓栋</a>
- 引擎算法研发：<a href="http://www.lamda.nju.edu.cn/tanp/" style="text-decoration: none; color: inherit;" target="_blank">谭鹏</a>
- 前端设计与开发：<a href="http://www.lamda.nju.edu.cn/zhengqc/" style="text-decoration: none; color: inherit;" target="_blank">郑钦城</a>
- 后端架构与开发：邹晓川
- 算法开发与开源学件准备：<a href="http://www.lamda.nju.edu.cn/xiey/" style="text-decoration: none; color: inherit;" target="_blank">谢逸</a>、刘海天、史浩宇、张鑫宇 -->