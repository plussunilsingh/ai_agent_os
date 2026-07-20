// Sidebar.tsx

import React from 'react';
import { Link } from 'react-router-dom';

interface Props {
    currentDomain: string;
}

const Sidebar: React.FC<Props> = ({ currentDomain }) => {
    const domains = [
        { name: 'Dashboard', path: '/dashboard' },
        { name: 'Inventory', path: '/inventory' },
        { name: 'Orders', path: '/orders' },
        { name: 'Customers', path: '/customers' },
        { name: 'Settings', path: '/settings' }
    ];

    return (
        <div className="sidebar">
            <h3>Domain Switcher</h3>
            <ul className="domain-list">
                {domains.map(domain => (
                    <li key={domain.path}>
                        <Link
                            to={domain.path}
                            className={`nav-link ${currentDomain === domain.name ? 'active' : ''}`}
                        >
                            {domain.name}
                        </Link>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Sidebar;

### Explanation:
1. **Props Interface**: The component accepts a `props` object with a `currentDomain` string to determine the currently active domain.
2. **Domains List**: An array of objects representing each domain, including its name and path.
3. **Rendering Domains**: Each domain is rendered as an `<li>` element containing a `<Link>` component from React Router.
4. **Active Class**: The `active` class is added to the link of the currently active domain.

This code is designed to be production-ready, ensuring clean syntax and functionality for switching between different domains in your application.