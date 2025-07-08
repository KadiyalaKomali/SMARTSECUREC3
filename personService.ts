import api from './api';

export const personService = {
  getPersons: async () => {
    // Mock data - replace with actual API calls
    return [
      {
        id: '1',
        name: 'John Doe',
        employee_id: 'EMP001',
        department: 'Security',
        role: 'Security Officer',
        authorized: true,
        face_encodings: true,
        created_at: '2024-01-01T00:00:00Z'
      },
      {
        id: '2',
        name: 'Jane Smith',
        employee_id: 'EMP002',
        department: 'Operations',
        role: 'Warehouse Manager',
        authorized: true,
        face_encodings: true,
        created_at: '2024-01-01T00:00:00Z'
      },
      {
        id: '3',
        name: 'Bob Johnson',
        employee_id: 'EMP003',
        department: 'Logistics',
        role: 'Logistics Coordinator',
        authorized: true,
        face_encodings: false,
        created_at: '2024-01-01T00:00:00Z'
      }
    ];
  },

  createPerson: async (personData: any) => {
    const response = await api.post('/persons', personData);
    return response.data;
  },

  updatePerson: async (id: string, personData: any) => {
    const response = await api.put(`/persons/${id}`, personData);
    return response.data;
  },

  deletePerson: async (id: string) => {
    const response = await api.delete(`/persons/${id}`);
    return response.data;
  }
};