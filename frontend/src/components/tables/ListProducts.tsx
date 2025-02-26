import React, { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Avatar,
  Typography,
  Box,
} from "@mui/material";
import { Link } from "react-router-dom";

type Product = {
  _id: string;
  name: string;
  description: string;
  price: number;
  category_ids: string[];
  image_url?: string;
};

const ListProducts = () => {
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    fetch("http://0.0.0.0:8000/api/products")
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch((err) => console.error("Error fetching products:", err));
  }, []);

  console.log("Products:", products);

  return (
    <Box sx={{ display: "flex", justifyContent: "center", flexDirection: "column" }}>
    <Link to="/products/create" style={{ textDecoration: "none" }}>New Product</Link>

    <TableContainer component={Paper} sx={{ mt: 4 }}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Image</TableCell>
            <TableCell>Name</TableCell>
            <TableCell>Description</TableCell>
            <TableCell>Price</TableCell>
            <TableCell>Categories</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {products.length > 0 ? (
            products.map((product) => (
              <TableRow key={product._id}>
                <TableCell>
                {/* <Avatar src={product.image_url} alt={product.name} /> */}
                  {product.image_url ? (
                    <Avatar src={product.image_url} alt={product.name} />
                  ) : (
                    <Avatar>{product.name.charAt(0).toUpperCase()}</Avatar>
                  )}
                </TableCell>
                <TableCell>
                  <Typography fontWeight="bold">{product.name}</Typography>
                </TableCell>
                <TableCell>{product.description}</TableCell>
                <TableCell>${product.price.toFixed(2)}</TableCell>
                <TableCell>
                  <Box>
                    {product.category_ids.length > 0
                      ? product.category_ids.join(", ")
                      : "No categories"}
                  </Box>
                </TableCell>
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={5} align="center">
                No products found
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </TableContainer>
    </Box>
  );
};

export default ListProducts;
