import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMaterialIntakes } from '../../actions/materialIntakeActions';
import { IRootState } from '../../store/rootReducer';
import MaterialIntakeItem from './MaterialIntakeItem';

interface MaterialIntake {
    id: number;
    materialName: string;
    quantity: number;
    dateOfIntake: Date;
}

const MaterialIntakeView: React.FC = () => {
    const dispatch = useDispatch();
    const { materialIntakes } = useSelector((state: IRootState) => state.materialIntakeReducer);
    const [intakes, setIntakes] = useState<MaterialIntake[]>([]);

    useEffect(() => {
        dispatch(fetchMaterialIntakes());
    }, [dispatch]);

    useEffect(() => {
        if (materialIntakes) {
            setIntakes(materialIntakes);
        }
    }, [materialIntakes]);

    return (
        <div className="material-intake-view">
            <h2>Raw Material Intake Catalog</h2>
            {intakes.length > 0 ? (
                intakes.map(intake => (
                    <MaterialIntakeItem
                        key={intake.id}
                        id={intake.id}
                        materialName={intake.materialName}
                        quantity={intake.quantity}
                        dateOfIntake={intake.dateOfIntake}
                    />
                ))
            ) : (
                <p>No raw materials have been recorded yet.</p>
            )}
        </div>
    );
};

export default MaterialIntakeView;

This code defines a React component `MaterialIntakeView` that displays a list of raw material intakes. It uses Redux for state management and fetches data using an action creator.

### Explanation:
1. **Imports**: The necessary imports are included to use React hooks, Redux features, and custom components.
2. **State Management**:
   - `useDispatch` and `useSelector` hooks are used to interact with the Redux store.
   - `fetchMaterialIntakes` is a Redux action creator that fetches material intakes from the backend.
3. **Effects**:
   - The first effect dispatches an action to fetch materials on component mount.
   - The second effect updates the local state when the material intakes data changes in the store.
4. **Rendering**:
   - A list of `MaterialIntakeItem` components is rendered for each item in the `intakes` array.
   - If no items are present, a message is displayed.

### Notes:
- Ensure that your Redux store is properly set up to handle state management and that you have appropriate actions and reducers defined.
- The `MaterialIntakeItem` component should be defined elsewhere (not included here) as it will display the details of each material intake.