import React , { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import CoreService from "../services/CoreService";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import Divider from "@material-ui/core/Divider";
import Link from '@material-ui/core/Link';
import makeStyles from "@material-ui/core/styles/makeStyles";
import Box from "@material-ui/core/Box";



const useStyles = makeStyles({
    left: {
        float: "left"
    },
    right: {
        float: "right"
    },
});


function BookPage(props) {
    const classes = useStyles();
    const { book } = props;
    const [ results, setResults ] = useState([]);
    const [ next, setNext ] = useState("")
    const [ previous, setPrevious ] = useState("")

    useEffect(() => {
        let coreService = new CoreService();
        coreService.getBookContentsByBookId(book.id).then( e => {
            setResults(e.results);
            setNext(e.next);
            setPrevious(e.previous);
            coreService.createBookAccess(book.id).then(e => console.log(`book access created ${book.id}`));
        });
    }, []);

    const handleNavigate = (direction) => {
        if(direction) {
            new CoreService().getUrl(direction).then( e => {
                setResults(e.results);
                setNext(e.next);
                setPrevious(e.previous);
            });
        }
    }

    return (
        <Grid item xs={12} md={8}>
          <Typography variant="h6" gutterBottom>
            {book.title}
          </Typography>
          <Divider />
          {results && results.map((result) => (
              <Typography variant="body1" paragraph>
                  {result.content}
              </Typography>
          ))}
          <Grid xs={12}>
              {previous && (<Link
                color="inherit"
                noWrap
                variant="body2"
                className={classes.left}
                onClick={() => handleNavigate(previous)}
              >
                previous
              </Link>)} {!previous && (<Link className={classes.left} />)}
                {next && (<Link
                color="inherit"
                noWrap
                className={classes.right}
                variant="body2"
                onClick={() => handleNavigate(next)}
              >
                next
              </Link>)} {!next && (<Link className={classes.right} />)}
          </Grid>
        </Grid>
    );
}

BookPage.propTypes = {
    book: PropTypes.any.isRequired,
};

export default BookPage;