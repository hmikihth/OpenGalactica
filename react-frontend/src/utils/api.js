// src/utils/api.js
import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8008/api/v1/',
    withCredentials: true,
});


export default api;
