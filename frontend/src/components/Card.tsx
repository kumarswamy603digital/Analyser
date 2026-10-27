interface Props {
  className?: string;
  title?: React.ReactNode;
  children: React.ReactNode;
}

export default function Card({ className = "", title, children }: Props) {
  return (
    <div className={`card ${className}`}>
      {title && (
        <div className="mb-3 text-lg font-semibold text-slate-800 dark:text-slate-100">
          {title}
        </div>
      )}
      {children}
    </div>
  );
}
