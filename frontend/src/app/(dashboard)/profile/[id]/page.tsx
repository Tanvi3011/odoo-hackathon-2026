export default function ProfilePage({ params }: { params: { id: string } }) {
  return (
    <div>
      <h1 className="text-2xl font-bold text-foreground">Profile</h1>
      <p className="mt-2 text-sm text-text-secondary">Employee profile for ID {params.id}.</p>
    </div>
  );
}
