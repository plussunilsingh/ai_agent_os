import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchManufacturingProcesses, selectManufacturingProcesses } from './manufacturingProcessesSlice';
import { ManufacturingProcess } from './types';

const ManufacturingProcessView: React.FC = () => {
    const dispatch = useDispatch();
    const manufacturingProcesses = useSelector(selectManufacturingProcesses);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        dispatch(fetchManufacturingProcesses());
        // Fetch processes on component mount
        return () => {
            // Cleanup if needed
        };
    }, [dispatch]);

    useEffect(() => {
        if (manufacturingProcesses.length > 0) {
            setLoading(false);
        }
    }, [manufacturingProcesses]);

    return (
        <div>
            {loading ? (
                <p>Loading...</p>
            ) : (
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>Work Order ID</th>
                            <th>Status</th>
                            <th>Start Time</th>
                            <th>End Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        {manufacturingProcesses.map((process: ManufacturingProcess) => (
                            <tr key={process.id}>
                                <td>{process.workOrderID}</td>
                                <td>{process.status}</td>
                                <td>{new Date(process.startTime).toLocaleTimeString()}</td>
                                <td>{process.endTime ? new Date(process.endTime).toLocaleTimeString() : 'N/A'}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default ManufacturingProcessView;

### Explanation:
1. **State Management**: 
   - `loading` state to handle loading UI.
   
2. **Fetching Data**:
   - `useEffect` hook to dispatch an action to fetch manufacturing processes on component mount.

3. **Data Display**:
   - Conditional rendering based on the presence of data and loading state.
   - Simple table to display work order details like ID, status, start time, and end time.

4. **Performance Considerations**:
   - Minimal re-renders by using hooks.
   - Proper key usage in `map` to ensure efficient updates.

### Notes:
- Ensure that the state management (Redux) slice (`manufacturingProcessesSlice`) is properly set up with actions for fetching processes and selectors for reading them.
- The `ManufacturingProcess` type should be defined according to your application's schema.