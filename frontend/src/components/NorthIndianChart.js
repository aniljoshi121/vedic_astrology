import React from 'react';

const NorthIndianChart = ({ houses, planets }) => {
  // Map planets to their house positions
  const getPlanetsInHouse = (houseNum) => {
    if (!planets) return [];
    return Object.entries(planets)
      .filter(([_, data]) => data.rashi_num === houseNum)
      .map(([planet]) => planet);
  };

  // Diamond layout positions for 12 houses
  const housePositions = [
    { x: 150, y: 10, num: 1 },   // Top center
    { x: 220, y: 50, num: 2 },   // Top right
    { x: 260, y: 120, num: 3 },  // Right top
    { x: 260, y: 180, num: 4 },  // Right center
    { x: 220, y: 250, num: 5 },  // Right bottom
    { x: 150, y: 290, num: 6 },  // Bottom center
    { x: 80, y: 250, num: 7 },   // Left bottom
    { x: 40, y: 180, num: 8 },   // Left center
    { x: 40, y: 120, num: 9 },   // Left top
    { x: 80, y: 50, num: 10 },   // Top left
    { x: 110, y: 80, num: 11 },  // Inner top left
    { x: 190, y: 80, num: 12 }   // Inner top right
  ];

  return (
    <svg viewBox="0 0 300 300" className="w-full max-w-lg mx-auto" data-testid="north-indian-chart">
      {/* Outer diamond */}
      <polygon
        points="150,0 300,150 150,300 0,150"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        className="text-primary"
      />
      
      {/* Inner cross lines */}
      <line x1="0" y1="150" x2="300" y2="150" stroke="currentColor" strokeWidth="1.5" className="text-border" />
      <line x1="150" y1="0" x2="150" y2="300" stroke="currentColor" strokeWidth="1.5" className="text-border" />
      <line x1="75" y1="75" x2="225" y2="225" stroke="currentColor" strokeWidth="1.5" className="text-border" />
      <line x1="225" y1="75" x2="75" y2="225" stroke="currentColor" strokeWidth="1.5" className="text-border" />

      {/* House numbers and planets */}
      {housePositions.map((pos) => {
        const house = houses?.find(h => h.house_num === pos.num);
        const planetsInHouse = getPlanetsInHouse(house?.rashi_num);
        
        return (
          <g key={pos.num}>
            {/* House number */}
            <circle cx={pos.x} cy={pos.y} r="12" fill="currentColor" className="text-primary/20" />
            <text
              x={pos.x}
              y={pos.y + 4}
              textAnchor="middle"
              className="text-xs font-bold fill-current"
            >
              {pos.num}
            </text>
            
            {/* Planets in this house */}
            {planetsInHouse.map((planet, idx) => (
              <text
                key={planet}
                x={pos.x}
                y={pos.y + 20 + (idx * 12)}
                textAnchor="middle"
                className="text-[10px] font-semibold fill-amber-600 dark:fill-amber-400"
              >
                {planet.substring(0, 2)}
              </text>
            ))}
          </g>
        );
      })}
    </svg>
  );
};

export default NorthIndianChart;
