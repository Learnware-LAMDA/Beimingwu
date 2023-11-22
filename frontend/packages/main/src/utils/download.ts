import { BACKEND_URL } from "../request";

function downloadLearnwareSync(id: string): void {
  const url = `${BACKEND_URL}/engine/download_learnware?learnware_id=${id}`;
  window.open(url);
}

function downloadMultipleLearnwaresSync(ids: string[]): void {
  const url = `${BACKEND_URL}/engine/download_multi_learnware?${ids
    .map((id) => `learnware_ids=${id}`)
    .join("&")}`;
  window.open(url);
}

export { downloadLearnwareSync, downloadMultipleLearnwaresSync };
