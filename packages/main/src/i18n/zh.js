export default {
  Page: {
    Home: "首页",
    Search: "查搜",
    Submit: "提交",
    Docs: "文档",
    User: {
      User: "用户",
      Login: "登录",
      Register: "注册",
      ChangePassword: "修改密码",
      MyLearnware: "我的学件",
      ClientToken: "客户端令牌",
      Logout: "登出",
    },
    Language: {
      Language: "语言",
      Chinese: "中文",
      English: "English",
    },
    LearnwareDetail: "学件详情",
    Summary: "概览",
    Learnwares: "所有学件",
    Users: "所有用户",
  },
  Home: {
    Cover: {
      SmallModelsDo: "小模型做",
      Big: "大事",
      Slogan:
        "学件范式系统地重用大量不同的模型来完成甚至可能超出其原始目的的事情，并使用户能够轻松识别和重用有用的模型，而不需要从头开始构建模型。",
      Try: "小试牛刀",
      Submit: "大展身手",
    },
    What: {
      Title: "什么是学件？",
      Description:
        "学习件是一种性能良好的训练有素的机器学习模型，其规范使其能够根据预先对学习件一无所知的未来用户的需求进行充分识别并重用。",
    },
    Why: {
      Title: "为什么我们需要学件？",
      Description:
        "当前的机器学习技术存在许多问题，例如需要大量的训练数据和熟练的训练技巧，持续学习的困难，灾难性遗忘的风险，数据隐私/信息的泄漏等。",
      LackOfTrainingDataSkills: "缺乏训练数据/技能",
      LackOfTrainingDataSkillsDescription:
        "即使对于缺乏训练技能或数据量较小的普通用户，也可以获得强大的机器学习模型，因为用户可以调整或改进性能良好的学件，而不是自己从头开始构建模型。",
      ContinualLearning: "持续学习",
      ContinualLearningDescription:
        "学件市场自然实现了持续和终身学习，因为随着不断提交的性能良好的学件，学件市场中的知识正在不断丰富。",
      CatastrophicForgetting: "灾难性遗忘",
      CatastrophicForgettingDescription:
        "一旦学件被接受，它将永远被容纳在学件市场中，除非其功能的每个方面都可以被其他学件替换。因此，学件市场中的旧知识总是被保留。没有什么可遗忘的。",
      DataPrivacyProprietary: "数据隐私/信息",
      DataPrivacyProprietaryDescription:
        "开发人员只提交他们的模型而不共享自己的数据，因此，数据隐私/信息可以得到很好的保护。尽管人们不能否认通过逆向工程模型的可能性，但与许多其他保护隐私的解决方案相比，风险太小了。",
    },
    How: {
      Title: "学件是如何工作的？",
      Description:
        "有三个重要的实体：开发人员，用户和市场。开发人员通常是机器学习专家，他们生产并希望分享/出售他们的性能良好的训练有素的机器学习模型。用户需要机器学习服务，但通常只有有限的数据并且缺乏机器学习知识和技能。学件市场从开发人员那里接受/购买性能良好的训练模型，将其容纳在市场中，并通过识别和重用学件来帮助用户解决当前任务，向用户提供/销售服务。",
    },
    SpecificationWorld: {
      Title: "规约世界",
      Description:
        "如果不同规约时间的联系被发现，则对应于来自不同特征/标签空间的模型规约岛可以合并。",
    },
    Footer: {
      About: "关于我们",
      Github: "Github",
      ContactUs: "联系我们",
      RightClickToCopy: "右键复制",
      AllRightsReserved: "版权所有",
    },
  },
  Login: {
    Login: "登录",
    Email: "邮箱",
    Password: "密码",
    NoAccount: "没有账号？",
    RegisterFirst: "请先注册",
    Success: "登录成功",
    Error: {
      InvalidEmail: "邮箱格式不正确",
      PasswordAtLeast8Chars: "密码至少需要8个字符",
    },
  },
  Register: {
    Register: "注册",
    Username: "用户名",
    Email: "邮箱",
    Password: "密码",
    ConfirmPassword: "确认密码",
    Error: {
      UsernameAtLeast2Chars: "用户名至少需要2个字符",
      InvalidEmail: "邮箱格式不正确",
      PasswordAtLeast8Chars: "密码至少需要8个字符",
      PasswordNotEmpty: "密码不能为空",
      PasswordNotMatch: "两次输入的密码不一致",
    },
  },
  ChangePassword: {
    ChangePassword: "修改密码",
    OldPassword: "旧密码",
    NewPassword: "新密码",
    ConfirmNewPassword: "确认新密码",
    Change: "修改",
    Success: "密码修改成功",
    Error: {
      NewPasswordAtLeast8Chars: "新密码至少需要8个字符",
      NewPasswordNotMatch: "两次输入的新密码不一致",
    },
  },
  ClientToken: {
    Title: "客户端令牌",
    Description: "您已生成的可用于访问学件api的令牌。",
    Generate: "生成",
  },
  Submit: {
    Step: "步骤",
    Name: {
      Name: "名称",
      Title: "输入学件名称",
      Placeholder: "请输入学件名称",
      Description: "这是您将提交的学件的名称",
      Error: {
        AtLeast5Chars: "学件名称至少需要5个字符",
      },
    },
    Tag: {
      Tag: "标签",
      Title: "选择学件的标签（语义规约）",
      DataType: {
        DataType: "数据类型",
        Error: {
          NotEmpty: "数据类型不能为空",
        },
        Type: {
          Table: "表格",
          Image: "图像",
          Text: "文本",
          Audio: "音频",
          Video: "视频",
        },
        DescriptionInput: {
          Name: "特征",
          FeatureTips:
            "在左侧为每个特征填写描述，或在右侧粘贴JSON对象。澄清每个特征的描述将有助于您的学件适用于具有异构特征空间的任务。",
          FeatureTipsSmall:
            "为每个特征填写描述或粘贴JSON对象。澄清每个特征的描述将有助于您的学件适用于具有异构特征空间的任务。",
        },
      },
      TaskType: {
        TaskType: "任务类型",
        Error: {
          NotEmpty: "任务类型不能为空",
        },
        Type: {
          Classification: "分类",
          Regression: "回归",
          Clustering: "聚类",
          Ranking: "排序",
          ObjectDetection: "目标检测",
          FeatureExtraction: "特征提取",
          Segmentation: "分割",
          Others: "其他",
          OtherTask: "其他任务",
        },
        DescriptionInput: {
          Name: "输出",
          Description: "描述",
          FeatureTips:
            "在左侧为每个输出维度填写描述，或在右侧粘贴JSON对象。澄清每个特征的描述将有助于您的学件适用于具有异构输出空间的任务。",
          FeatureTipsSmall:
            "为每个输出维度填写描述或粘贴JSON对象。澄清每个特征的描述将有助于您的学件适用于具有异构输出空间的任务。",
        },
      },
      LibraryType: {
        LibraryType: "库类型",
        Error: {
          NotEmpty: "库类型不能为空",
        },
        Type: {
          PyTorch: "PyTorch",
          TensorFlow: "TensorFlow",
          "Scikit-learn": "Scikit-learn",
          Others: "其他",
          OtherLibrary: "其他库",
        },
      },
      Scenario: {
        Scenario: "应用场景",
        Type: {
          Business: "商业",
          Financial: "金融",
          Health: "医疗",
          Politics: "政治",
          Computer: "计算机",
          Internet: "互联网",
          Traffic: "交通",
          Nature: "自然",
          Fashion: "时尚",
          Industry: "工业",
          Agriculture: "农业",
          Education: "教育",
          Entertainment: "娱乐",
          Architecture: "建筑",
        },
      },
    },
    Description: {
      Description: "描述",
      Title: "输入学件的描述",
      Placeholder: "请输入学件的描述",
      Error: {
        AtLeast10Chars: "描述至少需要10个字符",
      },
    },
    File: {
      File: "文件",
      Title: "上传模型和统计规约",
      DragFileHere: "拖拽文件到此处",
      ClickHere: "点击此处",
      ForInstructionsOnHowToCreateTheRequiredZipFile: "查看如何创建所需的zip文件",
    },
    Navigation: {
      NextStep: "下一步",
      PreviousStep: "上一步",
      Finish: "完成",
    },
    Success: "提交成功",
  },
  Search: {
    Search: "查搜",
    ChooseSemanticRequirement: "选择语义需求",
    SearchByName: "按名称查找",
    LearnwareName: "学件名称",
    UploadStatisticalRequirement: "上传统计需求",
  },
  Learnware: {
    OopsThereNoLearnware: "哦豁，这里没有学件。",
  },
  Public: {
    Description: "描述",
  },
};
