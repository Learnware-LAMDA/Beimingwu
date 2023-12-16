export default {
  Cover: {
    Beiming: "北冥坞：学件基座系统",
    Introduction:
      "学件由表现良好的模型和描述其能力的规约构成。北冥坞系统以便捷的方式帮助缺乏机器学习资源/经验的用户通过复用推荐学件解决机器学习任务。",
    Try: "学件查搜",
    Submit: "学件上传",
    LearnwareName: "学件",
    LearnwareDescription: "这是一个学件。",
    Developer: "开发者",
    ServeralLinesOfCode: "几行代码",
    SolveYourTasks: "解决您的任务",
    Example: {
      Simplified: "简化示例",
      Single: "单模型示例",
      Multiple: "多模型示例",
    },
  },
  What: {
    Title: "学件是什么？",
    Description:
      "学件由性能优良的机器学习模型和描述模型的规约组成。规约刻画了模型的能力，使得模型在未来能够根据用户需求被充分识别和复用。规约由两部分构成：语义规约通过文本描述模型的功能，而统计规约刻画模型所蕴含的统计信息。",
    RKMESpecification: "RKME规约",
    SpecificationSpace: "规约空间",
    Learnware: "学件",
    LearnwareDescription: "这是一个学件。",
    Developer: "开发者",
    Updated: "更新于",
  },
  Function: {
    Title: "北冥坞系统的主要功能是什么？",
    SearchAndDeploy: {
      Title: "查搜部署学件：",
      Description:
        "当用户提交任务需求后，学件基座系统会根据学件规约推荐对用户任务有帮助的学件并指导用户进行部署和复用。",
    },
    Submit: {
      Title: "提交优质学件：",
      Description:
        "开发者可以自发地提交各式各样的学件到学件基座系统，而系统会对这些学件进行质量检查和进一步的组织。",
    },
  },
  Feature: {
    Title: "北冥坞系统有哪些特点？",
    Description:
      "通过对学件的系统组织，北冥坞系统能够帮助用户额外使用任务的统计信息进行精准地学件查搜，帮助用户安全地部署学件，便捷地复用学件；并且充分保护用户的数据隐私。",
    Recommendation: {
      Name: "利用统计信息的查搜能推荐更有效的模型",
      Description:
        "通过利用统计信息，北冥坞系统可以为您的任务提供更加精准的模型推荐，这些模型往往具有更好的复用性能。即使北冥坞系统里不存在一个模型能较好的解决您的问题，多个模型的组合可能足以解决。对于表格型任务，系统初步支持查搜（和复用）特征空间不对齐的模型。",
      HomoTable: "同构表格示例",
      HeteroTable: "异构表格示例",
    },
    loadAndReuse: {
      Name1: "安全的学件加载",
      Name2: "便捷的学件复用",
      Description:
        "获取学件后，您无需为模型运行的环境烦恼，也无需担心恶意代码和恶意攻击，一行代码即可安全加载学件，同时系统提供多种接口帮助您复用学件以解决任务。",
    },
    Privacy: {
      Name: "我们非常关心您的隐私",
      Description:
        "如果您可以提供任务的统计信息，这将帮助您的需求或者模型被更好的匹配。统计规约可以在保护您原始数据不被泄露的情况下提供任务的统计信息。生成统计规约的过程在本地进行且代码公开。",
    },
    OpenSource: {
      Name: "北冥坞系统完全开源",
      Description:
        "北冥坞系统是首个完全开源的模型平台，引擎、前端、后端完全开源，支持多种部署方式。我们诚邀社区体验使用系统并共同开发完善系统。",
    },
  },
  Why: {
    Title: "为什么需要学件基座系统？",
    Description:
      "当前的机器学习技术面临着诸多问题，例如需要大量的训练数据和高超的训练技巧、持续学习的困境、灾难性遗忘的风险以及数据隐私/所有权的泄漏等。学件基座系统为上述问题提供了统一的解决方案。",
    LackOfTrainingDataSkills: "缺乏训练数据/技能",
    LackOfTrainingDataSkillsDescription:
      "即使对于数据量较小或缺乏训练技能的普通用户，也可以获得强大的机器学习模型，因为用户可以从学件基座系统中获取性能优良的学件，并进一步调整和改进，而不必自己从头开始构建模型。",
    ContinualLearning: "持续学习",
    ContinualLearningDescription:
      "随着在各种不同任务上训练得到的、性能优良的学件加入到学件市场，学件基座系统中的知识将不断丰富，进而自然地实现持续和终身学习。",
    CatastrophicForgetting: "灾难性遗忘",
    CatastrophicForgettingDescription:
      "一旦学件被接收，它将永远容纳在学件基座系统中，除非其各方面被其他学件占优。因此，学件基座系统中的旧知识总是会被保留，而不会被遗忘。",
    DataPrivacyProprietary: "数据隐私/所有权",
    DataPrivacyProprietaryDescription:
      "开发者只提交模型而不共享私有数据，因此数据隐私/所有权可以得到很好的保护。尽管无法完全排除对模型进行逆向工程的可能性，但与许多其它隐私保护方案相比，学件基座系统泄露隐私的风险非常小。",
  },
  How: {
    Title: "学件基座系统是如何工作的？",
    Description:
      "学件基座系统是学件范式的核心实体。学件范式共有三个重要实体：开发者、用户和学件基座系统。开发者通常是机器学习专家，他们构建并希望分享/出售他们性能优良的机器学习模型。用户需要机器学习服务，但通常只拥有有限的数据，并且缺乏机器学习知识和技能。学件基座系统从开发者那里接收性能优良的机器学习模型，将它们纳入系统，并通过识别和复用学件向用户提供服务，以帮助用户解决当前的任务。",
  },
  SpecificationWorld: {
    Title: "规约世界",
    Description:
      "来自不同特征/标记空间学件的规约，构成各种各样的规约岛屿，所有规约岛屿共同构成学件基座系统中的规约世界。在规约世界中，如果能够发现并建立不同岛屿之间的联系，那么对应的规约岛屿可以进行合并。",
  },
  Footer: {
    About: "关于我们",
    Github: "Github",
    ContactUs: "联系我们",
    UserAgreement: "用户协议",
    PrivacyPolicy: "隐私政策",
    RightClickToCopy: "右键复制",
    AllRightsReserved: "版权所有",
  },
};
