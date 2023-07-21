import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import MenuItem from '@mui/material/MenuItem';
import LocalDrinkIcon from '@mui/icons-material/LocalDrink';
import { Link as RouterLink } from 'react-router-dom';
import SignOutButton from './login/SignOutButton.jsx';

const ResponsiveAppBar = () => {
  const [anchorElNav, setAnchorElNav] = React.useState(null);

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const smallSizes = ['xs', 'sm', 'md'];
  const small = (value) => {
    const display = {};
    for (const size of smallSizes) {
      display[size] = value;
    }
    return display;
  };
  const big = 'lg';

  return (
    <AppBar position="fixed">
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <LocalDrinkIcon sx={{ display: { ...small('none'), md: 'flex' }, mr: 1 }} />
          <Typography
            variant="h6"
            noWrap
            component={RouterLink}
            to="/"
            sx={{
              mr: 2,
              display: { ...small('none'), [big]: 'flex' },
              fontFamily: 'monospace',
              fontWeight: 700,
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            Pi-na Colada
          </Typography>
          {/* hide when big */}
          <Box sx={{ flexGrow: 1, display: { ...small('flex'), [big]: 'none' } }}>
            <IconButton
              size="medium"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{
                display: { ...small('block'), [big]: 'none' },
              }}
            >
              <MenuItem key={'home'} onClick={handleCloseNavMenu}>
                <Typography
                  textAlign="center"
                  component={RouterLink}
                  to="/"
                  sx={{ textDecoration: 'none', color: 'black' }}
                >
                  Pour Drink
                </Typography>
              </MenuItem>
              <MenuItem key={'createDrink'} onClick={handleCloseNavMenu}>
                <Typography
                  textAlign="center"
                  component={RouterLink}
                  to="/createDrink"
                  sx={{ textDecoration: 'none', color: 'black' }}
                >
                  Create Drink
                </Typography>
              </MenuItem>
              <MenuItem key={'createIngredient'} onClick={handleCloseNavMenu}>
                <Typography
                  textAlign="center"
                  component={RouterLink}
                  to="/createIngredient"
                  sx={{ textDecoration: 'none', color: 'black' }}
                >
                  Create Ingredient
                </Typography>
              </MenuItem>
              <MenuItem key={'drinks'} onClick={handleCloseNavMenu}>
                <Typography
                  textAlign="center"
                  component={RouterLink}
                  to="/drinks"
                  sx={{ textDecoration: 'none', color: 'black' }}
                >
                  View Drinks
                </Typography>
              </MenuItem>
              <MenuItem key={'ingredients'} onClick={handleCloseNavMenu}>
                <Typography
                  textAlign="center"
                  component={RouterLink}
                  to="/ingredients"
                  sx={{ textDecoration: 'none', color: 'black' }}
                >
                  View Ingredients
                </Typography>
              </MenuItem>
            </Menu>
          </Box>
          <LocalDrinkIcon sx={{ display: { ...small('flex'), [big]: 'none' }, mr: 1 }} />
          <Typography
            variant="h5"
            noWrap
            component="a"
            sx={{
              mr: 2,
              display: { ...small('flex'), [big]: 'none' },
              flexGrow: 1,
              fontFamily: 'monospace',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            Pi-na Colada
          </Typography>
          {/* hide when small */}
          <Box sx={{ flexGrow: 1, display: { ...small('none'), [big]: 'flex' } }}>
            <Button
              key={'Home'}
              //onClick={handleCloseNavMenu}
              component={RouterLink}
              to="/"
              sx={{ my: 2, color: 'white', display: 'flex' }}
            >
              Pour Drink
            </Button>

            <Button
              key={'createDrink'}
              //onClick={handleCloseNavMenu}
              component={RouterLink}
              to="/createDrink"
              sx={{ my: 2, color: 'white', display: 'flex' }}
            >
              Create Drink
            </Button>

            <Button
              key={'createIngredient'}
              //onClick={handleCloseNavMenu}
              component={RouterLink}
              to="/createIngredient"
              sx={{ my: 2, color: 'white', display: 'flex' }}
            >
              Create Ingredient
            </Button>
            <Button
              key={'drinks'}
              //onClick={handleCloseNavMenu}
              component={RouterLink}
              to="/drinks"
              sx={{ my: 2, color: 'white', display: 'flex' }}
            >
              View Drinks
            </Button>
            <Button
              key={'ingredients'}
              //onClick={handleCloseNavMenu}
              component={RouterLink}
              to="/ingredients"
              sx={{ my: 2, color: 'white', display: 'flex' }}
            >
              View Ingredients
            </Button>
          </Box>

          {/* right box */}
          <Box sx={{ flexGrow: 0 }}>
            <SignOutButton />{' '}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};
export default ResponsiveAppBar;
