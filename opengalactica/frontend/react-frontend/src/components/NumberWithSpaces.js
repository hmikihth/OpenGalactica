import React from 'react';

const NumberWithSpaces = ({ number }) => {
  const formattedNumber = new Intl.NumberFormat('en-US', {
    useGrouping: true,
  }).format(number).replace(/,/g, ' '); // Replace commas with spaces

  return <span>{formattedNumber}</span>;
};

export default NumberWithSpaces;
