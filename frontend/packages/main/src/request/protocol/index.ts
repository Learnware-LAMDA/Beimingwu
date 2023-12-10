import { BACKEND_URL } from "..";

function showUserAgreement(): void {
  window.open(`${BACKEND_URL}/protocol/user_agreement`);
}

function showPrivacyPolicy(): void {
  window.open(`${BACKEND_URL}/protocol/privacy_policy`);
}

export { showUserAgreement, showPrivacyPolicy };
