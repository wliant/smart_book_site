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
import AddIcon from "@material-ui/icons/Add";
import Button from "@material-ui/core/Button";
import HelpIcon from '@material-ui/icons/Help';
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContent from "@material-ui/core/DialogContent";
import TextField from "@material-ui/core/TextField";
import DialogActions from "@material-ui/core/DialogActions";
import Dialog from "@material-ui/core/Dialog";
import Snackbar from "@material-ui/core/Snackbar";
import Fade from "@material-ui/core/Fade";
import MuiAlert from "@material-ui/lab/Alert";

function Alert(props) {
    return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const useStyles = makeStyles((theme) => ({
    left: {
        float: "left"
    },
    right: {
        float: "right"
    },
    hiddenButton: {
        margin: theme.spacing(1),
    },
    hiddenMenu: {
        marginBottom: theme.spacing(1)
    },
    bottomGrid: {
        minHeight: 20
    },
    paragraphTextField: {
        minWidth: 500
    },
}));


function BookViewer(props) {
    const classes = useStyles();
    const {book, editable} = props;
    const [results, setResults] = useState([]);
    const [dialogOpen, setDialogOpen] = useState(false);
    const [paragraph, setParagraph] = useState("");
    const [next, setNext] = useState("")
    const [previous, setPrevious] = useState("")
    const [pageNum, setPageNum] = useState(0);
    const [totalPage, setTotalPage] = useState(0);
    const [categories, setCategories] = useState(book.categories);
    const [transitionState, setTransitionState] = useState({
        open: false,
        Transition: Fade,
        severity: "",
        message: ""
    });

    useEffect(() => {
        let coreService = new CoreService();
        coreService.getBookContentsByBookId(book.id).then(e => {
            setResults(e.results);
            setNext(e.next);
            setPrevious(e.previous);
            setPageNum(1);
            setTotalPage(Math.ceil(e.count * 1.0 / ViewerPageLimit));
            if (!editable) {
                coreService.createBookAccess(book.id).then(e => console.log(`book access created ${book.id}`));
            }
        });
    }, []);

    const handleDialogCancel = () => {
        setDialogOpen(false);
        setParagraph("");
    };

    const handleDialogConfirm = () => {
        new CoreService().createBookContent(book.id, paragraph).then(e => {
            setTransitionState({open: true, Transition: Fade, message: "New paragraph added", severity: "success"});
            setDialogOpen(false);
            setParagraph("");
            let coreService = new CoreService();
            coreService.getBookContentsByBookId(book.id).then(e => {
                setResults(e.results);
                setNext(e.next);
                setPrevious(e.previous);
                setPageNum(1);
                setTotalPage(Math.ceil(e.count * 1.0 / ViewerPageLimit));
            });
        });
    };

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
    };

    const handleCategorize = () => {
        new CoreService().categorizeBook(book.id).then(e => {
            new CoreService().getBook(book.id).then(e => {
                setCategories(e.categories);
            });
        });
    };

    const closeSnackBar = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }
        setTransitionState({open: false, Transition: Fade});
    };

    return (
        <main>
            <Grid item xs={12} spacing={3}>
                <Grid container justify={"space-between"} spacing={24}>
                    <Typography variant="h6" gutterBottom>
                        {`${book.title} - ${categories.join(", ")}`}
                    </Typography>
                    <Typography variant="body2">
                        {`${pageNum}/${totalPage}`}
                    </Typography>
                </Grid>
                {editable && (
                    <Grid item xs={12} spacing={4} className={classes.hiddenMenu}>
                        <Button
                            variant="outlined"
                            size="small"
                            startIcon={<AddIcon/>}
                            className={classes.hiddenButton}
                            onClick={() => setDialogOpen(true)}
                        >
                            Add Paragraph
                        </Button>
                        <Button
                            variant="outlined"
                            size="small"
                            className={classes.hiddenButton}
                            startIcon={<HelpIcon/>}
                            onClick={handleCategorize}
                        >
                            Categorize
                        </Button>
                    </Grid>)}
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
            <Dialog open={dialogOpen}>
                <DialogTitle>Add new paragraph</DialogTitle>
                <DialogContent>
                    <TextField
                        className={classes.paragraphTextField}
                        margin="dense"
                        multiline
                        variant="outlined"
                        value={paragraph}
                        onChange={(e) => setParagraph(e.target.value)}
                        label="New Paragraph"/>
                </DialogContent>
                <DialogActions>
                    <Button color="primary" onClick={handleDialogCancel}>
                        Cancel
                    </Button>
                    <Button color="primary" onClick={handleDialogConfirm}>
                        Confirm
                    </Button>
                </DialogActions>
            </Dialog>
            <Snackbar
                open={transitionState.open}
                onClose={closeSnackBar}
                TransitionComponent={transitionState.Transition}
                autoHideDuration={3500}
            >
                <Alert onClose={closeSnackBar} severity={transitionState.severity}>
                    {transitionState.message}
                </Alert>
            </Snackbar>
        </main>
    );
}

BookViewer.propTypes = {
    book: PropTypes.any.isRequired,
    editable: PropTypes.bool
};

export default BookViewer;