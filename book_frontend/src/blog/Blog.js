import * as React from 'react';
import {useState, useEffect} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Container from '@material-ui/core/Container';
import Header from './Header';
import Footer from './Footer';
import Chatbot from './../chatbot/Chatbot';
import BookViewer from "./BookViewer";
import Browse from "./Browse";
import MyBooks from "./MyBooks";
import BookDetail from "./BookDetail";

const useStyles = makeStyles((theme) => ({
    mainGrid: {
        marginTop: theme.spacing(3),
    },
}));

export const NavigationContext = React.createContext(null);

export default function Blog() {
    const classes = useStyles();
    const [navigationState, setNavigationState] = useState({name: "browse"})

    const sections = [
        {title: 'Browse', onClick: () => setNavigationState({name: "browse"})},
        {title: 'My Books', onClick: () => setNavigationState({name: "mybooks"})},
    ];

    const navigator = {
        ShowBook: (book) => {
            setNavigationState({name: "bookDetail", data: book});
        },
        ReadBook: (book) => {
            setNavigationState({name: "bookView", data: book});
        },
        EditBook: (book) => {
            setNavigationState( {name: "bookEdit", data: book });
        },
    }

    const renderMain = (state) => {
        switch (state.name) {
            case 'browse':
                return (<Browse/>);
            case 'mybooks':
                return (<MyBooks/>);
            case 'bookDetail':
                return (<BookDetail book={state.data} />);
            case 'bookView':
                return (<BookViewer editable={false} book={state.data} />);
            case 'bookEdit':
                return (<BookViewer editable={true} book={state.data} />);
            default:
                return "";
        }
    };

    return (
        <NavigationContext.Provider value={navigator}>
            <React.Fragment>
                <CssBaseline/>
                <Container maxWidth="lg">
                    <Header title="Smart Book" sections={sections}/>
                    {renderMain(navigationState)}
                </Container>
                <Chatbot/>
                <Footer
                    title="Practical Language Processing"
                    description="Brought to you by Darryl, Tang Meng, Raymond, William"
                />
            </React.Fragment>
        </NavigationContext.Provider>
    );
}
