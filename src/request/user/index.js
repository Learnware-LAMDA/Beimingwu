import { checkedFetch } from "../utils";
import { getSemanticSpecification } from "../engine";

const BASE_URL = "./api/user";

function changePassword({ oldPasswordMd5, newPasswordMd5 }) {
  return checkedFetch(`${BASE_URL}/change_password`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      old_password: oldPasswordMd5,
      new_password: newPasswordMd5,
    }),
  }).then((res) => res.json());
}

function deleteLearnware({ id }) {
  return checkedFetch(`${BASE_URL}/delete_learnware`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      learnware_id: id,
    }),
  }).then((res) => res.json());
}

function getLearnwareList({ page, limit }) {
  return checkedFetch(`${BASE_URL}/list_learnware`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      page,
      limit,
    }),
  }).then((res) => res.json());
}

function addLearnware({ name, dataType, taskType, libraryType, tagList, description, files }) {
  return getSemanticSpecification()
    .then((res) => {
      const semanticSpec = res.data.semantic_specification;
      semanticSpec.Name.Values = name;
      semanticSpec.Data.Values = (dataType && [dataType]) || [];
      semanticSpec.Task.Values = (taskType && [taskType]) || [];
      semanticSpec.Library.Values = (libraryType && [libraryType]) || [];
      semanticSpec.Scenario.Values = tagList;
      semanticSpec.Description.Values = description;

      const fd = new FormData();
      fd.append("learnware_file", files[0]);
      fd.append("semantic_specification", JSON.stringify(semanticSpec));
      return fd;
    })
    .then((fd) =>
      checkedFetch(`${BASE_URL}/add_learnware`, {
        method: "POST",
        body: fd,
      }),
    )
    .then((res) => res.json());
}

export { changePassword, deleteLearnware, getLearnwareList, addLearnware };
