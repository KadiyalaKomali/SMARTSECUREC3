import { useEffect } from 'react';
import { websocketService } from '../services/websocketService';
import { useAuthStore } from '../store/authStore';

export const useWebSocket = () => {
  const { isAuthenticated } = useAuthStore();

  useEffect(() => {
    if (isAuthenticated()) {
      websocketService.connect();
    }

    return () => {
      websocketService.disconnect();
    };
  }, [isAuthenticated]);

  return websocketService;
};

export const useWebSocketEvent = (eventType: string, handler: Function) => {
  useEffect(() => {
    websocketService.on(eventType, handler);

    return () => {
      websocketService.off(eventType, handler);
    };
  }, [eventType, handler]);
};