function downloadLearnware(id) {
  const url = `/api/engine/download_learnware?learnware_id=${id}`;
  window.open(url);
}

export { downloadLearnware };
