export default {
  Step: "步骤",
  Name: {
    Name: "名称",
    Title: "输入学件名称",
    Placeholder: "请输入学件名称",
    Description: "这是您将提交的学件的名称",
    Error: {
      FewerThan5Chars: "学件名称至少需要 5 个字符",
      MoreThan50Chars: "学件名称不能超过 50 个字符",
    },
  },
  SemanticSpecification: {
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
      },
      DescriptionInput: {
        Name: "输入",
        Description: "描述",
        InputTips:
          "请在左侧为每个特征填写描述，或在右侧粘贴 JSON 对象。描述清楚每一维特征有助于您的学件应用异构特征空间的任务。",
        InputTipsSmall:
          "请为每个特征填写描述或粘贴 JSON 对象。描述清楚每个特征有助于您的学件应用异构特征空间的任务。",
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
        "Object Detection": "目标检测",
        "Feature Extraction": "特征提取",
        Segmentation: "分割",
        Others: "其他",
        OtherTask: "其他任务",
      },
      DescriptionOutput: {
        Name: "输出",
        Description: "描述",
        OutputTipsClassification:
          "请在左侧为每个分类标记（从 0 开始编号）填写描述，或在右侧粘贴 JSON 对象。描述清楚每一维输出有助于您的学件应用异构输出空间的任务。",
        OutputTipsSmallClassification:
          "请为每个分类标记（从 0 开始编号）填写描述或粘贴 JSON 对象。描述清楚每一维输出有助于您的学件应用异构输出空间的任务。",
        OutputTipsRegression:
          "请在左侧为每个输出维度填写描述，或在右侧粘贴 JSON 对象。描述清楚每一维输出有助于您的学件应用异构输出空间的任务。",
        OutputTipsSmallRegression:
          "请为每个输出维度填写描述或粘贴 JSON 对象。描述清楚每一维输出有助于您的学件应用异构输出空间的任务。",
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
        Others: "其他",
        OtherScenario: "其他应用场景",
      },
      Error: {
        NotEmpty: "应用场景不能为空",
      },
    },
    License: {
      License: "开源协议",
      Type: {
        Others: "其他",
        OtherLicense: "其他开源协议",
      },
      Error: {
        NotEmpty: "开源协议不能为空",
      },
    },
  },
  Description: {
    Description: "描述",
    Title: "输入学件的描述",
    Placeholder: "请输入学件的描述",
    Error: {
      FewerThan10Chars: "描述至少需要 10 个字符",
      MoreThan10000Chars: "描述不能超过 10000 个字符",
    },
  },
  File: {
    File: "文件",
    Title: "上传模型和统计规约",
    DragFileHere: "拖拽 {file} 文件到此处",
    ClickHere: "点击此处",
    ForInstructionsOnHowToCreateTheRequiredZipFile: "查看如何创建所需的 zip 文件",
    ToDownloadTemplate: "下载模板学件",
    YourOldLearnware: "您的旧学件文件",
    Error: {
      NoFile: "请上传模型和统计规约",
      NotZipFile: "请上传 zip 文件",
      GreaterThan1GB: "请上传小于 1GB 的文件",
      FileNotFound: "找不到文件 {filename}",
      FileNotJSON: "文件 {filename} 不是 JSON 文件",
      KeyNotFoundInFile: "文件 {filename} 中找不到键 '{key}'",
      KeyEmptyInFile: "文件 {filename} 中的键 '{key}' 为空",
      KeyNotFoundOrEmptyInFile: "文件 {filename} 中的键 '{key}' 不存在或为空",
      KeyNotNonEmptyArrayInFile: "文件 {filename} 中的键 '{key}' 不是非空数组",
    },
  },
  Navigation: {
    NextStep: "下一步",
    PreviousStep: "上一步",
    Finish: "完成",
  },
  Submiting: "正在上传，请等待...",
  Success: "提交成功",
};
