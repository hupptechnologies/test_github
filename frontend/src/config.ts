// Frontend Configuration
export const config = {
  // API Configuration
  API_BASE: import.meta.env.VITE_API_BASE || 'http://localhost:8000/api',
  WS_URL: import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/chat',
  
  // App Configuration
  APP_TITLE: import.meta.env.VITE_APP_TITLE || 'AI Chat Application',
  DEBUG: import.meta.env.VITE_DEBUG === 'true',
  
  // Development Configuration
  IS_DEV: import.meta.env.DEV,
  IS_PROD: import.meta.env.PROD,
} as const;

// Type-safe environment variables
export type Config = typeof config; 