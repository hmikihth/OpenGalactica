// src/utils/api.js
import axios from 'axios';

const api = axios.create({
//    Development
//    baseURL: 'http://localhost:8008/api/v1/',

//    Production
    baseURL: 'http://82.165.219.231:8000/api/v1/',
    withCredentials: true,
});


export default api;
