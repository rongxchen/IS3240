// Request interceptors for API calls
axios.interceptors.request.use(
    config => {
        if (localStorage.getItem("token")) {
            config.headers['Authorization'] = `Bearer ${localStorage.getItem('token')}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);
