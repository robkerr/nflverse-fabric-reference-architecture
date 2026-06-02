"use client";

import { useMsal, useIsAuthenticated } from "@azure/msal-react";
import { loginRequest, apiBaseUrl } from "../authConfig";
import { InteractionRequiredAuthError } from "@azure/msal-browser";

export function useApi() {
  const { instance, accounts } = useMsal();

  async function getAccessToken(): Promise<string> {
    const account = accounts[0];
    if (!account) throw new Error("No authenticated account");

    try {
      const response = await instance.acquireTokenSilent({
        ...loginRequest,
        account,
      });
      return response.accessToken;
    } catch (error) {
      if (error instanceof InteractionRequiredAuthError) {
        const response = await instance.acquireTokenPopup(loginRequest);
        return response.accessToken;
      }
      throw error;
    }
  }

  async function apiFetch<T>(path: string, params?: Record<string, string>): Promise<T> {
    const token = await getAccessToken();
    const url = new URL(path, apiBaseUrl);
    if (params) {
      Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));
    }

    const response = await fetch(url.toString(), {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`API error ${response.status}: ${text}`);
    }

    return response.json();
  }

  return { apiFetch, getAccessToken };
}

export { useIsAuthenticated };
