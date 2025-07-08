import React, { useState, useEffect } from 'react';
import { 
  Video, 
  Plus, 
  Play, 
  Pause, 
  Settings, 
  Trash2,
  Camera,
  Wifi,
  WifiOff
} from 'lucide-react';
import { videoService } from '../services/videoService';
import toast from 'react-hot-toast';

const VideoManagement: React.FC = () => {
  const [cameras, setCameras] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    name: '',
    rtsp_url: '',
    location: '',
    ai_detection_enabled: true
  });

  useEffect(() => {
    loadCameras();
  }, []);

  const loadCameras = async () => {
    try {
      const data = await videoService.getCameras();
      setCameras(data);
    } catch (error) {
      toast.error('Failed to load cameras');
    } finally {
      setLoading(false);
    }
  };

  const handleAddCamera = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await videoService.createCamera(formData);
      toast.success('Camera added successfully');
      setShowAddModal(false);
      setFormData({ name: '', rtsp_url: '', location: '', ai_detection_enabled: true });
      loadCameras();
    } catch (error) {
      toast.error('Failed to add camera');
    }
  };

  const handleDeleteCamera = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this camera?')) {
      try {
        await videoService.deleteCamera(id);
        toast.success('Camera deleted successfully');
        loadCameras();
      } catch (error) {
        toast.error('Failed to delete camera');
      }
    }
  };

  const toggleCameraStatus = async (id: string, currentStatus: boolean) => {
    try {
      await videoService.updateCamera(id, { is_active: !currentStatus });
      toast.success(`Camera ${!currentStatus ? 'activated' : 'deactivated'}`);
      loadCameras();
    } catch (error) {
      toast.error('Failed to update camera status');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Video Management</h1>
          <p className="text-gray-600">Manage your surveillance cameras and video feeds</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2 hover:bg-blue-700 transition-colors"
        >
          <Plus className="h-4 w-4" />
          <span>Add Camera</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {cameras.map((camera: any) => (
          <div key={camera.id} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            <div className="aspect-video bg-gray-900 flex items-center justify-center">
              <Camera className="h-12 w-12 text-gray-400" />
            </div>
            <div className="p-4">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-semibold text-gray-900">{camera.name}</h3>
                <div className="flex items-center space-x-1">
                  {camera.is_active ? (
                    <Wifi className="h-4 w-4 text-green-600" />
                  ) : (
                    <WifiOff className="h-4 w-4 text-red-600" />
                  )}
                  <span className={`text-sm ${camera.is_active ? 'text-green-600' : 'text-red-600'}`}>
                    {camera.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
              </div>
              <p className="text-sm text-gray-600 mb-2">{camera.location}</p>
              <p className="text-xs text-gray-500 mb-4">AI Detection: {camera.ai_detection_enabled ? 'Enabled' : 'Disabled'}</p>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => toggleCameraStatus(camera.id, camera.is_active)}
                  className={`flex items-center space-x-1 px-3 py-1 rounded text-sm ${
                    camera.is_active 
                      ? 'bg-red-100 text-red-700 hover:bg-red-200' 
                      : 'bg-green-100 text-green-700 hover:bg-green-200'
                  }`}
                >
                  {camera.is_active ? <Pause className="h-3 w-3" /> : <Play className="h-3 w-3" />}
                  <span>{camera.is_active ? 'Stop' : 'Start'}</span>
                </button>
                <button className="flex items-center space-x-1 px-3 py-1 rounded text-sm bg-gray-100 text-gray-700 hover:bg-gray-200">
                  <Settings className="h-3 w-3" />
                  <span>Settings</span>
                </button>
                <button
                  onClick={() => handleDeleteCamera(camera.id)}
                  className="flex items-center space-x-1 px-3 py-1 rounded text-sm bg-red-100 text-red-700 hover:bg-red-200"
                >
                  <Trash2 className="h-3 w-3" />
                  <span>Delete</span>
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Add Camera Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Add New Camera</h2>
            <form onSubmit={handleAddCamera} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Camera Name
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter camera name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  RTSP URL
                </label>
                <input
                  type="url"
                  required
                  value={formData.rtsp_url}
                  onChange={(e) => setFormData({ ...formData, rtsp_url: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="rtsp://camera-ip:port/stream"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Location
                </label>
                <input
                  type="text"
                  required
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter camera location"
                />
              </div>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="ai_detection"
                  checked={formData.ai_detection_enabled}
                  onChange={(e) => setFormData({ ...formData, ai_detection_enabled: e.target.checked })}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="ai_detection" className="ml-2 block text-sm text-gray-700">
                  Enable AI Detection
                </label>
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Add Camera
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default VideoManagement;