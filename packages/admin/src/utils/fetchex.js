import Router from '@/router/index';
import store from '@main/store'


function fetchex(url, options) {

  const token = localStorage.getItem("token")  
  if (token !== null) {
      if (options === undefined) {
          options = {};
      }
      if (!("headers" in options)) {
          options.headers = {};
      }
      options.headers["Authorization"] = `Bearer ${token}`;
  }
  return fetch(url, options).then((response) => {

    if (response.status === 200) {
      return response
    } 
    else if (response.status === 401) {
        // Unauthorized
        Router.push("/login");
        store.commit("setLoggedIn", false)
    }
    else{
        throw new Error(`Network error: ${response.status}${response.statusText ? ` - ${response.statusText}` : ""}`);
    }
  })
}


export { fetchex };