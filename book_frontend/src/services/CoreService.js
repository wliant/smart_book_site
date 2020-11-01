import axios from 'axios';
import {ViewerPageLimit} from "../blog/Constants";
import Qs from "qs";

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

    getBook = async (book_id) => {
        const result = await axios.get(`${base_url}/books/${book_id}/`, {...this.defaultOptions});

        return result.data;
    }

    // http://localhost:8000/api/bookContents/?search:{id}&search_fields=book__id
    getBookContentsByBookId = async (book_id) => {
        const queryParams = {
            search: book_id,
            limit: ViewerPageLimit,
            search_fields: "book__id"
        }

        const result = await axios.get(
            `${base_url}/bookContents/`,
            {
                ...this.defaultOptions,
                params: queryParams,
            }
        );

        return result.data;
    }

    createBook = async (title, storyline, thumbnail) => {
        const formData = new FormData();
        formData.append("title", title);
        formData.append("story_line", storyline);
        if (thumbnail) {
            formData.append("thumbnail", thumbnail);
        }


        const result = await axios.post(`${base_url}/books/`, formData, {...this.defaultOptions});

        return result.data;
    }

    createBookAccess = async (book_id) => {
        const body = {book: book_id}

        const result = await axios.post(`${base_url}/bookAccesses/`, body, {...this.defaultOptions});

        return result.data;
    }

    createBookReview = async (book_id, review_text) => {
        const body = {book: book_id, content: review_text};

        const result = await axios.post(`${base_url}/reviews/`, body, {...this.defaultOptions});

        return result.data;
    }

    createBookContent = async (book_id, content) => {
        const body = {book: book_id, content: content};

        const result = await axios.post(`${base_url}/bookContents/`, body, {...this.defaultOptions});

        return result.data;
    }

    categorizeBook = async (book_id) => {
        const queryParams = {
            book: book_id
        }
        const result = await axios.post(
            `${base_url}/categorize/`,
            {...this.defaultOptions, params: queryParams}
        );
        return result.data;
    }

    // http://localhost:8000/api/books/
    // http://localhost:8000/api/books/?search=adventure&search_fields=categories__name
    getBooks = async (field, text) => {
        let sf = [];
        switch (field) {
            case "categories":
                sf = ["categories__name"]
                break;
            case "title":
                sf = ["title"]
                break;
            case "author":
                sf = ["author"]
                break;
            case "all":
            default:
                sf = ["title", "author", "categories__name"]
                break;
        }
        const queryParams = {
            search: text,
            search_fields: sf,
            limit: 10,
        }
        const result = await axios.get(
            `${base_url}/books/`,
            {
                ...this.defaultOptions,
                params: queryParams,
                paramsSerializer: params => Qs.stringify(params, {arrayFormat: 'repeat'}),
            }
        );
        return result.data;
    }

    getRecommendedBooks = async () => {
        const queryParams = {
            limit: 4
        }
        const result = await axios.get(
            `${base_url}/recommend/`,
            {...this.defaultOptions, params: queryParams}
        );
        return result.data;
    }

    getBooksByCategory = async (category_name) => {
        const queryParams = {
            search: category_name,
            search_fields: "categories__name"
        };

        const result = await axios.get(
            `${base_url}/books/`,
            {...this.defaultOptions, queryParams}
        );

        return result.data;
    }

    getCategories = async () => {
        const result = await axios.get(`${base_url}/categorys/`, {...this.defaultOptions});

        return result.data;
    }

    getBookReviews = async (bookId) => {
        const queryParams = {
            search: bookId,
            limit: 10,
            search_fields: "book__id"
        };

        const result = await axios.get(
            `${base_url}/reviews/`,
            {...this.defaultOptions, params: queryParams}
        );

        return result.data;
    }

}