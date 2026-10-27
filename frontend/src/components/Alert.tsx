interface Props {
  type: "error" | "success" | "warning" | "info";
  children: React.ReactNode;
}

const map = {
  error: "bg-red-50 text-red-800 border-red-200 dark:bg-red-950 dark:text-red-200 dark:border-red-800",
  success: "bg-green-50 text-green-800 border-green-200 dark:bg-green-950 dark:text-green-200 dark:border-green-800",
  warning: "bg-amber-50 text-amber-800 border-amber-200 dark:bg-amber-950 dark:text-amber-200 dark:border-amber-800",
  info: "bg-blue-50 text-blue-800 border-blue-200 dark:bg-blue-950 dark:text-blue-200 dark:border-blue-800",
};

export default function Alert({ type, children }: Props) {
  return (
    <div role="alert" className={`rounded-lg border px-4 py-3 text-sm ${map[type]}`}>
      {children}
    </div>
  );
}
