import axios from "axios";
import { camelizeKeys, decamelizeKeys } from "humps";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use(
  (config) => {
    if (config.data) {
      config.data = decamelizeKeys(config.data);
    }

    if (config.params) {
      config.params = decamelizeKeys(config.params);
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => {
    if (response.data) {
      response.data = camelizeKeys(response.data);
    }

    return response;
  },
  async (error) => {
    // TODO: Handle various API errors here.
    if (error.response?.data) {
      error.response.data = camelizeKeys(error.response.data);
    }
    return Promise.reject(error);
  }
);

export default api;
