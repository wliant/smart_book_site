import axios from 'axios';
const base_url = 'http://localhost:8000/api';
export default class AuthService {

    logout = () => {
        localStorage.removeItem("token");
    }
    login_fake = async (username, password) => {
        return "abcd";
    }
    login = async (username, password) => {
        const formData = new FormData();
        formData.set("username", username);
        formData.set("password", password);
        const authorization = await axios({
            method: "POST",
            url: `${base_url}/auth/token/login/`,
            data: formData,
            config: {
                headers: { "Content-Type": "multipart/form-data" }
            }
        });

        return authorization.data.auth_token;
    }

    signup = async (firstname, lastname, username, password) => {
        const formData = new FormData();
        formData.set("username", username);
        formData.set("password", password);
        formData.set("first_name", firstname);
        formData.set("last_name", lastname);

        const registration = await axios ({
            method: "POST",
            url: `${base_url}/auth/users/`,
            data: formData,
            config: {
                headers: { "Content-Type": "multipart/form-data" }
            }
        });
    }
}