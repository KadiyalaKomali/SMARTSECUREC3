import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'admin' | 'security' | 'manager';
  tenant_id: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
  isAuthenticated: () => boolean;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      setAuth: (user: User, token: string) => {
        set({ user, token });
      },
      logout: () => {
        set({ user: null, token: null });
      },
      isAuthenticated: () => {
        const { user, token } = get();
        return !!(user && token);
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);