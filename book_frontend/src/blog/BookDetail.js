import {makeStyles} from "@material-ui/core/styles";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import Link from "@material-ui/core/Link";
import PropTypes from "prop-types";
import * as React from "react";
import Card from "@material-ui/core/Card";
import CardActionArea from "@material-ui/core/CardActionArea";
import CardMedia from "@material-ui/core/CardMedia";
import CardActions from "@material-ui/core/CardActions";
import Button from "@material-ui/core/Button";
import ChromeReaderModeIcon from '@material-ui/icons/ChromeReaderMode';
import CommentIcon from '@material-ui/icons/Comment';
import EditIcon from '@material-ui/icons/Edit';
import CardContent from "@material-ui/core/CardContent";
import TextField from "@material-ui/core/TextField";
import {NavigationContext} from "./Blog";
import {useEffect, useState} from "react";
import CoreService from "../services/CoreService";
import ReviewList from "./ReviewList";
import MenuItem from "@material-ui/core/MenuItem";
import IconButton from "@material-ui/core/IconButton";
import SearchIcon from "@material-ui/icons/Search";
import ArrowBackIosIcon from "@material-ui/icons/ArrowBackIos";
import ArrowForwardIosIcon from "@material-ui/icons/ArrowForwardIos";
import BookCard from "./BookCard";
import Divider from "@material-ui/core/Divider";
import InputBase from "@material-ui/core/InputBase";
import Dialog from "@material-ui/core/Dialog";
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContent from "@material-ui/core/DialogContent";
import DialogActions from "@material-ui/core/DialogActions";


const useStyles = makeStyles((theme) => ({
    main: {
        marginTop: theme.spacing(3),
        marginBottom: theme.spacing(3)
    },
    sub: {
        marginTop: theme.spacing(1),
        marginBottom: theme.spacing(3)
    },
    reviewCard: {
        minWidth: 120,
        minHeight: 90,
        margin: theme.spacing(1)
    },
    card: {
        display: 'flex'
    },
    cardDetails: {
        flex: 1,
    },
    cardMedia: {
        width: 320,
    },
    dialogText: {
        minWidth:400
    },
}));

const renderField = (fieldName, value) => {
    return (
        <div>
            <Typography variant="caption" color="textSecondary">
                {fieldName}
            </Typography>
            <Typography variant="subtitle1" color="textPrimary">
                {value}
            </Typography>
        </div>
    );
};

function BookDetail(props) {
    const classes = useStyles();
    const {book} = props;
    const [reviews, setReviews] = useState([])
    const [dialogOpen, setDialogOpen] = useState(false);
    const [dialogText, setDialogText] = useState("");
    const {ReadBook} = React.useContext(NavigationContext);

    useEffect(() => {
        loadReviews();
    }, []);

    const handleAddReview = () => {
        setDialogOpen(true);
    }

    const handleDialogConfirm = () => {
        new CoreService().createBookReview(book.id, dialogText).then(() => {
            setDialogText("");
            setDialogOpen(false);
            loadReviews();
        });
    };

    const handleDialogCancel = () => {
        setDialogOpen(false);
    };

    const loadReviews = () => {
        new CoreService().getBookReviews(book.id).then(e => setReviews(e));
    };
    return (
        <main>
            <Grid item xs={12} className={classes.main}>
                <Card className={classes.card}>
                    <CardMedia
                        component="img"
                        image={book.thumbnail}
                        className={classes.cardMedia}
                    />
                    <div className={classes.cardDetails}>
                        <CardContent>
                            {renderField("Title", book.title)}
                            {renderField("Author", book.author)}
                            {renderField("Categories", book.categories.join(", "))}
                            {renderField("Created on", book.created)}
                            {renderField("Storyline", book.story_line)}
                        </CardContent>

                        <CardActions>
                            <Button
                                variant="outlined"
                                size="small"
                                startIcon={<ChromeReaderModeIcon/>}
                                onClick={() => ReadBook(book)}
                            >
                                Read
                            </Button>
                            <Button
                                variant="outlined"
                                size="small"
                                startIcon={<CommentIcon/>}
                                onClick={handleAddReview}
                            >
                                Add Review
                            </Button>
                            <Button
                                variant="outlined"
                                size="small"
                                startIcon={<EditIcon/>}
                            >
                                Write More
                            </Button>
                        </CardActions>
                    </div>
                </Card>
            </Grid>
            <Typography variant="h6" gutterBottom>
                Book Reviews
            </Typography>
            <Divider/>
            <Grid container spacing={2} className={classes.sub}>
                {reviews &&
                reviews.map((review) => (
                    <Card className={classes.reviewCard}>
                        <CardContent>
                            <Typography variant="caption" gutterBottom color="textSecondary" paragraph>
                                {review.created} <br />
                                {review.writer}
                            </Typography>
                            <TextField multiline disabled
                                       variant="outlined"
                                       value={review.content}
                                       color="textPrimary"
                            />
                        </CardContent>
                    </Card>
                ))}
            </Grid>
            <Dialog open={dialogOpen}>
                <DialogTitle>Add Review</DialogTitle>
                <DialogContent>
                    <TextField
                        className={classes.dialogText}
                        autofocus
                        margin="dense"
                        multiline
                        variant="outlined"
                        value={dialogText}
                        onChange={(e) => setDialogText(e.target.value)}
                        label="review" />
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
        </main>

    );
}

BookDetail.propTypes = {
    book: PropTypes.objectOf({
        id: PropTypes.number.isRequired,
        categories: PropTypes.array.isRequired,
        title: PropTypes.string.isRequired,
        created: PropTypes.string.isRequired,
        story_line: PropTypes.string.isRequired,
        thumbnail: PropTypes.string.isRequired
    }).isRequired,
};

export default BookDetail;