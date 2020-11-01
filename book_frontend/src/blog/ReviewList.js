import makeStyles from "@material-ui/core/styles/makeStyles";
import * as React from 'react';
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import Typography from "@material-ui/core/Typography";
import Divider from "@material-ui/core/Divider";

const useStyles = makeStyles(theme => ({
    root: {
        width: "100%",
        backgroundColor: theme.palette.background.paper
    },
    fonts: {
        fontWeight: "bold"
    },
    inline: {
        display: "inline"
    }
}));

function ReviewList({reviews}) {
    const classes = useStyles();
    return (
        <List className={classes.root}>
            {reviews.map(review => {
                console.log("Comment", review);
                return (
                    <React.Fragment key={review.id}>
                        <ListItem key={review.id} alignItems="flex-start">
                            <ListItemText
                                primary={
                                    <Typography className={classes.fonts}>
                                        {review.writer}
                                    </Typography>
                                }
                                secondary={
                                    <>
                                        <Typography
                                            component="span"
                                            variant="body2"
                                            className={classes.inline}
                                            color="textPrimary"
                                        >

                                        </Typography>
                                        {` - ${review.content}`}
                                    </>
                                }
                            />
                        </ListItem>
                        <Divider/>
                    </React.Fragment>
                );
            })}
        </List>
    );
};

export default ReviewList;