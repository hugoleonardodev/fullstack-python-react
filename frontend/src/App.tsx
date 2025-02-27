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
import ListOrders from 'components/tables/ListOrders';
import OrderForm from 'components/forms/OrderForm';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<div>LOGIN ???</div>} />
            <Route path="/" element={<MainLayout />}>
              <Route index element={<MainDashboard />} />
            </Route>
            <Route path="/products" element={<MainLayout />}>
              <Route index element={<ListProducts />} />
              <Route path=':create' element={<ProductForm />} />
            </Route>
            <Route path="/orders" element={<MainLayout />}>
              <Route index element={<ListOrders />} />
              <Route path=':create' element={<OrderForm />} />
            </Route>
            <Route path="*" element={<div>NOT FOUND</div>} />
          </Routes>
        </BrowserRouter>
      </AppProvider>
    </ThemeProvider>
  );
}

export default App;