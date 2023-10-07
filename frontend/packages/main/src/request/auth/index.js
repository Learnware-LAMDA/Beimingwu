import { checkedFetch } from "../utils";

const BASE_URL = "./api/auth";

function login({ email, passwordMd5 }) {
  return checkedFetch(`${BASE_URL}/login`, {
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
  return checkedFetch(`${BASE_URL}/logout`, {
    method: "POST",
  }).then((res) => res.json());
}

function register({ username, email, passwordMd5 }) {
  return checkedFetch(`${BASE_URL}/register`, {
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
  return checkedFetch(`${BASE_URL}/get_role`, {
    method: "POST",
  }).then((res) => res.json());
}

function verifyEmail(params) {
  return checkedFetch(`${BASE_URL}/email_confirm?` + params, {
    method: "POST",
  }).then((res) => res.json());
}

function resendEmail(email) {
  return checkedFetch(`${BASE_URL}/resend_email_confirm`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
    }),
  }).then((res) => res.json());  
}

export { login, logout, register, getRole, verifyEmail, resendEmail };
