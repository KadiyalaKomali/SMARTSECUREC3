import api from './api';

export const videoService = {
  getCameras: async () => {
    // Mock data - replace with actual API calls
    return [
      {
        id: '1',
        name: 'Main Gate Camera',
        rtsp_url: 'rtsp://192.168.1.100:554/stream1',
        location: 'Main Gate',
        is_active: true,
        ai_detection_enabled: true,
        created_at: '2024-01-01T00:00:00Z'
      },
      {
        id: '2',
        name: 'Warehouse A Camera',
        rtsp_url: 'rtsp://192.168.1.101:554/stream1',
        location: 'Warehouse A',
        is_active: true,
        ai_detection_enabled: true,
        created_at: '2024-01-01T00:00:00Z'
      },
      {
        id: '3',
        name: 'Exit Gate Camera',
        rtsp_url: 'rtsp://192.168.1.102:554/stream1',
        location: 'Exit Gate',
        is_active: false,
        ai_detection_enabled: true,
        created_at: '2024-01-01T00:00:00Z'
      }
    ];
  },

  createCamera: async (cameraData: any) => {
    const response = await api.post('/cameras', cameraData);
    return response.data;
  },

  updateCamera: async (id: string, cameraData: any) => {
    const response = await api.put(`/cameras/${id}`, cameraData);
    return response.data;
  },

  deleteCamera: async (id: string) => {
    const response = await api.delete(`/cameras/${id}`);
    return response.data;
  }
};