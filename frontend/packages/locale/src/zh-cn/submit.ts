export default {
  Step: "步骤",
  Name: {
    Name: "名称",
    Title: "输入学件名称",
    Placeholder: "请输入学件名称",
    Description: "这是您将提交的学件的名称",
    Error: {
      AtLeast5Chars: "学件名称至少需要 5 个字符",
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
        Audio: "音频",
        Video: "视频",
      },
      DescriptionInput: {
        Name: "特征",
        Description: "描述",
        FeatureTips:
          "在左侧为每个特征填写描述，或在右侧粘贴 JSON 对象。澄清每个特征的描述将有助于您的学件适用于具有异构特征空间的任务。",
        FeatureTipsSmall:
          "为每个特征填写描述或粘贴 JSON 对象。澄清每个特征的描述将有助于您的学件适用于具有异构特征空间的任务。",
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
      DescriptionOutput: {
        Name: "输出",
        Description: "描述",
        LabelTips:
          "在左侧为每个输出维度填写描述，或在右侧粘贴 JSON 对象。澄清每个特征的描述将有助于您的学件适用于具有异构输出空间的任务。",
        LabelTipsSmall:
          "为每个输出维度填写描述或粘贴 JSON 对象。澄清每个特征的描述将有助于您的学件适用于具有异构输出空间的任务。",
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
      AtLeast10Chars: "描述至少需要 10 个字符",
    },
  },
  File: {
    File: "文件",
    Title: "上传模型和统计规约",
    DragFileHere: "拖拽{file}文件到此处",
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
