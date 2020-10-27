import * as React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Hidden from '@material-ui/core/Hidden';

const useStyles = makeStyles({
  card: {
    display: 'flex',
  },
  cardDetails: {
    flex: 1,
  },
  cardMedia: {
    width: 160,
  },
});

function FeaturedPost(props) {
  const classes = useStyles();
  const { book, onClick } = props;

  return (
    <Grid item xs={12} md={6}>
      <CardActionArea component="a" onClick={() => onClick(book)}>
        <Card className={classes.card}>
          <div className={classes.cardDetails}>
            <CardContent>
              <Typography component="h2" variant="h5">
                {book.title}
              </Typography>
              <Typography variant="subtitle1" color="textSecondary">
                {book.author}
              </Typography>
              <Typography variant="subtitle1" paragraph>
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

FeaturedPost.propTypes = {
  book: PropTypes.any.isRequired,
  onClick: PropTypes.func.isRequired,
};

export default FeaturedPost;
