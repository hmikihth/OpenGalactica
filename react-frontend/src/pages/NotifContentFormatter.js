import React from 'react';

const NotifContentFormatter = ({ ntype, content }) => {
  if (!content || typeof content !== 'object') {
    return <span>Invalid content</span>;
  }

  switch (ntype) {
    case 'Production': {
      const { source, ships } = content;
      const shipList = Object.entries(ships)
        .map(([name, count]) => `${count} ${name}`)
        .join(', ');
      return (
        <span>
          {source.toUpperCase()}: You have started production of the following ship(s): {shipList}.
        </span>
      );
    }

    case 'Research':
      return (
        <span>
          {content.source.toUpperCase()}: Research "{content.research}" has been completed.
        </span>
      );

    case 'Building':
      return (
        <span>
          {content.source.toUpperCase()}: Construction started on {content.building}.
        </span>
      );

    case 'War':
      return <span>WAR ALERT: {content.message}</span>;

    case 'News':
      return <span>NEWS: {content.headline}</span>;

    default:
      return <span>{JSON.stringify(content)}</span>;
  }
};

export default NotifContentFormatter;
