import React from 'react';

interface GradientPanelProps {
  className?: string;
  children: React.ReactNode;
}

/**
 * A glassmorphism panel with a subtle animated gradient border.
 * Use for hero CTAs, contact section, featured cards.
 */
const GradientPanel: React.FC<GradientPanelProps> = ({
  className = '',
  children,
}) => {
  return (
    <div
      className={`gradient-border relative overflow-hidden rounded-3xl bg-surface-900/60 backdrop-blur-xl ${className}`}
    >
      {children}
    </div>
  );
};

export default GradientPanel;
