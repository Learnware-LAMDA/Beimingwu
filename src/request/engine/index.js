import { checkedFetch } from "../utils";

function downloadLearnware({ id }) {
  return checkedFetch(`/api/engine/download_learnware?learnware_id=${id}`);
}

function getLearnwareDetailById({ id }) {
  return checkedFetch(`/api/engine/get_learnware_info?learnware_id=${id}`).then((res) =>
    res.json(),
  );
}

function getSemanticSpecification() {
  return checkedFetch("/api/engine/get_semantic_specification").then((res) => res.json());
}

function searchLearnware({ name, dataType, taskType, libraryType, tagList, files, page, limit }) {
  return getSemanticSpecification()
    .then((res) => {
      const semanticSpec = res.data.semantic_specification;
      semanticSpec.Name.Values = name || "";
      semanticSpec.Data.Values = (dataType && [dataType]) || [];
      semanticSpec.Task.Values = (taskType && [taskType]) || [];
      semanticSpec.Library.Values = (libraryType && [libraryType]) || [];
      semanticSpec.Scenario.Values = (tagList && tagList.map((tag) => tag.id)) || [];
      semanticSpec.Description.Values = "";

      const fd = new FormData();
      fd.append("semantic_specification", JSON.stringify(semanticSpec));
      fd.append("statistical_specification", (files.length > 0 && files[0]) || null);
      fd.append("limit", limit);
      fd.append("page", page);
      return fd;
    })
    .then((fd) =>
      checkedFetch("/api/engine/search_learnware", {
        method: "POST",
        body: fd,
      }),
    )
    .then((res) => res.json());
}

export { downloadLearnware, getLearnwareDetailById, getSemanticSpecification, searchLearnware };
