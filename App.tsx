import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { useAuthStore } from './store/authStore';
import { useWebSocket } from './hooks/useWebSocket';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import VideoManagement from './pages/VideoManagement';
import PersonManagement from './pages/PersonManagement';
import VehicleManagement from './pages/VehicleManagement';
import EventLogs from './pages/EventLogs';
import Settings from './pages/Settings';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  const { user } = useAuthStore();
  
  // Initialize WebSocket connection
  useWebSocket();

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#10B981',
                secondary: '#fff',
              },
            },
            error: {
              duration: 5000,
              iconTheme: {
                primary: '#EF4444',
                secondary: '#fff',
              },
            },
          }}
        />
        <Routes>
          <Route path="/login" element={!user ? <Login /> : <Navigate to="/dashboard" />} />
          <Route path="/" element={<Navigate to="/dashboard" />} />
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <Layout>
                <Dashboard />
              </Layout>
            </ProtectedRoute>
          } />
          <Route path="/video-management" element={
            <ProtectedRoute>
              <Layout>
                <VideoManagement />
              </Layout>
            </ProtectedRoute>
          } />
          <Route path="/person-management" element={
            <ProtectedRoute>
              <Layout>
                <PersonManagement />
              </Layout>
            </ProtectedRoute>
          } />
          <Route path="/vehicle-management" element={
            <ProtectedRoute>
              <Layout>
                <VehicleManagement />
              </Layout>
            </ProtectedRoute>
          } />
          <Route path="/event-logs" element={
            <ProtectedRoute>
              <Layout>
                <EventLogs />
              </Layout>
            </ProtectedRoute>
          } />
          <Route path="/settings" element={
            <ProtectedRoute>
              <Layout>
                <Settings />
              </Layout>
            </ProtectedRoute>
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;