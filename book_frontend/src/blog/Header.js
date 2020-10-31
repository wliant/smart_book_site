import * as React from 'react';
import PropTypes from 'prop-types';
import {makeStyles} from '@material-ui/core/styles';
import Toolbar from '@material-ui/core/Toolbar';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import AddIcon from '@material-ui/icons/Add';
import PersonIcon from '@material-ui/icons/Person';
import Typography from '@material-ui/core/Typography';
import Link from '@material-ui/core/Link';
import {Link as RouterLink} from 'react-router-dom';
import AuthService from './../services/AuthService';
import Tooltip from "@material-ui/core/Tooltip";
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContent from "@material-ui/core/DialogContent";
import TextField from "@material-ui/core/TextField";
import DialogActions from "@material-ui/core/DialogActions";
import Dialog from "@material-ui/core/Dialog";
import {useState} from "react";
import Snackbar from "@material-ui/core/Snackbar";
import Fade from "@material-ui/core/Fade";
import MuiAlert from "@material-ui/lab/Alert";
import CoreService from "../services/CoreService";
import {DropzoneArea} from "material-ui-dropzone";

const useStyles = makeStyles((theme) => ({
    toolbar: {
        borderBottom: `1px solid ${theme.palette.divider}`,
    },
    toolbarTitle: {
        flex: 1,
    },
    toolbarSecondary: {
        justifyContent: 'center',
        overflowX: 'auto',
    },
    toolbarLink: {
        padding: theme.spacing(1),
        flexShrink: 0,
    },
    storylineTextField: {
        minWidth: 400
    },
}));

function Alert(props) {
    return <MuiAlert elevation={6} variant="filled" {...props} />;
}

function Header(props) {
    const classes = useStyles();
    const [dialogOpen, setDialogOpen] = useState(false);
    const [bookTitle, setBookTitle] = useState("");
    const [bookStoryline, setBookStoryline] = useState("");
    const {sections, title} = props;
    const [selectedFile, setSelectedFile] = useState(null);
    const username = localStorage.getItem("username");
    const [transitionState, setTransitionState] = useState({
        open: false,
        Transition: Fade,
        severity: "",
        message: ""
    });

    const handleDialogCancel = () => {
        setBookTitle("");
        setBookStoryline("");
        setSelectedFile(null);
        setDialogOpen(false);
    };
    const handleDialogConfirm = () => {
        new CoreService().createBook(bookTitle, bookStoryline, selectedFile).then(() => {
            setTransitionState({open: true, Transition: Fade, message: "Book Created", severity: "success"});
            setDialogOpen(false);
            setBookTitle("");
            setBookStoryline("");
            setSelectedFile(null);
        });
    };
    const closeSnackBar = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }
        setTransitionState({open: false, Transition: Fade});
    };

    const handleDropzone = (files) => {
        setSelectedFile(files[0]);
    }

    return (
        <React.Fragment>
            <Toolbar className={classes.toolbar}>
                <Button
                    variant="outlined"
                    size="small"
                    startIcon={<AddIcon/>}
                    onClick={() => setDialogOpen(true)}
                >
                    Create Book
                </Button>
                <Typography
                    component="h2"
                    variant="h5"
                    color="inherit"
                    align="center"
                    noWrap
                    className={classes.toolbarTitle}
                >
                    {title}
                </Typography>
                <Tooltip title={username}>
                    <PersonIcon/>
                </Tooltip>
                <RouterLink onClick={() => {
                    new AuthService().logout()
                }} to="/auth/login">
                    <Button variant="outlined" size="small">
                        Log out
                    </Button>
                </RouterLink>
            </Toolbar>
            <Toolbar
                component="nav"
                variant="dense"
                className={classes.toolbarSecondary}
            >
                {sections.map((section) => (
                    <Link
                        color="inherit"
                        component="button"
                        noWrap
                        key={section.title}
                        variant="body2"
                        onClick={section.onClick}
                        className={classes.toolbarLink}
                    >
                        {section.title}
                    </Link>
                ))}
            </Toolbar>
            <Dialog open={dialogOpen}>
                <DialogTitle>Create a new book</DialogTitle>
                <DialogContent>
                    <DropzoneArea
                        filesLimit={1}
                        showAlerts={['error']}
                        acceptedFiles={['image/*']}
                        dropzoneText="Thumbnail"
                        onChange={handleDropzone}
                    /> <br/>
                    <TextField
                        autofocus
                        margin="dense"
                        variant="outlined"
                        value={bookTitle}
                        onChange={(e) => setBookTitle(e.target.value)}
                        label="Title"/> <br/>
                    <TextField
                        className={classes.storylineTextField}
                        margin="dense"
                        multiline
                        variant="outlined"
                        value={bookStoryline}
                        onChange={(e) => setBookStoryline(e.target.value)}
                        label="Storyline"/>
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
        </React.Fragment>
    );
}

Header.propTypes = {
    sections: PropTypes.arrayOf(
        PropTypes.shape({
            title: PropTypes.string.isRequired,
            onClick: PropTypes.func.isRequired,
        }),
    ).isRequired,
    title: PropTypes.string.isRequired,
};

export default Header;
