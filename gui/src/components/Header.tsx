import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import AuthService from '../services/AuthService';

const Header: React.FC = () => {
  const handleLogout = () => {
    AuthService.logout().then(() => {
      window.location.reload();
    });
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          BeerHub
        </Typography>
        <Button color="inherit" onClick={handleLogout}>
          Logout
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default Header;