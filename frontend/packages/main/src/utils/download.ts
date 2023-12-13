import { checkedFetch } from "../request";
import { BACKEND_URL } from "../constants";

function downloadLearnwareSync(id: string): Promise<void> {
  return checkedFetch(`${BACKEND_URL}/engine/generate_download_token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      learnware_ids: [id],
    }),
  })
    .then((res) => res.json())
    .then((res) => {
      if (res.code === 0) {
        const url = `${BACKEND_URL}/engine/download_by_token?token=${res.data.token}`;
        window.open(url);
      } else {
        throw new Error(res.msg);
      }
    });
}

function downloadMultipleLearnwaresSync(ids: string[]): Promise<void> {
  return checkedFetch(`${BACKEND_URL}/engine/generate_download_token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      learnware_ids: ids,
    }),
  })
    .then((res) => res.json())
    .then((res) => {
      if (res.code === 0) {
        const url = `${BACKEND_URL}/engine/download_multi_learnware_by_token?token=${res.data.token}`;
        window.open(url);
      } else {
        throw new Error(res.msg);
      }
    });
}

export { downloadLearnwareSync, downloadMultipleLearnwaresSync };
