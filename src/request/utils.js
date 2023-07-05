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

export { checkStatus, checkedFetch };
