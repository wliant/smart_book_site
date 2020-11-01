import * as React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Link from '@material-ui/core/Link';

const useStyles = makeStyles((theme) => ({
  sidebarAboutBox: {
    padding: theme.spacing(2),
    backgroundColor: theme.palette.grey[200],
  },
  sidebarSection: {
    marginTop: theme.spacing(3),
  },
}));

function Sidebar(props) {
  const classes = useStyles();
  const { categories, social, categoryClicked } = props;

  return (
    <Grid item xs={12} md={2}>
      <Typography variant="h6" gutterBottom className={classes.sidebarSection}>
        Categories
      </Typography>
      {categories.map((category) => (
        <Link
          display="block"
          component="button"
          variant="body1"
          key={category.name}
          onClick={() => categoryClicked(category.name)}
        >
          {`${category.name} (${category.book_count})`}
        </Link>
      ))}

      <Typography variant="h6" gutterBottom className={classes.sidebarSection}>
        Social
      </Typography>
      {social.map((network) => (
        <Link display="block" variant="body1" href="#" key={network.name} component="button">
          <Grid container direction="row" spacing={1} alignItems="center">
            <Grid item>
              <network.icon />
            </Grid>
            <Grid item>{network.name}</Grid>
          </Grid>
        </Link>
      ))}
    </Grid>
  );
}

Sidebar.propTypes = {
  categories: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      book_count: PropTypes.number.isRequired,
    }),
  ).isRequired,
  categoryClicked: PropTypes.func,
  social: PropTypes.arrayOf(
    PropTypes.shape({
      icon: PropTypes.elementType.isRequired,
      name: PropTypes.string.isRequired,
    }),
  ).isRequired
};

export default Sidebar;
