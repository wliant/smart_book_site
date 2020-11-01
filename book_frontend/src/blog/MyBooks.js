import {makeStyles} from "@material-ui/core/styles";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import Link from "@material-ui/core/Link";
import PropTypes from "prop-types";
import * as React from "react";
import BookCard from "./BookCard";
import BookSearch from "./BookSearch";
import Sidebar from "./Sidebar";
import {useEffect, useState} from "react";
import CoreService from "../services/CoreService";


const useStyles = makeStyles((theme) => ({
  main: {
    marginTop: theme.spacing(3),
  },
}));

function MyBooks(props) {
  const classes = useStyles();
  const [books, setBooks ] = useState({});
  const username = localStorage.getItem("username");

  useEffect(() => {
    new CoreService().getBooks("author", username).then(e => setBooks(e));
  }, []);

  return (
      <main>
          <Typography variant="h5" gutterBottom>
              My Books
          </Typography>
          <Grid container spacing={4} className={classes.grid}>
              {books.results &&
              books.results.map((book) => (
                  <BookCard key={book.id} book={book} md={12} minHeight={120} />
              ))}
            {
              (!books.results || books.results.length == 0) && (
                  <Typography variant="subtitle1">
                    I have no books.
                  </Typography>
              )
            }
          </Grid>
      </main>
  );
}

MyBooks.propTypes = {

};

export default MyBooks;