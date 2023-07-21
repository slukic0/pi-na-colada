import { Typography, TextField, Button, Snackbar, Grid, Alert, Container } from '@mui/material';
import { useState } from 'react';
import axios from 'axios';
import ipConstants from '../constants/ipConstants';

const CreateIngredient = () => {
  const [formValues, setFormValues] = useState();
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

  const createIngredient = async () => {
    const URL = `http://${ipConstants.BACKEND_HOST}/createIngredient`;
    const ingredient = {
      name: formValues.name,
      description: formValues.description,
    };
    try {
      setErrorState(null);
      const response = await axios.post(URL, ingredient);
      console.log(response.data);
      setOpen(true);
    } catch (error) {
      setErrorState(error.response);
    } finally {
      setOpen(true);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    await createIngredient();
  };

  return (
    <Container>
      <Typography variant="h6" gutterBottom>
        Create Ingredient
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
              autoComplete="ingredient-name"
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
              autoComplete="ingredient-description"
              variant="standard"
              onChange={handleInputChange}
            />
          </Grid>
          <Grid item xs={12}>
            {errorState && (
              <Alert severity="error" sx={{ margin: '5px' }}>
                Cannot create ingredient - {errorState.data.message}
              </Alert>
            )}
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
          {errorState ? `Error: ${errorState.data.message}` : 'Ingredient created!'}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default CreateIngredient;
