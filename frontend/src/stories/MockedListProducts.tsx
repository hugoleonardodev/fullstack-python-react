import ListProducts from 'components/tables/ListProducts'
import React from 'react'
import { BrowserRouter } from 'react-router-dom'

function MockedListProducts() {
  return (
    <BrowserRouter>
        <ListProducts />
    </BrowserRouter>
  )
}

export default MockedListProducts