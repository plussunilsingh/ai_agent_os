import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchSalesOrders, dispatchSalesOrder } from '../../store/sales-order/actions';
import { selectSalesOrders, selectIsLoading } from '../../store/sales-order/selectors';
import { SalesOrder } from '../../models/SalesOrder';

interface SalesDispatchViewProps {}

const SalesDispatchView: React.FC<SalesDispatchViewProps> = () => {
    const dispatch = useDispatch();
    const salesOrders = useSelector(selectSalesOrders);
    const isLoading = useSelector(selectIsLoading);

    useEffect(() => {
        dispatch(fetchSalesOrders());
    }, [dispatch]);

    const handleDispatchOrder = (order: SalesOrder) => {
        // Assuming `order` is the selected order to be dispatched
        dispatch(dispatchSalesOrder(order));
    };

    return (
        <div>
            {isLoading ? (
                <p>Loading...</p>
            ) : salesOrders.length > 0 ? (
                <table>
                    <thead>
                        <tr>
                            <th>Order ID</th>
                            <th>Customer Name</th>
                            <th>Dispatch Order</th>
                        </tr>
                    </thead>
                    <tbody>
                        {salesOrders.map(order => (
                            <tr key={order.id}>
                                <td>{order.id}</td>
                                <td>{order.customerName}</td>
                                <td>
                                    <button onClick={() => handleDispatchOrder(order)}>Dispatch</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>No orders available.</p>
            )}
        </div>
    );
};

export default SalesDispatchView;

### Explanation:
1. **State Management**: The component uses `useSelector` to subscribe to the store for sales orders and loading state.
2. **Effect Hook**: A `useEffect` hook is used to dispatch an action to fetch sales orders when the component mounts.
3. **Fetching Data**: The `fetchSalesOrders` action is dispatched to load data from the Redux store.
4. **Rendering**: The component renders a table displaying each order's ID, customer name, and a button to dispatch the order. 
5. **Dispatching Orders**: When the "Dispatch" button is clicked, it calls the `handleDispatchOrder` function with the selected order.

### Notes:
- Ensure that your Redux store has actions (`fetchSalesOrders`, `dispatchSalesOrder`) and selectors (`selectSalesOrders`, `selectIsLoading`) properly defined.
- The `SalesOrder` model should be imported from the appropriate file, defining properties like `id`, `customerName`, etc.