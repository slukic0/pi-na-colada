import { getAuth } from 'firebase/auth';
import { initializeApp } from 'firebase/app';
import { Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { UserContext } from '../../App';
import { useContext } from 'react';

const firebaseConfig = {
  apiKey: 'AIzaSyA8VEoX-GbUJMJCQKwc8mLBbKdEeuEfZ1M',
  authDomain: 'pi-na-colada.firebaseapp.com',
  databaseURL: 'https://pi-na-colada-default-rtdb.firebaseio.com/',
  storageBucket: 'pi-na-colada.appspot.com',
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const SignOutButton = () => {
  const { user, setUser } = useContext(UserContext);
  const navigate = useNavigate();

  const signOutUser = async () => {
    await auth.signOut();
    setUser(null);
    navigate('/signIn');
  };

  return user ? (
    <Button variant="secondary" onClick={signOutUser}>
      Logout
    </Button>
  ) : null;
};

export default SignOutButton;
