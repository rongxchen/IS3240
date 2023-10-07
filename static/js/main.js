axios.interceptors.request.use(
    config => {
        if (localStorage.getItem("token")) {
            config.headers['Authorization'] = `Bearer ${localStorage.getItem('token')}`;
        }
        // config.headers["Authorization"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidXNlci0wMTdiMjRlMy0xZWY5LTRlMWUtYjg0Ni1mODQ5MGRhMTE5MGEiLCJleHAiOjE2OTY2ODQyMDg5Nzh9.pSOUo-EqGulCgzyT9VCjCwrhf5cexz_FJPDSJnSBSd8";
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);