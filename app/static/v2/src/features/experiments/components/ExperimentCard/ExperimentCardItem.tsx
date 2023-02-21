import React from 'react';

export interface ExperimentCardItemProps {
  label: string;
  value: unknown;
}

function valueToString(value: unknown): string {
  if (typeof value === 'number' || typeof value == 'string' || typeof value === 'boolean') {
    return value.toString();
  } else if (value instanceof Array) {
    return value.join(', ');
  }
  console.error('Invalid value:', JSON.stringify(value));
  return 'ERROR';
}

export const ExperimentCardItem = ({ label, value }: ExperimentCardItemProps) => {
  return (
    <li className="card-list-item">
      <strong className="text-capitalize">{label}: </strong>
      <span>{valueToString(value)}</span>
    </li>
  );
};
