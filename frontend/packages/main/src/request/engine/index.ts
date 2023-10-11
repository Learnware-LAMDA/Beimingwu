import { checkedFetch } from "../utils";
import {
  Name,
  DataType,
  TaskType,
  LibraryType,
  TagList,
  SemanticSpecification,
} from "types/learnware";

const BASE_URL = "./api/engine";

function downloadLearnware({ id }: { id: string }): Promise<Response> {
  return checkedFetch(`${BASE_URL}/download_learnware?learnware_id=${id}`);
}

function getLearnwareDetailById({ id }: { id: string }): Promise<{
  code: number;
  msg: string;
  data: {
    learnware_info: {
      semantic_specification: SemanticSpecification;
    };
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
  tagList,
  files,
  page,
  limit,
}: {
  name: Name
  dataType: DataType;
  taskType: TaskType;
  libraryType: LibraryType;
  tagList: TagList;
  files: File[];
  page: number;
  limit: number;
}): Promise<Response> {
  return getSemanticSpecification()
    .then((res) => {
      const semanticSpec = res.data.semantic_specification;
      semanticSpec.Name.Values = name || "";
      semanticSpec.Data.Values = (dataType && [dataType]) || [];
      semanticSpec.Task.Values = (taskType && [taskType]) || [];
      semanticSpec.Library.Values = (libraryType && [libraryType]) || [];
      semanticSpec.Scenario.Values = (tagList && tagList.map((tag) => tag)) || [];
      semanticSpec.Description.Values = "";

      const fd = new FormData();
      fd.append("semantic_specification", JSON.stringify(semanticSpec));
      fd.append("statistical_specification", (files.length > 0 && files[0]) || "");
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
