import {
  Button,
  Table,
  TableBody,
  TableRow,
  TableCell,
  CircularProgress,
  Box,
  Typography,
  Snackbar,
  Alert,
} from '@mui/material';
import '../App.css';
import SelectDropdown from './SelectDropdown';
import ipConstants from '../constants/ipConstants';
import axios from 'axios';
import { Fragment, useEffect, useState, useContext } from 'react';
import { UserContext } from '../App';

const Home = () => {
  const { user } = useContext(UserContext);
  const [isLoading, setIsLoading] = useState(true);
  const [isDrinksLoading, setIsDrinksLoading] = useState(true);
  const [ingredients, setIngredients] = useState();
  const [selectedIngredients, setSelectedIngredients] = useState({});
  const [availableDrinks, setAvailableDrinks] = useState({});
  const [drink, setDrink] = useState('');
  const machines = { realPi: { name: 'Real Pi' }, mockPi: { name: 'Mock Pi' } };
  const [machine, setMachine] = useState('realPi');
  const [error, setError] = useState();
  const [open, setOpen] = useState();

  const getIngredients = async () => {
    const URL = `http://${ipConstants.BACKEND_HOST}/getIngredients`;
    const response = await axios.get(URL);
    setIngredients(response.data);
    setIsLoading(false);
  };

  useEffect(() => {
    getIngredients();
  }, []);

  const handleIngredientChange = (event, i) => {
    setDrink('');
    const temp = { ...selectedIngredients };
    if (event.target.value === '') {
      delete temp[i];
    } else {
      temp[i] = event.target.value;
    }

    setSelectedIngredients(temp);
  };

  const getAvailableDrinks = async () => {
    const URL = `http://${ipConstants.BACKEND_HOST}/getDrinksFromIngredients`;
    const response = await axios.post(URL, {
      ingredients: Object.values(selectedIngredients),
      userId: user.uid,
    });
    const drinks = {};
    for (const drink of response.data) {
      drinks[drink.id] = { name: drink.name };
    }
    setAvailableDrinks(drinks);
  };

  useEffect(() => {
    setIsDrinksLoading(true);
    getAvailableDrinks();
    setIsDrinksLoading(false);
  }, [selectedIngredients]);

  const pourDrink = async () => {
    let URL;
    if (machine === 'mockPi') {
      URL = `http://${ipConstants.BACKEND_HOST}/mockPourDrink`;
    } else {
      URL = `http://${ipConstants.BACKEND_HOST}/pourDrink`;
    }

    const pour = {
      drinkId: drink,
      pumps: selectedIngredients,
      userId: user.uid,
    };
    try {
      console.log(pour);
      const response = await axios.post(URL, pour);
      console.log(response.data);
    } catch (error) {
      console.error(error.response);
      setError(error.response.data);
    } finally {
      setOpen(true);
    }
  };

  const disableItem = (key) => {
    return Object.values(selectedIngredients).find((e) => e === key) !== undefined ? true : false;
  };

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpen(false);
  };

  const createRows = () => {
    const rows = [];
    for (let i = 1; i <= 4; i++) {
      rows.push(
        <TableRow key={i}>
          <TableCell>
            <SelectDropdown
              key={i}
              id={i.toString()}
              label={`Pump ${i} Ingredient`}
              items={ingredients}
              itemDisabled={disableItem}
              showNone={true}
              onChange={(event) => handleIngredientChange(event, i)}
            />
          </TableCell>
        </TableRow>,
      );
    }
    return rows;
  };

  const drinksAvailable =
    !isDrinksLoading && Object.keys(availableDrinks).length != 0 && machine !== '';

  return isLoading ? (
    <CircularProgress />
  ) : (
    <Fragment>
      <Typography variant="h6" gutterBottom>
        Please enter Pump Ingredients and Select Drink
      </Typography>
      <Table sx={{ minWidth: 300 }} aria-label="simple table">
        <TableBody>
          <TableRow>
            <TableCell>
              <SelectDropdown
                id="machine"
                label="Cocktail Machine"
                items={machines}
                value={'realPi'}
                onChange={(event) => setMachine(event.target.value)}
                showNone={false}
              />
            </TableCell>
          </TableRow>
          {createRows()}
          <TableRow>
            <TableCell>
              <SelectDropdown
                id="Drink"
                label="Drink"
                items={drinksAvailable ? availableDrinks : null}
                disabled={!drinksAvailable}
                onChange={(event) => setDrink(event.target.value)}
                showNone={false}
              />
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
      <Box p={2}>
        <Button
          variant="contained"
          color="primary"
          type="submit"
          onClick={pourDrink}
          disabled={drink === '' || !drinksAvailable}
        >
          Pour Drink
        </Button>
      </Box>
      <Snackbar open={open} autoHideDuration={6000} onClose={handleClose}>
        <Alert onClose={handleClose} severity={error ? 'error' : 'success'} sx={{ width: '100%' }}>
          {error ? `Error: ${error.message}` : 'Drink poured!'}
        </Alert>
      </Snackbar>
    </Fragment>
  );
};

export default Home;
