import axios from 'axios';
const instance = axios.create({
    baseURL: 'http://localhost:8000',
    followRedirect: true,
})
export default instance;