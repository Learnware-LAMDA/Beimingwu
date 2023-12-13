import { checkedFetch } from "../utils";
import type { LearnwareDetailInfo } from "@beiming-system/types/response";
import { BACKEND_URL } from "../../constants";

const BASE_URL = BACKEND_URL + "/admin";

function listLearnware({
  page,
  limit,
  isVerified,
  userId,
}: {
  userId: string;
  page: number;
  isVerified: boolean | null;
  limit: number;
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
      user_id: userId,
      page,
      limit,
      is_verified: isVerified,
    }),
  })
    .then((res) => res.json())
    .then((json) => ({
      ...json,
      data: {
        ...json.data,
        learnware_list: json.data.learnware_list_single,
      },
    }));
}

function deleteLearnware(id: string): Promise<{ code: number; msg: string }> {
  return checkedFetch(BACKEND_URL + "/admin/delete_learnware", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      learnware_id: id,
    }),
  }).then((res) => res.json());
}

export { listLearnware, deleteLearnware };
