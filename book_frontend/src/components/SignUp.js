import React, { useState } from 'react';
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
    marginTop: theme.spacing(3),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

export default function SignUp() {
  const classes = useStyles();
  const [ loading, setLoading ] = useState(false);
  const [ firstname, setFirstname ] = useState("");
  const [ lastname, setLastname ] = useState("");
  const [ username, setUsername ] = useState("");
  const [ password, setPassword ] = useState("");

  const [transitionState, setTransitionState] = useState({
    open: false,
    Transition: Fade,
    severity: "",
    message: ""
  });

  const handleSignUp = () => {
    setLoading(true);
    new AuthService().signup(firstname, lastname, username, password).then((token) => {
      setLoading(false);
      setTransitionState({open: true, Transition: Fade, message: "Sign up successful", severity: "success"});
      setPassword("");
    }).catch(() => {
      setTransitionState({open: true, Transition: Fade, message: "unable to signup", severity: "error"});
      setLoading(false);
      setPassword("");
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
          Sign up
        </Typography>
        <form className={classes.form} noValidate>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField
                autoComplete="fname"
                onChange={e => setFirstname(e.target.value)}
                name="firstName"
                variant="outlined"
                required
                fullWidth
                id="firstName"
                label="First Name"
                autoFocus
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                variant="outlined"
                onChange={e => setLastname(e.target.value)}
                required
                fullWidth
                id="lastName"
                label="Last Name"
                name="lastName"
                autoComplete="lname"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                onChange={e => setUsername(e.target.value)}
                required
                fullWidth
                id="username"
                label="Username"
                name="username"
                autoComplete="username"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                onChange={e => setPassword(e.target.value)}
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="current-password"
              />
            </Grid>
          </Grid>
          <Button
            fullWidth
            onClick={handleSignUp}
            variant="contained"
            color="primary"
            className={classes.submit}
          >
            {!loading && ("Sign Up")}
            {loading && (<CircularProgress color="secondary" size={20} />)}
          </Button>
          <Grid container justify="flex-end">
            <Grid item>
              <RouterLink to="/auth/login">
                <Link href="#" variant="body2">
                  Already have an account? Sign in
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
          <Alert onClose={closeSnackBar} severity={transitionState.severity}>
            {transitionState.message}
          </Alert>
      </Snackbar>
      <Box mt={5}>
        <Copyright />
      </Box>
    </Container>
  );
}