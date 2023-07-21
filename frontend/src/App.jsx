import React, { useState, createContext } from 'react';
import './App.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { Container, CircularProgress } from '@mui/material';
import AppBar from './components/AppBar';
//import Home from './components/Home';
import PourDrink from './components/PourDrink';
import CreateDrink from './components/CreateDrink';
import CreateIngredient from './components/CreateIngredient';
import ViewDrinks from './components/ViewDrinks';
import ViewIngredients from './components/ViewIngredients';
import SignIn from './components/login/SignIn';
import SignUp from './components/login/SignUp';
import { initializeApp } from 'firebase/app';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import ResetPassword from './components/login/ResetPassword';

const firebaseConfig = {
  apiKey: 'AIzaSyA8VEoX-GbUJMJCQKwc8mLBbKdEeuEfZ1M',
  authDomain: 'pi-na-colada.firebaseapp.com',
  databaseURL: 'https://pi-na-colada-default-rtdb.firebaseio.com/',
  storageBucket: 'pi-na-colada.appspot.com',
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export const UserContext = createContext(null);
function App() {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  onAuthStateChanged(auth, (user) => {
    if (user) {
      // User is signed in, see docs for a list of available properties
      // https://firebase.google.com/docs/reference/js/firebase.User
      setUser(user);
      setIsLoading(false);
      // ...
    } else {
      setIsLoading(false);
    }
  });

  return isLoading ? (
    <CircularProgress />
  ) : (
    <div className="App">
      <UserContext.Provider value={{ user: user, setUser: setUser }}>
        <BrowserRouter>
          <AppBar />
          <br />
          <br />
          <Container maxWidth="lg">
            <Routes>
              <Route path="/" element={!user ? <SignIn /> : <PourDrink />} />
              <Route path="/createDrink" element={!user ? <SignIn /> : <CreateDrink />} />
              <Route path="/createIngredient" element={!user ? <SignIn /> : <CreateIngredient />} />
              <Route path="/drinks" element={!user ? <SignIn /> : <ViewDrinks />} />
              <Route path="/ingredients" element={!user ? <SignIn /> : <ViewIngredients />} />
              <Route path="/signIn" element={<SignIn />} />
              <Route path="/signUp" element={<SignUp />} />
              <Route path="/reset" element={<ResetPassword />} />
            </Routes>
          </Container>
        </BrowserRouter>
      </UserContext.Provider>
    </div>
  );
}

export default App;
