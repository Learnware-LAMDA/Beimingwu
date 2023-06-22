function checkStatus(res) {
  if (res.status === 200) {
    return res;
  }
  throw new Error(`Network error: ${res.status}${res.statusText ? ` - ${res.statusText}` : ""}`);
}

function checkedFetch(url, options) {
  return fetch(url, options).then(checkStatus);
}

export { checkStatus, checkedFetch };
