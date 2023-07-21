import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import '../App.css';
import cocktail from '../assets/cocktail.png';

const Home = () => {
  return (
    <Grid>
      <Grid item>
        <Box
          component="img"
          sx={{
            height: 1 / 4,
            width: 1 / 4,
          }}
          alt="Image of a cocktail."
          src={cocktail}
        />
      </Grid>
    </Grid>
  );
};

export default Home;
