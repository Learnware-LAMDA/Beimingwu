import Store from "../store";
import Router from "../router";

function checkStatus(res) {
  if (res.status === 200) {
    return res;
  }
  if (res.status === 401) {
    // Unauthorized
    Router.push("/login");
    Store.commit("setLoggedIn", false);
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
    if (!("headers" in options)) {
      options.headers = {};
    }
    options.headers["Authorization"] = `Bearer ${token}`;
  }

  return fetch(url, options).then(checkStatus);
}

function useProgressedFetch(onProgress) {
  const progressedFetch = (url, options) => {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open(options.method || "get", url);
      for (const k in options.headers || {}) {
        xhr.setRequestHeader(k, options.headers[k]);
      }
      xhr.setRequestHeader("Authorization", `Bearer ${localStorage.getItem("token")}`);
      xhr.onload = (e) => {
        resolve(e.target);
      };
      xhr.onerror = reject;
      if (xhr.upload) {
        xhr.upload.addEventListener(
          "progress",
          (e) => {
            if (e.lengthComputable) {
              onProgress(e.loaded / e.total);
            }
          },
          false,
        );
      }
      xhr.send(options.body);
    })
      .then(checkStatus)
      .then((res) => ({
        json() {
          return JSON.parse(res.responseText);
        },
      }));
  };
  return { progressedFetch };
}

export { checkStatus, checkedFetch, useProgressedFetch };
