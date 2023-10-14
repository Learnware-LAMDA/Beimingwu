import { checkedFetch } from "../utils";
import { Response } from "types";

const BASE_URL = "./api/admin";

function listLearnware({
  page,
  limit,
  userId,
}: {
  userId: string;
  page: number;
  limit: number;
}): Promise<{
  code: number;
  msg: string;
  data: {
    learnware_list: Response.LearnwareDetailInfo[];
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
    }),
  })
    .then((res) => res.json())
    .then((json) => ({
      ...json,
      data: {
        ...json.data,
        learnware_list: json.data.learnware_list,
      },
    }));
}

export { listLearnware };
