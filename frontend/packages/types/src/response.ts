import { SemanticSpecification } from "./learnware";

export interface LearnwareInfo {
  learnware_id: string;
  semantic_specification: SemanticSpecification;
}

export interface LearnwareDetailInfo extends LearnwareInfo {
  last_modify: string;
  verify_status: string;
}

export interface LearnwareDetailInfoWithUserId extends LearnwareInfo {
  user_id: string;
  last_modify: string;
  verify_status: string;
}

export interface LearnwareSearchInfo extends LearnwareInfo {
  last_modify: string;
  username: string;
  matching: number;
}
