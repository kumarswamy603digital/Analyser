/**
 * Renders one horizontal bar per label in `scores` (map of label -> 0..1).
 * Positive label is green; negative is red; others fall back to a neutral colour.
 */
interface Props {
  scores: Record<string, number>;
}

function colorFor(label: string): string {
  const l = label.toLowerCase();
  if (l === "positive") return "bg-green-500";
  if (l === "negative") return "bg-red-500";
  if (l === "neutral") return "bg-slate-400";
  return "bg-indigo-500";
}

export default function ScoreBar({ scores }: Props) {
  const entries = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  return (
    <div className="space-y-2">
      {entries.map(([label, score]) => {
        const pct = Math.round(score * 100);
        return (
          <div key={label} className="flex items-center gap-3 text-sm">
            <span className="w-24 font-medium capitalize">{label}</span>
            <div className="flex-1 rounded-full bg-slate-200 h-2.5 overflow-hidden dark:bg-slate-700">
              <div
                className={`h-full rounded-full transition-all ${colorFor(label)}`}
                style={{ width: `${pct}%` }}
                role="progressbar"
                aria-valuenow={pct}
                aria-valuemin={0}
                aria-valuemax={100}
                aria-label={`${label} score: ${pct}%`}
              />
            </div>
            <span className="w-12 text-right tabular-nums">{pct}%</span>
          </div>
        );
      })}
    </div>
  );
}
