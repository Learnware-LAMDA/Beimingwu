export default {
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
  SemanticSpecification: {
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
      },
      DescriptionInput: {
        Name: "Feature",
        Description: "Description",
        FeatureTips:
          "Fill in the description for each feature on the left or paste a JSON object on the right. Clarifying the description for each feature will help your learnware to be available for tasks with hetergenous feature space.",
        FeatureTipsSmall:
          "Fill in the description for each feature or paste a JSON object. Clarifying the description for each feature will help your learnware to be available for tasks with hetergenous feature space.",
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
        "Object Detection": "Object Detection",
        "Feature Extraction": "Feature Extraction",
        Segmentation: "Segmentation",
        Others: "Others",
        OtherTask: "Other Task",
      },
      DescriptionOutput: {
        Name: "Label",
        Description: "Description",
        LabelTips:
          "Fill in the description for each label on the left or paste a JSON object on the right. Clarifying the description for each label will help your learnware to be available for tasks with hetergenous label space.",
        LabelTipsSmall:
          "Fill in the description for each label or paste a JSON object. Clarifying the description for each label will help your learnware to be available for tasks with hetergenous label space.",
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
        Others: "Others",
        OtherScenario: "Other Scenario",
      },
      Error: {
        NotEmpty: "Scenario list must not be empty.",
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
    DragFileHere: "Drag {file} file here",
    ClickHere: "Click here",
    ForInstructionsOnHowToCreateTheRequiredZipFile:
      "for instructions on how to create the required zip file",
    ToDownloadTemplate: "to download a template",
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
  Example: {
    Examples: "Examples",
    ExamplesDescription: "We provide some examples for you to refer to.",
    HomogeneousExamples: "Homogeneous Examples",
    HeterogeneousExamples: "Heterogeneous Examples",
    Table: "Table",
    Image: "Image",
    Text: "Text",
  },
  Submiting: "Submiting, please wait...",
  Success: "Submit successfully",
};
