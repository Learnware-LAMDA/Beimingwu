import { checkedFetch } from "../utils";

function login({ email, passwordMd5 }) {
  return checkedFetch("/api/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
      password: passwordMd5,
    }),
  }).then((res) => res.json());
}

function logout() {
  return checkedFetch("/api/auth/logout", {
    method: "POST",
  }).then((res) => res.json());
}

function register({ username, email, passwordMd5 }) {
  return checkedFetch("/api/auth/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username,
      email,
      password: passwordMd5,
    }),
  }).then((res) => res.json());
}

function getRole() {
  return checkedFetch("/api/auth/get_role", {
    method: "POST",
  }).then((res) => res.json());
}

export { login, logout, register, getRole };
