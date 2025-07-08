import api from './api';

export const dashboardService = {
  getDashboardData: async () => {
    // Mock data - replace with actual API calls
    return {
      stats: {
        totalCameras: 8,
        activeCameras: 6,
        totalPersons: 45,
        totalVehicles: 23,
        todayEvents: 127,
        alerts: 3
      },
      recentEvents: [
        {
          id: '1',
          type: 'alert',
          message: 'Unauthorized person detected in restricted area',
          camera: 'Camera 01 - Main Gate',
          timestamp: '2 minutes ago',
          status: 'pending'
        },
        {
          id: '2',
          type: 'detection',
          message: 'Vehicle ABC-1234 detected at exit gate',
          camera: 'Camera 05 - Exit Gate',
          timestamp: '5 minutes ago',
          status: 'resolved'
        },
        {
          id: '3',
          type: 'detection',
          message: 'Face match: John Doe (Employee ID: EMP001)',
          camera: 'Camera 03 - Warehouse A',
          timestamp: '8 minutes ago',
          status: 'resolved'
        }
      ],
      chartData: [
        { date: '2024-01-01', detections: 45, events: 23 },
        { date: '2024-01-02', detections: 52, events: 28 },
        { date: '2024-01-03', detections: 38, events: 19 },
        { date: '2024-01-04', detections: 67, events: 34 },
        { date: '2024-01-05', detections: 71, events: 41 },
        { date: '2024-01-06', detections: 58, events: 29 },
        { date: '2024-01-07', detections: 63, events: 32 }
      ]
    };
  }
};