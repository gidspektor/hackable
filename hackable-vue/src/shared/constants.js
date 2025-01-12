export const API_URL = import.meta.env.VITE_API_URL
export const ENV = import.meta.env.VITE_ENV || 'dev'
export const BASE_ROUTE = import.meta.env.VITE_BASE_ROUTE

const constants = {
  API_URL,
  ENV,
  BASE_ROUTE,
}

export default {
  ...constants
}
