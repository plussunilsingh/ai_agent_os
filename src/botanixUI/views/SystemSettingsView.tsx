import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchSystemSettings, updateSystemSetting } from '../../store/systemSettingsSlice';
import { useNavigate } from 'react-router-dom';

interface SystemSetting {
    id: number;
    name: string;
    value: string;
}

const SystemSettingsView: React.FC = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();

    // State to hold the list of system settings
    const [systemSettings, setSystemSettings] = useState<SystemSetting[]>([]);
    
    // Fetch initial system settings on component mount
    useEffect(() => {
        dispatch(fetchSystemSettings());
    }, [dispatch]);

    // Selector for the system settings from Redux store
    const systemSettingsFromStore = useSelector((state) => state.systemSettings.settings);

    useEffect(() => {
        if (systemSettingsFromStore.length > 0) {
            setSystemSettings(systemSettingsFromStore);
        }
    }, [systemSettingsFromStore]);

    // Handle form submission to update a setting
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>, id: number, name: string, value: string) => {
        event.preventDefault();
        
        try {
            await dispatch(updateSystemSetting({ id, name, value }));
            setSystemSettings(systemSettings.map(setting => 
                setting.id === id ? { ...setting, value } : setting
            ));
        } catch (error) {
            console.error('Failed to update system setting:', error);
        }
    };

    return (
        <div className="system-settings-view">
            <h2>System Settings</h2>
            <table className="settings-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Value</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {systemSettings.map(setting => (
                        <tr key={setting.id}>
                            <td>{setting.name}</td>
                            <td><input type="text" value={setting.value} onChange={(e) => {} /* Not used in this example */}/></td>
                            <td>
                                <form onSubmit={(event) => handleSubmit(event, setting.id, setting.name, e.target[1].value)}>
                                    <button type="submit">Update</button>
                                </form>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {/* Add a button to navigate back or perform other actions */}
            <button onClick={() => navigate(-1)}>Back</button>
        </div>
    );
};

export default SystemSettingsView;

### Explanation:
- **State Management**: The component uses `useState` for the list of system settings.
- **Redux Integration**: Utilizes `useDispatch` and `useSelector` from React-Redux to fetch and manage state.
- **Initial Fetch**: A side-effect runs on mount to fetch initial settings using an action dispatched through `dispatch`.
- **Form Handling**: Handles form submissions to update the settings via another action dispatched with `updateSystemSetting`.
- **Table Rendering**: Displays the list of system settings in a table format, allowing inline editing.
- **Navigation**: Provides a back button to navigate away from this view.

### Notes:
- The placeholder for handling input changes (onChange) is not implemented and should be added if needed.
- Ensure proper error handling and validation are integrated as per your application's requirements.