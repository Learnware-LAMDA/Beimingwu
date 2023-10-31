import { BACKEND_URL } from "@main/request";

function downloadLearnware(id: string): void {
  const url = `${BACKEND_URL}/engine/download_learnware?learnware_id=${id}`;
  window.open(url);
}

export { downloadLearnware };
