import React from "react";

interface NavbarProps {
  onGoHome: () => void;
  onGoProducts: () => void;
  onGoCart: () => void;
  token: string | null;
  onLogout: () => void;
}

const Navbar: React.FC<NavbarProps> = ({
  onGoHome,
  onGoProducts,
  onGoCart,
  token,
  onLogout,
}) => {
  return (
    <nav className="bg-cloud-primary text-cloud-light shadow-md">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <button
          className="text-xl font-bold tracking-wide"
          onClick={onGoHome}
        >
          CloudCom
        </button>
        <div className="flex items-center gap-4">
          <button
            className="hover:text-cloud-accent transition-colors"
            onClick={onGoProducts}
          >
            Products
          </button>
          <button
            className="hover:text-cloud-accent transition-colors"
            onClick={onGoCart}
          >
            Cart
          </button>
          {token ? (
            <button
              className="ml-4 px-3 py-1 rounded-md bg-cloud-secondary text-cloud-primary font-medium hover:bg-cloud-accent transition-colors"
              onClick={onLogout}
            >
              Logout
            </button>
          ) : null}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;