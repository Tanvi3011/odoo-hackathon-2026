export default function ChangePasswordPage() {
  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md rounded-lg border border-border bg-card p-8 shadow-sm">
        <h1 className="text-2xl font-bold text-foreground">Change Password</h1>
        <p className="mt-2 text-sm text-text-secondary">
          Password reset flow can be wired to your FastAPI endpoint here.
        </p>
      </div>
    </div>
  );
}
