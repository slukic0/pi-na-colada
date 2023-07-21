import { useEffect, useState } from 'react';
import ipConstants from '../constants/ipConstants';
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

const ViewIngredients = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [ingredients, setIngredients] = useState();

  const getIngredients = async () => {
    const URL = `http://${ipConstants.BACKEND_HOST}/getIngredients`;
    const response = await axios.get(URL);
    setIngredients(response.data);
    setIsLoading(false);
    return response.data;
  };

  useEffect(() => {
    getIngredients();
  }, []);

  const handleDelete = async (ingredientId) => {
    const URL = `http://${ipConstants.BACKEND_HOST}/deleteIngredient/${ingredientId}`;
    const response = await axios.delete(URL);

    const temp = { ...ingredients };
    delete temp[ingredientId];
    setIngredients(temp);
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
            <TableCell align="center">Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {Object.entries(ingredients).map(([key, value]) => (
            <TableRow key={key} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
              <TableCell component="th" scope="row">
                {value.name || ''}
              </TableCell>
              <TableCell align="center">
                <IconButton onClick={() => handleDelete(key)}>
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

export default ViewIngredients;
