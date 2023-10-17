import { checkedFetch } from "../utils";

const BASE_URL = "./api/auth";

function login({
  email,
  passwordMd5,
}: {
  email: string;
  passwordMd5: string;
}): Promise<{ code: number; msg: string; data: { token: string } }> {
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

function logout(): Promise<{
  code: number;
  msg: string;
}> {
  return checkedFetch(`${BASE_URL}/logout`, {
    method: "POST",
  }).then((res) => res.json());
}

function register({
  username,
  email,
  passwordMd5,
}: {
  username: string;
  email: string;
  passwordMd5: string;
}): Promise<{
  code: number;
  msg: string;
}> {
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

function getRole(): Promise<{ code: number; msg: string }> {
  return checkedFetch(`${BASE_URL}/get_role`, {
    method: "POST",
  }).then((res) => res.json());
}

function verifyEmail(params: string): Promise<{ code: number; msg: string }> {
  return checkedFetch(`${BASE_URL}/email_confirm?` + params, {
    method: "POST",
  }).then((res) => res.json());
}

function resendEmail(email: string): Promise<{
  code: number;
  msg: string;
}> {
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

function sendResetPasswordEmail(
  email: string,
): Promise<{ code: number; msg: string}> {
  return checkedFetch(`${BASE_URL}/send_reset_password_email`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
    }),
  }).then((res) => res.json());
}

function resetPassword(
  verificationCode: string,
  userId: string
): Promise<{ code: number; msg: string; data: {password: string}}> {
  return checkedFetch(`${BASE_URL}/reset_password`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      code: verificationCode,
      user_id: userId,
    }),
  }).then((res) => res.json());
}

export { login, logout, register, getRole, verifyEmail, resendEmail, sendResetPasswordEmail, resetPassword };
