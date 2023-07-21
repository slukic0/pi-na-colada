import { useEffect, useState, useContext } from 'react';
import ipConstants from '../constants/ipConstants';
import { UserContext } from '../App';
import axios from 'axios';
import {
  CircularProgress,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

const ViewDrinks = () => {
  const { user } = useContext(UserContext);
  const [isLoading, setIsLoading] = useState(true);
  const [drinks, setDrinks] = useState();

  const getIngredients = async (ids) => {
    const URL = `http://${ipConstants.BACKEND_HOST}/getIngredient`;
    const response = await axios.post(URL, { ingredients: ids });
    return response.data;
  };

  const getDrinks = async (userId) => {
    const URL = `http://${ipConstants.BACKEND_HOST}/getUserDrinks`;
    const response = await axios.post(URL, { id: userId });
    return response.data;
  };

  useEffect(() => {
    const loadData = async () => {
      const drinks = await getDrinks(user.uid);

      // get the ingredient names
      const ingredientIds = [];
      for (const drink of drinks) {
        for (const ingredient of drink.mixture) {
          ingredientIds.push(ingredient.ingredientId);
        }
      }
      const ingredients = await getIngredients(ingredientIds);

      // add names to each drink
      for (const drink of drinks) {
        for (const ingredient of drink.mixture) {
          ingredient.name = ingredients[ingredient.ingredientId].name;
        }
      }
      setDrinks(drinks);
      setIsLoading(false);
    };
    loadData();
  }, []);

  const handleDelete = async (drinkId) => {
    console.log('Delete drink with id ', drinkId);
    const URL = `http://${ipConstants.BACKEND_HOST}/deleteDrink/${drinkId}/${user.uid}`;
    const response = await axios.delete(URL);

    const filtered = drinks.filter((x) => x.id !== drinkId);
    setDrinks(filtered);

    return response.data;
  };

  return isLoading ? (
    <CircularProgress />
  ) : (
    <TableContainer component={Paper}>
      <Table aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell align="left">Name</TableCell>
            <TableCell align="right">Mixture</TableCell>
            <TableCell align="center">Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {drinks.map((drink) => (
            <TableRow key={drink.id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
              <TableCell component="th" scope="row">
                {drink.name}
              </TableCell>
              <TableCell align="right">{drink.mixture.map((x) => x.name).join(', ')}</TableCell>
              <TableCell align="center">
                <IconButton onClick={() => handleDelete(drink.id)}>
                  <DeleteIcon />
                </IconButton>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default ViewDrinks;
