import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  Tooltip,
} from "chart.js";
import { Bar } from "react-chartjs-2";
import type { SearchResult } from "../lib/api";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

type Props = { result: SearchResult };

export function ResultView({ result }: Props) {
  const labels = result.accounts.map((a) => a.platform);
  const values = result.accounts.map((a) => a.confidence);

  const chartData = {
    labels,
    datasets: [
      {
        label: "Confidence",
        data: values,
        backgroundColor: "#f97316",
        borderRadius: 6,
      },
    ],
  };

  return (
    <section className="panel">
      <h2>Profile Dashboard</h2>
      <p className="muted">Primary identifier: {result.primary_identifier}</p>

      <h3>Accounts</h3>
      {result.accounts.length > 0 ? (
        <>
          <div className="chart-wrap">
            <Bar data={chartData} options={{ scales: { y: { min: 0, max: 100 } } }} />
          </div>
          <ul className="list">
            {result.accounts.map((account) => (
              <li key={`${account.platform}-${account.url}`}>
                <a href={account.url} target="_blank" rel="noreferrer">
                  {account.platform}
                </a>
                <span>{account.confidence}%</span>
              </li>
            ))}
          </ul>
        </>
      ) : (
        <p>No account matches.</p>
      )}

      <h3>Mentions</h3>
      <ul className="list">
        {result.mentions.map((mention) => (
          <li key={`${mention.source}-${mention.url}`}>
            <a href={mention.url} target="_blank" rel="noreferrer">
              {mention.title}
            </a>
            <span>{mention.confidence}%</span>
          </li>
        ))}
      </ul>

      <h3>Connection Graph (Edges)</h3>
      <ul className="list">
        {result.graph_edges.map((edge, idx) => (
          <li key={`${edge.source}-${edge.target}-${idx}`}>
            <span>{edge.source}</span>
            <span>{edge.relation}</span>
            <span>{edge.target}</span>
          </li>
        ))}
      </ul>

      <h3>Risk Notes</h3>
      <ul className="list">
        {result.risk_notes.map((note) => (
          <li key={note}>{note}</li>
        ))}
      </ul>
    </section>
  );
}
