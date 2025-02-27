import React, { useState, useEffect } from "react";
import {
  TextField,
  Button,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
  Container,
  Box,
} from "@mui/material";
import { useForm, Controller } from "react-hook-form";

type OrderFormData = {
  date: string;
  product_ids: string[];
  total: number;
  category_ids: string[];
};

const OrderForm = () => {
  const { control, handleSubmit, register } = useForm<OrderFormData>();
  const [products, setProducts] = useState<{ _id: string; name: string }[]>([]);
  const [categories, setCategories] = useState<{ _id: string; name: string }[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/products")
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch((err) => console.error("Error fetching products:", err));

    fetch("http://localhost:8000/api/categories")
      .then((res) => res.json())
      .then((data) => setCategories(data))
      .catch((err) => console.error("Error fetching categories:", err));
  }, []);

  const onSubmit = async (data: OrderFormData) => {
    try {
      await fetch("http://0.0.0.0:8000/api/orders", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
        }
      });
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 4 }}>
        <TextField
          label="Date"
          type="datetime-local"
          fullWidth
          margin="normal"
          {...register("date")}
        />

        <TextField
          label="Total"
          fullWidth
          margin="normal"
          type="number"
          {...register("total")}
        />

        <FormControl fullWidth margin="normal">
          <InputLabel>Products</InputLabel>
          <Controller
            name="product_ids"
            control={control}
            defaultValue={[]}
            render={({ field }) => (
              <Select {...field} multiple>
                {products.map((product) => (
                  <MenuItem key={product._id} value={product._id}>
                    {product.name}
                  </MenuItem>
                ))}
              </Select>
            )}
          />
        </FormControl>

        <FormControl fullWidth margin="normal">
          <InputLabel>Categories</InputLabel>
          <Controller
            name="category_ids"
            control={control}
            defaultValue={[]}
            render={({ field }) => (
              <Select {...field} multiple>
                {categories.map((category) => (
                  <MenuItem key={category._id} value={category._id}>
                    {category.name}
                  </MenuItem>
                ))}
              </Select>
            )}
          />
        </FormControl>

        <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>
          Submit Order
        </Button>
      </Box>
    </Container>
  );
};

export default OrderForm;
