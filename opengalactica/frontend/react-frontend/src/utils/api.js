// src/utils/api.js
import axios from 'axios';

axios.defaults.withCredentials = true;

const api = axios.create({
    baseURL: '/api/v1/',
});


export default api;
