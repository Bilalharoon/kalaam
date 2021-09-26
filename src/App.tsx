import React from 'react';

import {
  BrowserRouter as Router,
  Switch,
  Route,
  // eslint-disable-next-line
  Link
} from "react-router-dom";

import Home from "./Components/Home"
import { ThemeProvider, createTheme } from '@mui/material/styles';
function App() {

  const theme = createTheme({

    palette: {
      mode: "dark",
      primary: {
        main: "#019000",
      },
      secondary: {
        main: "#F30079"
      }
    }
  })
  return (

    <Router>
      <Switch>
        <Route path="/">
          <ThemeProvider theme={theme}>
            <Home />
          </ThemeProvider>
        </Route>
      </Switch>
    </Router>

  );
}

export default App;
