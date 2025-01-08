export const API_URL = import.meta.env.VITE_API_URL
export const ENV = import.meta.env.VITE_ENV || 'dev'

const constants = {
  API_URL,
  ENV,
}

export default {
  ...constants
}
