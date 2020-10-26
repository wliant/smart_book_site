import axios from 'axios';

const base_url = "http://localhost:8000/api";
export default class CoreService {

    getBookContentsByBookId = async (book_id) => {
        const queryParams = {
            search: book_id,
            search_fields: "book__id"
        }

        const result = await axios.get(
            `${base_url}/bookContents/`,
            { params: queryParams}
        );

        return result.data;
    }


    getBooks = async () => {
        const result = await axios.get(
            `${base_url}/books/`
        );
        return result.data;
    }

}