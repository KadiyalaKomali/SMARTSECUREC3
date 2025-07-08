import api from './api';

export const authService = {
  login: async (email: string, password: string) => {
    // Mock authentication - replace with actual API call
    if (email === 'admin@demo.com' && password === 'admin123') {
      return {
        user: {
          id: '1',
          email: 'admin@demo.com',
          full_name: 'Admin User',
          role: 'admin' as const,
          tenant_id: 'demo-tenant'
        },
        access_token: 'mock-admin-token'
      };
    }
    
    if (email === 'security@demo.com' && password === 'security123') {
      return {
        user: {
          id: '2',
          email: 'security@demo.com',
          full_name: 'Security Officer',
          role: 'security' as const,
          tenant_id: 'demo-tenant'
        },
        access_token: 'mock-security-token'
      };
    }
    
    if (email === 'manager@demo.com' && password === 'manager123') {
      return {
        user: {
          id: '3',
          email: 'manager@demo.com',
          full_name: 'Manager User',
          role: 'manager' as const,
          tenant_id: 'demo-tenant'
        },
        access_token: 'mock-manager-token'
      };
    }
    
    throw new Error('Invalid credentials');
  },

  logout: async () => {
    // Mock logout - replace with actual API call
    return Promise.resolve();
  },

  register: async (userData: any) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  }
};