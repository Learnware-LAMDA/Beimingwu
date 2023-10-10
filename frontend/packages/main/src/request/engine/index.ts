import { checkedFetch } from "../utils";

const BASE_URL = "./api/engine";

export interface SemanticSpecification {
  Name: {
    Values: string;
    Type: string;
    Description: string;
  };
  Data: {
    Values: string[];
    Type: string;
    Description: string;
  };
  Task: {
    Values: string[];
    Type: string;
    Description: string;
  };
  Library: {
    Values: string[];
    Type: string;
    Description: string;
  };
  Scenario: {
    Values: string[];
    Type: string;
    Description: string;
  };
  Description: {
    Values: string;
    Type: string;
    Description: string;
  };
  Input: string;
  Output: string;
}

function downloadLearnware({ id }: { id: string }): Promise<Response> {
  return checkedFetch(`${BASE_URL}/download_learnware?learnware_id=${id}`);
}

function getLearnwareDetailById({ id }: { id: string }): Promise<Response> {
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
  name: string;
  dataType: string;
  taskType: string;
  libraryType: string;
  tagList: string[];
  files: File[];
  page: string;
  limit: string;
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
      fd.append("limit", limit);
      fd.append("page", page);
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
