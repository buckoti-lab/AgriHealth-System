const URLS = {
    localhost: "http://127.0.0.1:8000",
    "192.168.137.1": "http://192.168.137.1:8000",
    "172.16.1.81": "http://172.16.1.81:8000"
};
const BASE_URL =
    URLS[window.location.hostname] || "http://127.0.0.1:8000";
