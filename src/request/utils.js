function checkStatus(res) {
  if (res.status === 200) {
    return res;
  }
  throw new Error(`Network error: ${res.status}${res.statusText ? ` - ${res.statusText}` : ""}`);
}

function checkedFetch(url, options) {
  // get token from local storage and set in header
  const token = localStorage.getItem("token");

  if (options === undefined) {
    options = {};
  }

  if (token !== null) {
    // check header exist
    if (!('headers' in options)) {
      options.headers = {};
    }
    options.headers["Authorization"] = `Bearer ${token}`;
  }

  return fetch(url, options).then(checkStatus);
}

export { checkStatus, checkedFetch };
