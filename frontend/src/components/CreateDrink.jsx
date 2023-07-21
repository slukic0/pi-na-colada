import { useContext, useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ipConstants from '../constants/ipConstants';
import {
  Typography,
  TextField,
  Button,
  Snackbar,
  Grid,
  Alert,
  Container,
  CircularProgress,
} from '@mui/material';
import RowTable from './IngredientRowTable';
import { UserContext } from '../App';

const CreateDrink = () => {
  const { user } = useContext(UserContext);
  const [formValues, setFormValues] = useState();
  const [ingredients, setIngredients] = useState();
  const [isLoading, setIsLoading] = useState(true);
  const rowTableRef = useRef();

  const [errorState, setErrorState] = useState();
  const [open, setOpen] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormValues({
      ...formValues,
      [name]: value,
    });
  };

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpen(false);
  };

  useEffect(() => {
    getIngredients();
  }, []);

  const getIngredients = async () => {
    const URL = `http://${ipConstants.BACKEND_HOST}/getIngredients`;
    try {
      setErrorState(null);
      const response = await axios.get(URL);
      setIngredients(response.data);
      setIsLoading(false);
    } catch (error) {
      setErrorState(error.response);
      setOpen(true); // only open if error
    }
  };

  const createDrink = async () => {
    // get row table data
    const mixtureArray = rowTableRef.current.getRows();
    const mixture = [];
    for (const [ingredientId, amount] of mixtureArray) {
      mixture.push({ amount: amount, ingredientId: ingredientId });
    }
    const drink = {
      name: formValues.name,
      description: formValues.description,
      mixture,
      userId: user.uid,
    };

    const URL = `http://${ipConstants.BACKEND_HOST}/createDrink`;

    try {
      setErrorState(null);
      const response = await axios.post(URL, drink);
      console.log(`Created drink ${response.data}`, drink);
    } catch (error) {
      setErrorState(error.response);
    } finally {
      setOpen(true);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    await createDrink();
  };

  return isLoading ? (
    <CircularProgress />
  ) : (
    <Container>
      <Typography variant="h6" gutterBottom>
        Create Drink
      </Typography>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              id="name"
              name="name"
              label="Name"
              fullWidth
              autoComplete="drink-name"
              variant="standard"
              onChange={handleInputChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              id="description"
              name="description"
              label="Description"
              fullWidth
              autoComplete="drink-description"
              variant="standard"
              onChange={handleInputChange}
            />
          </Grid>
          <Grid item xs={12}>
            <RowTable ref={rowTableRef} ingredients={ingredients} />
          </Grid>
          <Grid item xs={12}>
            <Button variant="contained" color="primary" type="submit">
              Create
            </Button>
          </Grid>
        </Grid>
      </form>
      <Snackbar open={open} autoHideDuration={6000} onClose={handleClose}>
        <Alert
          onClose={handleClose}
          severity={errorState ? 'error' : 'success'}
          sx={{ width: '100%' }}
        >
          {errorState ? `Error: ${errorState.data.message}` : 'Drink created!'}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default CreateDrink;
