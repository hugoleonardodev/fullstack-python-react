import React, { useState } from "react";
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

type ProductFormData = {
  name: string;
  description: string;
  price: number;
  category_ids: string[]; // Using strings for category IDs
  image_url?: string;
};

const ProductForm = () => {
  const { control, handleSubmit, register } = useForm<ProductFormData>();
  const [categories] = useState([
    { id: "60f7d4c1e1c9a6a1e4b3b3b3", name: "Category 1" },
    { id: "60f7d4c1e1c9a6a1e4b3b3b4", name: "Category 2" },
  ]);

  const onSubmit = async (data: ProductFormData) => {
    console.log("Submitting:", data);

    try {
      const response = await fetch("http://0.0.0.0:8000/products", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        alert("Product created successfully!");
      } else {
        alert("Error creating product.");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 4 }}>
        <TextField
          label="Name"
          fullWidth
          margin="normal"
          {...register("name")}
        />
        <TextField
          label="Description"
          fullWidth
          margin="normal"
          multiline
          rows={3}
          {...register("description")}
        />
        <TextField
          label="Price"
          fullWidth
          margin="normal"
          type="number"
          {...register("price")}
        />

        <FormControl fullWidth margin="normal">
          <InputLabel>Category</InputLabel>
          <Controller
            name="category_ids"
            control={control}
            defaultValue={[]}
            render={({ field }) => (
              <Select {...field} multiple>
                {categories.map((category) => (
                  <MenuItem key={category.id} value={category.id}>
                    {category.name}
                  </MenuItem>
                ))}
              </Select>
            )}
          />
        </FormControl>

        <TextField
          label="Image URL"
          fullWidth
          margin="normal"
          {...register("image_url")}
        />

        <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>
          Submit
        </Button>
      </Box>
    </Container>
  );
};

export default ProductForm;
