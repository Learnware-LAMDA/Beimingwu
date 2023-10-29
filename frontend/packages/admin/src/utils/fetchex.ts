import Router from "../router";
import store from "@main/store";

async function fetchex(url: string, options: RequestInit = {}): Promise<Response | undefined> {
  const token = localStorage.getItem("token");
  if (token !== null) {
    options.headers = new Headers(options.headers || {});
    options.headers.set("Authorization", `Bearer ${token}`);
  }
  return fetch(url, options).then((response) => {
    if (response.status === 200) {
      return response;
    }
    if (response.status === 401) {
      // Unauthorized
      Router.push("/login");
      store.dispatch("logout");
      return;
    }
    throw new Error(
      `Network error: ${response.status}${response.statusText ? ` - ${response.statusText}` : ""}`,
    );
  });
}

export { fetchex };
