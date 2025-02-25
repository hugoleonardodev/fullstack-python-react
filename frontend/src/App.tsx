// src/App.js
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import theme from './theme';
import { AppProvider } from './contexts/AppContext';
import MainLayout from './components/layouts/MainLayout';
import ProductForm from 'components/forms/ProductForm';
import ListProducts from 'components/tables/ListProducts';
import MainDashboard from 'components/dashboards/MainDashboard';

// Import your pages here
// import Dashboard from './pages/Dashboard';
// import Login from './pages/Login';
// import NotFound from './pages/NotFound';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<div>LOGIN ???</div>} />
            <Route path="/" element={<MainLayout />}>
              {/* Nested routes that use the MainLayout */}
              <Route index element={<MainDashboard />} />
              {/* Add more routes here */}
            </Route>
            <Route path="/products" element={<MainLayout />}>
              {/* Nested routes that use the MainLayout */}
              <Route index element={<ListProducts />} />
              <Route path=':create' element={<ProductForm />} />
              {/* Add more routes here */}
            </Route>
            <Route path="*" element={<div>NOT FOUND</div>} />
          </Routes>
        </BrowserRouter>
      </AppProvider>
    </ThemeProvider>
  );
}

export default App;