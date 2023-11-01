import { BACKEND_URL } from "@main/request";

function downloadLearnwareSync(id: string): void {
  const url = `${BACKEND_URL}/download_learnware?learnware_id=${id}`;
  window.open(url);
}

export { downloadLearnwareSync };
