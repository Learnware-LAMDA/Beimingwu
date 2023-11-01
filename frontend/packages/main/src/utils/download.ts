import { BACKEND_URL } from "../request";

function downloadLearnwareSync(id: string): void {
  const url = `${BACKEND_URL}/engine/download_learnware?learnware_id=${id}`;
  window.open(url);
}

export { downloadLearnwareSync };
