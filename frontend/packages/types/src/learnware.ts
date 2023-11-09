export type Name = string;
export type DataType = "Table" | "Image" | "Text";
export type TaskType =
  | "Classification"
  | "Regression"
  | "Object Detection"
  | "Feature Extraction"
  | "Segmentation"
  | "Others";
export type LibraryType = "PyTorch" | "TensorFlow" | "Scikit-learn" | "Others";
export type Scenario =
  | "Business"
  | "Financial"
  | "Health"
  | "Politics"
  | "Computer"
  | "Internet"
  | "Traffic"
  | "Nature"
  | "Fashion"
  | "Industry"
  | "Agriculture"
  | "Education"
  | "Entertainment"
  | "Architecture";
export type ScenarioList = Scenario[];
export type Description = string;
export type DataTypeDescription = {
  Dimension: number;
  Description: Record<number, string>;
};
export type TaskTypeDescription = {
  Dimension: number;
  Description: Record<number, string>;
};
export type Files = File[];

export interface SemanticSpecification {
  Name: {
    Values: Name;
  };
  Data: {
    Values: DataType[];
  };
  Task: {
    Values: TaskType[];
  };
  Library: {
    Values: LibraryType[];
  };
  Scenario: {
    Values: ScenarioList;
  };
  Description: {
    Values: Description;
  };
  Input: DataTypeDescription;
  Output: DataTypeDescription;
}

export interface LearnwareInfo {
  id: string;
  name: Name | "";
  description: Description;
  dataType: DataType | "";
  taskType: TaskType | "";
  libraryType: LibraryType | "";
  scenarioList: ScenarioList;
}

export interface LearnwareDetailInfo extends LearnwareInfo {
  lastModify: string;
  verifyStatus: string;
}

export interface LearnwareDetailInfoWithDescription extends LearnwareInfo {
  lastModify: string;
  verifyStatus: string;
  input: DataTypeDescription;
  output: TaskTypeDescription;
}

export interface LearnwareSingleSearchInfo extends LearnwareInfo {
  lastModify: string;
  username: string;
  matchScore: number;
}

export interface LearnwareMultiSearchInfo extends LearnwareInfo {
  lastModify: string;
  username: string;
}

export interface LearnwareCardInfo extends LearnwareInfo {
  username?: string;
  lastModify: string;
  verifyStatus?: string;
  matchScore?: number;
}

export interface Filter {
  id: string;
  name: Name;
  dataType: DataType | "";
  taskType: TaskType | "";
  libraryType: LibraryType | "";
  scenarioList: ScenarioList;
  files: Files;
}
