export type Name = string;
export type DataType = "Table" | "Image" | "Text" | "Video" | "Audio" | "";
export type TaskType =
  | "Classification"
  | "Regression"
  | "Clustering"
  | "Ranking"
  | "Object Detection"
  | "Feature Extraction"
  | "Segmentation"
  | "Others";
export type LibraryType = "PyTorch" | "TensorFlow" | "scikit" | "Scikit-learn" | "Others";
export type Tag =
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
export type TagList = Tag[];
export type Description = string;

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
    Values: TagList;
  };
  Description: {
    Values: Description;
  };
}