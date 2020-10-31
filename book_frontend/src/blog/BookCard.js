import * as React from 'react';
import PropTypes from 'prop-types';
import {makeStyles} from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Hidden from '@material-ui/core/Hidden';
import {NavigationContext} from "./Blog";


function BookCard(props) {
    const {book, md, minHeight} = props;
    const useStyles = makeStyles({
        card: {
            display: 'flex',
            minHeight: minHeight,
        },
        cardDetails: {
            flex: 1,
        },
        cardMedia: {
            width: 160,
        },
    });

    const classes = useStyles();
    const {ShowBook} = React.useContext(NavigationContext);

    return (
        <Grid item xs={12} md={md}>
            <CardActionArea component="a" onClick={() => ShowBook(book)}>
                <Card className={classes.card}>
                    <div className={classes.cardDetails}>
                        <CardContent>
                            <Typography component="h5" variant="h6">
                                {book.title}
                            </Typography>
                            <Typography variant="subtitle1" color="textSecondary">
                                {book.author}
                            </Typography>
                            <Typography variant="caption" paragraph>
                                {book.story_line}
                            </Typography>
                            <Typography variant="subtitle1" color="primary">
                                Continue reading...
                            </Typography>
                        </CardContent>
                    </div>
                    <Hidden smDown>
                        <CardMedia
                            className={classes.cardMedia}
                            image={book.thumbnail}
                        />
                    </Hidden>
                </Card>
            </CardActionArea>
        </Grid>
    );
}

BookCard.propTypes = {
    book: PropTypes.any.isRequired,
    md: PropTypes.number.isRequired,
    minHeight: PropTypes.number.isRequired,
};

export default BookCard;
