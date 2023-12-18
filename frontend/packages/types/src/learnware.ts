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
  | "Architecture"
  | "Others";
export type ScenarioList = Scenario[];
export type License =
  | "MIT"
  | "Apache-2.0"
  | "BSD-2-Clause"
  | "BSD-3-Clause"
  | "GPL-2.0"
  | "GPL-3.0"
  | "LGPL-2.1"
  | "LGPL-3.0"
  | "AGPL-3.0"
  | "ECL-2.0"
  | "AFL-3.0"
  | "CC-BY-4.0"
  | "CC-BY-SA-4.0"
  | "Others";
export type LicenseList = License[];
export type Description = string;
export type InputDescription = {
  Dimension: number;
  Description: Record<number, string>;
};
export type OutputDescription = {
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
  License: {
    Values: LicenseList;
  };
  Description: {
    Values: Description;
  };
  Input: InputDescription;
  Output: OutputDescription;
}

export interface LearnwareInfo {
  id: string;
  name: Name | "";
  description: Description;
  dataType: DataType | "";
  taskType: TaskType | "";
  libraryType: LibraryType | "";
  scenarioList: ScenarioList;
  licenseList: LicenseList;
}

export interface LearnwareDetailInfo extends LearnwareInfo {
  lastModify: string;
  verifyStatus: string;
}

export interface LearnwareDetailInfoWithDescription extends LearnwareInfo {
  lastModify: string;
  verifyStatus: string;
  input: InputDescription;
  output: OutputDescription;
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
  licenseList: LicenseList;
  files: Files;
  inputDescription?: InputDescription;
  outputDescription?: OutputDescription;
}
