import React from 'react';

export interface PageTitleProps {
  children: string;
}

export const PageTitle = ({ children }: PageTitleProps) => {
  return (
    <h2>
      <span style={{ color: 'red' }}>CONP Portal</span> | {children}
    </h2>
  );
};
