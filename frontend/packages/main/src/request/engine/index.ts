import { checkedFetch } from "../utils";
import type {
  Name,
  DataType,
  TaskType,
  LibraryType,
  ScenarioList,
  Files,
  SemanticSpecification,
} from "@beiming-system/types/learnware";
import type { LearnwareDetailInfo, LearnwareSearchInfo } from "@beiming-system/types/response";
import { BACKEND_URL } from "..";

const BASE_URL = BACKEND_URL + "/engine";

function downloadLearnware({ id }: { id: string }): Promise<Response> {
  return checkedFetch(`${BASE_URL}/download_learnware?learnware_id=${id}`);
}

function getLearnwareDetailById({ id }: { id: string }): Promise<{
  code: number;
  msg: string;
  data: {
    learnware_info: LearnwareDetailInfo;
  };
}> {
  return checkedFetch(`${BASE_URL}/learnware_info?learnware_id=${id}`).then((res) => res.json());
}

function getSemanticSpecification(): Promise<{
  data: {
    semantic_specification: SemanticSpecification;
  };
}> {
  return checkedFetch(`${BASE_URL}/semantic_specification`).then((res) => res.json());
}

function searchLearnware({
  name,
  dataType,
  taskType,
  libraryType,
  scenarioList,
  files,
  isVerified,
  heterogeneousMode,
  page,
  limit,
}: {
  name: Name;
  dataType: DataType | "";
  taskType: TaskType | "";
  libraryType: LibraryType | "";
  scenarioList: ScenarioList;
  files: Files;
  isVerified: boolean;
  heterogeneousMode: boolean;
  page: number;
  limit: number;
}): Promise<{
  code: number;
  msg: string;
  data: {
    learnware_list_single: LearnwareSearchInfo[];
    learnware_list_multi: LearnwareSearchInfo[];
    total_pages: number;
  };
}> {
  return getSemanticSpecification()
    .then((res) => {
      const semanticSpec = res.data.semantic_specification;
      semanticSpec.Name.Values = name || "";
      semanticSpec.Data.Values = (dataType && [dataType]) || [];
      semanticSpec.Task.Values = (taskType && [taskType]) || [];
      semanticSpec.Library.Values = (libraryType && [libraryType]) || [];
      semanticSpec.Scenario.Values =
        (scenarioList && scenarioList.map((scenario) => scenario)) || [];
      semanticSpec.Description.Values = "";

      const fd = new FormData();
      fd.append("semantic_specification", JSON.stringify(semanticSpec));
      fd.append("statistical_specification", (files.length > 0 && files[0]) || "");
      fd.append("heterogeneous_mode", String(heterogeneousMode));
      fd.append("is_verified", String(isVerified));
      fd.append("limit", String(limit));
      fd.append("page", String(page));
      return fd;
    })
    .then((fd) =>
      checkedFetch(`${BASE_URL}/search_learnware`, {
        method: "POST",
        body: fd,
      }),
    )
    .then((res) => res.json());
}

export { downloadLearnware, getLearnwareDetailById, getSemanticSpecification, searchLearnware };
