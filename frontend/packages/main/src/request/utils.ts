import Store from "../store";
import Router from "../router";

function checkStatus(res: Response): Response {
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

function checkedFetch(url: string, options: RequestInit = {}): Promise<Response> {
  // get token from local storage and set in header
  const token = localStorage.getItem("token");

  if (options === undefined) {
    options = {};
  }

  if (token !== null) {
    options.headers = new Headers(options.headers || {});
    options.headers.set("Authorization", `Bearer ${token}`);
  }

  return fetch(url, options).then(checkStatus);
}

interface Fetch {
  (url: string, options?: RequestInit): Promise<Response>;
}

function useProgressedFetch(onProgress: (progress: number) => void): {
  progressedFetch: Fetch
} {
  const progressedFetch = (url: string, options: RequestInit = {}): Promise<Response> => {
    return new Promise<Response>((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open(options.method || "get", url);
      for (const k in options.headers || {}) {
        xhr.setRequestHeader(k, (options.headers as Headers).get(k) as string);
      }
      xhr.setRequestHeader("Authorization", `Bearer ${localStorage.getItem("token")}`);
      xhr.onload = (e): void => {
        const target = e.target as XMLHttpRequest;
        resolve(new Response(target.response, { status: target.status }));
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
      xhr.send(options.body as XMLHttpRequestBodyInit);
    }).then(checkStatus);
  };
  return { progressedFetch };
}

export { checkStatus, checkedFetch, useProgressedFetch };
