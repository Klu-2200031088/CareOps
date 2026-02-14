import { create } from 'zustand';

interface AuthState {
  token: string | null;
  user: any | null;
  setAuth: (token: string, user: any) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: typeof window !== 'undefined' ? localStorage.getItem('token') : null,
  user: null,
  setAuth: (token: string, user: any) => {
    localStorage.setItem('token', token);
    set({ token, user });
  },
  logout: () => {
    localStorage.removeItem('token');
    set({ token: null, user: null });
  },
}));

interface WorkspaceState {
  currentWorkspace: any | null;
  setWorkspace: (workspace: any) => void;
}

export const useWorkspaceStore = create<WorkspaceState>((set) => ({
  currentWorkspace: null,
  setWorkspace: (workspace: any) => set({ currentWorkspace: workspace }),
}));
