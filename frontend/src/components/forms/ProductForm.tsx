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
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { styled } from '@mui/material/styles';
import { useForm, Controller } from "react-hook-form";


type ProductFormData = {
  name: string;
  description: string;
  price: number;
  category_ids: string[]; // Using strings for category IDs
  image_url?: string;
  image_file?: File;
};

const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

const ProductForm = () => {
  const { control, handleSubmit, register } = useForm<ProductFormData>();
  const [categories, setCategories] = useState<{ _id: string; name: string }[]>([]);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
        const file = event.target.files[0];
        setImageFile(file);
        setImagePreview(URL.createObjectURL(file));
    }
  };

  const handleUpload = async () => {
      if (!imageFile) return;
      const formData = new FormData();
      formData.append("file", imageFile);

      try {
          const response = await fetch("http://localhost:8000/api/products/image/upload", {
              method: "POST",
              body: formData
          });
          console.log("File uploaded:", response.status);
          const result = await response.json();
          return result;
      } catch (error) {
          console.error("Upload failed:", error);
      }
  };


  const onSubmit = async (data: ProductFormData) => {
    console.log("Submitting:", data);

    const { image_url } = await handleUpload();


    console.log("imageUrl", image_url);

    const dataWithImage = {
      ...data,
      image_url: image_url.replace("localstack", "0.0.0.0"),
    };

    console.log("Data with image:", dataWithImage);

    try {
      await fetch("http://0.0.0.0:8000/api/products", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dataWithImage),
      });
    } catch (error) {
      console.error("Error:", error);
    }
  };

  React.useEffect(() => {
    console.log("Categories:", categories);
    fetch("http://localhost:8000/api/categories")
    .then((res) => res.json())
    .then((data) => setCategories(data))
    .catch((err) => console.error("Error fetching products:", err));
  }, []);

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
                  <MenuItem key={category._id} value={category._id}>
                    {category.name}
                  </MenuItem>
                ))}
              </Select>
            )}
          />
        </FormControl>

        {imagePreview && <img src={imagePreview} alt="Preview" width={100} style={{ marginTop: 10 }} />}

        <Button
          component="label"
          role={undefined}
          variant="contained"
          tabIndex={-1}
          startIcon={<CloudUploadIcon />}
        >
          Upload files
          <VisuallyHiddenInput
            type="file"
            multiple
            accept="image/*"
            onChange={handleFileChange}
          />
        </Button>

        <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>
          Submit
        </Button>
      </Box>
    </Container>
  );
};

export default ProductForm;
