import axios from 'axios';

const base_url = "http://localhost:8000/api";
export default class CoreService {

    constructor() {
        this.token = localStorage.getItem("token");
        this.defaultOptions = {
            headers: {
                Authorization: `Token ${this.token}`
            }
        };
    }

    getUrl = async (url) => {
        const result = await axios.get(url, {...this.defaultOptions});
        return result.data;
    }

    // http://localhost:8000/api/bookContents/?search:{id}&search_fields=book__id
    getBookContentsByBookId = async (book_id) => {
        const queryParams = {
            search: book_id,
            search_fields: "book__id"
        }

        const result = await axios.get(
            `${base_url}/bookContents/`,
            { ...this.defaultOptions, params: queryParams }
        );

        return result.data;
    }

    createBookAccess = async (book_id) => {
        const body = { book: book_id }

        const result = await axios.post(`${base_url}/bookAccesses/`, body, {...this.defaultOptions});

        return result.data;
    }

    // http://localhost:8000/api/books/
    // http://localhost:8000/api/books/?search=adventure&search_fields=categories__name
    getBooks = async () => {
        const result = await axios.get(
            `${base_url}/books/`,
            { ...this.defaultOptions }
        );
        return result.data;
    }

    getBooksByCategory = async(category_name) => {
        const queryParams = {
            search: category_name,
            search_fields: "categories__name"
        };

        const result = await axios.get(
            `${base_url}/books/`,
            {...this.defaultOptions, queryParams}
        )
    }

}