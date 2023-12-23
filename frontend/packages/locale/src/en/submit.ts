export default {
  Step: "Step",
  Name: {
    Name: "Name",
    Step: {
      Title: "Step 1",
      SubTitle: "Name",
    },
    Title: "Type the name of your learnware",
    Placeholder: "Please type the name of your learnware",
    Description: "This is the name of your learnware you will submit",
    Error: {
      FewerThan5Chars: "Learnware name needs to be at least 5 characters.",
      MoreThan50Chars: "Learnware name cannot be longer than 50 characters.",
    },
  },
  SemanticSpecification: {
    Step: {
      Title: "Step 2",
      SubTitle: "Tag",
    },
    Title: "Choose the tags (semantic specification)",
    DataType: {
      DataType: "Data type",
      Error: {
        NotEmpty: "Data type must not be empty.",
      },
      Type: {
        Table: "Table",
        Image: "Image",
        Text: "Text",
      },
      DescriptionInput: {
        Name: "Input",
        Description: "Description",
        InputTips:
          "Please fill in the description for each feature on the left or paste a JSON object on the right. Clarifying the description for each feature will help your learnware to be available for tasks with heterogenous feature space.",
        InputTipsSmall:
          "Please fill in the description for each feature or paste a JSON object. Clarifying the description for each feature will help your learnware to be available for tasks with heterogenous feature space.",
      },
    },
    TaskType: {
      TaskType: "Task type",
      Error: {
        NotEmpty: "Task type must not be empty.",
      },
      Type: {
        Classification: "Classification",
        Regression: "Regression",
        "Object Detection": "Object Detection",
        "Feature Extraction": "Feature Extraction",
        Segmentation: "Segmentation",
        Others: "Others",
        OtherTask: "Other Task",
      },
      DescriptionOutput: {
        Name: "Output",
        Description: "Description",
        OutputTipsClassification:
          "Please fill in the description for each class label (numbered from 0) on the left or paste a JSON object on the right. Clarifying the description for each label will help your learnware to be available for tasks with heterogenous output space.",
        OutputTipsSmallClassification:
          "Please fill in the description for each class label (numbered from 0) or paste a JSON object. Clarifying the description for each label will help your learnware to be available for tasks with heterogenous output space.",
        OutputTipsRegression:
          "Please fill in the description for each output dimension on the left or paste a JSON object on the right. Clarifying the description for each output dimension will help your learnware to be available for tasks with heterogenous output space.",
        OutputTipsSmallRegression:
          "Please fill in the description for each output dimension or paste a JSON object. Clarifying the description for each output dimension will help your learnware to be available for tasks with heterogenous output space.",
      },
    },
    LibraryType: {
      LibraryType: "Library type",
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
        Others: "Others",
        OtherScenario: "Other Scenario",
      },
      Error: {
        NotEmpty: "Scenario list must not be empty.",
      },
    },
    License: {
      License: "License",
      Type: {
        Others: "Others",
        OtherLicense: "Other License",
      },
      Error: {
        NotEmpty: "License must not be empty.",
      },
    },
  },
  Description: {
    Description: "Description",
    Step: {
      Title: "Step 3",
      SubTitle: "Description",
    },
    Title: "Type the description of your learnware",
    Placeholder: "Please type the description of your learnware",
    Error: {
      FewerThan10Chars: "Description needs to be at least 10 characters.",
      MoreThan10000Chars: "Description cannot be longer than 10000 characters.",
    },
  },
  File: {
    Step: {
      Title: "Step 4",
      SubTitle: "File",
    },
    Title: "Upload your model & statistical specification",
    DragFileHere: "Drag {file} file here",
    ClickHere: "Click here",
    ForInstructionsOnHowToCreateTheRequiredZipFile:
      "for instructions on how to create the required zip file",
    ToDownloadTemplate: "to download a learnware template ",
    YourOldLearnware: "Your old learnware",
    Error: {
      NoFile: "Please upload your model & statistical specification.",
      NotZipFile: "Please upload a zip file.",
      GreaterThan1GB: "Please upload a file smaller than 1GB.",
      FileNotFound: "File {filename} not found",
      FileNotJSON: "File {filename} is not a JSON file",
      KeyNotFoundInFile: "Key '{key}' not found in file {filename}",
      KeyEmptyInFile: "Key '{key}' is empty in file {filename}",
      KeyNotFoundOrEmptyInFile: "Key '{key}' not found or empty in file {filename}",
      KeyNotNonEmptyArrayInFile: "Key '{key}' is not an non-empty array in file {filename}",
    },
  },
  Navigation: {
    NextStep: "Next Step",
    PreviousStep: "Previous Step",
    Finish: "Finish",
  },
  Submiting: "Submiting, please wait...",
  Success: "Submit successfully",
};
