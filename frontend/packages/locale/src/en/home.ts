export default {
  Cover: {
    Beiming: "Beimingwu: A Learnware Dock System",
    Introduction:
      'Beimingwu is the first systematic open-source implementation of learnware dock system, providing a preliminary research platform for learnware studies. Developers worldwide can submit their models freely to the learnware dock. They can generate specifications for the model with the help of Beimingwu without disclosing their raw data, and then the model and specification can be assembled into a learnware, which will be accommodated in the learnware dock. Future users can solve their tasks by submitting their requirements and reusing helpful learnwares returned by Beimingwu, while also not disclosing their own data. It is anticipated that after Beimingwu accumulates millions of learnwares, an "emergent" behavior may occur: machine learning tasks that have never been specifically tackled may be solved by assembling and reusing some existing learnwares. For more in-depth information, you can access the complete paper here: ',
    PaperLinkDescription: "Paper Link",
    CodeRepo: {
      Description: "Beimingwu is completely open-source. The related code repositories can be accessed by clicking: ",
      Beimingwu: "System Frontend & Backend",
      Learnware: "System Engine & Toolkit",
    },
    Try: "Try It Out",
    Submit: "Be A Developer",
    LearnwareName: "Learnware",
    LearnwareDescription: "This is a learnware.",
    ServeralLinesOfCode: "Solve Machine Learning Tasks",
    SolveYourTasks: "with a few lines",
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
      "A learnware is a well-performed trained model with a specification describing its capabilities. The specification includes a semantic specification in text and a statistical specification sketching the model's statistical information.",
    RKMESpecification: "RKME specification",
    SpecificationSpace: "Specification space",
    Learnware: "Learnware",
    LearnwareDescription: "This is a learnware.",
    Developer: "Developer",
    Updated: "Updated",
  },
  Function: {
    Title: "What are the main functions of Beimingwu?",
    Description:
      "The Beimingwu learnware dock system, serving as a preliminary research platform for the learnware paradigm, systematically accomplishes the entire process of learnware from submission to deployment as follows:",
    SearchAndDeploy: {
      Title: "Search and deploy learnwares: ",
      Description:
        "After the user submits the task requirements, Beimingwu will recommend learnwares that are helpful to the user's task according to the learnware specification and guide the user to deploy and reuse them.",
    },
    Submit: {
      Title: "Submit high-quality learnwares: ",
      Description:
        "Developers can submit various learnwares to Beimingwu freely, and the system will check the quality of these learnwares and organize them further.",
    },
  },
  Feature: {
    Title: "What are the features of Beimingwu?",
    Description:
      "The learnware dock system Beimingwu enables users to search learnware(s) using additional task-related statistical information, facilitating convenient deployment and reuse of learnwares, while not disclosing user's original data. Its scalable architecture offers a rich set of interfaces, supporting implementation of newly developed algorithms in research of learnware specifications, searching, organization, and reuse.",
    Recommendation: {
      Name: "Recommend models with statistical specification",
      Description:
        "Except for natural language descriptions, Beimingwu can utilize statistical information of tasks to recommend more targeted models. Besides, Beimingwu preliminarily supports searching and reusing models from different feature spaces for tabular tasks with baseline algorithm.",
      HomoTable: "Homogeneous table examples",
      HeteroTable: "Heterogeneous table examples",
    },
    loadAndReuse: {
      Name1: "A unified way to load and reuse learnwares conveniently",
      Name2: "",
      Description:
        "After the user obtains the learnwares from Beimingwu, Beimingwu allows for effortless deployment of arbitrary learnwares in a unified way based on containerized isolation, with little concerns about environment compatibility and safety. Also, Beimingwu provides several baseline reuse methods in a uniform format for convenient usage.",
    },
    Privacy: {
      Name: "Not disclosing user's raw data",
      Description:
        "To search helpful learnwares based on statistical information, instead of uploading raw data, user can generate and submit the statistical specification using API, which captures the data distribution while not disclosing the raw data.",
    },
    OpenSource: {
      Name: "Completely open-source: co-building the learnware ecosystem",
      Description:
        "Beimingwu is completely open-source. As the algorithms improve and the number of learnware increases, the capability of Beimingwu to solve tasks will be constantly enhanced. Beimingwu is still young, and we sincerely invite the open-source community to join us in developing and perfecting the system, uploading various models, and researching and improving learnware-related algorithms.",
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
    Git: "GitLink",
    GitHub: "GitHub",
    ContactUs: "Contact Us",
    UserAgreement: "User Agreement",
    PrivacyPolicy: "Privacy Policy",
    RightClickToCopy: "Right click to copy",
    AllRightsReserved: "All rights reserved",
  },
};
