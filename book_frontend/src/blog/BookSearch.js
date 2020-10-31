import {makeStyles} from "@material-ui/core/styles";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import Link from "@material-ui/core/Link";
import PropTypes from "prop-types";
import * as React from "react";
import SearchIcon from '@material-ui/icons/Search';
import TextField from "@material-ui/core/TextField";
import MenuItem from "@material-ui/core/MenuItem";
import {useEffect, useState} from "react";
import CoreService from "../services/CoreService";
import BookCard from "./BookCard";
import IconButton from "@material-ui/core/IconButton";
import Divider from "@material-ui/core/Divider";
import ArrowBackIosIcon from "@material-ui/icons/ArrowBackIos";
import ArrowForwardIosIcon from "@material-ui/icons/ArrowForwardIos";


const useStyles = makeStyles((theme) => ({
    main: {
        marginTop: theme.spacing(3),
    },
    searchField: {
        minWidth: 120,
    },
    searchText: {
        minWidth: 240,
    },
    navigate: {
        align: "right",
    },
    grid: {
        width: "100%",
        marginTop: theme.spacing(3),
    }
}));

function BookSearch({category}) {
    const classes = useStyles();
    const [books, setBooks] = useState([]);
    const [searchText, setSearchText] = useState(category);
    const [next, setNext] = useState(null);
    const [previous, setPrevious] = useState(null);
    const [searchField, setSearchField] = useState(category ? "categories" : "all");
    const fieldMenus = [
        {label: "All", value: "all"},
        {label: "Title", value: "title"},
        {label: "Category", value: "categories"},
        {label: "Author", value: "author"},
    ];


    useEffect(() => {
        let text = searchText;
        let field = searchField;
        if (category) {
            text = category;
            field = "categories";
        }
        let coreService = new CoreService();
        coreService.getBooks(field, text).then(e => {
            setBooks(e);
            setSearchField(field);
            setSearchText(text);
            setNext(e.next);
            setPrevious(e.previous);
        });
    }, [category]);

    const handleSearch = () => {
        new CoreService().getBooks(searchField, searchText).then(e => {
            setBooks(e);
            setNext(e.next);
            setPrevious(e.previous);
        });
    };
    const handleNavigate = (direction) => {
        if (direction) {
            new CoreService().getUrl(direction).then(e => {
                setBooks(e);
                setNext(e.next);
                setPrevious(e.previous);
            });
        }
    }
    return (
        <Grid item xs={12} md={10} spacing={2}>
            <Typography variant="h6" gutterBottom>
                Listing
            </Typography>
            <Divider/>
            <Grid container spacing={3} className={classes.main}>
                <Grid container xs={8} justify="space-evenly" spacing={3}>
                    <TextField
                        select
                        label="Field"
                        value={searchField}
                        className={classes.searchField}
                        onChange={(e) => setSearchField(e.target.value)}
                    >
                        {fieldMenus.map((option) => (
                            <MenuItem key={option.value} value={option.value}>
                                {option.label}
                            </MenuItem>
                        ))}
                    </TextField>
                    <TextField value={searchText}
                               label="Search"
                               InputLabelProps={{ shrink: true }}
                               className={classes.searchText}
                               onChange={(e) => setSearchText(e.target.value)}/>
                    <IconButton onClick={handleSearch}>
                        <SearchIcon/>
                    </IconButton>
                </Grid>
                <Grid container xs={4} justify="flex-end">
                    {previous && (
                        <IconButton onClick={() => handleNavigate(previous)}>
                            <ArrowBackIosIcon/>
                        </IconButton>
                    )} {!previous && (<Link className={classes.navigate}/>)}
                    {next && (
                        <IconButton onClick={() => handleNavigate(next)}>
                            <ArrowForwardIosIcon/>
                        </IconButton>
                    )} {!next && (<Link className={classes.navigate}/>)}
                </Grid>
            </Grid>
            <Grid container spacing={1} className={classes.grid}>
                {books.results &&
                books.results.map((book) => (
                    <BookCard key={book.id} book={book} md={12} minHeight={120}/>
                ))}
            </Grid>
        </Grid>
    );
}

BookSearch.propTypes = {
    category: PropTypes.string,
};

export default BookSearch;