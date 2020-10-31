import React, {useEffect, useState} from 'react';
import PropTypes from 'prop-types';
import CoreService from "../services/CoreService";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import Divider from "@material-ui/core/Divider";
import Link from '@material-ui/core/Link';
import makeStyles from "@material-ui/core/styles/makeStyles";
import ArrowBackIosIcon from '@material-ui/icons/ArrowBackIos';
import ArrowForwardIosIcon from '@material-ui/icons/ArrowForwardIos';
import IconButton from "@material-ui/core/IconButton";
import {ViewerPageLimit} from "./Constants";


const useStyles = makeStyles({
    left: {
        float: "left"
    },
    right: {
        float: "right"
    },
    bottomGrid: {
        minHeight: 20
    }
});


function BookViewer(props) {
    const classes = useStyles();
    const {book} = props;
    const [results, setResults] = useState([]);
    const [next, setNext] = useState("")
    const [previous, setPrevious] = useState("")
    const [pageNum, setPageNum] = useState(0);
    const [totalPage, setTotalPage] = useState(0);

    useEffect(() => {
        let coreService = new CoreService();
        coreService.getBookContentsByBookId(book.id).then(e => {
            setResults(e.results);
            setNext(e.next);
            setPrevious(e.previous);
            setPageNum(1);
            setTotalPage(Math.ceil(e.count *1.0 / ViewerPageLimit));
            coreService.createBookAccess(book.id).then(e => console.log(`book access created ${book.id}`));
        });
    }, []);

    const handleNavigate = (pageNum, direction) => {
        if (direction) {
            new CoreService().getUrl(direction).then(e => {
                setResults(e.results);
                setNext(e.next);
                setPrevious(e.previous);
                setPageNum(pageNum);
                window.scrollTo(0, 0);
            });
        }
    }

    return (
        <main>
            <Grid xs={12} container justify={"space-between"} spacing={24}>
                <Typography variant="h6" gutterBottom>
                    {book.title}
                </Typography>
                <Typography variant="body2">
                    {`${pageNum}/${totalPage}`}
                </Typography>
            </Grid>
            <Divider/>
            {results && results.map((result) => (
                <Typography variant="body1" paragraph>
                    {result.content}
                </Typography>
            ))}
            <Grid xs={12} container justify="space-between" spacing={24}>
                {previous && (
                    <IconButton onClick={() => handleNavigate(pageNum - 1, previous)}>
                        <ArrowBackIosIcon/>
                    </IconButton>
                )} {!previous && (<Link className={classes.left}/>)}
                {next && (
                    <IconButton onClick={() => handleNavigate(pageNum + 1, next)}>
                        <ArrowForwardIosIcon/>
                    </IconButton>
                )} {!next && (<Link className={classes.right}/>)}
            </Grid>
        </main>
    );
}

BookViewer.propTypes = {
    book: PropTypes.any.isRequired,
};

export default BookViewer;