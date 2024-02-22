# Version Announcement

## Beimingwu v1.0 Version (2024.01)

The Beimingwu learnware dock system v1.0 version is the first systematic open-source implementation of _learnware_, offering a preliminary research platform for learnware-related studies.
The system is designed to help users efficiently solve machine learning tasks without starting from scratch by effectively searching for and reusing learnware(s).

### v1.0 System Features

1. **Learnware Specification Generation**: The Beimingwu system provides a specification generation tool in the `learnware` Python package, supporting multiple data types (tables, images, and text), and can be efficiently generated locally.
2. **Learnware Quality Detection**: The Beimingwu system has multiple detection mechanisms to ensure the quality of each learnware in the system.
3. **Diverse Learnware Search**: The Beimingwu system supports both semantic specification and statistical specification search, covering data types including tables, images, and text. Additionally, for tabular tasks, the system preliminarily supports the search of heterogeneous table learnwares.
4. **Local Learnware Deployment**: The Beimingwu system provides a unified user interface for learnware deployment and reuse in the `learnware` Python package, helping users to deploy and reuse arbitrary learnwares conveniently.
5. **Raw Data Protection**: The learnware submission, identification, and deployment of the Beimingwu system doesn't require users to upload raw data, and all involved statistical specifications are generated locally by users using open-source API.
6. **Open Source System**: The source code of the Beimingwu system, including the `learnware` Python package and frontend and backend codes, are open source.

### v1.0 R&D Team

The Beimingwu R&D (Research and Development) Team consists of <a href="http://cs.nju.edu.cn/zhouzh" style="text-decoration: none; color: inherit;" target="_blank">Zhi-Hua Zhou</a>, <a href="http://www.lamda.nju.edu.cn/yuy" style="text-decoration: none; color: inherit;" target="_blank">Yang Yu</a>, <a href="http://www.lamda.nju.edu.cn/tanzh/" style="text-decoration: none; color: inherit;" target="_blank">Zhi-Hao Tan</a>, <a href="http://www.lamda.nju.edu.cn/liujd/" style="text-decoration: none; color: inherit;" target="_blank">Jian-Dong Liu</a>, <a href="http://www.lamda.nju.edu.cn/tanp/" style="text-decoration: none; color: inherit;" target="_blank">Peng Tan</a>, <a href="http://www.lamda.nju.edu.cn/bixd/" style="text-decoration: none; color: inherit;" target="_blank">Xiao-Dong Bi</a>, <a href="http://www.lamda.nju.edu.cn/zhengqc/" style="text-decoration: none; color: inherit;" target="_blank">Qin-Cheng Zheng</a>, Xiao-Chuan Zou, <a href="http://www.lamda.nju.edu.cn/xiey/" style="text-decoration: none; color: inherit;" target="_blank">Yi Xie</a>, Hai-Tian Liu, Hao-Yu Shi, Xin-Yu Zhang and others. Additionally, <a href="https://www.lamda.nju.edu.cn/guolz/" style="text-decoration: none; color: inherit;" target="_blank">Lan-Zhe Guo</a>, <a href="http://www.lamda.nju.edu.cn/chenzx/" style="text-decoration: none; color: inherit;" target="_blank">Zi-Xuan Chen</a>, <a href="http://www.lamda.nju.edu.cn/zhouz/" style="text-decoration: none; color: inherit;" target="_blank">Zhi Zhou</a>, <a href="http://www.lamda.nju.edu.cn/jinyx/" style="text-decoration: none; color: inherit;" target="_blank">Yi-Xuan Jin</a>, and others also participated in the early prototype development.

<!-- System Principal: <a href="http://cs.nju.edu.cn/zhouzh" style="text-decoration: none; color: inherit;" target="_blank">Zhi-Hua Zhou</a>、<a href="http://www.lamda.nju.edu.cn/yuy" style="text-decoration: none; color: inherit;" target="_blank">Yang Yu</a>
- System R&D Principal: <a href="http://www.lamda.nju.edu.cn/tanzh/" style="text-decoration: none; color: inherit;" target="_blank">Zhi-Hao Tan</a>
- System Architect & Developer: <a href="http://www.lamda.nju.edu.cn/liujd/" style="text-decoration: none; color: inherit;" target="_blank">Jian-Dong Liu</a>
- Engine Architect & Developer: <a href="http://www.lamda.nju.edu.cn/bixd/" style="text-decoration: none; color: inherit;" target="_blank">Xiao-Dong Bi</a>
- Engine Algorithm R&D: <a href="http://www.lamda.nju.edu.cn/tanp/" style="text-decoration: none; color: inherit;" target="_blank">Peng Tan</a>
- Frontend Designer & Developer: <a href="http://www.lamda.nju.edu.cn/zhengqc/" style="text-decoration: none; color: inherit;" target="_blank">Qin-Cheng Zheng</a>
- Backend Architect & Developer: Xiao-Chuan Zou
- Algorithm Developer & Learnware Preparation: <a href="http://www.lamda.nju.edu.cn/xiey/" style="text-decoration: none; color: inherit;" target="_blank">Yi Xie</a>、Hai-Tian Liu、Hao-Yu Shi、Xin-Yu Zhang -->