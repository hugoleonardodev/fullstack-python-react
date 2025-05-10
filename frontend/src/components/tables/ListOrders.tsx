import React, { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Box,
} from "@mui/material";
import { Link } from "react-router-dom";

// Definição do tipo Order
type Order = {
  _id: string;
  date: string;
  product_ids: string[];
  total: number;
  category_ids: string[];
};

const ListOrders = () => {
  const [orders, setOrders] = useState<Order[]>([]);

  useEffect(() => {
    fetch("http://0.0.0.0:8000/api/orders")
      .then((res) => res.json())
      .then((data) => setOrders(data))
      .catch((err) => console.error("Error fetching orders:", err));
  }, []);

  console.log("Orders:", orders);

  return (
    <Box sx={{ display: "flex", justifyContent: "center", flexDirection: "column" }}>
      <Link to="/orders/create" style={{ textDecoration: "none" }}>New Order</Link>

      <TableContainer component={Paper} sx={{ mt: 4 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Date</TableCell>
              <TableCell>Products</TableCell>
              <TableCell>Total</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {orders.length > 0 ? (
              orders.map((order) => (
                <TableRow key={order._id}>
                  <TableCell>
                    <Typography fontWeight="bold">
                      {new Date(order.date).toLocaleString()}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Box>
                      {order.product_ids.length > 0
                        ? order.product_ids.join(", ")
                        : "No products"}
                    </Box>
                  </TableCell>
                  <TableCell>${order.total.toFixed(2)}</TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={4} align="center">
                  No orders found
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default ListOrders;
