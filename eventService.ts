import api from './api';

export const eventService = {
  getEvents: async () => {
    // Mock data - replace with actual API calls
    return [
      {
        id: '1',
        event_type: 'face_detection',
        description: 'Face detected: John Doe (Employee ID: EMP001)',
        camera_name: 'Main Gate Camera',
        timestamp: '2024-01-15T10:30:00Z',
        confidence: 0.95,
        metadata: { person_id: '1', match_score: 0.95 }
      },
      {
        id: '2',
        event_type: 'vehicle_detection',
        description: 'Vehicle detected: ABC-1234 (Authorized)',
        camera_name: 'Exit Gate Camera',
        timestamp: '2024-01-15T10:25:00Z',
        confidence: 0.88,
        metadata: { vehicle_id: '1', license_plate: 'ABC-1234' }
      },
      {
        id: '3',
        event_type: 'intrusion',
        description: 'Unauthorized person detected in restricted area',
        camera_name: 'Warehouse A Camera',
        timestamp: '2024-01-15T10:20:00Z',
        confidence: 0.92,
        metadata: { area: 'restricted', alert_level: 'high' }
      },
      {
        id: '4',
        event_type: 'object_detection',
        description: 'Gunny bags counted: 45 items detected',
        camera_name: 'Warehouse B Camera',
        timestamp: '2024-01-15T10:15:00Z',
        confidence: 0.87,
        metadata: { object_count: 45, object_type: 'gunny_bag' }
      }
    ];
  },

  createEvent: async (eventData: any) => {
    const response = await api.post('/events', eventData);
    return response.data;
  }
};