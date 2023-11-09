import { checkedFetch, useProgressedFetch } from "../utils";
import { getSemanticSpecification } from "../engine";
import { BACKEND_URL } from "..";
import type {
  Name,
  DataType,
  TaskType,
  LibraryType,
  ScenarioList,
  Files,
  Description,
} from "@beiming-system/types/learnware";
import type { LearnwareDetailInfo } from "@beiming-system/types/response";

const BASE_URL = BACKEND_URL + "/user";

function getProfile(): Promise<{
  code: number;
  msg: string;
  data: {
    user_id: string;
    username: string;
    email: string;
    role: number;
  };
}> {
  return checkedFetch(`${BASE_URL}/profile`, {
    method: "POST",
  }).then((res) => res.json());
}

function changePassword({
  oldPasswordMd5,
  newPasswordMd5,
}: {
  oldPasswordMd5: string;
  newPasswordMd5: string;
}): Promise<{ code: number; msg: string }> {
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

function deleteLearnware({ id }: { id: string }): Promise<{
  code: number;
  msg: string;
}> {
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

function getLearnwareList({
  page,
  limit,
  isVerified,
}: {
  page: number;
  limit: number;
  isVerified: boolean | null;
}): Promise<{
  code: number;
  msg: string;
  data: {
    learnware_list: LearnwareDetailInfo[];
    page: number;
    limit: number;
    total_pages: number;
  };
}> {
  return checkedFetch(`${BASE_URL}/list_learnware`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      page,
      limit,
      is_verified: isVerified,
    }),
  }).then((res) => res.json());
}

function addLearnware({
  edit = false,
  name,
  dataType,
  taskType,
  libraryType,
  scenarioList,
  dataTypeDescription,
  taskTypeDescription,
  description,
  files,
  learnwareId,
  onProgress,
}: {
  edit?: boolean;
  name: Name;
  dataType: DataType;
  taskType: TaskType;
  libraryType: LibraryType;
  scenarioList: ScenarioList;
  dataTypeDescription: string;
  taskTypeDescription: string;
  description: Description;
  files: Files;
  learnwareId: string;
  onProgress: (progress: number) => void;
}): Promise<{ code: number; msg: string }> {
  const { progressedFetch } = useProgressedFetch(onProgress);

  return getSemanticSpecification()
    .then((res) => {
      const semanticSpec = res.data.semantic_specification;
      semanticSpec.Name.Values = name;
      semanticSpec.Data.Values = (dataType && [dataType]) || [];
      semanticSpec.Task.Values = (taskType && [taskType]) || [];
      semanticSpec.Library.Values = (libraryType && [libraryType]) || [];
      semanticSpec.Scenario.Values = scenarioList;
      semanticSpec.Description.Values = description;
      semanticSpec.Input = JSON.parse(dataTypeDescription);
      semanticSpec.Output = JSON.parse(taskTypeDescription);

      const fd = new FormData();
      fd.append("learnware_file", files[0].size === 0 ? "" : files[0]);
      fd.append("semantic_specification", JSON.stringify(semanticSpec));
      edit && learnwareId && fd.append("learnware_id", learnwareId);
      return fd;
    })
    .then((fd) =>
      edit
        ? progressedFetch(`${BASE_URL}/update_learnware`, {
            method: "POST",
            body: fd,
          })
        : progressedFetch(`${BASE_URL}/add_learnware`, {
            method: "POST",
            body: fd,
          }),
    )
    .then((res) => res.json());
}

function verifyLog({ learnware_id }: { learnware_id: string }): Promise<{ data: string }> {
  return checkedFetch(`${BASE_URL}/verify_log?learnware_id=${learnware_id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((res) => res.json());
}

function createToken(): Promise<{
  code: number;
  msg: string;
}> {
  return checkedFetch(`${BASE_URL}/create_token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((res) => res.json());
}

function listToken(): Promise<{
  code: number;
  msg: string;
  data: {
    token_list: string[];
  };
}> {
  return checkedFetch(`${BASE_URL}/list_token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((res) => res.json());
}

function deleteToken({ token }: { token: string }): Promise<{
  code: number;
  msg: string;
}> {
  return checkedFetch(`${BASE_URL}/delete_token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      token: token,
    }),
  }).then((res) => res.json());
}

export {
  getProfile,
  changePassword,
  deleteLearnware,
  getLearnwareList,
  addLearnware,
  verifyLog,
  createToken,
  listToken,
  deleteToken,
};
