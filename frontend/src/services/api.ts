import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE,
});

export const authApi = {
  register: (data: { email: string; password: string; full_name: string; phone_number?: string }) =>
    api.post('/auth/register', data),
  
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  
  verifySMS: (email: string, code: string) =>
    api.post('/auth/verify-sms', { code }, { params: { email } }),
  
  resendSMS: (email: string) =>
    api.post('/auth/resend-sms', {}, { params: { email } }),
};

export const workspaceApi = {
  create: (token: string, data: any) =>
    api.post('/workspace/create', data, {
      headers: { Authorization: `Bearer ${token}` }
    }),
  
  list: (token: string) =>
    api.get('/workspace/list', {
      headers: { Authorization: `Bearer ${token}` }
    }),
  
  get: (token: string, workspaceId: number) =>
    api.get(`/workspace/${workspaceId}`, {
      headers: { Authorization: `Bearer ${token}` }
    }),
  
  activate: (token: string, workspaceId: number) =>
    api.post(`/workspace/${workspaceId}/activate`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    }),
};

export const contactsApi = {
  create: (token: string, workspaceId: number, data: any) =>
    api.post(`/contacts/${workspaceId}/create`, data, {
      headers: { Authorization: `Bearer ${token}` }
    }),
  
  list: (token: string, workspaceId: number) =>
    api.get(`/contacts/${workspaceId}/list`, {
      headers: { Authorization: `Bearer ${token}` }
    }),
};

export const bookingsApi = {
  create: (token: string, workspaceId: number, contactId: number, data: any) =>
    api.post(`/bookings/${workspaceId}/${contactId}/create`, data, {
      headers: { Authorization: `Bearer ${token}` }
    }),
  
  list: (token: string, workspaceId: number) =>
    api.get(`/bookings/${workspaceId}/list`, {
      headers: { Authorization: `Bearer ${token}` }
    }),
};

export const dashboardApi = {
  get: (token: string, workspaceId: number) =>
    api.get(`/dashboard/${workspaceId}`, {
      headers: { Authorization: `Bearer ${token}` }
    }),
};

export const inboxApi = {
  getConversations: (token: string, workspaceId: number) =>
    api.get(`/inbox/${workspaceId}/conversations`, {
      headers: { Authorization: `Bearer ${token}` }
    }),
  
  sendMessage: (token: string, workspaceId: number, conversationId: number, message: any) =>
    api.post(`/inbox/${workspaceId}/conversations/${conversationId}/send`, message, {
      headers: { Authorization: `Bearer ${token}` }
    }),
};
