import api from './api';

export const vehicleService = {
  getVehicles: async () => {
    // Mock data - replace with actual API calls
    return [
      {
        id: '1',
        license_plate: 'ABC-1234',
        vehicle_type: 'truck',
        owner_name: 'John Transport',
        company: 'ABC Logistics',
        authorized: true,
        created_at: '2024-01-01T00:00:00Z'
      },
      {
        id: '2',
        license_plate: 'XYZ-5678',
        vehicle_type: 'car',
        owner_name: 'Jane Doe',
        company: 'Internal Security',
        authorized: true,
        created_at: '2024-01-01T00:00:00Z'
      },
      {
        id: '3',
        license_plate: 'DEF-9012',
        vehicle_type: 'van',
        owner_name: 'Bob Delivery',
        company: 'Fast Delivery Co.',
        authorized: false,
        created_at: '2024-01-01T00:00:00Z'
      }
    ];
  },

  createVehicle: async (vehicleData: any) => {
    const response = await api.post('/vehicles', vehicleData);
    return response.data;
  },

  updateVehicle: async (id: string, vehicleData: any) => {
    const response = await api.put(`/vehicles/${id}`, vehicleData);
    return response.data;
  },

  deleteVehicle: async (id: string) => {
    const response = await api.delete(`/vehicles/${id}`);
    return response.data;
  }
};