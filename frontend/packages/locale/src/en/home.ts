export default {
  Cover: {
    Beiming: "Beimingwu: A Learnware Dock System",
    Introduction:
      "A learnware is composed of a well-performed trained machine learning model and a specification which enables it to be adequately identified and reused according to the requirement of future users who know nothing about the learnware in advance. Beimingwu is a learnware dock system that helps users lacking machine learning resources/skills to solve machine learning tasks by reusing recommended learnwares in a convenient way.",
    Try: "Try It Out",
    Submit: "Be A Developer",
    LearnwareName: "Learnware",
    LearnwareDescription: "This is a learnware.",
    ServeralLinesOfCode: "Solve Your Tasks",
    SolveYourTasks: "with several lines of code",
    Developer: "Developer",
    Example: {
      Simplified: "Simplified demo",
      Single: "Single learnware demo",
      Multiple: "Multiple learnwares demo",
    },
  },
  What: {
    Title: "What is Learnware?",
    Description:
      "A learnware is a well-performed trained machine learning model with a specification which enables it to be adequately identified to reuse according to the requirement of future users who know nothing about the learnware in advance.",
    RKMESpecification: "RKME specification",
    SpecificationSpace: "Specification space",
    Learnware: "Learnware",
    LearnwareDescription: "This is a learnware.",
    Developer: "Developer",
    Updated: "Updated",
  },
  Function: {
    Title: "What are the main functions of Beimingwu?",
    SearchAndDeploy:
      "Search and deploy learnwares: After the user submits the task requirements, Beimingwu will recommend learnwares that are helpful to the user's task according to the learnware specification and guide the user to deploy and reuse them.",
    Submit:
      "Submit high-quality learnwares: Developers can spontaneously submit various learnwares to Beimingwu, and the system will check the quality of these learnwares and organize them further.",
  },
  Feature: {
    Title: "System Features",
    Recommendation: {
      Name: "Recommend more effective models with statistical information",
      Description:
        "By utilizing statistical information, Beimingwu can provide more accurate model recommendations for your tasks, which often have better reusability. Even if there is no model in Beimingwu that can solve your problem well, the combination of multiple models may be enough. For tabular tasks, the system initially supports searching (and reusing) models with feature space misalignment.",
      HomoTable: "Homogeneous table examples",
      HeteroTable: "Heterogeneous table examples",
    },
    loadAndReuse: {
      Name1: "Secure learnware loading and",
      Name2: "convenient learnware reuse",
      Description:
        "After obtaining the learnware, you don't need to worry about the environment in which the model runs, nor do you need to worry about malicious code and malicious attacks. You can safely load the learnware with one line of code, and the system provides multiple interfaces to help you reuse the learnware to solve the task.",
    },
    Privacy: {
      Name: "We care about your privacy",
      Description:
        "If you can provide the statistical information of the task, this will help your requirements or models be better matched. The statistical specification can provide the statistical information of the task without leaking your original data. The process of generating the statistical specification is performed locally and the code is open source.",
    },
    OpenSource: {
      Name: "Beimingwu is completely open source",
      Description:
        "Beimingwu is the first completely open-source model platform. The engine, front-end, and back-end are completely open-source and support multiple deployment methods. We sincerely invite the community to experience and use the system and jointly develop and improve the system.",
    },
  },
  Why: {
    Title: "Why is a learnware dock system necessary?",
    Description:
      "There are complaints about current machine learning techniques such as the requirement of a huge amount of training data and proficient training skills, the difficulty of continual learning, the risk of catastrophic forgetting, the leaking of data privacy/proprietary, etc. The learnware dock system provides a unified solution to the aforementioned issues.",
    LackOfTrainingDataSkills: "Lack of training data/skills",
    LackOfTrainingDataSkillsDescription:
      "Strong machine learning models can be attained even for ordinary users with little training skills or limited data, because the users can acquire well-performed learnwares from the learnware dock system and further adapt or refine them, instead of starting from scratch.",
    ContinualLearning: "Continual learning",
    ContinualLearningDescription:
      "The learnware dock system naturally realizes continual and lifelong learning, because with the constant submissions of well-performed learnwares trained from diverse tasks, the knowledge held in the learnware dock system is being continually enriched.",
    CatastrophicForgetting: "Catastrophic forgetting",
    CatastrophicForgettingDescription:
      "A learnware will always be accommodated in the learnware dock system once it is accepted, unless every aspect of its function can be replaced by other learnwares. Thus, the old knowledge in the learnware dock system is always held. Nothing to be forgotten.",
    DataPrivacyProprietary: "Data privacy/proprietary",
    DataPrivacyProprietaryDescription:
      "The developers only submit their models without sharing their own data, and thus, the data privacy/proprietary can be well preserved. Although one could not deny the possibility of reverse engineering the models, the risk would be too small compared with many other privacy-preserving solutions.",
  },
  How: {
    Title: "How does the learnware dock system work?",
    Description:
      "The learnware dock system is the core entity within the learnware paradigm, which encompasses three key entities: developers, users, and the learnware dock system. The developers are usually machine learning experts who produce and want to share/sell their well-performed trained machine learning models. The users need machine learning services but usually have only limited data and lack machine learning knowledge and skills. The learnware dock system accepts well-performed trained models from developers, accommodates them in the system, and provides services to users via identifying and reusing learnwares to help users tackle their present tasks.",
  },
  SpecificationWorld: {
    Title: "Specification world",
    Description:
      "The specifications of models from different feature/label spaces constitute various specification islands, and all specification islands together constitute the specification world in the learnware dock system. In this world, if connections between different islands can be discovered and established, the corresponding specification islands can be merged.",
  },
  Footer: {
    About: "About",
    Github: "Github",
    ContactUs: "Contact Us",
    UserAgreement: "User Agreement",
    PrivacyPolicy: "Privacy Policy",
    RightClickToCopy: "Right click to copy",
    AllRightsReserved: "All rights reserved",
  },
};
