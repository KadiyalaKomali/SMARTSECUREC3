import React, { useState, useEffect } from 'react';
import { 
  Search, 
  Filter, 
  AlertCircle, 
  Eye, 
  User, 
  Car,
  Calendar,
  Clock
} from 'lucide-react';
import { eventService } from '../services/eventService';
import { format } from 'date-fns';
import toast from 'react-hot-toast';

const EventLogs: React.FC = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [dateRange, setDateRange] = useState({
    from: '',
    to: ''
  });

  useEffect(() => {
    loadEvents();
  }, []);

  const loadEvents = async () => {
    try {
      const data = await eventService.getEvents();
      setEvents(data);
    } catch (error) {
      toast.error('Failed to load events');
    } finally {
      setLoading(false);
    }
  };

  const getEventIcon = (type: string) => {
    switch (type) {
      case 'face_detection':
        return <User className="h-4 w-4" />;
      case 'vehicle_detection':
        return <Car className="h-4 w-4" />;
      case 'intrusion':
        return <AlertCircle className="h-4 w-4" />;
      default:
        return <Eye className="h-4 w-4" />;
    }
  };

  const getEventColor = (type: string) => {
    switch (type) {
      case 'face_detection':
        return 'bg-blue-100 text-blue-800';
      case 'vehicle_detection':
        return 'bg-green-100 text-green-800';
      case 'intrusion':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const filteredEvents = events.filter((event: any) => {
    const matchesSearch = event.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         event.camera_name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterType === 'all' || event.event_type === filterType;
    return matchesSearch && matchesFilter;
  });

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
          <h1 className="text-2xl font-bold text-gray-900">Event Logs</h1>
          <p className="text-gray-600">Monitor and search surveillance events and detections</p>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="p-6 border-b border-gray-200">
          <div className="flex flex-col md:flex-row md:items-center md:space-x-4 space-y-4 md:space-y-0">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search events..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div className="flex items-center space-x-2">
              <Filter className="h-4 w-4 text-gray-400" />
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Events</option>
                <option value="face_detection">Face Detection</option>
                <option value="vehicle_detection">Vehicle Detection</option>
                <option value="intrusion">Intrusion</option>
                <option value="object_detection">Object Detection</option>
              </select>
            </div>
            <div className="flex items-center space-x-2">
              <Calendar className="h-4 w-4 text-gray-400" />
              <input
                type="date"
                value={dateRange.from}
                onChange={(e) => setDateRange({ ...dateRange, from: e.target.value })}
                className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <span className="text-gray-500">to</span>
              <input
                type="date"
                value={dateRange.to}
                onChange={(e) => setDateRange({ ...dateRange, to: e.target.value })}
                className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        <div className="divide-y divide-gray-200">
          {filteredEvents.map((event: any) => (
            <div key={event.id} className="p-6 hover:bg-gray-50">
              <div className="flex items-start space-x-4">
                <div className={`p-2 rounded-full ${getEventColor(event.event_type)}`}>
                  {getEventIcon(event.event_type)}
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <h3 className="text-sm font-medium text-gray-900">{event.description}</h3>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getEventColor(event.event_type)}`}>
                      {event.event_type.replace('_', ' ')}
                    </span>
                  </div>
                  <div className="mt-1 flex items-center space-x-4 text-sm text-gray-500">
                    <span className="flex items-center">
                      <Eye className="h-3 w-3 mr-1" />
                      {event.camera_name}
                    </span>
                    <span className="flex items-center">
                      <Clock className="h-3 w-3 mr-1" />
                      {format(new Date(event.timestamp), 'MMM dd, yyyy HH:mm:ss')}
                    </span>
                    {event.confidence && (
                      <span>Confidence: {(event.confidence * 100).toFixed(1)}%</span>
                    )}
                  </div>
                  {event.metadata && (
                    <div className="mt-2 text-xs text-gray-600">
                      {JSON.stringify(event.metadata)}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredEvents.length === 0 && (
          <div className="p-12 text-center">
            <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">No events found matching your criteria.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default EventLogs;