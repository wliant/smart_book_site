import React, { useState }  from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import { useHistory } from "react-router";
import { Link as RouterLink } from 'react-router-dom';
import CircularProgress from '@material-ui/core/CircularProgress';
import AuthService from './../services/AuthService';
import MuiAlert from '@material-ui/lab/Alert';
import Snackbar from '@material-ui/core/Snackbar';
import Fade from '@material-ui/core/Fade';

function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {'Copyright © '}
      <Link color="inherit" href="https://material-ui.com/">
        Your Website
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

export default function SignIn() {
  const classes = useStyles();
  const [ loading, setLoading ] = useState(false);
  const [ username, setUsername ] = useState("");
  const [ password, setPassword ] = useState("");
  const [transitionState, setTransitionState] = useState({
    open: false,
    Transition: Fade,
    message: ""
  })
  const history = useHistory();

  const handleLogin = () => {
    setLoading(true);
    new AuthService().login(username, password).then((token) => {
      localStorage.setItem("token", token);
      setLoading(false);
      history.push("/");
    }).catch(() => {
      setTransitionState({open: true, Transition: Fade, message: "login failed"});
      setLoading(false);
    });
  }

  const closeSnackBar = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setTransitionState({ open: false, Transition: Fade });
  }

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Avatar className={classes.avatar}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign in
        </Typography>
        <form className={classes.form} noValidate>
          <TextField
            variant="outlined"
            onChange={e => setUsername(e.target.value)}
            margin="normal"
            required
            fullWidth
            id="email"
            label="Username"
            name="username"
            autoComplete="username"
            autoFocus
          />
          <TextField
            variant="outlined"
            onChange={e => setPassword(e.target.value)}
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
          />
          <Button
            onClick={handleLogin}
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
          >
            {!loading && ("Sign In")}
            {loading && (<CircularProgress color="secondary" size={20} />)}
          </Button>

          <Grid container>
            <Grid item xs>
            </Grid>
            <Grid item>
              <RouterLink to="/auth/signUp">
                <Link href="#" variant="body2">
                  {"Don't have an account? Sign Up"}
                </Link>
              </RouterLink>
            </Grid>
          </Grid>
        </form>
      </div>
      <Snackbar
          open={transitionState.open}
          onClose={closeSnackBar}
          TransitionComponent={transitionState.Transition}
          autoHideDuration={3500}
        >
          <Alert onClose={closeSnackBar} severity="error">
            {transitionState.message}
          </Alert>
      </Snackbar>
      <Box mt={8}>
        <Copyright />
      </Box>
    </Container>
  );
}