import {makeStyles} from "@material-ui/core/styles";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import * as React from "react";
import {useEffect, useState} from "react";
import CoreService from "../services/CoreService";
import BookCard from "./BookCard";
import Sidebar from "./Sidebar";
import GitHubIcon from '@material-ui/icons/GitHub';
import FacebookIcon from '@material-ui/icons/Facebook';
import TwitterIcon from '@material-ui/icons/Twitter';
import BookSearch from "./BookSearch";


const useStyles = makeStyles((theme) => ({
    mainGrid: {
        marginTop: theme.spacing(3),
        width: "100%",
    },
    grid: {
        width: "100%",
    }
}));

const posts = ["Not surprisingly, Peter's iPhone now pinged with an incoming reply from Katherine.",
    "Mal'akh put the car back in park and stared out at the distant silhouette of the SMSC. Ten minutes. Peter Solomon's sprawling warehouse housed over thirty million treasures, but Mal'akh had come here tonight to obliterate only the two most valuable.",
    "All of Katherine Solomon's research."];

function Browse(props) {
    const classes = useStyles();
    const [books, setBooks] = useState([]);
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState(null);

    const social = [
        {name: 'GitHub', icon: GitHubIcon},
        {name: 'Twitter', icon: TwitterIcon},
        {name: 'Facebook', icon: FacebookIcon},
    ];

    useEffect(() => {
        let coreService = new CoreService();
        Promise.all([coreService.getRecommendedBooks(), coreService.getCategories()]).then((values) => {
            setBooks(values[0]);
            setCategories(values[1]);
        });
    }, []);

    const handleCategoryClicked = (categoryName) => {
        setSelectedCategory(categoryName);
        console.log(categoryName);
    }

    return (
        <main>
            <Typography variant="h5" gutterBottom>
                Recommended for you
            </Typography>
            <Grid container spacing={4} className={classes.grid}>
                {books &&
                books.map((book) => (
                    <BookCard key={book.id} book={book} md={6} minHeight={300} />
                ))}
            </Grid>

            <Grid container spacing={5} className={classes.mainGrid}>
                <BookSearch category={selectedCategory} />
                <Sidebar
                    categories={categories}
                    categoryClicked={handleCategoryClicked}
                    social={social}
                />
            </Grid>
        </main>
    );
}

Browse.propTypes = {};

export default Browse;