import api from './api';

export const settingsService = {
  getSettings: async () => {
    // Mock data - replace with actual API calls
    return {
      profile: {
        full_name: 'Admin User',
        email: 'admin@demo.com',
        phone: '+1234567890',
        department: 'Security'
      },
      notifications: {
        email_alerts: true,
        push_notifications: true,
        intrusion_alerts: true,
        face_detection_alerts: false,
        vehicle_detection_alerts: false
      },
      security: {
        two_factor_enabled: false,
        password_expiry: 30,
        session_timeout: 60
      },
      system: {
        ai_detection_threshold: 0.7,
        max_concurrent_streams: 10,
        storage_retention_days: 30
      }
    };
  },

  updateSettings: async (settings: any) => {
    const response = await api.put('/settings', settings);
    return response.data;
  }
};