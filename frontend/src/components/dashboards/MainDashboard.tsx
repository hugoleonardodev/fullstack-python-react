import React, { useEffect, useState } from "react";
import { Box, Grid, Paper, Typography } from "@mui/material";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import AttachMoneyIcon from "@mui/icons-material/AttachMoney";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";
import ReceiptIcon from "@mui/icons-material/Receipt";

type Order = {
  id: string;
  total: number;
  date: string; // Data do pedido
};

const MainDashboard = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [totalOrders, setTotalOrders] = useState(0);
  const [averageOrderValue, setAverageOrderValue] = useState(0);
  const [totalRevenue, setTotalRevenue] = useState(0);
  const [ordersPerPeriod, setOrdersPerPeriod] = useState<{ period: string; count: number }[]>([]);

  useEffect(() => {
    fetch("http://0.0.0.0:8000/api/orders")
      .then((res) => res.json())
      .then((data: Order[]) => {
        setOrders(data);

        const total = data.length;
        const revenue = data.reduce((sum, order) => sum + order.total, 0);
        const average = total > 0 ? revenue / total : 0;

        console.log('revenue', revenue);
        console.log('average', average);

        setTotalOrders(total);
        setTotalRevenue(revenue);
        setAverageOrderValue(average);

        // Agrupar pedidos por mês
        const grouped = data.reduce((acc, order) => {
          const month = new Date(order.date).toLocaleString("en-US", { month: "short" });
          console.log('month', month);
          acc[month] = (acc[month] || 0) + 1;
          return acc;
        }, {} as Record<string, number>);

        setOrdersPerPeriod(Object.entries(grouped).map(([month, count]) => ({ period: month, count })));
      })
      .catch((err) => console.error("Erro ao buscar pedidos:", err));
  }, []);

  console.log('orders', orders);

  return (
    <Box sx={{ p: 3 }}>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={4}>
          <Paper sx={{ p: 3, display: "flex", alignItems: "center" }}>
            <ShoppingCartIcon sx={{ fontSize: 40, mr: 2, color: "blue" }} />
            <Box>
              <Typography variant="h6">Total de Pedidos</Typography>
              <Typography variant="h4">{totalOrders}</Typography>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} sm={4}>
          <Paper sx={{ p: 3, display: "flex", alignItems: "center" }}>
            <AttachMoneyIcon sx={{ fontSize: 40, mr: 2, color: "green" }} />
            <Box>
              <Typography variant="h6">Valor Médio por Pedido</Typography>
              <Typography variant="h4">${averageOrderValue.toFixed(2)}</Typography>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} sm={4}>
          <Paper sx={{ p: 3, display: "flex", alignItems: "center" }}>
            <ReceiptIcon sx={{ fontSize: 40, mr: 2, color: "red" }} />
            <Box>
              <Typography variant="h6">Receita Total</Typography>
              <Typography variant="h4">${totalRevenue.toFixed(2)}</Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>

      <Box sx={{ mt: 4 }}>
        <Typography variant="h6" gutterBottom>
          Pedidos por Período (Mensal)
        </Typography>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={ordersPerPeriod}>
            <XAxis dataKey="period" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </Box>
    </Box>
  );
};

export default MainDashboard;
