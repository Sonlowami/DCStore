import axios from "axios";


const AuthService = {
    login: async (email, password) => {
        const res = await axios.post('/api/v1/login', { email, password });
        if (res.data['x-token']) {
            localStorage.setItem('x-token', res.data['x-token']);
        }
        return res.data;
    },
    register: async ({ fullname, username, email, password, role }) => {
        const res = await axios.post('/api/v1/register', { fullname, username, email, password, role });
        return res.data;
    },
    logout: () => {
        localStorage.removeItem('x-token');
    },
    isAuthenticated: () => {
        return localStorage.getItem('x-token') !== null;
    },
    getToken: () => {
        return localStorage.getItem('x-token');
    },
};

export default AuthService;
