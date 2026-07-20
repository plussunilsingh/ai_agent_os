// Navbar.tsx

import React from 'react';
import { Link } from 'react-router-dom';

interface INavbarProps {
    activeTab?: string;
}

const Navbar: React.FC<INavbarProps> = ({ activeTab }) => {
    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <div className="container-fluid">
                <Link to="/" className="navbar-brand">
                    BotanixUI
                </Link>
                <button
                    className="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarNavDropdown"
                    aria-controls="navbarNavDropdown"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span className="navbar-toggler-icon" />
                </button>
                <div className="collapse navbar-collapse" id="navbarNavDropdown">
                    <ul className="navbar-nav">
                        <li className="nav-item">
                            <Link
                                to="/dashboard"
                                className={`nav-link ${activeTab === 'dashboard' ? 'active' : ''}`}
                            >
                                Dashboard
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link
                                to="/plants"
                                className={`nav-link ${activeTab === 'plants' ? 'active' : ''}`}
                            >
                                Plants
                            </Link>
                        </li>
                        <li className="nav-item dropdown">
                            <a
                                className="nav-link dropdown-toggle"
                                href="#"
                                id="navbarDropdownMenuLink"
                                role="button"
                                data-bs-toggle="dropdown"
                                aria-expanded="false"
                            >
                                Settings
                            </a>
                            <ul className="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                                <li>
                                    <Link to="/settings/profile" className="dropdown-item">
                                        Profile
                                    </Link>
                                </li>
                                <li>
                                    <Link to="/settings/security" className="dropdown-item">
                                        Security
                                    </Link>
                                </li>
                            </ul>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;

### Explanation:
- **Navbar Component**: This component is designed to be a responsive navigation bar using Bootstrap classes for styling.
- **Props**:
  - `activeTab`: A prop that determines the active tab in the navbar. The current tab will have an "active" class applied to it, which can be used to highlight the currently selected menu item.
- **Links**: Links are created using `react-router-dom`'s `Link` component for smooth navigation without page reloads.
- **Dropdown Menu**: A dropdown menu is included under the "Settings" tab, providing additional options.

### Styling:
- The navbar uses Bootstrap classes to ensure it is responsive and looks good on all devices.
- Active tabs are highlighted using a simple class check in the `Link` component.

This code can be used as part of a larger React application following best practices for maintainability and readability.