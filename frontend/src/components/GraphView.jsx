const STATUS_COLORS = {
  favourite: "#22c55e",
  working_on: "#f59e0b",
  exploring: "#ef4444",
};

const NODE_RADIUS = 40;

function layoutNodes(nodes, width, height) {
  if (nodes.length === 0) return [];
  if (nodes.length === 1) {
    return [{ ...nodes[0], x: width / 2, y: height / 2 }];
  }
  const centerX = width / 2;
  const centerY = height / 2;
  const radius = Math.min(width, height) / 3;
  return nodes.map((node, i) => ({
    ...node,
    x: centerX + radius * Math.cos((2 * Math.PI * i) / nodes.length - Math.PI / 2),
    y: centerY + radius * Math.sin((2 * Math.PI * i) / nodes.length - Math.PI / 2),
  }));
}

export default function GraphView({ nodes, edges }) {
  const width = 800;
  const height = 600;
  const positioned = layoutNodes(nodes, width, height);
  const nodeMap = Object.fromEntries(positioned.map((n) => [n.id, n]));

  return (
    <svg viewBox={`0 0 ${width} ${height}`} className="graph-svg">
      {edges.map((edge) => {
        const from = nodeMap[edge.from_node];
        const to = nodeMap[edge.to_node];
        if (!from || !to) return null;
        const color = STATUS_COLORS[edge.status] || "#6b7a90";
        return (
          <g key={edge.id}>
            <line
              x1={from.x}
              y1={from.y}
              x2={to.x}
              y2={to.y}
              stroke={color}
              strokeWidth={2}
            />
            <text
              x={(from.x + to.x) / 2}
              y={(from.y + to.y) / 2 - 8}
              textAnchor="middle"
              fill={color}
              fontSize={11}
            >
              {edge.label}
            </text>
          </g>
        );
      })}
      {positioned.map((node) => {
        const hasEdge = edges.some(
          (e) => e.from_node === node.id || e.to_node === node.id,
        );
        return (
          <g key={node.id}>
            <circle
              cx={node.x}
              cy={node.y}
              r={NODE_RADIUS}
              fill="#161a20"
              stroke="#9aa8ba"
              strokeWidth={hasEdge ? 2 : 2}
              strokeDasharray={hasEdge ? "none" : "6 3"}
            />
            <text
              x={node.x}
              y={node.y}
              textAnchor="middle"
              dominantBaseline="central"
              fill="#e8ecf0"
              fontSize={12}
            >
              {node.label}
            </text>
          </g>
        );
      })}
    </svg>
  );
}
