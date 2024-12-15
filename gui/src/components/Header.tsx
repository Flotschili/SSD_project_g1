import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import AuthService from '../services/AuthService';
import logo from '../logo_cropped.jpg';

const Header: React.FC = () => {
  const handleLogout = () => {
    AuthService.logout().then(() => {
      window.location.reload();
    });
  };

  return (
    <AppBar position="static" sx={{marginBottom: '1rem'}}>
      <Toolbar>
        <Box sx={{ flexGrow: 1 }}>
          <img src={logo} alt="Beer" style={{ height: '3rem' }} />
        </Box>
        <Button color="inherit" onClick={handleLogout}>
          Logout
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default Header;