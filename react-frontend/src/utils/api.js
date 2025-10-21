// src/utils/api.js
import axios from 'axios';

const api = axios.create({
//    Development
//    baseURL: 'http://localhost:8008/api/v1/',

//    Production
    baseURL: 'https://backend.opengalactica.space/api/v1/',
    withCredentials: true,
});


export default api;
