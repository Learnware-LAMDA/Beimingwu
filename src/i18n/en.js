export default {
  Page: {
    Home: "Home",
    Search: "Search",
    Submit: "Submit",
    Docs: "Docs",
    User: {
      User: "User",
      Login: "Login",
      Register: "Register",
      ChangePassword: "Change Password",
      MyLearnware: "My Learnware",
      ClientToken: "Client Token",
      Logout: "Logout",
    },
    Language: {
      Language: "Language",
      Chinese: "中文",
      English: "English",
    },
  },
  Home: {
    Cover: {
      SmallModelsDo: "Small models do",
      Big: "Big",
      Slogan:
        "Learnware paradigm systematically reuses numerous various models to do things that may even be beyond their original purposes, and enables users to easily identify and reuse helpful models, not need to build their models from scratch.",
      Try: "Try It Out",
      Submit: "Be A Developer",
    },
    What: {
      Title: "What is Learnware?",
      Description:
        "A learnware is a well-performed trained machine learning model with a specification which enables it to be adequately identified to reuse according to the requirement of future users who know nothing about the learnware in advance.",
    },
    Why: {
      Title: "Why do we need learnware?",
      Description:
        "There are complaints about current machine learning techniques such as the requirement of a huge amount of training data and proficient training skills, the difficulty of continual learning, the risk of catastrophic forgetting, the leaking of data privacy/proprietary, etc.",
      LackOfTrainingDataSkills: "Lack of training data/skills",
      LackOfTrainingDataSkillsDescription:
        "Strong machine learning models can be attained even for ordinary users with little training skills or small data, because the users can adapte or refine well-performed learnwares rather than building a model from scratch by themselves.",
      ContinualLearning: "Continual learning",
      ContinualLearningDescription:
        "The learnware market naturally realizes continual and lifelong learning, because with the constant submissions of well-performed learnwares trained from diverse tasks, the knowledge held in the learnware market is being continually enriched.",
      CatastrophicForgetting: "Catastrophic forgetting",
      CatastrophicForgettingDescription:
        "A learnware will always be accommodated in the learnware market once it is accepted, unless every aspect of its function can be replaced by other learnwares. Thus, the old knowledge in the learnware market is always held. Nothing to be forgotten.",
      DataPrivacyProprietary: "Data privacy/proprietary",
      DataPrivacyProprietaryDescription:
        "The developers only submit their models without sharing their own data, and thus, the data privacy/proprietary can be well preserved. Although one could not deny the possibility of reverse engineering the models, the risk would be too small compared with many other privacy-preserving solutions.",
    },
    How: {
      Title: "How does learnware work?",
      Description:
        "There are three important entities: developers, users, and the market. The developers are usually machine learning experts who produce and want to share/sell their well-performed trained machine learning models. The users need machine learning services but usually have only limited data and lack machine learning knowledge and skills. The learnware market accepts/buys well-performed trained models from developers, accommodates them in the market, and provides/sells services to users via identifying and reusing learnwares to help users tackle their present tasks.",
    },
    SpecificationWorld: {
      Title: "Specification world",
      Description:
        "Note that the specification islands, corresponding to models from different feature/label spaces, can be merged if their connections are discovered and established.",
    },
    Footer: {
      About: "About",
      Github: "Github",
      ContactUs: "Contact Us",
      RightClickToCopy: "Right click to copy",
      AllRightsReserved: "All rights reserved",
    },
  },
  Login: {
    Login: "Login",
    Email: "E-mail",
    Password: "Password",
    NoAccount: "Don't have an accounut?",
    RegisterFirst: "Register first",
    Success: "Login successfully",
    Error: {
      InvalidEmail: "Invalid e-mail address",
      PasswordAtLeast8Chars: "Password needs to be at least 8 characters.",
    },
  },
  Register: {
    Register: "Register",
    Username: "Username",
    Email: "E-mail",
    Password: "Password",
    ConfirmPassword: "Confirm Password",
    Error: {
      UsernameAtLeast2Chars: "Username needs to be at least 2 characters.",
      InvalidEmail: "Invalid e-mail address",
      PasswordAtLeast8Chars: "Password needs to be at least 8 characters.",
      PasswordNotEmpty: "Password must not be empty.",
      PasswordNotMatch: "The two passwords you entered do not match.",
    },
  },
  ChangePassword: {
    ChangePassword: "Change Password",
    OldPassword: "Old Password",
    NewPassword: "New Password",
    ConfirmNewPassword: "Confirm New Password",
    Change: "Change",
    Success: "Password changed successfully",
    Error: {
      NewPasswordAtLeast8Chars: "New password needs to be at least 8 characters.",
      NewPasswordNotMatch: "The two new passwords you entered do not match.",
    },
  },
  ClientToken: {
    Title: "Client Token",
    Description: "Tokens you have generated that can be used to access the learnware api.",
    Generate: "Generate",
  },
  Submit: {
    Step: "Step",
    Name: {
      Name: "Name",
      Title: "Type the name of your learnware",
      Placeholder: "Please type the name of your learnware",
      Description: "This is the name of your learnware you will submit",
      Error: {
        AtLeast5Chars: "Learnware name needs to be at least 5 characters.",
      },
    },
    Tag: {
      Tag: "Tag",
      Title: "Choose the tags (semantic specification)",
      DataType: {
        DataType: "Data Type",
        Error: {
          NotEmpty: "Data type must not be empty.",
        },
        Type: {
          Table: "Table",
          Image: "Image",
          Text: "Text",
          Audio: "Audio",
          Video: "Video",
        },
      },
      TaskType: {
        TaskType: "Task Type",
        Error: {
          NotEmpty: "Task type must not be empty.",
        },
        Type: {
          Classification: "Classification",
          Regression: "Regression",
          Clustering: "Clustering",
          Ranking: "Ranking",
          ObjectDetection: "Object Detection",
          FeatureExtraction: "Feature Extraction",
          Segmentation: "Segmentation",
          Others: "Others",
          OtherTask: "Other Task",
        },
      },
      LibraryType: {
        LibraryType: "Library Type",
        Error: {
          NotEmpty: "Library type must not be empty.",
        },
        Type: {
          PyTorch: "PyTorch",
          TensorFlow: "TensorFlow",
          "Scikit-learn": "Scikit-learn",
          Others: "Others",
          OtherLibrary: "Other Library",
        },
      },
      Scenario: {
        Scenario: "Scenario",
        Type: {
          Business: "Business",
          Financial: "Financial",
          Health: "Health",
          Politics: "Politics",
          Computer: "Computer",
          Internet: "Internet",
          Traffic: "Traffic",
          Nature: "Nature",
          Fashion: "Fashion",
          Industry: "Industry",
          Agriculture: "Agriculture",
          Education: "Education",
          Entertainment: "Entertainment",
          Architecture: "Architecture",
        },
      },
    },
    Description: {
      Description: "Description",
      Title: "Type the description of your learnware",
      Placeholder: "Please type the description of your learnware",
      Error: {
        AtLeast10Chars: "Description needs to be at least 10 characters.",
      },
    },
    File: {
      File: "File",
      Title: "Upload your model & statistical specification",
      DragFileHere: "Drag file here",
      ClickHere: "Click here",
      ForInstructionsOnHowToCreateTheRequiredZipFile:
        "For instructions on how to create the required zip file",
    },
    Navigation: {
      NextStep: "Next Step",
      PreviousStep: "Previous Step",
      Finish: "Finish",
    },
    Success: "Submit successfully",
  },
  Search: {
    Search: "Search",
    ChooseSemanticRequirement: "Choose semantic requirement",
    SearchByName: "Search by name",
    LearnwareName: "Learnware Name",
    UploadStatisticalRequirement: "Upload statistical requirement",
  },
};
