import { checkedFetch } from "../utils";

const BASE_URL = "./api/admin";

function listLearnware({ userId, page, limit }) {
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
  }).then((res) => res.json());
}

export { listLearnware };
